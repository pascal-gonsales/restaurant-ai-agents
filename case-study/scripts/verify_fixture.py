#!/usr/bin/env python3
"""Independently re-check every fixture invariant.

FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

This script deliberately does not import generate_fixture.py. It reads the
written files and recomputes each invariant from scratch, so a bug in the
generator cannot hide behind shared code. Exit code 0 means every invariant
holds.

Usage:
    python3 case-study/scripts/verify_fixture.py
    python3 case-study/scripts/verify_fixture.py --manifest case-study/inputs/manifest.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

CASE_STUDY = Path(__file__).resolve().parents[1]

BANNER = "FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY."
EXPECTED_POS_FILES = 4388
EXPECTED_SOURCE_DAYS = 1097
EXPECTED_MANIFEST_LINES = 4421
EXPECTED_ANNUAL_LINES = 1096
EXPECTED_QUARTERLY_FILES = 15
EXPECTED_LABOR_FILES = 12

TRAINING_START, TRAINING_END = date(2025, 8, 4), date(2025, 8, 17)
TRAINING_REF = "Server 3"
OVERLAP_DATES = (date(2025, 7, 1), date(2025, 7, 2))
SPIKE_START, SPIKE_END = date(2025, 5, 5), date(2025, 5, 18)
BASELINE_START, BASELINE_END = date(2025, 4, 7), date(2025, 5, 4)


class Report:
    def __init__(self) -> None:
        self.passes: list[str] = []
        self.failures: list[str] = []

    def check(self, ok: bool, label: str, detail: str = "") -> bool:
        if ok:
            self.passes.append(label)
        else:
            self.failures.append(f"{label}: {detail}")
        return ok

    def equal(self, got, want, label: str) -> bool:
        return self.check(got == want, label, f"got {got!r}, want {want!r}")


def d(value: str) -> Decimal:
    return Decimal(value)


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def daterange(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def pos_files(inputs: Path, commerce: str, pos: str, kind: str) -> list[Path]:
    return sorted((inputs / "pos" / commerce / pos / kind).glob("*.csv"))


def parse_day(path: Path) -> date:
    stamp = path.stem.rsplit("_", 1)[-1]
    return date(*(int(x) for x in stamp.split(".")))


# Column names differ per POS. Map them to one vocabulary.
DAILY_COLS = {
    "POS_A": {"date": "Business Date", "gross": "Gross Sales", "disc": "Discounts",
              "void": "Voids", "net": "Net Sales"},
    "POS_B": {"date": "business_date", "gross": "sales_total", "disc": "discount_total",
              "void": "void_total", "net": "net_total"},
}
PRODUCT_COLS = {
    "POS_A": {"gross": "Gross Revenue", "disc": "Discounts", "net": "Net Revenue",
              "units": "Quantity Sold", "price": None},
    "POS_B": {"gross": "gross_sales", "disc": "discount_value", "net": "net_sales",
              "units": "units", "price": "unit_price"},
}
VOID_COLS = {
    "POS_A": {"ref": "Employee ID", "amount": "Amount", "sent": "Sent to Kitchen At"},
    "POS_B": {"ref": "staff_ref", "amount": "void_value", "sent": "kitchen_sent_at"},
}
DISCOUNT_COLS = {
    "POS_A": {"amount": "Discount Amount"},
    "POS_B": {"amount": "discount_value"},
}

COVERAGE = (
    ("Commerce_01", "POS_A", date(2025, 1, 1), date(2025, 7, 2)),
    ("Commerce_01", "POS_B", date(2025, 7, 1), date(2025, 12, 31)),
    ("Commerce_02", "POS_B", date(2025, 1, 1), date(2025, 12, 31)),
    ("Commerce_03", "POS_B", date(2025, 1, 1), date(2025, 12, 31)),
)


def verify(inputs: Path, oracle_path: Path, manifest_path: Path, rep: Report) -> None:
    # ---- structure -------------------------------------------------------
    all_pos = list((inputs / "pos").rglob("*.csv"))
    rep.equal(len(all_pos), EXPECTED_POS_FILES, "POS file count")
    rep.equal(len(list((inputs / "labor").glob("*.csv"))), EXPECTED_LABOR_FILES, "labor file count")
    quarterly = [p for p in (inputs / "reports").glob("*.csv") if "Detailed_and_Summary" in p.name]
    rep.equal(len(quarterly), EXPECTED_QUARTERLY_FILES, "quarterly report count")

    # ---- coverage and the deliberate POS overlap -------------------------
    for commerce, pos, start, end in COVERAGE:
        got = {parse_day(p) for p in pos_files(inputs, commerce, pos, "daily")}
        want = set(daterange(start, end))
        rep.equal(got, want, f"{commerce}/{pos} daily coverage")

    a_days = {parse_day(p) for p in pos_files(inputs, "Commerce_01", "POS_A", "daily")}
    b_days = {parse_day(p) for p in pos_files(inputs, "Commerce_01", "POS_B", "daily")}
    rep.equal(a_days & b_days, set(OVERLAP_DATES), "Commerce_01 POS overlap is exactly Jul 1-2")

    total_source_days = sum(len(pos_files(inputs, c, p, "daily")) for c, p, _, _ in COVERAGE)
    rep.equal(total_source_days, EXPECTED_SOURCE_DAYS, "source-day count")

    # ---- per-day reconciliation -----------------------------------------
    daily_by_key: dict[tuple[str, str, date], dict] = {}
    net_mismatch, void_mismatch, disc_mismatch, product_mismatch = [], [], [], []

    for commerce, pos, start, end in COVERAGE:
        dc, pc, vc, xc = DAILY_COLS[pos], PRODUCT_COLS[pos], VOID_COLS[pos], DISCOUNT_COLS[pos]
        for day in daterange(start, end):
            stamp = day.strftime("%Y.%m.%d")
            base = inputs / "pos" / commerce / pos
            daily = read_csv(base / "daily" / f"{commerce}_{pos}_daily_{stamp}.csv")[0]
            products = read_csv(base / "products" / f"{commerce}_{pos}_products_{stamp}.csv")
            voids = read_csv(base / "voids" / f"{commerce}_{pos}_voids_{stamp}.csv")
            discounts = read_csv(base / "discounts" / f"{commerce}_{pos}_discounts_{stamp}.csv")
            daily_by_key[(commerce, pos, day)] = daily

            # products net must reconcile to the daily net, to the cent
            if sum(d(p[pc["net"]]) for p in products) != d(daily[dc["net"]]):
                net_mismatch.append(f"{commerce}/{pos}/{day}")
            # gross - discount == net, per product line
            for p in products:
                if d(p[pc["gross"]]) - d(p[pc["disc"]]) != d(p[pc["net"]]):
                    product_mismatch.append(f"{commerce}/{pos}/{day}/{p.get('sku') or p.get('Product ID')}")
                if pc["price"] and d(p[pc["price"]]) * int(p[pc["units"]]) != d(p[pc["gross"]]):
                    product_mismatch.append(f"price*units {commerce}/{pos}/{day}")
            # the daily void total counts post-send voids only
            post_send = [v for v in voids if v[vc["sent"]].strip() != ""]
            if sum(d(v[vc["amount"]]) for v in post_send) != d(daily[dc["void"]]):
                void_mismatch.append(f"{commerce}/{pos}/{day}")
            # discount lines reconcile to the daily discount total
            if sum(d(x[xc["amount"]]) for x in discounts) != d(daily[dc["disc"]]):
                disc_mismatch.append(f"{commerce}/{pos}/{day}")

    rep.check(not net_mismatch, "products net reconciles to daily net for all 1097 days",
              f"{len(net_mismatch)} mismatches, first: {net_mismatch[:3]}")
    rep.check(not product_mismatch, "per-product gross/discount/net and price*units are exact",
              f"{len(product_mismatch)} mismatches, first: {product_mismatch[:3]}")
    rep.check(not void_mismatch, "daily void_total equals post-send voids only",
              f"{len(void_mismatch)} mismatches, first: {void_mismatch[:3]}")
    rep.check(not disc_mismatch, "discount lines reconcile to daily discount total",
              f"{len(disc_mismatch)} mismatches, first: {disc_mismatch[:3]}")

    # ---- the voids export carries pre-send corrections the daily total omits
    pre_send_days = 0
    for commerce, pos, start, end in COVERAGE:
        vc = VOID_COLS[pos]
        for path in pos_files(inputs, commerce, pos, "voids"):
            rows = read_csv(path)
            if any(v[vc["sent"]].strip() == "" for v in rows):
                pre_send_days += 1
    rep.check(pre_send_days > 0, "voids export contains pre-send corrections absent from void_total",
              "no pre-send rows found anywhere")

    # ---- training window -------------------------------------------------
    window = list(daterange(TRAINING_START, TRAINING_END))
    ref_pre, ref_post, other_post, other_refs = 0, 0, 0, set()
    ref_pre_amt, ref_post_amt = Decimal("0"), Decimal("0")
    for day in window:
        stamp = day.strftime("%Y.%m.%d")
        rows = read_csv(inputs / "pos" / "Commerce_01" / "POS_B" / "voids"
                        / f"Commerce_01_POS_B_voids_{stamp}.csv")
        for v in rows:
            is_pre = v["kitchen_sent_at"].strip() == ""
            amount = d(v["void_value"])
            if v["staff_ref"] == TRAINING_REF:
                if is_pre:
                    ref_pre += 1
                    ref_pre_amt += amount
                else:
                    ref_post += 1
                    ref_post_amt += amount
            else:
                other_refs.add(v["staff_ref"])
                if not is_pre:
                    other_post += 1

    rep.equal(ref_pre + ref_post, 64, f"{TRAINING_REF} total events in training window")
    rep.equal(ref_pre, 56, f"{TRAINING_REF} pre-send corrections")
    rep.equal(ref_post, 8, f"{TRAINING_REF} post-send voids")
    rep.equal(ref_pre_amt + ref_post_amt, d("1184.00"), f"{TRAINING_REF} naive gross amount")
    rep.equal(ref_post_amt, d("176.00"), f"{TRAINING_REF} true post-send amount")
    rep.equal(other_post, 46, "other identifiers combined post-send voids")
    rep.equal(len(other_refs), 4, "other identifier count")
    rep.equal(round(other_post / len(other_refs), 2) if other_refs else 0, 11.5,
              "other identifiers mean post-send voids")

    # ---- the hidden spike, and no event label anywhere -------------------
    def net_of(day: date) -> Decimal:
        return d(daily_by_key[("Commerce_01", "POS_A", day)]["Net Sales"])

    baseline_days = list(daterange(BASELINE_START, BASELINE_END))
    spike_days = list(daterange(SPIKE_START, SPIKE_END))
    baseline_total = sum(net_of(x) for x in baseline_days)
    spike_total = sum(net_of(x) for x in spike_days)
    rep.equal(len(baseline_days), 28, "baseline period length")
    rep.equal(len(spike_days), 14, "exceptional period length")
    rep.equal(baseline_total, d("151200.00"), "baseline period net sales")
    rep.equal(spike_total, d("105840.00"), "exceptional period net sales")
    rep.equal(baseline_total / 28, d("5400.00"), "baseline net sales per day")
    rep.equal(spike_total / 14, d("7560.00"), "exceptional net sales per day")
    rep.equal(round((spike_total / 14) / (baseline_total / 28) - 1, 4), Decimal("0.4000"),
              "apparent lift is 40 percent")

    # ---- the four Q2 versions -------------------------------------------
    q2 = sorted((inputs / "reports").glob("Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2*.csv"))
    rep.equal(len(q2), 4, "Commerce_01 Q2 version count")
    date_sets, totals, stamps = [], {}, {}
    for path in q2:
        rows = read_csv(path)
        date_sets.append(tuple(sorted(r["business_date"] for r in rows)))
        totals[path.name] = sum(d(r["net_sales"]) for r in rows)
        stamps[path.name] = rows[0]["generated_at"]
    rep.check(len(set(date_sets)) == 1, "all four Q2 versions cover the same dates", "date sets differ")
    rep.equal(len(date_sets[0]), 91, "Q2 date count")
    rep.check(len(set(totals.values())) == 4, "all four Q2 versions carry different totals",
              f"totals: {totals}")

    daily_q2_total = sum(net_of(x) for x in daterange(date(2025, 4, 1), date(2025, 6, 30)))
    reconciling = [n for n, t in totals.items() if t == daily_q2_total]
    rep.equal(reconciling, ["Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2 (2).csv"],
              "the (2) version is the one that reconciles the daily exports")
    corrected = "Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2 CORRECTED.csv"
    rep.check(totals[corrected] != daily_q2_total,
              "the CORRECTED version does not reconcile", "CORRECTED unexpectedly reconciles")
    newest = max(stamps, key=lambda n: stamps[n])
    rep.check(newest != "Commerce_01_POS_A_Detailed_and_Summary_Report_2025.Q2 (2).csv",
              "generated_at does not betray the authoritative version",
              f"newest stamp is the authoritative file: {newest}")

    # ---- annual report ---------------------------------------------------
    annual_path = inputs / "reports" / "Demo_Group_Annual_Sales_Report_2025.csv"
    annual = read_csv(annual_path)
    rep.equal(len(annual) + 1, EXPECTED_ANNUAL_LINES, "annual report line count")
    seen = defaultdict(list)
    for r in annual:
        seen[(r["commerce_id"], r["business_date"])].append(r["source_pos"])
    dupes = {k: v for k, v in seen.items() if len(v) > 1}
    rep.check(not dupes, "annual report has no duplicated commerce-date", f"{list(dupes)[:3]}")
    for day in OVERLAP_DATES:
        rows = seen[("Commerce_01", day.isoformat())]
        rep.equal(rows, ["POS_B"], f"annual report resolves {day} to POS_B once")

    # ---- manifest --------------------------------------------------------
    manifest = read_csv(manifest_path)
    rep.equal(len(manifest) + 1, EXPECTED_MANIFEST_LINES, "manifest line count")
    bad_hash, missing = [], []
    for row in manifest:
        logical = row["path"]
        if logical == "config.json":
            target = CASE_STUDY / "config.json"
        else:
            target = inputs / logical.split("/", 1)[1]
        if not target.is_file():
            missing.append(logical)
            continue
        if hashlib.sha256(target.read_bytes()).hexdigest() != row["sha256"]:
            bad_hash.append(logical)
    rep.check(not missing, "every manifest row points at a real file", f"{missing[:3]}")
    rep.check(not bad_hash, "every manifest SHA-256 matches the file", f"{bad_hash[:3]}")
    listed = {r["path"] for r in manifest}
    on_disk = {f"inputs/{p.relative_to(inputs).as_posix()}" for p in inputs.rglob("*")
               if p.is_file() and p.name != "manifest.csv"}
    rep.check(on_disk <= listed, "no input file is missing from the manifest",
              f"{sorted(on_disk - listed)[:3]}")
    rep.check("inputs/manifest.csv" not in listed, "manifest excludes itself", "manifest lists itself")

    # ---- banners and secrecy --------------------------------------------
    for name in ("launch.md", "owner-answers.md"):
        text = (inputs / name).read_text(encoding="utf-8")
        rep.check(text.startswith(BANNER), f"{name} starts with the banner", "banner missing")
    rep.equal(len((inputs / "launch.md").read_text(encoding="utf-8").splitlines()), 20,
              "launch.md line count")
    rep.equal(len((inputs / "owner-answers.md").read_text(encoding="utf-8").splitlines()), 47,
              "owner-answers.md line count")

    traffic_text = (inputs / "traffic" / "offline-api-responses.json").read_text(encoding="utf-8")
    rep.equal(len(traffic_text.splitlines()), 74, "traffic capture line count")
    traffic = json.loads(traffic_text)
    rep.equal(traffic["usable_series_count"], 0, "traffic capture holds no usable data")

    # The two owner-held facts must not be discoverable in any agent-visible input.
    leak_terms = ("restaurant week", "citywide", "festival", "event week", "training",
                  "new hire", "new starter", "onboarding", "learning the")
    leaks = []
    for path in inputs.rglob("*"):
        if not path.is_file() or path.name == "manifest.csv":
            continue
        low = path.read_text(encoding="utf-8", errors="replace").lower()
        for term in leak_terms:
            if term in low:
                leaks.append(f"{path.name}: {term}")
    rep.check(not leaks, "no agent-visible input leaks the event or the training cause",
              f"{leaks[:5]}")

    # ---- oracle ----------------------------------------------------------
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    rep.equal(oracle["false_trend"]["hidden_cause"], "a citywide restaurant week", "oracle hidden cause")
    rep.equal(oracle["false_trend"]["baseline_period"]["net_sales"], "151200.00", "oracle baseline total")
    rep.equal(oracle["false_trend"]["exceptional_period"]["net_sales"], "105840.00", "oracle spike total")
    rep.equal(oracle["false_trend"]["apparent_lift_pct"], 40, "oracle lift")
    rep.equal(oracle["false_trend"]["naive_v1_error"]["extrapolated_impact"], "393120.00",
              "oracle V1 extrapolation")
    rep.equal(oracle["false_accusation"]["total_events"], 64, "oracle event count")
    rep.equal(oracle["false_accusation"]["pre_send_corrections"], 56, "oracle pre-send count")
    rep.equal(oracle["false_accusation"]["post_send_voids"], 8, "oracle post-send count")
    rep.equal(oracle["false_accusation"]["naive_gross_amount"], "1184.00", "oracle naive amount")
    rep.equal(oracle["false_accusation"]["true_post_send_amount"], "176.00", "oracle true amount")
    rep.equal(oracle["false_accusation"]["other_refs_post_send_events"], 46, "oracle other events")
    rep.equal(oracle["false_accusation"]["other_refs_mean_events"], 11.5, "oracle other mean")
    rep.check(oracle_path.resolve().parent == (CASE_STUDY / "oracle").resolve()
              or "oracle" in oracle_path.parts,
              "oracle lives in its own directory", str(oracle_path))
    rep.check(not (inputs / "ground-truth.json").exists(), "oracle is not inside inputs/",
              "ground-truth.json found under inputs/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Re-check the fixture invariants independently.")
    parser.add_argument("--inputs", type=Path, default=CASE_STUDY / "inputs")
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--oracle", type=Path, default=CASE_STUDY / "oracle" / "ground-truth.json")
    parser.add_argument("--checksums", type=Path, default=None,
                        help="Optional checksums file to cross-check against the manifest.")
    args = parser.parse_args()

    manifest = args.manifest or (args.inputs / "manifest.csv")
    rep = Report()
    verify(args.inputs, args.oracle, manifest, rep)

    if args.checksums and args.checksums.is_file():
        listed = {line.split()[1].lstrip("*") for line in
                  args.checksums.read_text(encoding="utf-8").splitlines() if line.strip()}
        rep.check(bool(listed), "checksums file is non-empty", "empty checksums file")

    for label in rep.passes:
        print(f"PASS  {label}")
    for failure in rep.failures:
        print(f"FAIL  {failure}", file=sys.stderr)
    print(f"\n{len(rep.passes)} passed, {len(rep.failures)} failed")
    return 1 if rep.failures else 0


if __name__ == "__main__":
    sys.exit(main())
