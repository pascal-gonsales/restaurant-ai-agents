<!-- FICTIONAL SAMPLE - synthetic data only, not a real venue or real numbers. -->

# Food Cost Variance Report - Cedar & Co Demo Kitchen
## Prepared by {{REPORT_BRAND}} Food Cost Sentinel

> FICTIONAL SAMPLE. Cedar & Co Demo Kitchen is invented. Period, ingredients,
> and figures are synthetic, round, and labeled (sample data). This is a Food
> Cost Sentinel output to show the shape of the deliverable. No real venue or
> supplier is described.

**Analysis period:** 2025-05-01 to 2025-05-31 (sample data).

## Summary
- Total theoretical ingredient cost: $10,000 (sample data)
- Total actual purchases: $12,000 (sample data)
- Overall variance: $2,000 (20%) (sample data)
- Number of red flags: 2

## Top 10 Variances by Dollar Impact
| Ingredient | Theoretical | Actual | Variance % | $ Impact | Flag |
|------------|-------------|--------|------------|----------|------|
| Protein A | $2,000 | $3,000 | +50% | $1,000 | RED |
| Protein B | $1,500 | $2,000 | +33% | $500 | RED |
| Cooking oil | $600 | $800 | +33% | $200 | YELLOW |
| Fresh herbs | $300 | $450 | +50% | $150 | YELLOW |
| Root vegetables | $500 | $600 | +20% | $100 | YELLOW |
| Dairy | $700 | $750 | +7% | $50 | LOW |
| Rice | $400 | $420 | +5% | $20 | LOW |
| Citrus | $200 | $210 | +5% | $10 | LOW |
| Specialty sauce | $300 | $300 | 0% | $0 | LOW |
| House stock | $250 | INSUFFICIENT_DATA | n/a | n/a | DATA GAP |

All figures above are (sample data). Dollar impact is stated before percentage, sorted by dollar impact descending.

## RED FLAGS - Requires Immediate Action

### 1. Protein A over-purchase - $1,000 impact (sample data)
- What: actual purchases ran 50% above theoretical usage for the period.
- Evidence: theoretical $2,000 vs actual $3,000, variance $1,000 (sample data). Math: (actual qty - theoretical qty) x unit price.
- Likely cause: possible over-ordering, waste pattern, or receiving error. Not an accusation, a pattern.
- Recommended action: review receiving logs and prep waste for the period; confirm portion sizes against the recipe.

### 2. Protein B over-purchase - $500 impact (sample data)
- What: actual purchases ran 33% above theoretical usage.
- Evidence: theoretical $1,500 vs actual $2,000, variance $500 (sample data).
- Likely cause: possible over-ordering or unmapped POS product inflating the gap.
- Recommended action: verify the POS-to-recipe mapping for dishes using Protein B before concluding it is waste.

## YELLOW FLAGS - Monitor Next Period
- Cooking oil +33% ($200), fresh herbs +50% ($150), root vegetables +20% ($100) (sample data). Each is within the $100 to $500 band. Watch whether the same items recur next period.

## DATA GAPS - Cannot Analyze (Missing Info)
- House stock: theoretical usage was INCOMPUTABLE because the recipe link was missing, so the variance is INSUFFICIENT_DATA. Provide the recipe-ingredient link to close this gap.

## Note
Target food cost 25 to 30%, acceptable up to 35%, is an industry benchmark for context, not this venue's own data.
