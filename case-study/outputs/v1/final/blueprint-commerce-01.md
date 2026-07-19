FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

> REVIEW STATUS: unreviewed agent draft. See `case-study/CORRECTIONS.md` for the
> substantive errors found in review. Do not quote a figure from this draft alone.

# Next Year Blueprint - Commerce_01
## Prepared by Performance Audit | 2026-07-17 | Version 1

### Executive Summary

- **Biggest finding:** Labor is not on target. The dashboard reads 30.41% of net (bare wages), but with the 18% payroll burden from config applied, labor is **35.88% of net, 5.88 points over the 30% target, a gap of $117,325.62 for the year**. Every single day of 2025 breaches the target on a burdened basis (365/365 days, range 34.02% to 37.75%). This is the largest number in the audit, and it is invisible on the current, un-burdened reporting. Source: labor export (730 rows) + POS net + config.
- **Biggest opportunity:** From **2025-05-05 to 2025-05-18**, a clean 14-day window delivered **+$30,754.11 of net on +1,533 covers**, at an unchanged $20.02 average check, unchanged 4.97% discount rate, and unchanged 35.84% labor ratio, then stopped dead. It was pure incremental traffic at close to full contribution margin, and it proves the venue can absorb about 38% more volume without the labor ratio degrading. **What caused it is not answerable from the data provided.** This is the single highest-value question in the audit.
- **Biggest risk:** One of the quarterly report files, `Q2 CORRECTED.csv`, is wrong. It inflates Q2 net by **$10,679.57 (+2.00%)** and would push FY net to $2,006,370.62. It is both the newest file and the one named "CORRECTED", so the two instincts an analyst reaches for (newest wins, "corrected" wins) both select the wrong file. Beyond that: three of the four data streams an audit normally leans on carry an owner-declared reliability caveat, and the fourth (foot traffic) does not exist at all.

**Data tier:** 4 (full) on financials from Agent 1. **0 (none)** on owner operational context from Agent 2 (0 of 15 standard questions answered) and **0 (none)** on foot traffic from Agent 3 (no data, subscription not active).

**Sources used:** Agent 1 (Data Analysis) completed with a deep, clean, tier-4 financial dataset. Agent 2 (Owner Context) returned only reporting-preference constraints; no operational context. Agent 3 (Traffic) returned no usable data.

**Confidence ceiling for this audit is 4, not 5.** A score of 5 requires POS, labor, and foot traffic data to align. Foot traffic is entirely absent and owner context is minimal, so no recommendation here can reach 5. The ceiling of 4 is reached only where two independent data sources agree.

> This is version 1. There is no prior version, so there is no "Changes from Previous Version" section.

---

### 1. Recommended Operating Days

The launch brief (via Agent 3) states all locations trade seven days a week, 11:00 to 23:00. The owner answered nothing about days, hours, or the case for closing any day (0 of 15 questions). No foot traffic data exists. So the day recommendation rests on POS revenue and labor alone.

| Day | Recommendation | Revenue (avg/day) | Burdened labor % | Traffic Data | Owner Input | Confidence |
|-----|----------------|-------------------|------------------|--------------|-------------|------------|
| Monday | Keep open | $4,503 | 35.37% | N/A | N/A | 2 |
| Tuesday | Keep open | $4,730 | 35.33% | N/A | N/A | 2 |
| Wednesday | Keep open | $5,178 | 35.30% | N/A | N/A | 2 |
| Thursday | Keep open | $5,696 | 35.39% | N/A | N/A | 2 |
| Friday | Keep open | $6,919 | 36.51% | N/A | N/A | 3 |
| Saturday | Keep open | $7,236 | 36.39% | N/A | N/A | 3 |
| Sunday | Keep open (see below) | $4,017 | 36.54% | N/A | N/A | 2 |

**No day is recommended for closure, and here is the reasoning (Rule 8).** Sunday is the weakest day at $4,017/day, 55.5% of Saturday's volume, and the highest burdened labor ratio at 36.54%. That makes it the obvious close-a-day candidate. It does not survive the test.

- To recommend closing a day, its contribution must be negative, or the freed resources must be redeployed for a demonstrated gain. Contribution = revenue lost - variable costs avoided - avoidable labor saved.
- **Revenue lost** if Sunday closed: $208,901/year (52 Sundays).
- **Variable costs avoided:** unknown. No COGS, food purchase, or invoice data was provided, so the food/variable side cannot be calculated at all.
- **Avoidable labor saved:** at most partial. Agent 1 tested the only available labor lever (bringing Sunday's ratio to Thursday's) and it is worth **$2,401.72/year, which is 2% of the labor gap.** Hours already track sales tightly on every day, so there is little loose labor to remove.
- With $208,901 of revenue on one side, an unknown (but non-zero) variable cost on the other, and only about $2,401.72 of avoidable labor in play, there is **no evidence Sunday's contribution is negative.** Closing it is not supported by the data.

To raise confidence on any day-level decision, provide: COGS/food cost so contribution per day can be computed, and owner input on whether Sunday, Monday, or Tuesday carry fixed costs that a closure would actually remove.

---

### 2. Recommended Hours

- **Door open / close:** 11:00 to 23:00, seven days a week. This is the only hours information available, and it comes from the launch brief (Agent 3), not the owner and not the POS. Confidence: 2.
- **Last seating, kitchen close, staff start, bar close:** **This requires data which was not available for this audit.** There is no hourly sales data, no daypart data, no owner input on service structure, and no reservation log. Revenue by hour was skipped entirely by Agent 1 because no hourly granularity exists (void timestamps exist but are not sales timestamps and cannot substitute).
- **No change to hours is recommended, because no data supports one.** Daypart analysis, peak-hour alignment, and "missed demand window" analysis all require an hourly traffic or sales series. None exists.

To raise confidence: provide an hourly sales export from both POS systems (unlocks daypart analysis, the last major revenue cut still closed), and a traffic subscription (see Market section).

---

### 3. Staffing Template

**What the data supports.** Labor exists as a daily aggregate split into BOH and FOH only. It carries hours, overtime, and wage cost by day. It supports the day-of-week view below (all figures FY2025, burdened at the 18% config rate):

| Day | Avg hours/day | Avg net/day | Burdened labor % | Annual wage (base) | SPLH |
|-----|---------------|-------------|------------------|--------------------|------|
| Monday | 68.0 | $4,503 | 35.37% | $70,180 | $66.23 |
| Tuesday | 71.3 | $4,730 | 35.33% | $73,650 | $66.31 |
| Wednesday | 78.0 | $5,178 | 35.30% | $82,106 | $66.35 |
| Thursday | 86.1 | $5,696 | 35.39% | $88,828 | $66.19 |
| Friday | 104.7 | $6,919 | 36.51% | $111,326 | $66.07 |
| Saturday | 109.1 | $7,236 | 36.39% | $116,032 | $66.29 |
| Sunday | 60.8 | $4,017 | 36.54% | $64,685 | $66.02 |

Loaded cost basis (shown once, used throughout): base wage $606,807.57 loaded at the config `payroll_burden_pct` of 18% gives **$716,032.93 burdened**. The 18% multiplier applies to gross wages, per config. (The venue's location and province were not established in any input, so no jurisdiction-specific burden was assumed; the config value governs.)

**What the labor model checklist requires but the data cannot provide.** The procedure's Schedule section calls for setup/cleanup time in every shift, an afternoon bridge plan, owner-operator patterns with the dollar value of each owner day, and named shift structure. **None of this can be built for Commerce_01.** The labor export is a daily aggregate with no headcount, no shift, and no employee columns, and the owner answered 0 of 15 questions, including every question on staff count, full-time/part-time split, who opens and closes, owner involvement and hours, wage rates by role, setup/cleanup, and the afternoon gap. Any shift-by-shift or owner-operator staffing plan built on this file would be built on nothing, and the procedure forbids filling that gap with generic content.

**One structural read the data does support.** Sales per labour hour (SPLH) sits in a $63.91 to $68.85 band across all 365 days, and never broke out of it even during the +38% May window. Hours are already pegged tightly to sales. There is no loose day to trim. This is why the labor gap (finding 1) is structural (rate, burden, fixed floor, or the frozen $20 check), not a scheduling error. Zero days show SPLH over $80, so no day is understaffed to the point of burning out the team.

To raise confidence: provide an employee-level labor export with shifts and headcount (unlocks shift-level staffing, verifies `min_foh_per_day`, and tests whether the gap is rate or hours) and owner answers on staffing and owner involvement.

**A config rule that cannot be checked.** `min_foh_per_day = 2` cannot be verified. The unit is ambiguous (hours or headcount). If it means FOH hours, it is never breached (minimum FOH hours on any day is 30.89). If it means headcount, the daily-aggregate export has no headcount column and the answer is unavailable.

---

### 4. Top 5 Actions (ranked by dollar impact)

Every dollar figure below is a specific, sourced number. Read the labels carefully: a "gap to target" is not recovered cash, and an "exposure" is not a proven loss.

#### Action 1: Restate the labor KPI on a burdened basis, then investigate the structural gap
- **What to do:** Stop reporting labor at 30.41%. Report it at 35.88% (base wage x 1.18 per config). Then investigate which of three levers can move it: rate, hours, or price.
- **Why:** The wage-only figure (30.41%) lands close enough to the 30% target to pass a glance and survive a management meeting. The burdened figure is 35.88%, and 365/365 days breach the target once burden is applied (34.02% to 37.75%). Source: labor export + POS net + config.
- **Impact:** **$117,325.62 gap to target.** This is a gap, not identified waste. Closing it requires rate, hours, or price to move, and the data cannot say which is available. The scheduling lever is nearly exhausted: the best day-mix fix (Sunday to Thursday's ratio) is worth only $2,401.72, about 2% of the gap.
- **Confidence: 4.** The arithmetic and the 365/365 breach are certain (labor + POS + config agree). Recoverability is low-confidence: no P&L, no wage-rate detail, no headcount.
- **How to implement:** (1) Change the labor line on every internal report to the burdened figure. (2) Re-run last year's key scheduling decisions against 35.88% to see which would have changed. (3) Pull wage rates by role to test whether the $20.13 blended rate is the lever. (4) Note that the average check has been frozen at $20.00 all year while labor sits 5.88 points over target, so the pricing side deserves at least equal attention to the cost side.
- **To raise confidence:** provide a FY2025 P&L (to know whether 35.88% burdened labor is survivable) and an employee-level labor export with wage rates.

#### Action 2: Install approval controls on voids and on the DSC_02 discount
- **What to do:** Require a manager code before a void can be completed, and remove the "no approval required" setting on the `DSC_02 Set Menu Adjustment` discount.
- **Why:** In 2025, **$50,609.70 of value left the business through channels with no approval trail** (2.5% of net). That is $39,925.43 via `DSC_02`, which requires no approval by design (4,438 uses, 1.9% of gross), plus $10,684.27 of voids with no approval reference (574 events, 37.9% of all voids). Source: discount detail + void detail files.
- **Impact:** **$50,609.70 of exposure.** This sizes a control gap; it is not a loss estimate, and there is no evidence any of it is improper. Within it, the most actionable subset is **$5,109.04 of food that was sent to the kitchen, cooked, and then voided with no manager sign-off** (273 events).
- **Confidence: 4.** The amounts and the absence of an approval requirement are certain. There is zero evidence that any of it is theft or abuse.
- **How to implement:** (1) Turn on the manager-code requirement for voids in the POS. (2) Reclassify `DSC_02` to require approval, or cap it. (3) Review the sent-to-kitchen-and-unapproved events as a process, not as people. (4) Report unapproved-void count weekly.
- **A hard constraint honored here:** the owner asked that no individual staff member be named. The data supports that constraint on its own merits. **No employee is an outlier:** void value spans just 0.95x to 1.06x of the team average across the staff, a total spread of 1.12x against a 2x flag threshold. That uniformity is itself the diagnostic. Theft clusters in a person; a rate identical across everyone is a **process** signature. The fix is a system control, not a conversation with an individual. Void reasons are also evenly spread with no dominant cause.

#### Action 3: Find out what drove 2025-05-05 to 2025-05-18
- **What to do:** Identify the external driver of the 14-day May window, then decide whether it is repeatable.
- **Why:** The window produced **+$30,754.11 of net on +1,533 covers** with sharp on/off boundaries (May 4 was $66 below baseline, May 5 jumped $1,801 above it, May 19 returned to normal). It was not a discount push (4.97% vs 5.00%), not a price move ($20.02 vs $20.00), not a mix shift ($20.06 net per excess cover), and not seasonality (it switches on and off on named days). Four of the year's only days beyond 2.5 standard deviations sit inside it. Source: POS daily exports vs a day-of-week median baseline.
- **Impact:** **$30,754.11 proven** for 14 days at close to full contribution margin. **This is not extrapolated.** If the driver turned out to be identifiable and repeatable, the upside is large, but with one occurrence and an unknown cause, no annualized figure is claimed.
- **Confidence: 2** on the recommendation to repeat it (the event is high-confidence, but the lever is unproven because the cause is unknown). Directional only; validate before committing resources.
- **How to implement:** (1) Ask the owner what happened in the first half of May 2025 (event, promotion, media mention, local calendar). (2) Check any marketing or reservation records for that window. (3) If a driver is found, test it again in a controlled way and measure against the day-of-week baseline.
- **To raise confidence:** provide the promotions calendar, event log, marketing spend, or local-calendar context for May 2025. This is the highest ratio of value to effort in the entire audit.

#### Action 4: Discard `Q2 CORRECTED.csv`; adopt `Q2 (2).csv` as the Q2 record
- **What to do:** Use `Q2 (2).csv` ($533,978.45) as the authoritative Q2 file. Delete or quarantine `Q2 CORRECTED.csv`.
- **Why:** Five files claim to report Q2 2025 with identical gross, discounts, and voids, but four different net totals. `Q2 (2).csv` uses `net = gross - discounts`, the convention that holds on 365/365 days across every other file, and it matches both the daily POS exports and the independently generated annual report to the cent on 91/91 days. `Q2 CORRECTED.csv` applies a flat 2% uplift to the correct number. Source: five Q2 report variants vs daily POS + annual report.
- **Impact:** **$10,679.57 of phantom revenue** avoided. Adopting the wrong file inflates FY net to $2,006,370.62 and shifts every ratio downstream (labor %, discount %, void %).
- **Confidence: 4.** Two independent, non-quarterly sources agree exactly on 91/91 days. This is the most certain conclusion in the dataset.
- **How to implement:** (1) Mark `Q2 (2).csv` as the record of truth for Q2. (2) Remove the other four Q2 variants from any reporting pipeline. (3) Do not trust filename signals ("CORRECTED") or timestamp signals ("newest") for this file; both point at the wrong one.

#### Action 5: Restate the void rate and start tracking pre-kitchen voids
- **What to do:** Report the void rate as **1.37%, not 1.00%**, and track voids that never reached the kitchen.
- **Why:** The daily-summary `voids` figure counts only voids where the item reached the kitchen (confirmed 365/365 days). The full void detail is **$28,803.41 (1.37% of gross)** across 1,514 events; the summary shows only **$21,024.89 (1.00%)**. That leaves **$7,778.52 of void activity invisible in every daily, quarterly, and annual report** (a 37% understatement of true void activity). Source: void detail files vs daily summaries.
- **Impact:** **$7,778.52 of unreported void value.** Both directions matter and point opposite ways: for food cost, the summary figure ($21,024.89 of food actually produced then binned) is arguably the right waste number; for integrity and training, the summary is wrong by 37%, because a void rung before the kitchen fires is still a keying error, a mispriced item, or a guest told the wrong thing.
- **Confidence: 4** on the definition (365/365 exact match). The recoverable share is unknown: without COGS, void dollars (menu value) cannot be converted to food cost dollars.
- **How to implement:** (1) Change the void KPI to count all void events, not only kitchen-sent ones. (2) Report the two numbers separately (all voids for integrity, kitchen-sent voids for food waste). (3) Pair with Action 2's manager-code control.

> **Note on ranking.** Actions 2 and 5 overlap: the $10,684.27 of unapproved voids inside Action 2's $50,609.70 exposure is the same void population Action 5 restates. They are listed separately because one is a control fix and the other is a reporting fix, but the dollars are not additive across the two.

---

### 5. Monthly Calendar View

FY2025 only. No prior year exists, so **no year-over-year comparison is possible.** The POS system changed mid-year, so any full-year trend crosses a system boundary (see Data Quality).

| Month | Net sales | MoM % | Covers | Note |
|-------|-----------|-------|--------|------|
| Jan | $157,005 | -- | 7,852 | |
| Feb | $144,262 | -8.1% | 7,215 | Lowest absolute total (shortest month) |
| Mar | $163,527 | +13.4% | 8,174 | |
| Apr | $160,100 | -2.1% | 8,005 | |
| **May** | **$204,089** | **+27.5%** | 10,199 | Best month, driven by the unexplained May 5-18 window |
| Jun | $169,790 | -16.8% | 8,487 | |
| Jul | $177,484 | +4.5% | 8,874 | POS system changes here |
| Aug | $180,793 | +1.9% | 9,040 | |
| Sep | $160,851 | -11.0% | 8,045 | |
| Oct | $165,673 | +3.0% | 8,284 | |
| Nov | $156,114 | -5.8% | 7,810 | |
| **Dec** | $156,004 | -0.1% | 7,797 | Weakest trading month on a per-day basis ($5,032/day vs Feb's $5,152/day) |

- **Expected strong window:** May, but only because of a 14-day event whose cause is unknown. **Do not plan around May as a repeatable seasonal peak** until the driver is identified. Strip May out and the year is a flat line at roughly $5,200 to $5,500/day.
- **Expected slow period:** December on a per-day basis; February on an absolute basis.
- **Trend:** flat. H1 net $998,771.89 vs H2 net $996,919.16 is -0.19%. This business did not grow and did not decline in 2025. **Read this with the POS caveat:** the two systems disagree by 3.89% and 6.50% on the only two days both covered, so H1 and H2 are measured with different rulers and the -0.19% carries an unquantified systematic error.
- **Marketing pushes, patio season, holiday plan:** **This requires data which was not available for this audit.** No owner seasonality input, no patio information, no lease or neighborhood context, and no marketing history exist. The one evidence-based timing insight is the May window, and it is a question, not a plan.

---

### 6. Cost Control Flags

The only cost line in the data is labor. Food cost % and prime cost % **cannot be calculated** because no COGS, food purchase, invoice, or P&L data was provided. That absence is itself the largest cost blind spot: prime cost is the number most operators manage against, and half of it is missing.

| # | Flag | What the data shows | Cost of inaction | Recommended fix | Confidence |
|---|------|---------------------|------------------|-----------------|------------|
| 1 | Burdened labor over target | 35.88% of net vs 30% target, all 365 days breach | $117,325.62/year gap to target (not identified waste) | Restate KPI, then investigate rate/hours/price (Action 1) | 4 |
| 2 | Approval control gap | $50,609.70 through no-approval channels (2.5% of net); $5,109.04 cooked then voided unapproved | Exposure, not a proven loss; true P&L cost of the cooked-and-binned food unknown without COGS | Manager code on voids, approval on DSC_02 (Action 2) | 4 |
| 3 | Void reporting understated | True void rate 1.37% vs reported 1.00%; $21,024.89 of food produced then binned | $7,778.52 of void activity invisible to every report | Restate void rate, track all voids (Action 5) | 4 |

Overtime is not a material lever: 2.84% of hours, stable all year (2.57% to 3.19%). No month shows a labor cost spike above 0.2 percentage points, so the 3-point month-over-month spike flag never fires.

---

### 7. Foot Traffic Opportunities (Market)

**No foot traffic data is available for Commerce_01. This section cannot be performed.**

Agent 3 recorded four captured API responses, all failures: the traffic feed for Commerce_01 (and its two sibling locations) returned HTTP 403 `subscription_required`, and the reservation endpoint returned HTTP 404 `not_configured`. No traffic subscription is active for the venue, and no live calls were possible. This is a complete absence of data, not a weak signal. It is explained, not mysterious: the owner confirmed "we never contracted a traffic feed" and reservations are taken by phone and not logged in an exportable system.

Because of this, none of the following can be produced: peak hours, quiet hours, missed demand windows, empty open hours, recommended staffing windows, or competitor comparison. There is also no venue name, address, or city in any permitted input, so no competitor lookup could be formed even in principle.

**To make this analysis possible, two owner decisions are needed:** (1) an active traffic subscription for the location, which resolves the 403, and (2) an explicit, verified venue name and city, which is a prerequisite for any query. Both are owner decisions, not gaps this audit can close.

---

### 8. Data Quality Notes (mandatory)

**Data provided:**
- POS_A `{daily, products, voids, discounts}`: 183 files each, 2025-01-01 to 2025-07-02.
- POS_B `{daily, products, voids, discounts}`: 184 files each, 2025-07-01 to 2025-12-31.
- Labor: `Scheduling_Tool_labor_2025.01-12.csv`, 730 Commerce_01 rows (365 days x BOH/FOH), daily aggregate.
- Reports: Q1, Q2 (five variants), Q3, Q4 for Commerce_01, plus the group annual sales report.
- Config: burden 18%, target labor 30%, min FOH/day 2, currency CAD, pos_time_offset null, dataset classification synthetic.
- All files parsed cleanly. No file was unreadable, corrupted, or unparseable.

**Data missing (blocks specific analysis):**
- **COGS / food purchases / invoices / P&L:** blocks food cost %, prime cost %, and any margin or profitability conclusion. Biggest gap. This audit can say labor is 35.88% of net; it cannot say whether the business makes money.
- **Owner operational context:** 0 of 15 standard questions answered. No hours, days, deliveries, prep, cleaning, staff counts, split-shift policy, owner involvement, wage rates, neighborhood, lease, seasonality, best/worst-day belief, past experiments, delivery mix, or planned changes.
- **Employee-level labor:** daily aggregate only, no headcount, shift, or employee ID. Blocks shift-level staffing, individual productivity, and verification of `min_foh_per_day`.
- **Hourly sales:** none. Blocks all daypart analysis. Void timestamps exist but are not sales timestamps.
- **Foot traffic and reservations:** none exist in exportable form (subscription not active; reservations not logged).
- **Marketing / events / promotions / local calendar:** blocks the May 5-18 question, the highest-value unanswered question in the audit.
- **Bank statements / accounting exports:** no third-party confirmation of deposits. Everything reconciles, but everything traces to one POS lineage; if the POS is misconfigured, every number inherits the error.
- **Tips for H2:** POS_A carries a tips column, POS_B does not, so a half-year series was not analysed.

**Sections skipped (and why):**
- Food cost % / prime cost %: no COGS. Not estimated.
- Revenue by hour: no hourly granularity. Not estimated.
- Year-over-year comparison: single calendar year (2025 only).
- Foot traffic, gap analysis, competitor comparison: no traffic data.
- Full owner-driven scheduling, owner-operator model, setup/cleanup, afternoon bridge: no owner answers and no headcount.

**Assumptions made (each with justification):**
1. `Q2 (2).csv` is authoritative for Q2. Justification: matches daily POS exports and the independently generated annual report on 91/91 days to the cent, and uses the `net = gross - discounts` convention that holds on 365/365 days everywhere else. Evidence-backed, not a preference.
2. POS_B is used for 2025-07-01 and 2025-07-02; the POS_A rows for those two dates are dropped. Justification: matches the annual and Q3 reports and yields exactly 365 unique days with no double count. **The two systems disagree by 3.89% and 6.50% on these days, and that is not reconciled.**
3. POS-reported net (`gross - discounts`) is used, not the procedure's `gross - voids - discounts - taxes`. Justification: the POS convention holds on 365/365 days, is what the annual report and product files use, and applying the procedure formula literally would double-deduct and understate net by roughly 11%. Flagged, not silently applied.
4. 18% payroll burden applied to base wage per config. Both burdened and un-burdened figures are shown so the reader sees the difference the assumption makes.
5. May baseline is the day-of-week median of the other eleven months. Justification: median resists the outliers it is meant to detect; day-of-week matching controls for the large Saturday-to-Sunday spread.

**Limitations (what this Blueprint cannot conclude):**
- The POS transition is not reconciled. H1 and H2 are measured with different instruments. Do not build a growth or decline narrative on the -0.19% H2-vs-H1 figure.
- No external verification. Everything reconciles, but everything traces to one POS lineage.
- The labor gap is a gap to a config target, not a recoverable saving. Whether and how it is recoverable needs rate and P&L data.
- Void dollars are menu value, not food cost. Without COGS, the true P&L impact of voids is materially smaller than the menu figure and is not guessed here.
- `min_foh_per_day = 2` is unverifiable (unit ambiguous, no headcount column).
- The May driver is unknown and is the most valuable thing in the dataset.
- Per-cover metrics carry the owner's own caveat: the owner said the cover counts are "approximately right, I would not bet the business on them." Net dollars reconcile four ways and are solid; anything derived per cover (average check, covers per hour) inherits that caveat, even though the check reads a near-perfect $20.00 all year.
- The owner's belief that "Commerce_01 carries the group" and that "the other two are steady" **cannot be verified here.** Agent 1 analysed Commerce_01 only and filtered out the sibling locations, so the audit holds no revenue-by-location comparison to confirm or challenge the premise on which the audit scope was set.
- This data is unusually regular (check within $0.02, labor within 0.2pp, SPLH in a $5 band, tax exactly 10.0%, discounts exactly 5.00%, all year). This is consistent with the declared synthetic classification. On messier real-world data the same findings would need wider tolerances.

**To improve this Blueprint, provide (in priority order):**
1. Supplier invoices or monthly COGS. Unlocks food cost %, prime cost %, and converts the $21,024.89 of kitchen-sent voids into a real P&L number. Single biggest unlock.
2. Whatever drove May 5-18 (promo calendar, event log, marketing spend, local calendar). Highest value-to-effort ratio.
3. A FY2025 P&L. The only way to answer whether 35.88% burdened labor is survivable.
4. Answers to the 15 owner questions, especially staffing, owner involvement, and wage rates.
5. An employee-level labor export with shifts and headcount.
6. Migration notes or a parallel run explaining the July 1-2 POS discrepancy.
7. An hourly sales export from both systems.
8. Bank statements or accounting exports (first genuinely independent check on the POS lineage).

---

### 9. What to Track Going Forward

Five metrics to monitor weekly to validate and defend these recommendations:

1. **Burdened labor % (base wage x 1.18), never the wage-only figure.** Target 30%. The whole point of finding 1 is that the un-burdened number hides the miss.
2. **Void rate on all void events, not just kitchen-sent.** Report both: all voids (integrity) and kitchen-sent voids (food waste). Watch for the 1.37% true rate, not the 1.00% summary.
3. **Count and value of unapproved voids and unapproved discounts each week.** This is the leading indicator that Action 2's control is working. Baseline: 574 unapproved void events and $39,925.43 of no-approval-required discounts across 2025.
4. **Daily covers versus the day-of-week baseline.** This is how you catch the next May-type window while it is happening instead of a year later.
5. **Average check.** It has not moved off $20.00 in twelve months. Any deliberate price test should show up here first; if it does not move the blended check, revenue stays a pure function of cover count.

---

### Questions for the Owner (mandatory)

The owner answered 0 of 15 standard questions and invited follow-up ("Ask me if something in the numbers does not make sense to you"). These are tied to the specific gaps found in the data.

**Operations**
1. What days and hours is Commerce_01 actually open, and has that changed during 2025?
2. What is the exact date of the POS cutover, and which system was in place before and after? (The July 1-2 seam shows a 3.89% and 6.50% discrepancy that is currently unreconciled.)
3. When do deliveries arrive, how many prep hours does the kitchen need, and is there a deep-clean day?
4. What happens during the afternoon gap between lunch and dinner?
5. Is the venue licensed for alcohol, and is it full service? (The entire beverage category is a single soft-drink SKU at 6.3% of net, with 32.9% attach; whether that is low depends on venue type, which the data cannot establish.)

**Staffing**
6. What is the full-time versus part-time split, and can staff work split shifts?
7. Are the owners a couple, partners, or solo, and how many hours per week does each work in the restaurant, in what role?
8. What are the actual hourly wage rates for FOH, cooks, and manager? (Needed to test whether the $20.13 blended rate is the lever on the labor gap.)
9. Does `min_foh_per_day = 2` mean two people or two hours?

**Revenue**
10. What happened at the restaurant between May 5 and May 18, 2025? (Event, promotion, media mention, anything on the local calendar.) This is the single most valuable question in the audit.
11. Has the menu price changed at all in 2025? The average check has not moved off $20.00 for twelve months.
12. What do you believe is your best and worst day of the week, and why?
13. Do you use delivery platforms, and roughly what share of revenue?

**Strategic**
14. Does Commerce_01 actually carry the group's revenue, and are the other two locations genuinely flat? (The audit scope rests on this belief but could not verify it, because only Commerce_01 was analysed.)
15. Is there a seasonal pattern, a patio, or any lease restriction on hours, noise, or signage?
16. What did you try last year that worked, and what flopped? (No experiment history is on file, so there is no protection against recommending something already tried.)
17. Any planned changes for the coming year (menu, renovation, concept, private events, catering)?
18. Can you share supplier invoices or monthly COGS, and a FY2025 P&L? (Unlocks food cost, prime cost, and the profitability question.)
