# Field Notes: The Failure Modes Behind the Rules

Every agent prompt in this repo carries a numbered ABSOLUTE RULES section, and
CI fails the build if one loses it. These notes explain the failure modes each
rule is designed to prevent.

The failure modes are the standard ways restaurant data goes wrong: mislabeled
exports, timezone-shifted hourly data, stale cached menus, unmapped POS
products. A wrong recommendation in this domain is not hypothetical damage:
operators change schedules, staffing, and menus based on these reports.

Each note below states the failure mode, the design call made in response, and
where that call is enforced.

---

## 1. A filename is not a date

**Failure mode:** POS exports are named by year, and the name can lie. A file
labeled one year can contain another year's transactions. The tell is usually
a gap year in the sequence plus an anomalous result in an adjacent year: a
sudden "crash" that is really an older year sitting under the wrong label.

**The call:** filenames are never accepted as date evidence. Every file must
yield an internal date reference (date columns, period headers, transaction
timestamps) or be flagged UNVERIFIED. When the year-over-year trajectory only
makes sense reordered, the report presents both interpretations and refuses to
build recommendations on the unverified label. The deliverable ships with an
open question instead of a clean but wrong narrative.

**Encoded in:** `performance-audit/agents/data-analyst.md`, rules 10 and 11.

## 2. One year, two POS systems

**Failure mode:** a venue migrates POS mid-year (one system through November,
a new one from December). Treated as one source, the "annual" total silently
double-counts the overlap or hides the gap at the seam.

**The call:** each system is a separate source. Totals are combined with
explicit sourcing, and the seam is inspected for overlap or missing days
before anything downstream uses the year.

**Encoded in:** `performance-audit/agents/data-analyst.md`, rule 12.

## 3. Hourly data lies about timezones

**Failure mode:** POS systems often store hourly data in UTC. Mapped naively
to local time, the whole revenue curve shifts by hours and the analysis
"discovers" a dead dinner service or a phantom morning rush that never
existed.

**The call:** if the timezone is not confirmed, the hourly table is omitted
entirely and the limitation is noted. A missing table is recoverable; a
confident wrong one drives a bad operating-hours decision.

**Encoded in:** `performance-audit/agents/blueprint-builder.md`, rule 15.

## 4. A revenue jump is not a second location

**Failure mode:** the data shows a step change in revenue and the tempting
story is expansion. Post-COVID reopening, a delivery-platform launch, a
renovation, or a menu overhaul produce the same curve at a single location.

**The call:** structural explanations are verified with the owner before they
enter the report. The data shows the jump; only the owner knows why.

**Encoded in:** `performance-audit/agents/blueprint-builder.md`, rule 16.

## 5. Owners are not interchangeable shift-fillers

**Failure mode:** labor models that treat the owner as a free or generic
employee produce schedules no owner will actually run. The real questions are
lifestyle questions: couple or solo, staggered days off, who closes, what a
replacement costs when the owner is absent.

**The call:** every schedule models the owners' actual pattern first and
prices each owner day (the cost difference between owner-in and owner-off).
Labor is costed loaded: gross base wage times roughly 1.20 for Quebec employer
burden (QPP, EI, CNESST, vacation, FSS, RQAP), shown once, then used
throughout. The multiplier applies to gross wages; applying it to net
take-home pay mixes two accounting bases and understates true cost. Setup and
cleanup time sit inside every shift calculation, because door hours are not
labor hours.

**Encoded in:** `performance-audit/agents/blueprint-builder.md`, rule 12.

## 6. Stale delivery menus poison food-cost math

**Failure mode:** delivery platforms cache aggressively. A venue that left a
platform years ago still shows a menu there, at prices from another era.
Food-cost percentages computed on those prices look precise and are garbage.

**The call:** prices unconfirmed from a live source within 90 days are marked
unverified, and unverified prices do not degrade the food-cost analysis, they
kill it. The section is skipped and the gap is stated. A missing analysis is
recoverable; a fake one destroys trust.

**Encoded in:** `demo-builder/agents/data-scout.md`, rule 7;
`demo-builder/agents/menu-cost-analyst.md`, rule 6.

## 7. Reconcile before you compute, compute before you accuse

**Failure mode:** variance analysis is where trust dies. A +50% variance on a
protein reads like theft. Often it is a data problem instead: a POS product
that never got mapped to a recipe, or a sales mix that does not reconcile to
the POS total.

**The call:** reconcile first, categorize second. The blocking gate: the sales
mix must reconcile to the POS revenue total within a $5 rounding tolerance, or
variance is not computed at all. Then a required output rule (not a second
gate): every variance flag states whether it is a data-quality issue or an
operational pattern, and flags describe data, never people. "Possible causes
include over-ordering, waste pattern, or theft; recommend manager review of
receiving logs for the period" is as far as a flag goes: theft may appear as a
possible cause category, but naming or implying a specific person never does.
An accusation is not a valid output of this system.

**Encoded in:** `food-cost-sentinel/agents/sales-mix-analyst.md`, rules 4
and 5; `food-cost-sentinel/agents/variance-detective.md`, rules 2, 3 and 5.

## 8. The 3-star review is the money review

**Failure mode:** review analysis that stares at 1-star reviews studies people
who were never coming back, and misses the recoverable ones.

**The call:** prioritize the most common complaint in 3-star reviews. The
working hypothesis (a prioritization heuristic, not a measured fact) is that
3-star guests are the most recoverable segment: engaged enough to write, not
angry enough to be gone for good. Sample-size honesty is enforced alongside
it: under 30 reviews, trend findings carry a small-sample disclaimer; under
15, trend findings are skipped entirely.

**Encoded in:** `demo-builder/agents/review-analyst.md`, the Money Patterns
section and rule 5.

## 9. Verify the city before you spend the budget

**Failure mode:** a street name exists in many cities. On a metered API, one
wrong-city query chain wastes both the analysis and the monthly credit
budget.

**The call:** location is narrowed from evidence already in the workspace
before any call is made: the language of the data files, bank references,
address format. Those clues narrow a region; they do not verify a city, so an
explicit city (from the launch prompt or a conclusive address source) is
required before any budget is spent. Spend is also capped in code:
`MAX_API_CALLS` defaults to 9 and is clamped to a hard ceiling of 10 per
audit, matching the prompt's 10-call budget against the free tier, and every
call is logged.

**Encoded in:** `performance-audit/agents/traffic-scout.md`, rules 8 and 10;
enforced in code in `performance-audit/scripts/traffic_scout.py`
(`MAX_API_CALLS` and the per-call log).

## 10. Operational status is not a finding

**Failure mode:** when a venue is closed or mid-reopening, the obvious
headline is the closure. The owner already knows their restaurant is closed.
Leading with it spends the report's one shot at attention on nothing.

**The call:** the headline is what the data reveals (revenue patterns, menu
concentration, platform dependency, seasonality). Operational status lives in
the data-quality notes.

**Encoded in:** `performance-audit/agents/blueprint-builder.md`, rule 11.

## 11. Reports are iterations, not verdicts

**Failure mode:** one-shot reports get corrected verbally and the corrections
evaporate. The next run repeats the same wrong assumption, and the operator
stops trusting the tool.

**The call:** owner corrections persist in `data/owner-feedback.md` and
calibrated parameters in `data/config.json` (payroll burden, minimum staffing,
targets). Every re-run must apply them, open with a "Changes from Previous
Version" section listing every number that moved and why, and pass a
consistency check (summary, schedule, and full analysis must agree) before
the report is final. To be clear about what this repo shows: the loop is a
written procedure in the prompt's ITERATION HANDLING section; no demonstrated
V1-to-V2 run is published here.

**Encoded in:** `performance-audit/agents/blueprint-builder.md`, the
ITERATION HANDLING section.

---

If a rule in the prompts looks oddly specific, this file is usually why.
