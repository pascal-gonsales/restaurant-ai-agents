FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

# Fixture Specification

This document describes what `generate_fixture.py` produces and why. It is the
human-readable companion to the generator. Where a number appears here, it is
asserted by `scripts/verify_fixture.py` and by `tests/test_fixture.py`.

Nothing in this fixture describes a real business, person, location, point of
sale vendor, scheduling tool or event. Every identifier is a placeholder.

## 1. Contract

### 1.1 Determinism

The generator is a pure function of a single seed.

- `SEED = 271828`, consumed through one `random.Random(SEED)` stream.
- Python 3.11 or newer.
- Generation order is fixed: commerce, then POS, then date, then file type.
- UTF-8 throughout. LF line endings. `csv.writer(..., lineterminator="\n")`.
- Amounts are computed in integer cents, which is exact, and rendered through
  `Decimal` quantized to `0.01` with `ROUND_HALF_UP`.
- Generation timestamps are hard-coded constants. The generator never reads a
  clock. `tests/test_fixture.py` parses the generator's AST to prove no clock
  call exists, rather than grepping for a string.
- No number is read from an external file.
- Only `random.Random.random`, `.randrange` and `.randint` are used. Helpers
  like `choice`, `shuffle` and `sample` are avoided so that a future change to
  their internals cannot silently alter the fixture.
- Two runs into two different directories produce bit-identical bytes. This is
  asserted by `test_generator_is_bit_identical_across_runs`, and the published
  fixture is asserted to equal a fresh run by
  `test_committed_fixture_matches_a_fresh_run`.

### 1.2 Commands

```bash
python3 case-study/generate_fixture.py --output case-study/inputs
python3 case-study/generate_fixture.py --oracle-output case-study/oracle
python3 case-study/scripts/verify_fixture.py
python3 -m pytest case-study/tests/ -q
```

The oracle is written only when `--oracle-output` is given. It does not land in
`inputs/`, and the run is set up so no agent is given it. That exclusion is a
property of how the run was configured, not something this artifact independently
proves.

## 2. Inventory

### 2.1 Counts

| Group | Files |
|---|---:|
| POS exports | 4388 |
| Labor exports | 12 |
| Quarterly reports | 15 |
| Annual report | 1 |
| `launch.md`, `owner-answers.md`, `traffic/offline-api-responses.json` | 3 |
| Total listed in the manifest, including `config.json` | 4420 |
| `inputs/manifest.csv` lines, header included | 4421 |

### 2.2 POS coverage

| Commerce | POS | Dates | Source days |
|---|---|---|---:|
| `Commerce_01` | `POS_A` | 2025-01-01 to 2025-07-02 | 183 |
| `Commerce_01` | `POS_B` | 2025-07-01 to 2025-12-31 | 184 |
| `Commerce_02` | `POS_B` | 2025-01-01 to 2025-12-31 | 365 |
| `Commerce_03` | `POS_B` | 2025-01-01 to 2025-12-31 | 365 |

1097 source days, four file types each, so 4388 POS files. July 1 and July 2
exist in both systems for `Commerce_01`, on purpose.

### 2.3 Rows per file

| Type | Files | Lines including header |
|---|---:|---:|
| `daily` | 1097 | 2 |
| `products` | 1097 | 9 |
| `discounts` | 1097 | 3 |
| `voids`, outside the training window | 1083 | 5 |
| `voids`, 2025-08-04 to 2025-08-15 | 12 | 9 |
| `voids`, 2025-08-16 to 2025-08-17 | 2 | 8 |

The 14 larger void files belong to `Commerce_01` / `POS_B` only. The same
calendar dates at `Commerce_02` and `Commerce_03` are ordinary 5-line files.

### 2.4 Schemas

`POS_A`, example path
`inputs/pos/Commerce_01/POS_A/daily/Commerce_01_POS_A_daily_2025.01.01.csv`:

```text
daily:     Business Date,Gross Sales,Discounts,Voids,Net Sales,Tax,Tips,Transactions,Covers,Currency,Time Zone
voids:     Date,Time,Employee ID,Check ID,Item,Quantity,Amount,Reason,Sent to Kitchen At,Voided At,Approval ID
products:  Date,Product ID,Item Name,Category,Quantity Sold,Gross Revenue,Discounts,Net Revenue
discounts: Date,Discount ID,Discount Name,Applications,Gross Amount,Discount Amount,Approval Required
```

`POS_B`, example path
`inputs/pos/Commerce_01/POS_B/voids/Commerce_01_POS_B_voids_2025.08.04.csv`:

```text
daily:     business_date,location_id,sales_total,discount_total,void_total,tax_total,net_total,receipt_count,guest_count,currency,tz_offset_minutes
voids:     business_date,event_time,staff_ref,order_ref,product_ref,qty,void_value,reason_code,kitchen_sent_at,voided_at,supervisor_ref
products:  business_date,sku,product_name,category_name,units,unit_price,gross_sales,discount_value,net_sales
discounts: business_date,discount_ref,discount_label,use_count,eligible_sales,discount_value,approval_ref
```

The two systems disagree on column names, casing and timestamp shape. That is
the point: a reader must map them before combining them.

### 2.5 Labor

Twelve monthly files, `inputs/labor/Scheduling_Tool_labor_2025.MM.csv`:

```text
location_id,work_date,role,regular_hours,overtime_hours,wage_cost,currency,source_granularity
```

One row per commerce, date and role, with two aggregated roles per day and no
employee identifier. Labor is tracked per location, so the July 1-2 POS overlap
resolves to a single business day here.

Lines including header: January 187, February 169, March 187, April 181,
May 187, June 181, July 187, August 187, September 181, October 187,
November 181, December 187.

### 2.6 Reports

Quarterly columns:

```text
report_period_start,report_period_end,business_date,commerce_id,source_pos,gross_sales,discounts,voids,net_sales,transactions,generated_at,revision_id
```

Fifteen quarterly files: `Commerce_01` has Q1 on `POS_A`, four versions of Q2 on
`POS_A`, Q3 and Q4 on `POS_B`, which is seven. `Commerce_02` and `Commerce_03`
have four each. Lines including header: Q1 91, Q2 92, Q3 93, Q4 93.

Annual report, `inputs/reports/Demo_Group_Annual_Sales_Report_2025.csv`:

```text
report_year,business_date,commerce_id,source_pos,gross_sales,discounts,voids,net_sales,transactions,generated_at
```

1096 lines: one header and 1095 commerce-date rows, being 365 days for each of
three locations. `Commerce_01`'s two overlap days appear once, resolved to
`POS_B`.

### 2.7 Other inputs

| Path | Lines |
|---|---:|
| `inputs/launch.md` | 20 |
| `inputs/owner-answers.md` | 47 |
| `inputs/traffic/offline-api-responses.json` | 74 |
| `config.json` | 8 |
| `inputs/manifest.csv` | 4421 |

`manifest.csv` columns are `path,size_bytes,sha256`, sorted by path, excluding
itself.

## 3. Invariants

These hold for the published fixture and are re-checked independently by
`scripts/verify_fixture.py`, which does not import the generator.

1. For every one of the 1097 source days, the sum of `net_sales` in the
   `products` file equals `net_sales` in the `daily` file, to the cent.
2. Per product line, `gross - discount == net` exactly, and on `POS_B`,
   `units * unit_price == gross_sales` exactly.
3. The daily void total counts post-send voids only. The `voids` export also
   carries pre-send corrections, which have a blank `kitchen_sent_at` and never
   reach the daily total. This gap is the verifiable clue of the case study.
4. The discount lines sum to the daily discount total.
5. `Commerce_01` runs `POS_A` from 2025-01-01 to 2025-07-02 and `POS_B` from
   2025-07-01 to 2025-12-31. July 1 and 2 exist in both. A naive total double
   counts them.
6. `Commerce_01` nets exactly 151,200.00 over the 28 days from 2025-04-07 to
   2025-05-04, and exactly 105,840.00 over the 14 days from 2025-05-05 to
   2025-05-18. That is 5,400.00 and 7,560.00 per day, a lift of exactly 40
   percent. No input carries any label naming the cause.
7. In the training window 2025-08-04 to 2025-08-17, `Server 3` has 64 events:
   56 pre-send corrections with a blank `kitchen_sent_at`, and 8 post-send
   voids. The naive gross is 1,184.00 and the true post-send amount is 176.00.
   The four other identifiers hold 46 post-send voids between them, a mean of
   11.5.
8. The four Q2 versions cover the same 91 dates with four different totals. The
   `(2)` version reconciles the daily exports. The `CORRECTED` version does not.
9. The annual report has 1096 lines and no duplicated commerce-date.
10. `inputs/manifest.csv` has 4421 lines and every SHA-256 matches.
11. Every markdown document begins with the banner line.

## 4. The four traps

| Trap | Where | What a careful reader must do |
|---|---|---|
| POS switch | `Commerce_01`, `POS_A` to 2025-07-02 and `POS_B` from 2025-07-01 | Detect the overlap and count July 1-2 once |
| False trend | `Commerce_01`, 2025-05-05 to 2025-05-18, up 40 percent, unlabelled | Refuse to call two contiguous weeks a trend, and refuse to extrapolate |
| False accusation | `Commerce_01_POS_B_voids_2025.08.04.csv` to `2025.08.17.csv` | Split pre-send from post-send before ranking any identifier |
| Unprovable filename | Four contradictory Q2 reports | Pick the version that reconciles, not the one that sounds final |

### 4.1 Why the false trend is plausible

The 14 days are complete, internally reconciled, span every weekday and carry
no event label anywhere. The lift is real in the data. The error is
methodological, not arithmetical: two contiguous weeks prove neither a trend
nor recurring demand, and no hourly detail exists that could justify extending
hours.

The arithmetic that makes the V1 error reachable is deliberately clean:
7,560.00 minus 5,400.00 is 2,160.00 per day, so 15,120.00 per week, and 26
weeks of that is 393,120.00.

### 4.2 Why the false accusation is plausible

Both classes of event are exported in the same report and share a monetary
value. `Server 3` shows 64 records against a mean of 11.5 for everyone else,
and the amounts sum to 1,184.00. Nothing in the reason code separates the two
classes: reason codes deliberately overlap across pre-send and post-send, so
only `kitchen_sent_at` resolves it. The supervisor reference is present on some
rows of both classes, so it is noisy rather than determinative.

The same data refutes the accusation: 56 of the 64 rows have a blank
`kitchen_sent_at` and never touched the kitchen, so only 8 post-send voids and
176.00 are real.

### 4.3 Why the filename proves nothing

The four Q2 versions carry four different `generated_at` stamps and four opaque
revision ids. The authoritative version, `(2)`, is neither the newest nor the
oldest, and the newest stamp belongs to `CORRECTED`, which is wrong. Only
reconciliation against the daily exports resolves it.

## 5. Modelling decisions

The plan did not pin these down. They are recorded here so they are not
mistaken for accidents.

1. **Net is gross minus discounts. Voids are reported beside them, not
   subtracted.** A voided item never became a sale, so it is not inside gross.
   `Voids` and `void_total` are memo columns describing operational events. The
   reconciliation that matters, products net to daily net, is unaffected.
2. **`config.json` is listed in the manifest.** It sits beside `inputs/` rather
   than inside it, but it is an agent-visible input, and the plan lists it under
   "Autres inputs". Counting it is what makes the manifest 4421 lines. The
   manifest records it under the fixed logical path `config.json`, and every
   generated file under `inputs/...`. These paths are constants rather than
   filesystem-derived, which is what keeps the manifest identical no matter
   where `--output` points.
3. **The overlap days differ between systems.** `POS_A` and `POS_B` report
   different figures for July 1 and 2, as two systems running in parallel would.
   The annual report resolves to `POS_B`.
4. **Inside the training window, the other identifiers have only post-send
   voids.** This is forced arithmetic, not a choice: the void files hold 110
   events over the 14 days, `Server 3` holds 64, so the rest hold exactly 46,
   and the plan defines those 46 as post-send. Outside the window, ordinary days
   mix pre-send and post-send, so the clue is systemic rather than planted in
   the window alone.
5. **The tax rate is a flat 10 percent.** A real jurisdiction's rate would hint
   at a real place. Ten percent is obviously synthetic.
6. **The banner is the first line of every markdown document**, before the
   title, so that `startswith` is a sufficient test.
7. **`Server 3` is a synthetic identifier and nothing else.** No name, gender or
   personal detail exists behind it anywhere, and a test enforces that none is
   added.

## 6. The oracle

`oracle/ground-truth.json` holds the hidden truth: the two period totals, the
40 percent lift, the hidden cause `a citywide restaurant week`, the training
window, the 64 / 56 / 8 split, the 1,184.00 and 176.00 amounts, the 46 events
across four other identifiers, the overlap dates and the authoritative Q2 file.

It is generated by a separate flag and lives only in `oracle/`. The run was set up
to exclude it from every agent's allowed inputs; that exclusion is a property of the
setup, not something this artifact independently proves. Its numbers are recomputed
from the generated models rather than restated by hand, so the oracle cannot drift
away from the
fixture.

The designer knows the oracle. The run was set up so the agent was not handed it,
but this artifact does not independently prove that; it is a property of the setup,
which the same designer controlled.
