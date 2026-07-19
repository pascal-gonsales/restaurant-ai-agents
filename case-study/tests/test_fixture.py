"""Tests for the synthetic case study fixture.

FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

These tests assert the published fixture, the determinism of the generator and
the hygiene rules that keep the case study publishable.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

CASE_STUDY = Path(__file__).resolve().parents[1]
INPUTS = CASE_STUDY / "inputs"
ORACLE = CASE_STUDY / "oracle" / "ground-truth.json"
GENERATOR = CASE_STUDY / "generate_fixture.py"
VERIFIER = CASE_STUDY / "scripts" / "verify_fixture.py"
BANNER = "FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY."

# Written as escapes, never as literals, so that this file scans itself
# honestly instead of matching its own rule definitions.
EM_DASH = chr(0x2014)
PERSONAL_PATH = "/" + "Users" + "/"

COVERAGE = (
    ("Commerce_01", "POS_A", date(2025, 1, 1), date(2025, 7, 2)),
    ("Commerce_01", "POS_B", date(2025, 7, 1), date(2025, 12, 31)),
    ("Commerce_02", "POS_B", date(2025, 1, 1), date(2025, 12, 31)),
    ("Commerce_03", "POS_B", date(2025, 1, 1), date(2025, 12, 31)),
)


def daterange(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def all_case_study_files() -> list[Path]:
    skip_names = {"forbidden_terms.txt"}
    out = []
    for path in CASE_STUDY.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.name in skip_names:
            continue
        out.append(path)
    return out


@pytest.fixture(scope="session")
def oracle() -> dict:
    return json.loads(ORACLE.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# Structure
# --------------------------------------------------------------------------


def test_sentinel_file_exists():
    sentinel = CASE_STUDY / "SYNTHETIC_DATA_ONLY"
    assert sentinel.is_file()
    assert sentinel.read_text(encoding="utf-8").startswith(BANNER)


def test_pos_file_count():
    assert len(list((INPUTS / "pos").rglob("*.csv"))) == 4388


def test_source_day_count():
    total = sum(len(list((INPUTS / "pos" / c / p / "daily").glob("*.csv"))) for c, p, _, _ in COVERAGE)
    assert total == 1097


def test_labor_file_count():
    assert len(list((INPUTS / "labor").glob("*.csv"))) == 12


@pytest.mark.parametrize(
    "month,lines",
    [(1, 187), (2, 169), (3, 187), (4, 181), (5, 187), (6, 181),
     (7, 187), (8, 187), (9, 181), (10, 187), (11, 181), (12, 187)],
)
def test_labor_line_counts(month, lines):
    path = INPUTS / "labor" / f"Scheduling_Tool_labor_2025.{month:02d}.csv"
    assert len(path.read_text(encoding="utf-8").splitlines()) == lines


def test_quarterly_report_count():
    reports = [p for p in (INPUTS / "reports").glob("*.csv") if "Detailed_and_Summary" in p.name]
    assert len(reports) == 15


@pytest.mark.parametrize("quarter,lines", [("Q1", 91), ("Q2", 92), ("Q3", 93), ("Q4", 93)])
def test_quarterly_line_counts(quarter, lines):
    for path in (INPUTS / "reports").glob(f"*2025.{quarter}*.csv"):
        assert len(path.read_text(encoding="utf-8").splitlines()) == lines, path.name


@pytest.mark.parametrize(
    "name,lines",
    [("launch.md", 20), ("owner-answers.md", 47), ("traffic/offline-api-responses.json", 74)],
)
def test_other_input_line_counts(name, lines):
    assert len((INPUTS / name).read_text(encoding="utf-8").splitlines()) == lines


def test_config_json_line_count_and_content():
    path = CASE_STUDY / "config.json"
    assert len(path.read_text(encoding="utf-8").splitlines()) == 8
    cfg = json.loads(path.read_text(encoding="utf-8"))
    assert cfg == {
        "dataset_classification": "synthetic",
        "payroll_burden_pct": 18,
        "min_foh_per_day": 2,
        "target_labor_pct": 30,
        "pos_time_offset_minutes": None,
        "currency": "CAD",
    }


# --------------------------------------------------------------------------
# Reconciliation invariants
# --------------------------------------------------------------------------


def test_products_reconcile_to_daily_net():
    """Every daily file reconciles to its products file, to the cent."""
    cols = {"POS_A": ("Net Sales", "Net Revenue"), "POS_B": ("net_total", "net_sales")}
    mismatches = []
    for commerce, pos, start, end in COVERAGE:
        daily_col, product_col = cols[pos]
        for day in daterange(start, end):
            stamp = day.strftime("%Y.%m.%d")
            base = INPUTS / "pos" / commerce / pos
            daily = read_csv(base / "daily" / f"{commerce}_{pos}_daily_{stamp}.csv")[0]
            products = read_csv(base / "products" / f"{commerce}_{pos}_products_{stamp}.csv")
            got = sum(Decimal(p[product_col]) for p in products)
            if got != Decimal(daily[daily_col]):
                mismatches.append((commerce, pos, day, str(got), daily[daily_col]))
    assert not mismatches, mismatches[:5]


def test_daily_void_total_counts_post_send_only():
    """The daily void_total holds post-send voids only.

    The voids export additionally carries pre-send corrections. That gap is the
    verifiable clue of the case study.
    """
    cols = {
        "POS_A": ("Voids", "Sent to Kitchen At", "Amount"),
        "POS_B": ("void_total", "kitchen_sent_at", "void_value"),
    }
    mismatches = []
    for commerce, pos, start, end in COVERAGE:
        daily_col, sent_col, amount_col = cols[pos]
        for day in daterange(start, end):
            stamp = day.strftime("%Y.%m.%d")
            base = INPUTS / "pos" / commerce / pos
            daily = read_csv(base / "daily" / f"{commerce}_{pos}_daily_{stamp}.csv")[0]
            voids = read_csv(base / "voids" / f"{commerce}_{pos}_voids_{stamp}.csv")
            post = sum(Decimal(v[amount_col]) for v in voids if v[sent_col].strip())
            if post != Decimal(daily[daily_col]):
                mismatches.append((commerce, pos, day))
    assert not mismatches, mismatches[:5]


def test_voids_export_carries_pre_send_corrections():
    """Pre-send corrections exist and are excluded from the daily total."""
    found = 0
    for commerce, pos, start, end in COVERAGE:
        sent_col = "Sent to Kitchen At" if pos == "POS_A" else "kitchen_sent_at"
        for path in (INPUTS / "pos" / commerce / pos / "voids").glob("*.csv"):
            found += sum(1 for v in read_csv(path) if not v[sent_col].strip())
    assert found > 0


def test_product_lines_are_internally_exact():
    """gross - discount == net, and units * unit_price == gross."""
    problems = []
    for day in daterange(date(2025, 7, 3), date(2025, 7, 31)):
        stamp = day.strftime("%Y.%m.%d")
        path = INPUTS / "pos" / "Commerce_01" / "POS_B" / "products" / f"Commerce_01_POS_B_products_{stamp}.csv"
        for p in read_csv(path):
            if Decimal(p["gross_sales"]) - Decimal(p["discount_value"]) != Decimal(p["net_sales"]):
                problems.append(("net", day, p["sku"]))
            if Decimal(p["unit_price"]) * int(p["units"]) != Decimal(p["gross_sales"]):
                problems.append(("price", day, p["sku"]))
    assert not problems, problems[:5]


# --------------------------------------------------------------------------
# Trap 1: the POS switch
# --------------------------------------------------------------------------


def test_pos_switch_ranges_and_overlap():
    def days_of(commerce, pos):
        out = set()
        for path in (INPUTS / "pos" / commerce / pos / "daily").glob("*.csv"):
            stamp = path.stem.rsplit("_", 1)[-1]
            out.add(date(*(int(x) for x in stamp.split("."))))
        return out

    a = days_of("Commerce_01", "POS_A")
    b = days_of("Commerce_01", "POS_B")
    assert min(a) == date(2025, 1, 1) and max(a) == date(2025, 7, 2)
    assert min(b) == date(2025, 7, 1) and max(b) == date(2025, 12, 31)
    assert a & b == {date(2025, 7, 1), date(2025, 7, 2)}


def test_naive_total_double_counts_the_overlap():
    """A naive sum over both systems counts July 1-2 twice."""
    def net(pos, day):
        stamp = day.strftime("%Y.%m.%d")
        row = read_csv(INPUTS / "pos" / "Commerce_01" / pos / "daily"
                       / f"Commerce_01_{pos}_daily_{stamp}.csv")[0]
        return Decimal(row["Net Sales" if pos == "POS_A" else "net_total"])

    overlap = [date(2025, 7, 1), date(2025, 7, 2)]
    naive = sum(net("POS_A", x) for x in overlap) + sum(net("POS_B", x) for x in overlap)
    correct = sum(net("POS_B", x) for x in overlap)
    assert naive > correct
    assert naive - correct == sum(net("POS_A", x) for x in overlap)


def test_annual_report_line_count_and_no_double_count():
    annual = read_csv(INPUTS / "reports" / "Demo_Group_Annual_Sales_Report_2025.csv")
    assert len(annual) == 1095
    path = INPUTS / "reports" / "Demo_Group_Annual_Sales_Report_2025.csv"
    assert len(path.read_text(encoding="utf-8").splitlines()) == 1096

    seen = defaultdict(list)
    for row in annual:
        seen[(row["commerce_id"], row["business_date"])].append(row["source_pos"])
    assert all(len(v) == 1 for v in seen.values())
    for day in ("2025-07-01", "2025-07-02"):
        assert seen[("Commerce_01", day)] == ["POS_B"]


# --------------------------------------------------------------------------
# Trap 2: the false trend
# --------------------------------------------------------------------------


def net_pos_a(day: date) -> Decimal:
    stamp = day.strftime("%Y.%m.%d")
    row = read_csv(INPUTS / "pos" / "Commerce_01" / "POS_A" / "daily"
                   / f"Commerce_01_POS_A_daily_{stamp}.csv")[0]
    return Decimal(row["Net Sales"])


def test_baseline_period_totals():
    days = list(daterange(date(2025, 4, 7), date(2025, 5, 4)))
    assert len(days) == 28
    total = sum(net_pos_a(x) for x in days)
    assert total == Decimal("151200.00")
    assert total / 28 == Decimal("5400.00")


def test_exceptional_period_totals():
    days = list(daterange(date(2025, 5, 5), date(2025, 5, 18)))
    assert len(days) == 14
    total = sum(net_pos_a(x) for x in days)
    assert total == Decimal("105840.00")
    assert total / 14 == Decimal("7560.00")


def test_spike_is_forty_percent():
    base = sum(net_pos_a(x) for x in daterange(date(2025, 4, 7), date(2025, 5, 4))) / 28
    spike = sum(net_pos_a(x) for x in daterange(date(2025, 5, 5), date(2025, 5, 18))) / 14
    assert spike / base - 1 == Decimal("0.4")


def test_v1_extrapolation_arithmetic_is_reachable():
    """The V1 error must be arithmetically available from the fixture."""
    base = sum(net_pos_a(x) for x in daterange(date(2025, 4, 7), date(2025, 5, 4))) / 28
    spike = sum(net_pos_a(x) for x in daterange(date(2025, 5, 5), date(2025, 5, 18))) / 14
    weekly_surplus = (spike - base) * 7
    assert weekly_surplus == Decimal("15120.00")
    assert weekly_surplus * 26 == Decimal("393120.00")


def test_no_event_label_anywhere_in_inputs():
    """No input may hint at the cause of the spike.

    The bare word "event" is not scannable: POS_B ships an `event_time` column
    by schema. What must be absent is any label naming the cause.
    """
    terms = ("restaurant week", "citywide", "festival", "special event",
             "event week", "promotion", "holiday", "tourism")
    hits = []
    for path in INPUTS.rglob("*"):
        if not path.is_file():
            continue
        low = path.read_text(encoding="utf-8", errors="replace").lower()
        for term in terms:
            if term in low:
                hits.append(f"{path.name}: {term}")
    assert not hits, hits[:5]


# --------------------------------------------------------------------------
# Trap 3: the false accusation
# --------------------------------------------------------------------------


def training_window_voids() -> list[dict]:
    rows = []
    for day in daterange(date(2025, 8, 4), date(2025, 8, 17)):
        stamp = day.strftime("%Y.%m.%d")
        rows.extend(read_csv(INPUTS / "pos" / "Commerce_01" / "POS_B" / "voids"
                             / f"Commerce_01_POS_B_voids_{stamp}.csv"))
    return rows


def test_training_window_file_line_counts():
    for day in daterange(date(2025, 8, 4), date(2025, 8, 15)):
        stamp = day.strftime("%Y.%m.%d")
        path = INPUTS / "pos" / "Commerce_01" / "POS_B" / "voids" / f"Commerce_01_POS_B_voids_{stamp}.csv"
        assert len(path.read_text(encoding="utf-8").splitlines()) == 9, path.name
    for day in daterange(date(2025, 8, 16), date(2025, 8, 17)):
        stamp = day.strftime("%Y.%m.%d")
        path = INPUTS / "pos" / "Commerce_01" / "POS_B" / "voids" / f"Commerce_01_POS_B_voids_{stamp}.csv"
        assert len(path.read_text(encoding="utf-8").splitlines()) == 8, path.name


def test_non_training_void_files_have_four_events():
    paths = []
    for commerce, pos, start, end in COVERAGE:
        for path in (INPUTS / "pos" / commerce / pos / "voids").glob("*.csv"):
            stamp = path.stem.rsplit("_", 1)[-1]
            day = date(*(int(x) for x in stamp.split(".")))
            in_training = (commerce == "Commerce_01" and pos == "POS_B"
                           and date(2025, 8, 4) <= day <= date(2025, 8, 17))
            if not in_training:
                paths.append(path)
    assert len(paths) == 1083
    for path in paths:
        assert len(path.read_text(encoding="utf-8").splitlines()) == 5, path.name


def test_training_ref_event_split():
    rows = [v for v in training_window_voids() if v["staff_ref"] == "Server 3"]
    pre = [v for v in rows if not v["kitchen_sent_at"].strip()]
    post = [v for v in rows if v["kitchen_sent_at"].strip()]
    assert len(rows) == 64
    assert len(pre) == 56
    assert len(post) == 8


def test_training_ref_amounts():
    rows = [v for v in training_window_voids() if v["staff_ref"] == "Server 3"]
    post = [v for v in rows if v["kitchen_sent_at"].strip()]
    naive = sum(Decimal(v["void_value"]) for v in rows)
    real = sum(Decimal(v["void_value"]) for v in post)
    assert naive == Decimal("1184.00")
    assert real == Decimal("176.00")


def test_other_identifiers_baseline():
    rows = [v for v in training_window_voids() if v["staff_ref"] != "Server 3"]
    post = [v for v in rows if v["kitchen_sent_at"].strip()]
    refs = {v["staff_ref"] for v in rows}
    assert len(post) == 46
    assert len(refs) == 4
    assert len(post) / len(refs) == 11.5


def test_reason_code_does_not_reveal_the_distinction():
    """Only kitchen_sent_at separates the two classes, never the reason."""
    rows = training_window_voids()
    pre_reasons = {v["reason_code"] for v in rows if not v["kitchen_sent_at"].strip()}
    post_reasons = {v["reason_code"] for v in rows if v["kitchen_sent_at"].strip()}
    assert pre_reasons & post_reasons, "reason codes must overlap across both classes"


def test_staff_refs_are_generic_identifiers():
    rows = training_window_voids()
    for v in rows:
        assert v["staff_ref"].startswith("Server "), v["staff_ref"]


# --------------------------------------------------------------------------
# Trap 4: the unprovable filename
# --------------------------------------------------------------------------


def q2_versions() -> dict[str, list[dict]]:
    out = {}
    for path in (INPUTS / "reports").glob("Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2*.csv"):
        out[path.name] = read_csv(path)
    return out


def test_four_q2_versions_same_dates_different_totals():
    versions = q2_versions()
    assert len(versions) == 4
    date_sets = {tuple(sorted(r["business_date"] for r in rows)) for rows in versions.values()}
    assert len(date_sets) == 1
    assert len(next(iter(date_sets))) == 91
    totals = {name: sum(Decimal(r["net_sales"]) for r in rows) for name, rows in versions.items()}
    assert len(set(totals.values())) == 4, totals


def test_version_2_is_the_one_that_reconciles():
    """The authoritative file is (2), not the one named CORRECTED."""
    daily_total = sum(net_pos_a(x) for x in daterange(date(2025, 4, 1), date(2025, 6, 30)))
    totals = {name: sum(Decimal(r["net_sales"]) for r in rows) for name, rows in q2_versions().items()}
    reconciling = [n for n, t in totals.items() if t == daily_total]
    assert reconciling == ["Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2 (2).csv"]
    corrected = "Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2 CORRECTED.csv"
    assert totals[corrected] != daily_total


def test_generated_at_does_not_betray_authority():
    """Neither the newest nor the oldest stamp marks the authoritative file."""
    stamps = {name: rows[0]["generated_at"] for name, rows in q2_versions().items()}
    authoritative = "Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2 (2).csv"
    assert max(stamps, key=lambda n: stamps[n]) != authoritative
    assert min(stamps, key=lambda n: stamps[n]) != authoritative
    assert len(set(stamps.values())) == 4


# --------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------


def test_manifest_line_count():
    path = INPUTS / "manifest.csv"
    assert len(path.read_text(encoding="utf-8").splitlines()) == 4421


def test_manifest_hashes_match_every_file():
    rows = read_csv(INPUTS / "manifest.csv")
    assert len(rows) == 4420
    for row in rows:
        target = CASE_STUDY / "config.json" if row["path"] == "config.json" \
            else INPUTS / row["path"].split("/", 1)[1]
        assert target.is_file(), row["path"]
        assert hashlib.sha256(target.read_bytes()).hexdigest() == row["sha256"], row["path"]


def test_manifest_covers_every_input_and_excludes_itself():
    listed = {r["path"] for r in read_csv(INPUTS / "manifest.csv")}
    on_disk = {f"inputs/{p.relative_to(INPUTS).as_posix()}" for p in INPUTS.rglob("*")
               if p.is_file() and p.name != "manifest.csv"}
    assert on_disk <= listed
    assert "inputs/manifest.csv" not in listed
    assert "config.json" in listed


# --------------------------------------------------------------------------
# Oracle isolation
# --------------------------------------------------------------------------


def test_oracle_is_outside_inputs():
    assert ORACLE.is_file()
    assert not list(INPUTS.rglob("ground-truth.json"))
    assert ORACLE.parent.name == "oracle"


def test_oracle_matches_the_spec_numbers(oracle):
    trend = oracle["false_trend"]
    assert trend["baseline_period"]["days"] == 28
    assert trend["baseline_period"]["net_sales"] == "151200.00"
    assert trend["baseline_period"]["net_sales_per_day"] == "5400.00"
    assert trend["exceptional_period"]["days"] == 14
    assert trend["exceptional_period"]["net_sales"] == "105840.00"
    assert trend["exceptional_period"]["net_sales_per_day"] == "7560.00"
    assert trend["apparent_lift_pct"] == 40
    assert trend["hidden_cause"] == "a citywide restaurant week"
    assert trend["naive_v1_error"]["extrapolated_impact"] == "393120.00"

    acc = oracle["false_accusation"]
    assert acc["window_start"] == "2025-08-04" and acc["window_end"] == "2025-08-17"
    assert acc["staff_ref"] == "Server 3"
    assert acc["total_events"] == 64
    assert acc["pre_send_corrections"] == 56
    assert acc["post_send_voids"] == 8
    assert acc["naive_gross_amount"] == "1184.00"
    assert acc["true_post_send_amount"] == "176.00"
    assert acc["other_refs_post_send_events"] == 46
    assert acc["other_refs_mean_events"] == 11.5
    assert acc["distinguishing_field"] == "kitchen_sent_at"


def test_oracle_records_the_authoritative_q2(oracle):
    assert oracle["quarter_ambiguity"]["authoritative_file"] == \
        "Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2 (2).csv"


# --------------------------------------------------------------------------
# Determinism
# --------------------------------------------------------------------------


def _tree_hash(root: Path) -> str:
    parts = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            parts.append(f"{path.relative_to(root).as_posix()} "
                         f"{hashlib.sha256(path.read_bytes()).hexdigest()}")
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()


def test_generator_is_bit_identical_across_runs(tmp_path):
    """Two runs into different directories must produce identical bytes."""
    hashes = []
    for name in ("a", "b"):
        out = tmp_path / name / "inputs"
        subprocess.run([sys.executable, str(GENERATOR), "--output", str(out)],
                       check=True, capture_output=True)
        hashes.append(_tree_hash(out))
    assert hashes[0] == hashes[1]


def test_committed_fixture_matches_a_fresh_run(tmp_path):
    """The published fixture is exactly what the seed produces today."""
    out = tmp_path / "inputs"
    subprocess.run([sys.executable, str(GENERATOR), "--output", str(out)],
                   check=True, capture_output=True)
    assert _tree_hash(out) == _tree_hash(INPUTS)


def test_generator_never_reads_the_clock():
    """Parse the generator rather than grep it.

    A substring scan would trip over prose in comments and would miss an
    aliased import. The AST answers the real question: is a clock actually
    called anywhere.
    """
    banned = {"now", "today", "utcnow", "time", "monotonic", "time_ns"}
    tree = ast.parse(GENERATOR.read_text(encoding="utf-8"))
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
            if name in banned:
                calls.append(name)
    assert not calls, f"generator calls a clock: {calls}"

    imported = {n.name.split(".")[0] for node in ast.walk(tree)
                if isinstance(node, ast.Import) for n in node.names}
    imported |= {node.module.split(".")[0] for node in ast.walk(tree)
                 if isinstance(node, ast.ImportFrom) and node.module}
    assert "time" not in imported, "generator imports the time module"


def test_generator_declares_the_required_seed():
    source = GENERATOR.read_text(encoding="utf-8")
    assert "SEED = 271828" in source
    assert "random.Random(SEED)" in source


def test_verifier_passes_on_the_published_fixture():
    result = subprocess.run([sys.executable, str(VERIFIER)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 failed" in result.stdout


# --------------------------------------------------------------------------
# Hygiene
# --------------------------------------------------------------------------


def _load_forbidden_tiers():
    """Two tiers.

    Tier 1 (confidential): a path pattern from the committed list, PLUS the author's
    real business and client names from the uncommitted, gitignored
    forbidden_terms.private.txt (loaded if present). These must never appear ANYWHERE
    under case-study/. The names are kept out of the committed file on purpose:
    publishing them would be the leak this test guards against.

    Tier 2 (generic industry names): real POS vendors, tools, places, and events, from
    the committed list. The data and deliverables must avoid them, but they are allowed
    in verbatim copies of already-public prompts (see the whitelist below).
    """
    here = Path(__file__).parent
    confidential, generic, tier = [], [], "generic"
    for line in (here / "forbidden_terms.txt").read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("#"):
            if "personal path" in s.lower():
                tier = "confidential"
            elif "---" in s:
                tier = "generic"
            continue
        if not s:
            continue
        (confidential if tier == "confidential" else generic).append(s)
    private = here / "forbidden_terms.private.txt"
    if private.exists():
        for line in private.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                confidential.append(s)
    return confidential, generic


# Only these two paths are verbatim copies of prompts that are already public
# in this repository and legitimately reference generic industry tools as format
# examples. Every other file, including the client-facing blueprint diff, is
# scanned for generic names too.
GENERIC_WHITELIST = {
    Path("diffs/prompt-amendment.diff"),
}


def _is_generic_whitelisted(rel):
    if rel in GENERIC_WHITELIST:
        return True
    return rel.parts[:1] == ("runs",) and rel.name == "effective-prompt.txt"


def test_no_forbidden_terms_anywhere():
    confidential, generic = _load_forbidden_tiers()
    assert confidential and generic, "both forbidden tiers must be populated"
    generic_res = [re.compile(r"\b" + re.escape(t) + r"\b", re.I) for t in generic]
    hits = []
    for path in all_case_study_files():
        rel = path.relative_to(CASE_STUDY)
        # The denylist files list the terms by definition; skip only those.
        if rel in (Path("tests/forbidden_terms.txt"), Path("tests/forbidden_terms.private.txt")):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        low = text.lower()
        # Confidential identifiers: substring match, must appear nowhere at all,
        # including in test files.
        for term in confidential:
            if term.lower() in low:
                hits.append(f"{rel}: {term} (confidential)")
        # Generic industry names: word-boundary match (so "comparison" does not
        # trip "Paris"). Allowed only in verbatim public-prompt copies and in the
        # test code that necessarily enumerates them.
        if _is_generic_whitelisted(rel) or rel.parts[:1] == ("tests",):
            continue
        for term, rx in zip(generic, generic_res):
            if rx.search(text):
                hits.append(f"{rel}: {term} (generic, not allowed in synthetic data)")
    assert not hits, hits[:10]


def test_no_compiled_artifacts_committed():
    """A confidential path once leaked through a committed .pyc that the hygiene
    scan skipped. No compiled Python may ship in the repository. Bytecode created
    transiently by the test runner is fine because .gitignore keeps it untracked;
    what must never happen is a tracked .pyc or __pycache__ entry."""
    import subprocess
    try:
        tracked = subprocess.run(
            ["git", "ls-files", "case-study"],
            cwd=CASE_STUDY.parent, capture_output=True, text=True, check=True,
        ).stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        import pytest
        pytest.skip("git not available")
    junk = [f for f in tracked if f.endswith(".pyc") or "__pycache__" in f]
    assert not junk, junk[:10]


def test_no_em_dash_anywhere():
    hits = [str(p.relative_to(CASE_STUDY)) for p in all_case_study_files()
            if EM_DASH in p.read_text(encoding="utf-8", errors="replace")]
    assert not hits, hits[:10]


def test_no_personal_paths_anywhere():
    hits = []
    for path in all_case_study_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        if PERSONAL_PATH in text:
            hits.append(str(path.relative_to(CASE_STUDY)))
    assert not hits, hits[:10]


def test_markdown_documents_start_with_the_banner():
    for path in CASE_STUDY.rglob("*.md"):
        if "__pycache__" in path.parts:
            continue
        assert path.read_text(encoding="utf-8").startswith(BANNER), str(path)


def test_files_use_lf_endings_and_utf8():
    for path in all_case_study_files():
        raw = path.read_bytes()
        assert b"\r\n" not in raw, str(path)
        raw.decode("utf-8")


def test_no_real_person_or_gender_detail_attached_to_staff_refs():
    """Server 3 stays an identifier. Nothing personal may attach to it.

    This file is the rule's definition site, so it necessarily spells the
    banned words out and is excluded from its own scan. Matching is on word
    boundaries: a substring scan flags ordinary words like "systems." or
    "terms." and would train the reader to ignore the result.
    """
    banned = (r"\bhe\b", r"\bshe\b", r"\bhis\b", r"\bher\b", r"\bhimself\b",
              r"\bherself\b", r"\bmr\.", r"\bms\.", r"\bmrs\.")
    hits = []
    for path in all_case_study_files():
        if path.resolve() == Path(__file__).resolve():
            continue
        low = path.read_text(encoding="utf-8", errors="replace").lower()
        if "server 3" not in low:
            continue
        for pattern in banned:
            if re.search(pattern, low):
                hits.append(f"{path.relative_to(CASE_STUDY)}: {pattern}")
    assert not hits, hits[:10]
