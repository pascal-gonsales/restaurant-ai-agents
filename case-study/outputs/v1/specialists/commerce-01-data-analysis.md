FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

> REVIEW STATUS: unreviewed agent working paper. See `case-study/CORRECTIONS.md`.

# Data Analysis - Commerce_01
## Prepared: 2026-07-16

Scope note: this analysis covers **Commerce_01 only**. Commerce_02 and Commerce_03 appear in the shared labor and reports files; their rows were filtered out and not analysed.

## Data Inventory

| File | Format | Date Range | Records | Quality | Enables |
|------|--------|-----------|---------|---------|---------|
| `pos/Commerce_01/POS_A/daily/*.csv` (183 files) | CSV | 2025-01-01 to 2025-07-02 | 183 day-rows | Complete | Daily revenue, covers, transactions, tips |
| `pos/Commerce_01/POS_A/products/*.csv` (183 files) | CSV | 2025-01-01 to 2025-07-02 | 8 SKU-rows/day | Complete | Category and item mix |
| `pos/Commerce_01/POS_A/voids/*.csv` (183 files) | CSV | 2025-01-01 to 2025-07-02 | 724 void events (to 06-30) | Complete | Void integrity, employee-level |
| `pos/Commerce_01/POS_A/discounts/*.csv` (183 files) | CSV | 2025-01-01 to 2025-07-02 | 2 discount-rows/day | Complete | Discount integrity |
| `pos/Commerce_01/POS_B/daily/*.csv` (184 files) | CSV | 2025-07-01 to 2025-12-31 | 184 day-rows | Complete | Daily revenue, covers, transactions (no tips column) |
| `pos/Commerce_01/POS_B/products/*.csv` (184 files) | CSV | 2025-07-01 to 2025-12-31 | 8 SKU-rows/day | Complete | Category and item mix (adds unit_price) |
| `pos/Commerce_01/POS_B/voids/*.csv` (184 files) | CSV | 2025-07-01 to 2025-12-31 | 790 void events | Complete | Void integrity, employee-level |
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
- Integrity Analysis: **populated** (voids and discounts, both to event level)

Revenue by hour is **SKIPPED**: no hourly sales data exists. Void events carry timestamps, but void timestamps are not sales timestamps and cannot be used to build an hourly revenue curve.

---

## Source Reconciliation (do this before trusting any number)

Four independent representations of Commerce_01's 2025 sales exist. They agree, once the Q2 question is settled:

| Check | Result |
|-------|--------|
| Annual report vs daily POS exports, all 365 days | **0 mismatches** on gross and net |
| Discount detail files vs daily summary `discounts` | **365/365 days match**, both total $105,066.95 |
| Product files net revenue vs daily summary net | Both total **$1,995,691.05** |
| Void detail files vs daily summary `voids` | **Match only under a specific definition** (see Integrity) |

This is an unusually clean dataset. That makes the two places where it is *not* clean worth taking seriously.

### The Q2 problem: five files, four different answers

Five files claim to report Commerce_01 Q2 2025. All five carry identical `gross_sales`, `discounts` and `voids`. They disagree only on `net_sales`, and each disagrees in a perfectly systematic way. I fitted a formula to each across all 91 days:

| File | revision_id | generated_at | Q2 net total | Formula fit (91/91 days) |
|------|-------------|--------------|--------------|--------------------------|
| `Q2 (1).csv` | rev-3a07 | 2025-07-07 | $562,030.00 | `net = gross` (discounts never applied) |
| `Q2 (2).csv` | rev-b45c | 2025-07-06 | **$533,978.45** | **`net = gross - discounts`** |
| `Q2 CORRECTED.csv` | rev-19de | 2025-07-08 | $544,658.02 | `net = (gross - discounts) x 1.02` |
| `Q2.csv` | rev-8f21 | 2025-07-05 | $539,485.67 | `net = gross - discounts + voids` (voids added back) |

**`Q2 (2).csv` is the authoritative file.** Two independent sources confirm it, and neither of them is a quarterly report:

1. The **daily POS_A exports** for the 91 Q2 days sum to net **$533,978.45** and match `Q2 (2).csv` on **91/91 days, to the cent**.
2. The **group annual report** (generated 2026-01-09, six months later, by a different process) matches `Q2 (2).csv` on **91/91 days, to the cent**.

`net = gross - discounts` is also the convention used by **every other file in the dataset**: Q1, Q3, Q4, the annual report, and all 365 daily exports from both POS systems. It holds on 365/365 days.

**The file named "CORRECTED" is the second-worst file in the set.** It applies a flat 2% uplift to the correct figure. It is the newest by `generated_at` and it has the most reassuring filename, which is exactly why it is dangerous: both of the signals an analyst would instinctively reach for (newest wins, "CORRECTED" wins) point at the wrong file. Using it overstates Q2 net by **$10,679.57 (+2.00%)** and inflates FY2025 net to $2,006,370.62.

Adopting `Q2 (2).csv` is not a close judgement call. It is the only variant that agrees with the underlying transaction data.

### The POS transition: a two-day overlap that does not reconcile

Commerce_01 changed POS mid-year. POS_A covers 2025-01-01 to 2025-07-02 (183 days). POS_B covers 2025-07-01 to 2025-12-31 (184 days). **Both systems reported 2025-07-01 and 2025-07-02.** On those two days they do not agree:

| Date | POS_A gross | POS_B gross | POS_A net | POS_B net | POS_A covers | POS_B covers | Gap |
|------|-------------|-------------|-----------|-----------|--------------|--------------|-----|
| 2025-07-01 | $5,561.00 | $5,353.00 | $5,284.97 | $5,077.70 | 264 | 253 | POS_A reads **3.89% higher** |
| 2025-07-02 | $6,176.00 | $5,799.00 | $5,852.90 | $5,493.68 | 292 | 275 | POS_A reads **6.50% higher** |

I follow the group convention and use POS_B from 2025-07-01 onward: this is what the annual report and the Q3 report both do, and it yields exactly 365 unique days with no double count. The POS_A rows for July 1-2 are excluded.

**This is a real limitation, not a footnote.** The two systems are measuring the same two days and producing answers 3.9% and 6.5% apart. That means H1 and H2 are measured with different rulers. Two days is far too small a sample to derive a correction factor, and I have not applied one. But it does mean the H2 vs H1 comparison below carries an unquantified systematic error, plausibly of the same order as the difference it is trying to measure.

---

## Revenue Analysis

All figures: Commerce_01, FY2025, CAD, from daily POS exports (POS_A 2025-01-01 to 2025-06-30, POS_B 2025-07-01 to 2025-12-31), independently confirmed by `Demo_Group_Annual_Sales_Report_2025.csv` on 365/365 days.

**Net sales definition.** The procedure's reference formula is `Net Sales = Gross Sales - Voids - Discounts - Taxes`. This dataset does **not** follow it. Across all 365 days and both POS systems, the reported net equals `gross - discounts` exactly. Tax sits outside gross (it is a clean 10.0% of net on the FY total), and voids are reported alongside rather than deducted. I use the POS-reported net, because it is internally consistent on 365/365 days, is what the annual report uses, and is what the product files sum to. Applying the procedure's formula literally would double-deduct voids and tax and understate net by roughly 11%. Flagging this rather than silently reconciling it.

### FY2025 headline

| Metric | Value | Source |
|--------|-------|--------|
| Gross sales | $2,100,758.00 | daily exports, `Gross Sales` / `sales_total` |
| Discounts | $105,066.95 (5.00% of gross) | daily exports, `Discounts` / `discount_total` |
| Voids (as reported) | $21,024.89 (1.00% of gross) | daily exports, `Voids` / `void_total` |
| **Net sales** | **$1,995,691.05** | daily exports, `Net Sales` / `net_total` |
| Transactions | 58,698 | `Transactions` / `receipt_count` |
| Covers | 99,782 | `Covers` / `guest_count` |
| Average check per cover | $20.00 | $1,995,691.05 / 99,782 |
| Average per transaction | $34.00 | $1,995,691.05 / 58,698 |
| Covers per transaction | 1.70 | 99,782 / 58,698 |
| Average net per day | $5,467.65 | $1,995,691.05 / 365 |

### Monthly

| Month | Days | Net sales | MoM % | Covers | Avg check | Void % | Disc % |
|-------|------|-----------|-------|--------|-----------|--------|--------|
| 2025-01 | 31 | $157,005 | -- | 7,852 | $20.00 | 1.12% | 4.97% |
| 2025-02 | 28 | $144,262 | -8.1% | 7,215 | $19.99 | 1.20% | 4.93% |
| 2025-03 | 31 | $163,527 | +13.4% | 8,174 | $20.01 | 1.08% | 4.97% |
| 2025-04 | 30 | $160,100 | -2.1% | 8,005 | $20.00 | 1.01% | 5.04% |
| **2025-05** | 31 | **$204,089** | **+27.5%** | 10,199 | $20.01 | 0.93% | 4.97% |
| 2025-06 | 30 | $169,790 | -16.8% | 8,487 | $20.01 | 1.01% | 4.98% |
| 2025-07 | 31 | $177,484 | +4.5% | 8,874 | $20.00 | 0.98% | 5.03% |
| 2025-08 | 31 | $180,793 | +1.9% | 9,040 | $20.00 | 1.00% | 5.01% |
| 2025-09 | 30 | $160,851 | -11.0% | 8,045 | $19.99 | 1.00% | 5.06% |
| 2025-10 | 31 | $165,673 | +3.0% | 8,284 | $20.00 | 0.84% | 4.98% |
| 2025-11 | 30 | $156,114 | -5.8% | 7,810 | $19.99 | 1.03% | 5.09% |
| **2025-12** | 31 | **$156,004** | -0.1% | 7,797 | $20.01 | 0.86% | 5.00% |

- **Best month:** May 2025, $204,089
- **Worst month:** February 2025, $144,262 (also the shortest month; on a per-day basis February at $5,152/day beats December at $5,032/day, so **December is the genuinely weakest trading month**)
- **Trend:** flat. H1 net $998,771.89 vs H2 net $996,919.16, a change of **-0.19%**. Strip May out and the year is a flat line at roughly $5,200-5,500/day. This business did not grow in 2025. It also did not decline. See the POS overlap caveat above before leaning on the H1/H2 comparison.
- **Average check never moves.** $19.99 to $20.01 in every one of twelve months. There was no price increase in 2025, and no mix shift large enough to move the blended check by two cents. Revenue in this business is a pure function of cover count.

### The May anomaly: the most important thing in this dataset

May is not a seasonal bump. It is a **14-day step change with sharp edges**, from **2025-05-05 to 2025-05-18**, against a day-of-week median baseline built from the other eleven months:

| Metric | May 5-18 window | Rest of year | Read |
|--------|-----------------|--------------|------|
| Excess net vs DOW baseline | **+$30,754.11** | -- | +$2,197/day for 14 straight days |
| Excess covers | **+1,533** | -- | the lift is entirely traffic |
| Average check | $20.02 | $20.00 | **unchanged** |
| Discount % of gross | 4.97% | 5.00% | **unchanged** |
| Burdened labor % | 35.84% | 35.88% | **unchanged** |

The boundaries are clean: 2025-05-04 sits $66 *below* baseline, then 2025-05-05 jumps $1,801 above it and stays elevated for fourteen consecutive days, then 2025-05-19 drops back to $372 above baseline and the rest of May is normal. Four days in the window (May 9, 10, 16, 17) are the only days in the entire year beyond 2.5 standard deviations of daily net.

What this rules out:
- **Not a discount push.** The discount rate inside the window is 4.97%, marginally *below* the 5.00% annual rate. Nobody bought this traffic with markdowns.
- **Not a price move.** Average check is $20.02 vs $20.00.
- **Not a mix shift.** Excess net per excess cover is $20.06, the same as a normal cover.
- **Not seasonality.** Seasonality does not switch on and off on named days with a flat line either side.

That leaves an external driver: a promotion, an event, a local one-off, a media mention. **Whatever it was, it produced $30,754 of incremental net at an unchanged average check and unchanged labor ratio, meaning it fell through at close to full contribution margin.** It is also the only evidence in the entire year that this venue has headroom: it absorbed 38% more covers per day for two weeks without the labor ratio degrading and without service quality showing up as elevated voids (May has the second-lowest void rate of the year at 0.93%).

**I cannot tell you what caused it.** My assigned inputs were POS, labor, reports and config. Nothing in them carries marketing, event, weather, reservation or local-calendar context. This is the single highest-value question in the dataset and it is answerable, but not from what I was given. See Data Quality.

### By day of week (FY2025)

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

### Category mix (FY2025)

Product files reconcile to the daily net exactly ($1,995,691.05).

| Category | Units | Net revenue | % of net |
|----------|-------|-------------|----------|
| Mains | 73,315 | $1,418,288.00 | 71.1% |
| Starters | 26,616 | $268,639.64 | 13.5% |
| Desserts | 24,192 | $183,942.78 | 9.2% |
| Beverages | 32,846 | $124,820.63 | 6.3% |

Top items: Grilled Chicken Plate $429,791.63 (21.5%), Beef Bowl $392,308.58 (19.7%), Pasta Special $354,511.15 (17.8%). Four Mains SKUs carry 71.1% of the business.

**The beverage program is one SKU.** The entire Beverages category is `SKU_008 Soft Drink`. Beverage attach is 32,846 units against 99,782 covers = **32.9%**: two out of three guests buy nothing to drink. There is no alcohol SKU in the data at all. Beverages at 6.3% of net is low against a typical full-service benchmark of 20-30% (**INDUSTRY BENCHMARK, not this venue's data**), but that comparison is only meaningful if this venue is licensed and full-service, which I cannot establish from the data. Flagging as a question, not a finding.

---

## Cost Analysis

**PARTIALLY SKIPPED: no COGS, food purchase, invoice or P&L data was provided.**

- Food cost %: **cannot be calculated.** DATA NOT PROVIDED.
- Prime cost %: **cannot be calculated.** Prime cost requires COGS. Only the labor half is available.
- Cost spike detection (3pp month-over-month): performed on labor only, see below. No month shows a labor spike above 0.2pp.

The only cost line available is labor. Everything below is labor.

---

## Labor Analysis

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

### The finding that the dashboard hides

**At 30.41%, labor looks on target. It is not. It is 35.88%.**

The `wage_cost` column in the scheduling export is bare wages. `config.json` specifies an 18% payroll burden. Apply it and labor is **35.88% of net, 5.88 points over the 30% target, a gap of $117,325.62 for the year.** This is the largest single number in the analysis.

The trap here is that the un-burdened figure reads as 30.41%, which lands close enough to the 30% target to pass a glance and to survive a management meeting. Every day of the year clears the target once burden is applied: **365/365 days exceed 30% burdened**, ranging 34.02% to 37.75%. On the wage-only reading it looks like a coin flip: 248/365 days over target. The venue is not marginally missing its labor target. It has never hit it, on any day, and the reported figure is the reason nobody has noticed.

I want to be precise about what this number is and is not. It is a **gap to a target set in config**, not $117,325.62 of identified waste. Recovering it means cutting hours, cutting rates, or raising sales. Which of those is available is not something the data can tell me. What the data *can* tell me is that the first move is to restate the labor KPI on a burdened basis, because every scheduling decision made against the 30.41% figure has been made against a number that is 5.5 points wrong.

### Scheduling quality is genuinely good, and that constrains the fix

Per the procedure's flags:
- **Overstaffed days (labor % > 30%):** on the wage-only basis, 248/365. On the burdened basis, **365/365**. This flag does not discriminate here and is not actionable as a day-picking exercise.
- **Understaffed days (SPLH > $80):** **zero days.** Daily SPLH ranges $63.91 (2025-04-13) to $68.85 (2025-11-10). No evidence of staff being burned out by understaffing.

That SPLH range is the real story. Across 365 days, through a 14-day period where volume ran 38% above baseline, sales per labour hour never left a $5 band. **Hours are already pegged tightly to sales.** Day-of-week burdened labor % confirms it: Monday 35.37%, Tuesday 35.33%, Wednesday 35.30%, Thursday 35.39%, Friday 36.51%, Saturday 36.39%, Sunday 36.54%. There is no sloppy day hiding in here.

I tested the obvious lever anyway. Bringing Sunday (the worst day, 36.54% burdened, $4,017 avg net) down to Thursday's ratio (35.39%) is worth **$2,401.72/year**. That is 2% of the labor gap. **The scheduling waste is not there.** Anyone proposing to close the labor gap by trimming Sunday shifts is solving a $2.4K problem while a $117K one sits next to it.

Since hours track sales almost perfectly and no day is loose, the labor gap is **structural**, not a scheduling error: it lives in the rate, the burden, the fixed staffing floor, or the $20.00 average check that has not moved in twelve months. Given the check has been frozen all year while labor sits 5.88 points over target, **the pricing side deserves at least as much attention as the cost side.**

Overtime at 2.84% of hours is stable all year (2.57% to 3.19%) and is not a material lever.

### What the labor data cannot support

- `config.json` sets `min_foh_per_day = 2`. The unit is ambiguous and the data cannot resolve it. If it means FOH **hours**, it is never breached: minimum FOH hours on any day is 30.89. If it means FOH **headcount**, **the data cannot answer**: the labor export is a daily aggregate with no headcount, no shift and no employee columns. Compliance with this rule is **unverifiable from the provided data.**
- No employee-level labor. Individual productivity, shift-level staffing and scheduling error are all out of reach.
- Labor is BOH/FOH only. No job-level breakdown (server vs host vs dish).

---

## Integrity Analysis

### Voids: the summary reports are hiding 27% of void activity

This is the second place the dataset is not clean, and it is a definitional trap rather than an error.

| Measure | Value | % of gross |
|---------|-------|-----------|
| Void detail files, **all events** (1,514 events) | **$28,803.41** | **1.37%** |
| Void detail, events **sent to kitchen** (1,099 events) | $21,024.89 | 1.00% |
| Daily summary `voids` column | $21,024.89 | 1.00% |
| **Void activity absent from every summary report** | **$7,778.52** | **0.37%** |

The daily summary `voids` figure equals the sum of void events **where `Sent to Kitchen At` / `kitchen_sent_at` is populated**, and it does so on **365/365 days**. It equals the full void total on only 113/365 days. This is not a rounding artifact, it is a definition: **the POS summary counts a void only if the item reached the kitchen.**

The consequence: **the reported void rate of 1.00% is not the void rate. The void rate is 1.37%.** $7,778.52 of voided value never appears in the daily exports, the quarterly reports, or the annual report, because those items were killed before the kitchen saw them. That figure is invisible to anyone reading any summary in this dataset.

Both directions of this matter, and they point opposite ways:
- For **food cost**, the summary figure is arguably the right one. $21,024.89 is the value of food that was actually produced and then thrown away. That is the real waste number.
- For **integrity and training**, the summary figure is the wrong one, and it is wrong by 37%. A void rung before the kitchen fires is still a keying error, a mispriced item, or a guest who was told the wrong thing. $7,778.52 of that is happening and no report shows it.

### Void approval control is weak, and the weakness is uniform

- **574 of 1,514 void events (37.9%), worth $10,684.27, carry no approval reference at all** (`Approval ID` / `supervisor_ref` empty).
- **273 events, worth $5,109.04, were both sent to the kitchen and unapproved.** Food was cooked, then written off, with no manager signature. This is the highest-exposure subset.

### No employee is an outlier, and that is the finding

The procedure asks me to rank employees by void value and flag anyone above 2x the team average. **Nobody is close.** Five staff, FY2025, both POS systems:

| Employee | Events | Void $ | % of voids | vs team avg |
|----------|--------|--------|-----------|-------------|
| Server 5 | 307 | $6,116.68 | 21.2% | 1.06x |
| Server 3 | 321 | $5,965.34 | 20.7% | 1.04x |
| Server 1 | 297 | $5,637.74 | 19.6% | 0.98x |
| Server 2 | 291 | $5,609.15 | 19.5% | 0.97x |
| Server 4 | 298 | $5,474.50 | 19.0% | 0.95x |

The spread from highest to lowest is **1.12x**. The threshold is 2x. There is no bad actor here, and I am not going to manufacture one. The unapproved-and-sent-to-kitchen subset splits the same way (62/56/55/52/48 events across the five).

**That uniformity is itself diagnostic.** Theft and abuse cluster in an individual. A void rate that is identical across five people is a **process** signature, not a people signature: the approval requirement is not being enforced on anyone, so nobody stands out. The fix is a system control (block the void without a manager code), not a conversation with a server. Void reasons are also evenly spread with no dominant cause: Guest request $6,341.02, Price adjust $6,288.31, Item changed $5,621.56, Order error $5,417.35, Kitchen issue $5,135.17.

### Discounts: reconcile perfectly, but 38% of the dollars need no approval

Discount detail matches the daily summary on **365/365 days**, both totalling $105,066.95 (**5.00% of gross**). The discount rate is flat all year, 4.93% to 5.09%. Two discount codes exist:

| Code | Name | Uses | Value | % of discounts | Approval required |
|------|------|------|-------|---------------|-------------------|
| DSC_01 | Loyalty Credit | 7,239 | $65,141.52 | 62.0% | **yes** |
| DSC_02 | Set Menu Adjustment | 4,438 | $39,925.43 | 38.0% | **no** |

**$39,925.43 of discount value was issued in 2025 under a code that requires no approval by design.** I have no evidence any of it is improper, and I am not alleging that. But it is an open control gap: 4,438 uses, no second pair of eyes, 1.9% of gross sales. Combined with $10,684.27 of unapproved voids, **$50,609.70 of value left the business in 2025 through channels with no approval trail.** That is 2.5% of net.

---

## Top 5 Findings (ranked by $ impact)

| # | Finding | Source | Annual Impact | Confidence |
|---|---------|--------|--------------|------------|
| 1 | **Labor is 35.88% of net, not 30.41%.** The scheduling export reports bare wages; applying the 18% payroll burden from config puts labor 5.88pp over the 30% target. All 365 days breach the target on a burdened basis (34.02%-37.75%); on the wage-only figure it looks like 248/365. Not a scheduling problem: SPLH is pinned in a $63.91-$68.85 band all year and the best day-mix fix (Sunday to Thursday's ratio) is worth only $2,401.72. | `labor/*.csv` (730 rows), `config.json` (`payroll_burden_pct`, `target_labor_pct`), daily POS net | **$117,325.62 gap to target.** A gap, not identified waste. Closing it needs rate, hours or price to move, and the data cannot say which is available. | **High** on the arithmetic and the 365/365 breach. **Low** on recoverability: no P&L, no wage detail, no headcount. |
| 2 | **`Q2 CORRECTED.csv` is wrong and overstates Q2 net by 2.00%.** Five Q2 variants, identical gross, four different nets, each fitting a clean formula at 91/91 days. The correct file is `Q2 (2).csv` ($533,978.45), confirmed to the cent on 91/91 days by both the daily POS exports and the independently-generated annual report. The file named CORRECTED applies a flat 2% uplift and is also the newest by `generated_at`, so both instinctive tiebreaks select the wrong file. | `reports/...Q2*.csv` (5 files) vs `pos/Commerce_01/POS_A/daily/*.csv` and `reports/Demo_Group_Annual_Sales_Report_2025.csv` | **$10,679.57** of phantom revenue if adopted. Gates every downstream number: FY net becomes $2,006,370.62 and every ratio shifts. | **Very high.** Two independent sources, exact agreement, 91/91 days. |
| 3 | **The reported void rate is wrong by 37%: 1.37%, not 1.00%.** Daily summaries count only voids where the item reached the kitchen (confirmed 365/365 days). $7,778.52 of void activity is invisible in every daily, quarterly and annual report. Separately, 37.9% of voids ($10,684.27) have no approval reference, and $5,109.04 was cooked and then written off unapproved. | `pos/Commerce_01/*/voids/*.csv` (1,514 events) vs daily summaries | **$7,778.52** of unreported void value; **$5,109.04** of unapproved cooked-and-binned food is the actionable subset. | **High** on the definition (365/365 exact match). Recoverable share unknown: no COGS to convert void $ to food cost $. |
| 4 | **$50,609.70 left the business through channels with no approval trail** (2.5% of net): $39,925.43 via `DSC_02 Set Menu Adjustment`, which requires no approval **by design** (4,438 uses), plus $10,684.27 of unapproved voids. No employee is an outlier: void value spans just 0.95x-1.06x of the team average across five staff, nowhere near the 2x flag. That uniformity says this is a missing system control, not a bad actor. | `pos/Commerce_01/*/discounts/*.csv`, `pos/Commerce_01/*/voids/*.csv` | **$50,609.70 exposed.** Not a loss estimate. No evidence of impropriety; this sizes the control gap, not a leak. | **High** on the amounts and the absence of an employee outlier. **Zero** evidence on whether any of it is improper. |
| 5 | **May 5-18 delivered +$30,754.11 on +1,533 covers at an unchanged $20.02 check, unchanged 4.97% discount rate and unchanged 35.84% labor ratio, then stopped dead.** Sharp boundaries (May 4 below baseline, May 5 +$1,801, May 19 back to normal). Not seasonality, not discounting, not pricing: pure incremental traffic at full margin. It is also proof the venue absorbs +38% volume without labor % degrading or voids rising. | daily POS exports vs day-of-week median baseline from the other 11 months | **$30,754.11 proven** for 14 days. If the driver were identifiable and repeatable monthly, the order of magnitude is large, but **I will not extrapolate that: one occurrence, cause unknown.** | **High** that it happened and that it was traffic-driven. **Zero** on cause. Nothing in my assigned inputs explains it. |

**A note on what is not in this list.** The year is flat (H1 $998,771.89 vs H2 $996,919.16, -0.19%) and the average check has not moved by more than two cents in twelve months. There is no growth story in this data and no organic decline to arrest. Combined with finding 1, the picture is a business running a tight, well-scheduled operation at a structurally unaffordable labor ratio on a price point nobody has touched all year. The single unexplored lever with proven upside is finding 5, and it is unexplored because the data to explain it was not in scope.

---

## Data Quality Notes

- **Data provided:**
  - `pos/Commerce_01/POS_A/{daily,products,voids,discounts}/`: 183 files each, 2025-01-01 to 2025-07-02
  - `pos/Commerce_01/POS_B/{daily,products,voids,discounts}/`: 184 files each, 2025-07-01 to 2025-12-31
  - `labor/Scheduling_Tool_labor_2025.01-12.csv`: 12 files, 730 Commerce_01 rows, 2025-01-01 to 2025-12-31
  - `reports/`: Q1, Q2 (x5 variants), Q3, Q4 for Commerce_01, plus `Demo_Group_Annual_Sales_Report_2025.csv`
  - `config.json`: burden 18%, target labor 30%, min FOH/day 2, currency CAD, `pos_time_offset_minutes: null`
  - All files parsed cleanly. **No file was unreadable, corrupted or unparseable.** No parse errors to log.

- **Data missing (blocks specific analysis):**
  - **COGS / food purchases / invoices**: blocks food cost % and prime cost %. This is the biggest gap. Prime cost is the number most operators actually manage against, and half of it is absent.
  - **P&L / financial statements**: blocks rent, utilities, overhead, and any margin conclusion. I can say labor is 35.88% of net; I cannot say whether the business makes money.
  - **Employee-level labor**: the export is `daily_aggregate` with no headcount, shift or employee ID. Blocks individual productivity, shift-level staffing, and verification of `min_foh_per_day`.
  - **Hourly sales**: blocks daypart analysis. Void timestamps exist but are not sales timestamps and cannot substitute.
  - **Marketing / events / promotions / local calendar**: blocks the May 5-18 question, which is the highest-value unanswered question in the dataset.
  - **Wage rates, roles, tenure**: blocks any assessment of whether the $20.13/hr blended rate is the lever.
  - **Bank statements**: no third-party confirmation of deposits. The reconciliation here is POS-internal: four representations of the same source system agreeing with each other is good, but it is not independent external verification. If the POS itself is misconfigured, every number in this report inherits the error.
  - **Tips data for H2**: POS_A carries a `Tips` column; POS_B's daily export does not. Tips were not analysed for either half, since a half-year series would mislead.

- **Sections skipped:**
  - **Food cost % / Prime cost %**: DATA NOT PROVIDED (no COGS). Not estimated.
  - **Revenue by hour**: DATA NOT PROVIDED (no hourly granularity).
  - **YoY comparison**: data covers 2025 only. Single calendar year, no comparison possible.
  - **Cost trend tables (food, prime)**: same reason as above.
  - **Tips analysis**: available in POS_A only; a half-year series would be misleading.

- **Assumptions made:**
  1. **`Q2 (2).csv` is authoritative for Q2.** Justification: it matches the daily POS_A exports and the independently-generated annual report on 91/91 days to the cent, and it is the only variant using the `net = gross - discounts` convention that holds on 365/365 days across every other file. This is evidence-backed, not a preference.
  2. **POS_B is used for 2025-07-01 and 2025-07-02, POS_A rows for those dates are dropped.** Justification: matches the convention of both the annual report and the Q3 report, and yields exactly 365 unique days with no double count. **The two systems disagree by 3.89% and 6.50% on these days and I have not reconciled that**: see limitations.
  3. **POS-reported net (`gross - discounts`) is used rather than the procedure's `gross - voids - discounts - taxes`.** Justification: the POS convention holds on 365/365 days across both systems, is what the annual report uses, and is what the product files sum to. Applying the procedure formula literally would double-deduct and understate net by roughly 11%. Flagged rather than silently applied.
  4. **18% payroll burden applied to `wage_cost` per `config.json`.** Justification: explicit config value. Both burdened and un-burdened figures are shown throughout so the reader can see the difference the assumption makes.
  5. **May baseline = day-of-week median of the other eleven months.** Justification: median resists the outliers it is meant to detect; DOW-matching controls for the 1.8x Saturday-to-Sunday spread.

- **Limitations:**
  - **The POS transition is not reconciled.** POS_A reads 3.89% and 6.50% higher than POS_B on the only two days both systems covered. H1 and H2 are measured with different instruments. Two days is far too small to derive a correction factor and I have not applied one. **The H2 vs H1 result of -0.19% carries an unquantified systematic error that could plausibly exceed the effect it measures.** Do not build a growth or decline narrative on it.
  - **No external verification.** Everything reconciles, but everything traces to one POS lineage. No bank statements, no accounting system, no third-party confirmation.
  - **Labor gap is a gap, not a recoverable saving.** $117,325.62 is the distance to a config target. Whether it is recoverable, and by which lever, needs rate and P&L data.
  - **Void dollars are not food cost dollars.** $21,024.89 of kitchen-sent voids is menu value, not the cost of the food. Without COGS I cannot convert it. The true P&L impact is materially smaller and I will not guess the ratio.
  - **`min_foh_per_day = 2` is unverifiable.** Unit ambiguous (hours vs headcount) and the labor export has no headcount column.
  - **The May driver is unknown**, and it is the most valuable thing in the dataset.
  - **This data is unusually regular.** Average check within $0.02 for twelve months, labor within 0.2pp for twelve months, SPLH in a $5 band for 365 days, tax exactly 10.0% of net, discounts exactly 5.00% of gross. Real venues are noisier. This is consistent with the dataset's declared `"dataset_classification": "synthetic"` and is stated here because that regularity is what makes the four genuine irregularities (the Q2 variants, the POS overlap gap, the void definition, the May window) stand out as clearly as they do. On messier real-world data the same findings would need wider tolerances.
  - **Scope.** I analysed only `pos/`, `labor/`, `reports/` and `config.json` as assigned. Other material exists in the inputs directory that I did not open, as instructed. **If any of it carries marketing, event or owner context, it may answer the May 5-18 question directly**, and that question is worth more than anything else on this list.

- **To improve this analysis, provide:**
  1. **Supplier invoices or COGS by month**: unlocks food cost %, prime cost %, and converts the $21,024.89 of kitchen-sent voids into a real P&L number. Single biggest unlock.
  2. **Whatever drove May 5-18**: promo calendar, event log, marketing spend, local calendar. Turns the $30,754.11 observation into a repeatable lever. Highest ratio of value to effort.
  3. **P&L for FY2025**: the only way to answer whether 35.88% burdened labor is survivable.
  4. **Employee-level labor export with shifts and headcount**: unlocks shift-level staffing, verifies `min_foh_per_day`, and tests whether the labor gap is rate or hours.
  5. **A POS_A vs POS_B parallel run**, or the migration notes explaining the July 1-2 discrepancy, reconciles the two halves of the year and makes the trend statement trustworthy.
  6. **Hourly sales export from both systems**: unlocks daypart analysis, the last major revenue cut still closed.
  7. **Bank statements or accounting exports**: first genuinely independent check on the POS lineage.
