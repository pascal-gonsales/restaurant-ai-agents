FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

> REVIEW STATUS: unreviewed agent working paper. The trend, event-magnitude, data-tier,
> and void-loss claims here were corrected in review. See `case-study/CORRECTIONS.md`.

# Data Analysis - Commerce_01 (V2)
## Prepared: 2026-07-17

Scope note: this analysis covers **Commerce_01 only**. Commerce_02 and Commerce_03 appear in the shared labor and reports files; their rows were filtered out and not analysed.

## V2 revision note (what changed from V1, and why)

Two changes, both driven by owner context that is not in any data file, applied under the amended procedure. Everything the owner did not touch is unchanged from V1.

1. **The May 5-18 window is a citywide restaurant week, a recurring annual event, not a new baseline** (owner). Under the amended revenue rule it is pulled out of the ordinary trend, reported on its own line with its exact dollar effect, and **not extrapolated**. The ordinary-trend figures are restated with those dates excluded, and both the with-event and without-event numbers are shown so the change is auditable. V1 had correctly flagged this window as the top open question but could not name the cause; the owner has now named it.

2. **The voids are split into pre-send corrections vs post-send voids** (amended integrity rule). A blank "Sent to Kitchen At" marks a pre-send correction, which is a workflow/training signal, **not lost sales**. Only post-send voids count toward the void rate and the loss figure. This **reverses V1's framing**: V1 called 1.37% "the void rate" and said the summaries were "hiding" 0.37% of void activity. Under the amended rule the void rate is the post-send rate **1.00%** (which is exactly what the daily summaries report, so they were right), and the 0.37% is a separate pre-send correction rate. The owner adds that the first two weeks of August reflect one team member new on the POS; that pre-send volume is framed as a training and workflow signal, named to no one.

---

## Data Inventory

| File | Format | Date Range | Records | Quality | Enables |
|------|--------|-----------|---------|---------|---------|
| `pos/Commerce_01/POS_A/daily/*.csv` (183 files) | CSV | 2025-01-01 to 2025-07-02 | 183 day-rows | Complete | Daily revenue, covers, transactions, tips |
| `pos/Commerce_01/POS_A/products/*.csv` (183 files) | CSV | 2025-01-01 to 2025-07-02 | 8 SKU-rows/day | Complete | Category and item mix |
| `pos/Commerce_01/POS_A/voids/*.csv` (183 files) | CSV | 2025-01-01 to 2025-07-02 | 724 void events (to 06-30) | Complete | Void integrity, employee-level, kitchen-sent flag |
| `pos/Commerce_01/POS_A/discounts/*.csv` (183 files) | CSV | 2025-01-01 to 2025-07-02 | 2 discount-rows/day | Complete | Discount integrity |
| `pos/Commerce_01/POS_B/daily/*.csv` (184 files) | CSV | 2025-07-01 to 2025-12-31 | 184 day-rows | Complete | Daily revenue, covers, transactions (no tips column) |
| `pos/Commerce_01/POS_B/products/*.csv` (184 files) | CSV | 2025-07-01 to 2025-12-31 | 8 SKU-rows/day | Complete | Category and item mix (adds unit_price) |
| `pos/Commerce_01/POS_B/voids/*.csv` (184 files) | CSV | 2025-07-01 to 2025-12-31 | 790 void events | Complete | Void integrity, employee-level, kitchen-sent flag |
| `pos/Commerce_01/POS_B/discounts/*.csv` (184 files) | CSV | 2025-07-01 to 2025-12-31 | 2 discount-rows/day | Complete | Discount integrity |
| `labor/Scheduling_Tool_labor_2025.01-12.csv` (12 files) | CSV | 2025-01-01 to 2025-12-31 | 730 rows for Commerce_01 | Complete but coarse | Hours, OT, wage cost by day and role (BOH/FOH) |
| `reports/Commerce_01_POS_A_..._2025.Q1.csv` | CSV | 2025-01-01 to 2025-03-31 | 90 | Complete | Q1 summary, reconciles clean |
| `reports/Commerce_01_POS_A_..._2025.Q2.csv` | CSV | 2025-04-01 to 2025-06-30 | 91 | **Unreliable** | Superseded, see Q2 section |
| `reports/Commerce_01_POS_A_..._2025.Q2 (1).csv` | CSV | 2025-04-01 to 2025-06-30 | 91 | **Unreliable** | Superseded, see Q2 section |
| `reports/Commerce_01_POS_A_..._2025.Q2 (2).csv` | CSV | 2025-04-01 to 2025-06-30 | 91 | **Authoritative** | The only Q2 variant that reconciles |
| `reports/Commerce_01_POS_A_..._2025.Q2 CORRECTED.csv` | CSV | 2025-04-01 to 2025-06-30 | 91 | **Unreliable despite filename** | See Q2 section |
| `reports/Commerce_01_POS_B_..._2025.Q3.csv` | CSV | 2025-07-01 to 2025-09-30 | 92 | Complete | Q3 summary, reconciles clean |
| `reports/Commerce_01_POS_B_..._2025.Q4.csv` | CSV | 2025-10-01 to 2025-12-31 | 92 | Complete | Q4 summary, reconciles clean |
| `reports/Demo_Group_Annual_Sales_Report_2025.csv` | CSV | 2025-01-01 to 2025-12-31 | 365 rows for Commerce_01 | Complete | Independent cross-check, reconciles 365/365 |
| `config.json` | JSON | n/a | 6 keys | Complete | Payroll burden, labor target, currency |

Internal date verification (Rule 10): every file carries internal date columns (`Business Date`, `business_date`, `work_date`, `report_period_start/end`, `report_year`). No year identification rests on filenames. All internal dates fall within calendar 2025. No gap year exists and no year label is in doubt, so the Rule 11 trajectory check does not apply here. The one filename that **is** misleading is `Q2 CORRECTED.csv`, and it is misleading about content, not date.

## Data Tier: 4 (full)

Daily POS sales + daily labor with wage cost + void and discount detail at event level + product mix. This is the deepest tier the procedure defines.

- Revenue Analysis: **populated** (monthly, day-of-week, category, average check)
- Cost Analysis: **partially populated**. Labor cost is available. **No COGS, no food purchases, no P&L, no invoices.** Food cost % and prime cost % are therefore **SKIPPED**.
- Labor Analysis: **populated** (hours, OT, wage cost, SPLH by day of week)
- Integrity Analysis: **populated** (voids and discounts, both to event level, with the pre-send / post-send split the amended rule requires)

Revenue by hour is **SKIPPED**: no hourly sales data exists. Void events carry timestamps, but void timestamps are not sales timestamps and cannot be used to build an hourly revenue curve.

---

## Source Reconciliation (do this before trusting any number)

Four independent representations of Commerce_01's 2025 sales exist. They agree, once the Q2 question is settled:

| Check | Result |
|-------|--------|
| Annual report vs daily POS exports, all 365 days | **0 mismatches** on gross and net |
| Discount detail files vs daily summary `discounts` | **365/365 days match**, both total $105,066.95 |
| Product files net revenue vs daily summary net | Both total **$1,995,691.05** |
| Void detail files vs daily summary `voids` | **Match under the post-send definition** (see Integrity) |

This is an unusually clean dataset. That makes the two places where it is *not* clean worth taking seriously.

### The Q2 problem: five files, four different answers (unchanged from V1)

Five files claim to report Commerce_01 Q2 2025. All five carry identical `gross_sales`, `discounts` and `voids`. They disagree only on `net_sales`, and each disagrees in a perfectly systematic way. I fitted a formula to each across all 91 days:

| File | revision_id | generated_at | Q2 net total | Formula fit (91/91 days) |
|------|-------------|--------------|--------------|--------------------------|
| `Q2 (1).csv` | rev-3a07 | 2025-07-07 | $562,030.00 | `net = gross` (discounts never applied) |
| `Q2 (2).csv` | rev-b45c | 2025-07-06 | **$533,978.45** | **`net = gross - discounts`** |
| `Q2 CORRECTED.csv` | rev-19de | 2025-07-08 | $544,658.02 | `net = (gross - discounts) x 1.02` |
| `Q2.csv` | rev-8f21 | 2025-07-05 | $539,485.67 | `net = gross - discounts + voids` (voids added back) |

**`Q2 (2).csv` is the authoritative file.** Two independent sources confirm it, neither a quarterly report: the **daily POS_A exports** for the 91 Q2 days sum to net **$533,978.45** and match on **91/91 days to the cent**, and the **group annual report** (generated 2026-01-09, a different process) matches on **91/91 days to the cent**. `net = gross - discounts` is the convention of **every other file** (Q1, Q3, Q4, annual, all 365 daily exports), holding 365/365 days.

**The file named "CORRECTED" is the second-worst file in the set.** It applies a flat 2% uplift to the correct figure and is the newest by `generated_at`, so both instinctive tiebreaks (newest wins, "CORRECTED" wins) point at the wrong file. Using it overstates Q2 net by **$10,679.57 (+2.00%)** and inflates FY2025 net to $2,006,370.62. Adopting `Q2 (2).csv` is not a close call; it is the only variant that agrees with the transaction data.

### The POS transition: a two-day overlap that does not reconcile (unchanged from V1)

Commerce_01 changed POS mid-year. POS_A covers 2025-01-01 to 2025-07-02 (183 days). POS_B covers 2025-07-01 to 2025-12-31 (184 days). **Both systems reported 2025-07-01 and 2025-07-02.** On those two days they do not agree:

| Date | POS_A gross | POS_B gross | POS_A net | POS_B net | POS_A covers | POS_B covers | Gap |
|------|-------------|-------------|-----------|-----------|--------------|--------------|-----|
| 2025-07-01 | $5,561.00 | $5,353.00 | $5,284.97 | $5,077.70 | 264 | 253 | POS_A reads **3.89% higher** |
| 2025-07-02 | $6,176.00 | $5,799.00 | $5,852.90 | $5,493.68 | 292 | 275 | POS_A reads **6.50% higher** |

I follow the group convention and use POS_B from 2025-07-01 onward (what the annual and Q3 reports do), yielding exactly 365 unique days with no double count. The POS_A rows for July 1-2 are excluded. **This is a real limitation, not a footnote:** H1 and H2 are measured with different rulers. Two days is far too small to derive a correction factor, and I have not applied one. The H2 vs H1 comparison below carries an unquantified systematic error, plausibly of the same order as the difference it is trying to measure.

---

## Revenue Analysis

All figures: Commerce_01, FY2025, CAD, from daily POS exports (POS_A 2025-01-01 to 2025-06-30, POS_B 2025-07-01 to 2025-12-31), independently confirmed by `Demo_Group_Annual_Sales_Report_2025.csv` on 365/365 days.

**Net sales definition.** The procedure's reference formula is `Net Sales = Gross Sales - Voids - Discounts - Taxes`. This dataset does **not** follow it. Across all 365 days and both POS systems, the reported net equals `gross - discounts` exactly. Tax sits outside gross (a clean 10.0% of net on the FY total), and voids are reported alongside rather than deducted. I use the POS-reported net, because it is internally consistent on 365/365 days, is what the annual report uses, and is what the product files sum to. Applying the procedure's formula literally would double-deduct voids and tax and understate net by roughly 11%. Flagging this rather than silently reconciling it.

### FY2025 headline (unchanged from V1)

| Metric | Value | Source |
|--------|-------|--------|
| Gross sales | $2,100,758.00 | daily exports, `Gross Sales` / `sales_total` |
| Discounts | $105,066.95 (5.00% of gross) | daily exports, `Discounts` / `discount_total` |
| Voids (post-send, as reported) | $21,024.89 (1.00% of gross) | daily exports, `Voids` / `void_total` |
| **Net sales** | **$1,995,691.05** | daily exports, `Net Sales` / `net_total` |
| Transactions | 58,698 | `Transactions` / `receipt_count` |
| Covers | 99,782 | `Covers` / `guest_count` |
| Average check per cover | $20.00 | $1,995,691.05 / 99,782 |
| Average per transaction | $34.00 | $1,995,691.05 / 58,698 |
| Covers per transaction | 1.70 | 99,782 / 58,698 |
| Average net per day (with event) | $5,467.65 | $1,995,691.05 / 365 |

### Monthly

May's cell is the reported (with-event) figure. It contains a recurring restaurant-week event that is isolated in the next section.

| Month | Days | Net sales | MoM % | Covers | Avg check | Void % (post-send) | Disc % |
|-------|------|-----------|-------|--------|-----------|--------|--------|
| 2025-01 | 31 | $157,005 | -- | 7,852 | $20.00 | 1.12% | 4.97% |
| 2025-02 | 28 | $144,262 | -8.1% | 7,215 | $19.99 | 1.20% | 4.93% |
| 2025-03 | 31 | $163,527 | +13.4% | 8,174 | $20.01 | 1.08% | 4.97% |
| 2025-04 | 30 | $160,100 | -2.1% | 8,005 | $20.00 | 1.01% | 5.04% |
| **2025-05 (incl. event)** | 31 | **$204,089** | **+27.5%** | 10,199 | $20.01 | 0.93% | 4.97% |
| 2025-06 | 30 | $169,790 | -16.8% | 8,487 | $20.01 | 1.01% | 4.98% |
| 2025-07 | 31 | $177,484 | +4.5% | 8,874 | $20.00 | 0.98% | 5.03% |
| 2025-08 | 31 | $180,793 | +1.9% | 9,040 | $20.00 | 1.00% | 5.01% |
| 2025-09 | 30 | $160,851 | -11.0% | 8,045 | $19.99 | 1.00% | 5.06% |
| 2025-10 | 31 | $165,673 | +3.0% | 8,284 | $20.00 | 0.84% | 4.98% |
| 2025-11 | 30 | $156,114 | -5.8% | 7,810 | $19.99 | 1.03% | 5.09% |
| **2025-12** | 31 | **$156,004** | -0.1% | 7,797 | $20.01 | 0.86% | 5.00% |

- **Best month, reported (with event):** May 2025, $204,089. But that title is entirely the restaurant week (below).
- **Best month, ordinary trend (event removed):** **August 2025, $180,793.** On ordinary trading May's run-rate is $173,334, which ranks **third** behind August and July.
- **Worst month:** February 2025, $144,262 (also the shortest month; on a per-day basis February at $5,152/day beats December at $5,032/day, so **December is the genuinely weakest trading month**).
- **Average check never moves.** $19.99 to $20.01 in every one of twelve months. No price increase in 2025, no mix shift large enough to move the blended check by two cents. Revenue here is a pure function of cover count.

### Restaurant week (2025-05-05 to 2025-05-18): isolated, not extrapolated

Owner-confirmed: this window is a **citywide restaurant week, a recurring annual event, not a new baseline**. Per the amended revenue rule it is reported on its own line and its lift is not carried into the ordinary trend or extrapolated.

**Event line (its exact dollar effect):**

| Item | Value |
|------|-------|
| Window | 2025-05-05 to 2025-05-18 (14 days) |
| Window net (actual) | $105,840.00 |
| Baseline-expected net for those 14 days (DOW median from the other 11 months) | $75,085.89 |
| **Event effect (excess net vs baseline)** | **+$30,754.11** (+$2,197/day for 14 straight days) |
| Excess covers | +1,533 |
| Average check in window | $20.02 (vs $20.00 rest of year, unchanged) |
| Discount % in window | 4.97% (vs 5.00%, unchanged) |
| Burdened labor % in window | 35.84% (vs 35.88% FY, unchanged) |

The boundaries are clean: 2025-05-04 sits $66 *below* baseline, 2025-05-05 jumps $1,801 above and stays elevated for fourteen consecutive days, then 2025-05-19 drops back to $372 above baseline and the rest of May is normal. Four days in the window (May 9, 10, 16, 17) are the only days all year beyond 2.5 standard deviations of daily net. The lift is pure incremental traffic: excess net per excess cover is $20.06, the same as a normal cover; it was not bought with markdowns (discount rate slightly below baseline) and it was not a price move.

**Ordinary trend, restated both ways (auditable):**

| Figure | With event | Without event | Basis for "without" |
|--------|-----------|---------------|---------------------|
| FY net | $1,995,691.05 | **$1,964,936.94** | 365 days, window reverted to baseline (FY net - $30,754.11 excess) |
| FY avg net/day | $5,467.65 | **$5,383.39** | $1,964,936.94 / 365 |
| FY net, ordinary days only | -- | $1,889,851.05 over 351 days | window's 14 days dropped entirely |
| FY avg net/day, ordinary days only | -- | $5,384.19 | $1,889,851.05 / 351 |
| May net | $204,089 | **$173,334** | May total - $30,754.11 event excess |
| H1 net | $998,771.89 | **$968,017.78** | H1 net - $30,754.11 event excess |
| H2 vs H1 | H2 -0.19% (H1 higher) | **H2 +2.99% (H2 higher)** | ordinary H1 968,017.78 vs H2 996,919.16 |

Two audit notes. First, the two "without event" run-rates converge: $5,383.39/day (remove the lift, keep 365 days) and $5,384.19/day (drop the 14 days, 351 days). Both say the ordinary business runs at roughly **$5,383/day**. Second, **the raw H1-ahead-of-H2 result was entirely the restaurant week.** Remove it and ordinary H1 sits about 3% below H2. Do not build a growth or decline narrative on this either way: it is inside the POS-transition error band (POS_A, which measures H1, reads 3.9-6.5% higher than POS_B, which measures H2). The honest read remains a **flat year at about $5,383/day of ordinary trading**, with one two-week recurring event on top.

**Forward note for the next edition (not a forecast).** The event proves the room absorbs **+38% covers/day for 14 days** with the burdened labor ratio unchanged (35.84% vs 35.88% FY) and the post-send void rate not rising (May's 0.93% is the second-lowest month of the year). That is a real, demonstrated capacity envelope. It is **not** a forecast: per the owner, the next edition must be sized against future booking/registration numbers, and those are not in the provided inputs. No projected figure is produced here. The proven envelope above is stated as an observed ceiling only; turning it into a plan needs the registration/reservation data (see Data Quality).

### By day of week (FY2025, unchanged from V1)

| Day | N | Net sales | Avg/day | Covers | Avg check | Hours | Wage $ | SPLH |
|-----|---|-----------|---------|--------|-----------|-------|--------|------|
| Saturday | 52 | $376,254 | $7,236 | 18,814 | $20.00 | 5,676 | $116,032 | $66.29 |
| Friday | 52 | $359,795 | $6,919 | 17,990 | $20.00 | 5,445 | $111,326 | $66.07 |
| Thursday | 52 | $296,191 | $5,696 | 14,802 | $20.01 | 4,475 | $88,828 | $66.19 |
| Wednesday | 53 | $274,445 | $5,178 | 13,718 | $20.01 | 4,136 | $82,106 | $66.35 |
| Tuesday | 52 | $245,967 | $4,730 | 12,303 | $19.99 | 3,710 | $73,650 | $66.31 |
| Monday | 52 | $234,138 | $4,503 | 11,709 | $20.00 | 3,535 | $70,180 | $66.23 |
| **Sunday** | 52 | **$208,901** | **$4,017** | 10,446 | $20.00 | 3,164 | $64,685 | $66.02 |

Friday plus Saturday = $736,049, **36.9% of the year in 2/7 of the days**. Sunday is the weakest day at 55.5% of Saturday's volume.

### Category mix (FY2025, unchanged from V1)

Product files reconcile to the daily net exactly ($1,995,691.05).

| Category | Units | Net revenue | % of net |
|----------|-------|-------------|----------|
| Mains | 73,315 | $1,418,288.00 | 71.1% |
| Starters | 26,616 | $268,639.64 | 13.5% |
| Desserts | 24,192 | $183,942.78 | 9.2% |
| Beverages | 32,846 | $124,820.63 | 6.3% |

Top items: Grilled Chicken Plate $429,791.63 (21.5%), Beef Bowl $392,308.58 (19.7%), Pasta Special $354,511.15 (17.8%). Four Mains SKUs carry 71.1% of the business. **The beverage program is one SKU** (`SKU_008 Soft Drink`); beverage attach is 32,846 units against 99,782 covers = **32.9%**, and there is no alcohol SKU in the data. Beverages at 6.3% of net is low against a typical full-service benchmark of 20-30% (**INDUSTRY BENCHMARK, not this venue's data**), but that comparison only holds if the venue is licensed and full-service, which the data cannot establish. Flagging as a question, not a finding.

---

## Cost Analysis

**PARTIALLY SKIPPED: no COGS, food purchase, invoice or P&L data was provided.**

- Food cost %: **cannot be calculated.** DATA NOT PROVIDED.
- Prime cost %: **cannot be calculated.** Requires COGS; only the labor half is available.
- Cost spike detection (3pp month-over-month): performed on labor only, see below. No month shows a labor spike above 0.2pp.

The only cost line available is labor. Everything below is labor.

---

## Labor Analysis (unchanged from V1)

Source: `labor/Scheduling_Tool_labor_2025.01-12.csv`, 730 rows for Commerce_01 (365 days x 2 roles), `source_granularity = daily_aggregate` on every row.

| Metric | Value |
|--------|-------|
| Regular hours | 29,283.44 |
| Overtime hours | 857.08 (**2.84%** of total hours) |
| Total hours | 30,140.52 |
| Wage cost (as reported) | $606,807.57 |
| **Burdened labor cost** (`config.json: payroll_burden_pct = 18`) | **$716,032.93** |
| Labor % of net, **wage only** | **30.41%** |
| Labor % of net, **burdened** | **35.88%** |
| Target (`config.json: target_labor_pct = 30`) | 30.00% |
| **Gap to target** | **$117,325.62** |
| SPLH (net / total hours) | $66.21 |
| Blended implied rate | $20.13/hr |
| BOH | 12,815.90 hrs, $272,952.04, $21.30/hr |
| FOH | 17,324.62 hrs, $333,855.53, $19.27/hr |

**At 30.41%, labor looks on target. It is not. It is 35.88%.** The `wage_cost` column is bare wages; applying the 18% config burden puts labor **5.88 points over the 30% target, a gap of $117,325.62 for the year** and the largest single number in the analysis. Every day clears the target once burden is applied: **365/365 days exceed 30% burdened** (34.02%-37.75%); on the wage-only figure it looks like a coin flip (248/365). The first move is to restate the labor KPI on a burdened basis, because every scheduling decision made against 30.41% has been made against a number 5.5 points wrong.

**Scheduling quality is genuinely good, and that constrains the fix.** Understaffed days (SPLH > $80): **zero.** Daily SPLH ranges $63.91 to $68.85, a $5 band across 365 days including the +38% restaurant-week fortnight. Hours are pegged tightly to sales. Day-of-week burdened labor % sits in a 35.30%-36.54% band, no loose day. Bringing Sunday (worst, 36.54%) to Thursday's ratio (35.39%) is worth only **$2,401.72/year**, 2% of the gap. The labor gap is **structural** (rate, burden, fixed floor, or the frozen $20.00 check), not a scheduling error. Given the check has not moved all year while labor sits 5.88 points over target, **the pricing side deserves at least as much attention as the cost side.** Overtime at 2.84% of hours is stable (2.57%-3.19%) and not a material lever.

`min_foh_per_day = 2` is **unverifiable**: if it means FOH hours it is never breached (min 30.89/day); if headcount, the daily-aggregate export has no headcount, shift or employee columns. No employee-level labor, so individual productivity and shift-level staffing are out of reach.

---

## Integrity Analysis

### Voids: two rates, kept separate (amended rule)

A void with a blank "Sent to Kitchen At" / `kitchen_sent_at` is a **pre-send correction** (the item never reached the kitchen). A void with that field populated is a **post-send void** (the item was fired, then reversed). Under the amended integrity rule these are two different things and are reported as two rates. Only the post-send rate is the void rate and the loss figure.

| Measure | Events | Value | % of gross | What it is |
|---------|--------|-------|-----------|-----------|
| **Post-send voids (the void rate / loss line)** | 1,099 | **$21,024.89** | **1.00%** | item fired then reversed; real reversal |
| **Pre-send corrections (workflow/training signal)** | 415 | $7,778.52 | 0.37% | corrected before the kitchen fired; not lost sales |
| Combined (pre + post) | 1,514 | $28,803.41 | 1.37% | **not the void rate**; mixes the two |

The daily summary `voids` column equals the **post-send** total on **365/365 days**. So the summary void figure of 1.00% is **correct** for the loss line, not an understatement. The $7,778.52 of pre-send activity is correctly outside that line: those items were killed before any food or cost was committed. The two rates must be tracked separately going forward, which is precisely what the amended rule and the owner both require.

**August 1-14, the owner's context: a training and workflow signal, not an allegation.** The owner states one team member was new on the POS during the first two weeks of August and was still learning it. The data is consistent with that: in that window, **49% of void events (49 of 100) are pre-send corrections**, against a **25.9%** pre-send share across the rest of the year. Whole-month August runs at **42.1%** pre-send and its total void event count (178) is well above the ~120/month norm, then the pre-send share falls back in the second half of the month as one would expect while someone learns the keys. This is framed as a training and workflow pattern. **No individual is named, and a high pre-send count is explicitly not an allegation.** The signal points at onboarding and POS workflow, not at a person.

### Void approval control, on a post-send (real-money) basis

The approval gap is real, but under the amended rule the money at stake is the **post-send** slice, because pre-send corrections did not commit food or revenue.

| Slice | Events | Value | Read |
|-------|--------|-------|------|
| **Post-send AND unapproved** (real-money control gap) | 273 | **$5,109.04** | food cooked, then written off with no manager reference |
| Pre-send AND unapproved | 301 | $5,575.23 | corrections without a ref; not lost money |
| All unapproved (both) | 574 | $10,684.27 | mixes the two; V1 headlined this figure |

The actionable control gap is the **$5,109.04** that was cooked and then binned without a manager signature. The fix is a system control (block the void without a manager code), consistent with the owner's read that this is a process issue.

### No employee is an outlier, on a post-send basis (the finding)

The amended rule ranks employees by **post-send** void $ only, and flags an identifier only if it exceeds 2x the team average **and** survives the pre-send split. Post-send void value across the five staff:

| Employee | Post-send events | Post-send void $ | vs team avg |
|----------|------------------|------------------|-------------|
| Server 5 | 220 | $4,389.17 | 1.044x |
| Server 1 | 229 | $4,325.14 | 1.029x |
| Server 2 | 217 | $4,258.35 | 1.013x |
| Server 4 | 226 | $4,121.79 | 0.980x |
| Server 3 | 207 | $3,930.44 | 0.935x |

Team average $4,204.98; the 2x flag threshold is $8,409.96. The highest is Server 5 at **1.044x**; the spread from highest to lowest is **1.117x**. **Nobody is close to the flag, and no candidate survives the pre-send split.** That uniformity is itself diagnostic: theft and abuse cluster in an individual, whereas a post-send void rate that is near-identical across five people is a **process** signature, the approval requirement simply is not enforced on anyone. The fix is the system control above, not a conversation with a server, and **no one is named**. Void reasons are evenly spread with no dominant cause (Guest request $6,341.02, Price adjust $6,288.31, Item changed $5,621.56, Order error $5,417.35, Kitchen issue $5,135.17; these are all-events figures).

### Discounts: reconcile perfectly, but 38% of the dollars need no approval (unchanged from V1)

Discount detail matches the daily summary on **365/365 days**, both totalling $105,066.95 (**5.00% of gross**), flat all year (4.93%-5.09%). Two codes:

| Code | Name | Uses | Value | % of discounts | Approval required |
|------|------|------|-------|---------------|-------------------|
| DSC_01 | Loyalty Credit | 7,239 | $65,141.52 | 62.0% | **yes** |
| DSC_02 | Set Menu Adjustment | 4,438 | $39,925.43 | 38.0% | **no** |

**$39,925.43 of discount value was issued under a code that requires no approval by design** (4,438 uses, 1.9% of gross). No evidence any of it is improper; it is an open control gap.

**No-approval real-money exposure (revised under the amended rule):** post-send unapproved voids $5,109.04 + DSC_02 $39,925.43 = **$45,034.47 (2.26% of net).** This revises V1's $50,609.70 / 2.5% figure downward: V1 included all unapproved voids ($10,684.27), but the amended rule excludes the pre-send unapproved corrections ($5,575.23) from the exposure, since no food or revenue was committed. This sizes a control gap, not an alleged loss.

---

## Top 5 Findings (ranked by $ impact)

| # | Finding | Source | Annual Impact | Confidence |
|---|---------|--------|--------------|------------|
| 1 | **Labor is 35.88% of net, not 30.41%.** The scheduling export reports bare wages; applying the 18% config burden puts labor 5.88pp over the 30% target. All 365 days breach on a burdened basis (34.02%-37.75%); on the wage-only figure it reads 248/365. Not a scheduling problem: SPLH is pinned in a $63.91-$68.85 band all year and the best day-mix fix is worth only $2,401.72. (Unchanged from V1.) | `labor/*.csv`, `config.json`, daily POS net | **$117,325.62 gap to target.** A gap, not identified waste; closing it needs rate, hours or price to move. | **High** on the arithmetic and 365/365 breach. **Low** on recoverability. |
| 2 | **`Q2 CORRECTED.csv` is wrong and overstates Q2 net by 2.00%.** Five variants, identical gross, four nets, each fitting a clean formula at 91/91 days. The correct file is `Q2 (2).csv` ($533,978.45), confirmed to the cent on 91/91 days by both the daily POS exports and the independently-generated annual report. CORRECTED applies a flat 2% uplift and is the newest, so both instinctive tiebreaks pick the wrong file. (Unchanged from V1.) | `reports/...Q2*.csv` vs daily POS and annual | **$10,679.57** phantom revenue if adopted; gates every downstream ratio. | **Very high.** Two independent sources, 91/91 days. |
| 3 | **Void rate is 1.00% (post-send), and the daily summary was right.** Reframed under the amended rule: the loss line is the 1,099 post-send voids, $21,024.89, 1.00%, exactly what the daily summary reports (365/365). The 415 pre-send corrections ($7,778.52, 0.37%) are a separate training/workflow signal, not lost sales. **No employee is an outlier on a post-send basis** (max Server 5 at 1.044x vs a 2x flag; spread 1.117x), so this is a process signature, not a person, fixed by a system control. Real-money control gap = **$5,109.04** cooked-and-binned unapproved. Owner-confirmed: the Aug 1-14 pre-send spike (49% vs 26% baseline) is a team member new on the POS, a training gap, named to no one. | `pos/Commerce_01/*/voids/*.csv` vs daily summaries; owner-feedback.md | **$5,109.04** unapproved post-send voids is the actionable subset. Void loss $ is menu value, not food cost (no COGS to convert). | **High** on the definition (365/365 exact) and the no-outlier result. |
| 4 | **$45,034.47 left through channels with no approval trail** (2.26% of net): $39,925.43 via `DSC_02 Set Menu Adjustment` (no approval by design, 4,438 uses) + $5,109.04 post-send unapproved voids. Revised down from V1's $50,609.70 because the amended rule excludes pre-send unapproved corrections ($5,575.23) from exposure. No evidence of impropriety; this sizes a control gap. | `pos/Commerce_01/*/discounts/*.csv`, `*/voids/*.csv` | **$45,034.47 exposed.** Not a loss estimate. | **High** on the amounts. **Zero** evidence any of it is improper. |
| 5 | **Restaurant week (May 5-18) delivered +$30,754.11 on +1,533 covers at full margin, then stopped dead, and it recurs annually.** Owner-confirmed citywide event, isolated and **not extrapolated**. Unchanged check ($20.02), discount rate (4.97%) and labor ratio (35.84%); sharp boundaries. Proof the room absorbs +38% volume for 14 days without the labor ratio or post-send void rate moving. Removing it, the ordinary year is flat at ~$5,383/day and the peak month is August, not May. | daily POS exports vs DOW baseline; labor; owner-feedback.md | **$30,754.11 proven** for 14 days. **Not extrapolated:** a next-edition forecast needs booking/registration data, which is not in scope. | **High** that it happened and was traffic-driven; cause now owner-confirmed. |

**A note on what is not in this list.** Ordinary trading is flat (H1 vs H2 within the POS error band, ~$5,383/day either way) and the average check has not moved by more than two cents in twelve months. There is no organic growth or decline to arrest. The picture is a business running a tight, well-scheduled operation at a structurally unaffordable labor ratio on a price point nobody has touched all year, with one recurring two-week event that fell through at close to full contribution margin. The lever with proven upside is a repeatable plan for that event, and sizing it properly needs booking data that was not in scope.

---

## Data Quality Notes

- **Data provided:**
  - `pos/Commerce_01/POS_A/{daily,products,voids,discounts}/`: 183 files each, 2025-01-01 to 2025-07-02
  - `pos/Commerce_01/POS_B/{daily,products,voids,discounts}/`: 184 files each, 2025-07-01 to 2025-12-31
  - `labor/Scheduling_Tool_labor_2025.01-12.csv`: 12 files, 730 Commerce_01 rows, 2025-01-01 to 2025-12-31
  - `reports/`: Q1, Q2 (x5 variants), Q3, Q4 for Commerce_01, plus `Demo_Group_Annual_Sales_Report_2025.csv`
  - `config.json`: burden 18%, target labor 30%, min FOH/day 2, currency CAD, `pos_time_offset_minutes: null`
  - Owner context (not a data file): `owner-feedback.md`, providing the restaurant-week identity of the May window and the Aug-onboarding context for voids.
  - All files parsed cleanly. **No file was unreadable, corrupted or unparseable.**

- **Data missing (blocks specific analysis):**
  - **COGS / food purchases / invoices**: blocks food cost % and prime cost %, and blocks converting $21,024.89 of post-send voids into a real food-cost number. Biggest gap.
  - **P&L / financial statements**: blocks any margin conclusion.
  - **Employee-level labor**: daily aggregate with no headcount/shift/employee ID. Blocks individual productivity, shift-level staffing, and verification of `min_foh_per_day`.
  - **Hourly sales**: blocks daypart analysis. Void timestamps are not sales timestamps.
  - **Booking / registration numbers for the restaurant week**: **now the highest-value gap for forward planning.** The event's cause is known (owner-confirmed), but sizing the next edition needs registration/reservation data, which is not in the provided inputs. Without it, only the proven capacity envelope (+38% covers, ratios held) can be stated, not a forecast.
  - **Wage rates, roles, tenure**: blocks assessing whether the $20.13/hr blended rate is the lever.
  - **Bank statements**: no third-party confirmation; the reconciliation is POS-internal.
  - **Tips data for H2**: POS_A carries `Tips`, POS_B daily does not. Not analysed for either half.

- **Sections skipped:** Food cost % / Prime cost % (no COGS); Revenue by hour (no hourly data); YoY (2025 only); cost trend tables (no COGS); Tips (POS_A only).

- **Assumptions made:**
  1. **`Q2 (2).csv` is authoritative for Q2.** Matches daily POS and the annual report on 91/91 days to the cent; the only variant using the `net = gross - discounts` convention that holds 365/365. (Unchanged from V1.)
  2. **POS_B is used for 2025-07-01 and 2025-07-02; POS_A rows for those dates are dropped.** Matches the annual and Q3 convention, yields exactly 365 unique days. The two systems disagree 3.89% and 6.50% on these days and I have not reconciled that. (Unchanged from V1.)
  3. **POS-reported net (`gross - discounts`) is used rather than the procedure's `gross - voids - discounts - taxes`.** Holds 365/365; procedure formula would understate net ~11%. (Unchanged from V1.)
  4. **18% payroll burden applied to `wage_cost` per `config.json`.** Both figures shown. (Unchanged from V1.)
  5. **The May 5-18 window is treated as a recurring special event, isolated from the ordinary trend, per owner context (`owner-feedback.md`).** Its lift ($30,754.11) is reported on its own line and not extrapolated; ordinary-trend figures are shown both with and without it. **New in V2.**
  6. **Voids are split at the "Sent to Kitchen At" field: post-send = void rate and loss; pre-send = correction/training signal, per the amended integrity rule and owner context.** Employee ranking is on post-send $ only. **New in V2.**

- **Limitations:**
  - **The POS transition is not reconciled.** POS_A reads 3.89% and 6.50% higher than POS_B on the only two shared days. The H1/H2 comparison, including the event-removed version (ordinary H2 +2.99% over H1), carries an unquantified systematic error that could exceed the effect. Do not build a trend narrative on it.
  - **No external verification.** Everything reconciles but traces to one POS lineage. No bank statements.
  - **Labor gap is a gap, not a recoverable saving.** $117,325.62 is distance to a config target.
  - **Void dollars are not food cost dollars.** $21,024.89 of post-send voids is menu value, not cost. Without COGS I cannot convert it.
  - **`min_foh_per_day = 2` is unverifiable** (unit ambiguous, no headcount column).
  - **The restaurant-week driver is now known** (owner: citywide restaurant week, recurring annual). What is still missing is the **booking data** to turn the proven capacity envelope into a next-edition plan. No forecast is produced.
  - **This data is unusually regular** (avg check within $0.02 for twelve months, labor within 0.2pp, SPLH in a $5 band, tax exactly 10.0% of net, discounts exactly 5.00% of gross), consistent with the declared `"dataset_classification": "synthetic"`. That regularity is what makes the genuine irregularities (Q2 variants, POS overlap, the pre/post-send void split, the restaurant-week window) stand out. On messier real-world data the same findings would need wider tolerances.
  - **Scope.** I analysed only `pos/`, `labor/`, `reports/` and `config.json` as assigned, plus the owner feedback I was directed to read. Other material in the inputs directory was not opened.

- **To improve this analysis, provide:**
  1. **Supplier invoices or COGS by month**: unlocks food cost %, prime cost %, and converts the $21,024.89 of post-send voids into a real P&L number. Single biggest unlock.
  2. **Restaurant-week booking / registration / reservation data**: turns the proven +$30,754.11 capacity envelope into a real next-edition forecast and staffing plan. Highest ratio of value to effort now that the cause is known.
  3. **P&L for FY2025**: the only way to answer whether 35.88% burdened labor is survivable.
  4. **Employee-level labor export with shifts and headcount**: unlocks shift-level staffing, verifies `min_foh_per_day`, tests whether the labor gap is rate or hours.
  5. **A POS_A vs POS_B parallel run** or the migration notes explaining the July 1-2 discrepancy: reconciles the two halves of the year.
  6. **Hourly sales export from both systems**: unlocks daypart analysis.
  7. **Bank statements or accounting exports**: first genuinely independent check on the POS lineage.
