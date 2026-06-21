#!/usr/bin/env python3
"""Foot Traffic Scout (Performance Audit, Agent 3 data pull).

Pulls Google Maps popular-times data for a target venue and nearby
competitors through a foot-traffic REST API, then writes the raw results to
disk for downstream analysis. The script is fully parameterized through
environment variables so it is self-documenting when run unconfigured.

Environment variables:
  FOOT_TRAFFIC_API_KEY   API key. Read from the live env first, then from a
                         line "FOOT_TRAFFIC_API_KEY=..." inside the
                         credentials file.
  CREDENTIALS_FILE       Path to the credentials file
                         (default: ~/.config/credentials.env).
  FOOT_TRAFFIC_API_BASE  Override the API base URL.
  TARGET_VENUE_NAME      Target restaurant name (placeholder when unset).
  TARGET_CITY / TARGET_REGION / TARGET_COUNTRY
                         Target location for the query string.
  COMPETITOR_CUISINE     Cuisine keyword used to discover competitors.
  COMPETITOR_NEIGHBORHOOD
                         Optional neighborhood for a second competitor query.
  OUTPUT_DIR             Where traffic-raw.json is written
                         (default: <repo>/performance-audit/output).
  MAX_API_CALLS          Hard ceiling on API calls per run (default: 9).

Exit codes:
  0  success, or the script is unconfigured (placeholder target, no HTTP).
  1  the API key could not be resolved (auth failure / key absence).

Only codes 0 and 1 are returned. Transport errors and unexpected HTTP
status codes are caught inside the API helpers, recorded in the call log,
and the run still completes with code 0.
"""

import json
import os
import time
from pathlib import Path

import requests

# --- Configuration (read once at import) -----------------------------------

CREDS_PATH = Path(
    os.environ.get("CREDENTIALS_FILE", "~/.config/credentials.env")
).expanduser()

TARGET_VENUE_NAME = os.environ.get("TARGET_VENUE_NAME", "<RESTAURANT_NAME>")
TARGET_CITY = os.environ.get("TARGET_CITY", "<CITY>")
TARGET_REGION = os.environ.get("TARGET_REGION", "<REGION>")
TARGET_COUNTRY = os.environ.get("TARGET_COUNTRY", "<COUNTRY>")

COMPETITOR_CUISINE = os.environ.get("COMPETITOR_CUISINE", "restaurant")
COMPETITOR_NEIGHBORHOOD = os.environ.get("COMPETITOR_NEIGHBORHOOD", "")

_DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", str(_DEFAULT_OUTPUT_DIR)))

MAX_API_CALLS = int(os.environ.get("MAX_API_CALLS", "9"))

API_BASE_URL = os.environ.get(
    "FOOT_TRAFFIC_API_BASE", "https://api.example.com/maps/search-v3"
)

POLL_BASE_WAIT_SECONDS = 8
POLL_INCREMENT_SECONDS = 4
POLL_MAX_ATTEMPTS = 10

REQUEST_FIELDS = (
    "name,full_address,popular_times,rating,reviews,type,"
    "working_hours,place_id,city,state"
)
REQUEST_TIMEOUT = 20


# --- API key resolution ----------------------------------------------------

def load_api_key():
    """Resolve the API key from the live env, then the credentials file.

    Returns the key string, or None if it cannot be found.
    """
    live = os.environ.get("FOOT_TRAFFIC_API_KEY")
    if live:
        return live

    if CREDS_PATH.exists():
        try:
            with open(CREDS_PATH, "r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    name, _, value = line.partition("=")
                    if name.strip() == "FOOT_TRAFFIC_API_KEY":
                        value = value.strip().strip('"').strip("'")
                        if value:
                            return value
        except OSError:
            return None

    return None


# --- Call budget tracking --------------------------------------------------

class CallTracker:
    """Counts API calls and records a per-call log to cap metered spend."""

    def __init__(self):
        self.calls_made = 0
        self.call_log = []

    def record(self, query, result, popular_times):
        self.call_log.append(
            {
                "query": query,
                "result": result,
                "popular_times": popular_times,
            }
        )
        self.calls_made += 1

    def can_call(self):
        return self.calls_made < MAX_API_CALLS


# --- Response normalization ------------------------------------------------

def _flatten_places(data):
    """Normalize varied API response shapes into a flat list of place dicts.

    Accepts a flat list of dicts, a nested list (list of lists of dicts), or
    odd shapes. Never raises; returns [] for anything unusable.
    """
    if not data:
        return []
    if not isinstance(data, list):
        return []

    places = []
    for entry in data:
        if isinstance(entry, dict):
            places.append(entry)
        elif isinstance(entry, list):
            for inner in entry:
                if isinstance(inner, dict):
                    places.append(inner)
        # Anything else (ints, strings, etc.) is ignored.
    return places


def extract_popular_times(place):
    """Pull the validated popular-times structure out of a place dict.

    Returns the list of valid day objects, or None when none are present.
    """
    if not place or not isinstance(place, dict):
        return None

    popular_times = place.get("popular_times")
    if not popular_times:
        return None
    if not isinstance(popular_times, list) or len(popular_times) == 0:
        return None

    valid_days = []
    for day_data in popular_times:
        if (
            isinstance(day_data, dict)
            and "day_text" in day_data
            and "popular_times" in day_data
        ):
            hours = day_data["popular_times"]
            if isinstance(hours, list) and len(hours) > 0:
                valid_days.append(day_data)

    if len(valid_days) == 0:
        return None

    return valid_days


# --- API calls -------------------------------------------------------------

def query_traffic_api(api_key, query, tracker, *, limit=1):
    """Query the foot-traffic API for one search.

    Handles both the synchronous response (body has non-empty "data") and the
    asynchronous submit-then-poll pattern (body carries "results_location").
    Both HTTP 200 and 202 are treated as accepted. Returns a flat list of
    place dicts (possibly empty). Never raises on transport / status errors.
    """
    if not tracker.can_call():
        return []

    headers = {"X-API-KEY": api_key}
    params = {"query": query, "limit": limit, "fields": REQUEST_FIELDS}

    try:
        response = requests.get(
            API_BASE_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT
        )
    except requests.RequestException as exc:
        tracker.record(query, f"transport error: {exc}", "NO")
        return []

    if response.status_code not in (200, 202):
        tracker.record(query, f"HTTP {response.status_code}", "NO")
        return []

    try:
        body = response.json()
    except ValueError:
        tracker.record(query, "invalid JSON body", "NO")
        return []

    # Synchronous path: results inline.
    data = body.get("data")
    if data:
        places = _flatten_places(data)
        tracker.record(query, f"{len(places)} place(s)", "YES" if places else "NO")
        return places

    # Asynchronous path: poll the results location.
    results_url = body.get("results_location")
    if not results_url:
        tracker.record(query, "NO RESULTS URL", "NO")
        return []

    return _poll_for_results(api_key, query, results_url, tracker)


def _poll_for_results(api_key, query, results_url, tracker):
    """Poll an async results URL until it reports Success or attempts run out.

    Linear backoff: wait per attempt = 8 + attempt * 4 seconds. Returns a flat
    list of place dicts (possibly empty). Never raises.
    """
    headers = {"X-API-KEY": api_key}

    for attempt in range(POLL_MAX_ATTEMPTS):
        time.sleep(POLL_BASE_WAIT_SECONDS + attempt * POLL_INCREMENT_SECONDS)

        try:
            response = requests.get(
                results_url, headers=headers, timeout=REQUEST_TIMEOUT
            )
        except requests.RequestException:
            # Transient transport error: retry on the next attempt.
            continue

        if response.status_code != 200:
            continue

        try:
            body = response.json()
        except ValueError:
            continue

        status = body.get("status")
        if status == "Success":
            places = _flatten_places(body.get("data"))
            if places:
                tracker.record(query, f"{len(places)} place(s)", "YES")
                return places
            tracker.record(query, "EMPTY SUCCESS", "NO")
            return []
        if status == "Pending":
            continue
        # Any other status is unexpected; stop polling.
        tracker.record(query, f"TIMEOUT (unexpected status: {status})", "NO")
        return []

    tracker.record(query, "TIMEOUT (poll attempts exhausted)", "NO")
    return []


# --- Query builders --------------------------------------------------------

def build_target_queries():
    """Return the query string(s) for the target venue.

    When unconfigured (TARGET_VENUE_NAME still the placeholder), return only
    the single full-form placeholder query.
    """
    full = f"{TARGET_VENUE_NAME}, {TARGET_CITY}, {TARGET_REGION}, {TARGET_COUNTRY}"
    if TARGET_VENUE_NAME.startswith("<"):
        return [full]
    short = f"{TARGET_VENUE_NAME}, {TARGET_CITY}"
    return [full, short]


def build_competitor_queries():
    """Return competitor discovery query string(s).

    Always includes the cuisine + city + region base query, plus a
    neighborhood-scoped query when COMPETITOR_NEIGHBORHOOD is set.
    """
    base = f"{COMPETITOR_CUISINE}, {TARGET_CITY}, {TARGET_REGION}"
    queries = [base]
    if COMPETITOR_NEIGHBORHOOD:
        queries.append(
            f"{COMPETITOR_CUISINE}, {COMPETITOR_NEIGHBORHOOD}, {TARGET_CITY}"
        )
    return queries


# --- Entry point -----------------------------------------------------------

def main():
    """Run the full pull. Returns 0 on success/unconfigured, 1 on no key."""
    api_key = load_api_key()
    if not api_key:
        print(
            "ERROR: FOOT_TRAFFIC_API_KEY not found in the environment or in "
            f"the credentials file ({CREDS_PATH}). Set the variable or add a "
            "FOOT_TRAFFIC_API_KEY=... line to the credentials file."
        )
        return 1

    if TARGET_VENUE_NAME.startswith("<"):
        print(
            "Script is unconfigured: TARGET_VENUE_NAME is still the "
            f"placeholder ({TARGET_VENUE_NAME}). Set TARGET_VENUE_NAME, "
            "TARGET_CITY, TARGET_REGION and TARGET_COUNTRY, then re-run. "
            "No API calls were made."
        )
        return 0

    tracker = CallTracker()

    # Target venue.
    target_place = None
    for query in build_target_queries():
        places = query_traffic_api(api_key, query, tracker)
        if places:
            target_place = places[0]
            break

    target = None
    if target_place:
        target = {
            "place": target_place,
            "popular_times": extract_popular_times(target_place),
        }

    # Competitors (deduped by place_id, target excluded).
    competitors = []
    seen_ids = set()
    target_id = (target_place or {}).get("place_id")
    if target_id:
        seen_ids.add(target_id)

    for query in build_competitor_queries():
        if not tracker.can_call():
            break
        for place in query_traffic_api(api_key, query, tracker, limit=5):
            place_id = place.get("place_id")
            name = place.get("name")
            if place_id and place_id in seen_ids:
                continue
            if name and name == TARGET_VENUE_NAME:
                continue
            if place_id:
                seen_ids.add(place_id)
            competitors.append(
                {
                    "place": place,
                    "popular_times": extract_popular_times(place),
                }
            )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "traffic-raw.json"
    payload = {
        "target": target,
        "competitors": competitors,
        "api_call_log": tracker.call_log,
        "api_calls_made": tracker.calls_made,
    }
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    print(f"Wrote {out_path}")
    print(f"API calls made: {tracker.calls_made} / {MAX_API_CALLS}")
    for entry in tracker.call_log:
        print(f"  - {entry['query']}: {entry['result']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
