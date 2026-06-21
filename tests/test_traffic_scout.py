"""Unit tests for traffic_scout.py.

All HTTP is mocked; no network access. The polling tests monkeypatch
ts.time.sleep to a no-op so the real linear-backoff wait schedule is skipped.
Tests confirm the corrected facts: the MAX_API_CALLS bound is enforced, both
HTTP 200 and 202 are accepted, and main() returns only 0 or 1 (never 2).
"""

import os
from unittest.mock import MagicMock, patch

import requests

from .conftest import traffic_scout as ts


def _make_poll_response(status_code, json_body=None, text=""):
    """Build a mocked requests.Response-like object."""
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    if json_body is None:
        response.json.side_effect = ValueError("no json")
    else:
        response.json.return_value = json_body
    return response


# --- CallTracker -----------------------------------------------------------

def test_call_tracker_starts_empty():
    tracker = ts.CallTracker()
    assert tracker.calls_made == 0
    assert tracker.call_log == []
    assert tracker.can_call() is True


def test_call_tracker_record_increments():
    tracker = ts.CallTracker()
    tracker.record("query A", "5 results", "see below")
    assert tracker.calls_made == 1
    assert tracker.call_log[0]["query"] == "query A"
    assert tracker.call_log[0]["result"] == "5 results"


def test_call_tracker_can_call_respects_max():
    tracker = ts.CallTracker()
    for _ in range(ts.MAX_API_CALLS):
        tracker.record("q", "r", "pt")
    assert tracker.can_call() is False


# --- extract_popular_times -------------------------------------------------

def test_extract_popular_times_none_input():
    assert ts.extract_popular_times(None) is None
    assert ts.extract_popular_times({}) is None


def test_extract_popular_times_no_pt_key():
    assert ts.extract_popular_times({"name": "X"}) is None


def test_extract_popular_times_pt_not_list():
    assert ts.extract_popular_times({"popular_times": "not a list"}) is None


def test_extract_popular_times_filters_invalid_entries():
    place = {
        "popular_times": [
            {"day_text": "Monday", "popular_times": [{"hour": 12, "percentage": 30}]},
            {"day_text": "Tuesday"},  # missing popular_times key
            {"popular_times": [{"hour": 12, "percentage": 30}]},  # missing day_text
            {"day_text": "Wednesday", "popular_times": []},  # empty list
            {"day_text": "Thursday", "popular_times": [{"hour": 18, "percentage": 70}]},
        ]
    }
    result = ts.extract_popular_times(place)
    assert result is not None
    assert len(result) == 2
    day_names = [day["day_text"] for day in result]
    assert day_names == ["Monday", "Thursday"]


def test_extract_popular_times_all_invalid_returns_none():
    assert ts.extract_popular_times({"popular_times": [{"day_text": "X"}]}) is None


# --- _flatten_places -------------------------------------------------------

def test_flatten_places_empty():
    assert ts._flatten_places(None) == []
    assert ts._flatten_places([]) == []
    assert ts._flatten_places({}) == []


def test_flatten_places_flat_list():
    data = [{"name": "A"}, {"name": "B"}]
    assert ts._flatten_places(data) == [{"name": "A"}, {"name": "B"}]


def test_flatten_places_nested_list():
    data = [[{"name": "A"}, {"name": "B"}]]
    assert ts._flatten_places(data) == [{"name": "A"}, {"name": "B"}]


def test_flatten_places_unexpected_shape():
    assert ts._flatten_places([1, 2, 3]) == []
    assert ts._flatten_places("string") == []


# --- query builders --------------------------------------------------------

def test_build_target_queries_unconfigured_returns_placeholder():
    assert ts.TARGET_VENUE_NAME.startswith("<")
    queries = ts.build_target_queries()
    assert len(queries) == 1
    assert "<RESTAURANT_NAME>" in queries[0]


def test_build_competitor_queries_default():
    queries = ts.build_competitor_queries()
    assert len(queries) >= 1
    assert ts.COMPETITOR_CUISINE in queries[0]


# --- load_api_key ----------------------------------------------------------

def test_load_api_key_from_env(monkeypatch):
    monkeypatch.setenv("FOOT_TRAFFIC_API_KEY", "test-key-from-env")
    assert ts.load_api_key() == "test-key-from-env"


def test_load_api_key_returns_none_when_missing(monkeypatch, tmp_path):
    monkeypatch.delenv("FOOT_TRAFFIC_API_KEY", raising=False)
    monkeypatch.setattr(ts, "CREDS_PATH", tmp_path / "does-not-exist.env")
    assert ts.load_api_key() is None


# --- query_traffic_api -----------------------------------------------------

def test_query_traffic_api_respects_max_calls():
    tracker = ts.CallTracker()
    for _ in range(ts.MAX_API_CALLS):
        tracker.record("q", "r", "pt")
    with patch.object(ts.requests, "get") as mock_get:
        result = ts.query_traffic_api("key", "query", tracker)
    assert result == []
    mock_get.assert_not_called()


def test_query_traffic_api_handles_sync_response():
    tracker = ts.CallTracker()
    body = {"data": [{"name": "Place A", "place_id": "p1"}]}
    response = _make_poll_response(200, json_body=body)
    with patch.object(ts.requests, "get", return_value=response):
        result = ts.query_traffic_api("key", "query", tracker)
    assert len(result) == 1
    assert tracker.calls_made == 1


def test_query_traffic_api_handles_unexpected_status():
    tracker = ts.CallTracker()
    response = _make_poll_response(500, json_body=None, text="server error")
    with patch.object(ts.requests, "get", return_value=response):
        result = ts.query_traffic_api("key", "query", tracker)
    assert result == []
    assert tracker.calls_made == 1
    assert "HTTP 500" in tracker.call_log[0]["result"]


def test_query_traffic_api_handles_transport_error():
    tracker = ts.CallTracker()
    with patch.object(ts.requests, "get", side_effect=requests.ConnectionError("boom")):
        result = ts.query_traffic_api("key", "query", tracker)
    assert result == []
    assert tracker.calls_made == 1
    assert "transport error" in tracker.call_log[0]["result"]


def test_query_traffic_api_async_no_results_location():
    tracker = ts.CallTracker()
    body = {"status": "Pending"}
    response = _make_poll_response(202, json_body=body)
    with patch.object(ts.requests, "get", return_value=response):
        result = ts.query_traffic_api("key", "query", tracker)
    assert result == []
    assert "NO RESULTS URL" in tracker.call_log[0]["result"]


# --- _poll_for_results -----------------------------------------------------

def test_poll_for_results_immediate_success(monkeypatch):
    monkeypatch.setattr(ts.time, "sleep", lambda *a, **k: None)
    tracker = ts.CallTracker()
    success = _make_poll_response(
        200, json_body={"status": "Success", "data": [{"name": "Place X"}]}
    )
    with patch.object(ts.requests, "get", return_value=success):
        result = ts._poll_for_results("key", "query", "http://results", tracker)
    assert len(result) == 1
    assert result[0]["name"] == "Place X"


def test_poll_for_results_pending_then_success(monkeypatch):
    monkeypatch.setattr(ts.time, "sleep", lambda *a, **k: None)
    tracker = ts.CallTracker()
    pending = _make_poll_response(200, json_body={"status": "Pending"})
    success = _make_poll_response(
        200, json_body={"status": "Success", "data": [{"name": "Place Y"}]}
    )
    with patch.object(ts.requests, "get", side_effect=[pending, success]):
        result = ts._poll_for_results("key", "query", "http://results", tracker)
    assert len(result) == 1
    assert result[0]["name"] == "Place Y"


def test_poll_for_results_non_200_then_success(monkeypatch):
    monkeypatch.setattr(ts.time, "sleep", lambda *a, **k: None)
    tracker = ts.CallTracker()
    busy = _make_poll_response(503, json_body=None, text="unavailable")
    success = _make_poll_response(
        200, json_body={"status": "Success", "data": [{"name": "Place Z"}]}
    )
    with patch.object(ts.requests, "get", side_effect=[busy, success]):
        result = ts._poll_for_results("key", "query", "http://results", tracker)
    assert len(result) == 1


def test_poll_for_results_unexpected_status(monkeypatch):
    monkeypatch.setattr(ts.time, "sleep", lambda *a, **k: None)
    tracker = ts.CallTracker()
    malformed = _make_poll_response(200, json_body={"status": "MalformedStatus"})
    with patch.object(ts.requests, "get", return_value=malformed):
        result = ts._poll_for_results("key", "query", "http://results", tracker)
    assert result == []
    assert any("TIMEOUT" in entry["result"] for entry in tracker.call_log)


def test_poll_for_results_transport_retry_then_success(monkeypatch):
    monkeypatch.setattr(ts.time, "sleep", lambda *a, **k: None)
    tracker = ts.CallTracker()
    success = _make_poll_response(
        200, json_body={"status": "Success", "data": [{"name": "Place R"}]}
    )
    with patch.object(
        ts.requests, "get", side_effect=[requests.ConnectionError("boom"), success]
    ):
        result = ts._poll_for_results("key", "query", "http://results", tracker)
    assert len(result) == 1


def test_poll_for_results_empty_success(monkeypatch):
    monkeypatch.setattr(ts.time, "sleep", lambda *a, **k: None)
    tracker = ts.CallTracker()
    success = _make_poll_response(200, json_body={"status": "Success", "data": []})
    with patch.object(ts.requests, "get", return_value=success):
        result = ts._poll_for_results("key", "query", "http://results", tracker)
    assert result == []
    assert any("EMPTY SUCCESS" in entry["result"] for entry in tracker.call_log)


def test_poll_for_results_timeout_after_max_attempts(monkeypatch):
    monkeypatch.setattr(ts.time, "sleep", lambda *a, **k: None)
    tracker = ts.CallTracker()
    pending = _make_poll_response(200, json_body={"status": "Pending"})
    with patch.object(ts.requests, "get", return_value=pending):
        result = ts._poll_for_results("key", "query", "http://results", tracker)
    assert result == []
    assert any("TIMEOUT" in entry["result"] for entry in tracker.call_log)


# --- main ------------------------------------------------------------------

def test_main_exits_cleanly_without_api_key(monkeypatch):
    monkeypatch.delenv("FOOT_TRAFFIC_API_KEY", raising=False)
    monkeypatch.setattr(ts, "CREDS_PATH", ts.Path("/nonexistent/creds.env"))
    assert ts.main() == 1


def test_main_exits_cleanly_when_unconfigured(monkeypatch):
    monkeypatch.setenv("FOOT_TRAFFIC_API_KEY", "present-key")
    assert ts.TARGET_VENUE_NAME.startswith("<")
    with patch.object(ts.requests, "get") as mock_get:
        result = ts.main()
    assert result == 0
    mock_get.assert_not_called()
