FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

# Corrections: an operator review of the agent drafts

The outputs in `outputs/` are the agent drafts with their errors intact, annotated
after the fact: each file has a review banner added on top, and the client blueprint
has one sentence neutralized (an allegation-adjacent phrase). No pristine,
byte-identical capture of the raw model emission was kept, so treat these as the
reviewed versions, not as an untouched record. Keeping the errors is the point:
catching them is the human-in-the-loop step. This file is that review pass. Anyone
auditing the case study should read it before quoting a number from the drafts.

An adversarial review (an independent model prompted to refute the drafts) flagged
four substantive problems. All four are real. Here is each one, the corrected
figure, and how to reproduce the correction from `inputs/`.

## 1. The "flat year became growing" headline is wrong. There is no material reversal.

**Draft claim (V2):** V1 read the year as flat (-0.19 percent, H1 vs H2 totals);
V2, after isolating the exceptional two-week period, showed ordinary H2 up
**+2.99 percent** over ordinary H1, and presented this as a reversal.

**The error:** the comparison is of totals over unequal periods. The first half
holds 181 days, the second half 184. Three extra days inflate the second half by
roughly 1.66 points before any real trend is measured. Comparing totals is the
same defect that produced V1's -0.19 percent.

**Corrected:** compare per day. Ordinary daily run rates are **$5,348.16** (H1)
and **$5,418.04** (H2), a difference of **+1.31 percent**. The two halves are also
measured on different POS systems whose only two shared days disagree by 3.89 and
6.50 percent. Those are two directional observations, not a measurement interval, so
they do not let anyone claim the year was "flat" any more than "growing."

**Honest read:** once the exceptional period is removed, the ordinary trend is
**indeterminate across the unreconciled POS change**. A +1.31 percent per-day gap
measured across a seam whose overlap days differ by more than that cannot support a
direction. The real human-in-the-loop value here is narrower and truer than the
draft claimed: operator context did not reveal growth, it stopped the analysis from
turning a sub-seam, unequal-period artifact into either a "growth" story (the V2
draft) or a "decline" story (V1). The honest output is "direction unknown until the
POS transition is reconciled," not a trend.

## 2. The event's dollar figure is an estimate against one baseline, not a proven number.

**Draft claim:** the two-week period delivered **$30,754.11**, described in places
as "proven," "the exact event effect," "pure incremental," and at "full contribution
margin."

**The error:** the figure is the excess over an analyst-chosen counterfactual (the
non-May weekday-day-of-week median). Owner confirmation that an event occurred does
not prove every dollar above that baseline was caused by it, and "full contribution
margin" is indefensible in the same report that says COGS and variable costs are
unavailable.

**Corrected language:** call it "an estimated excess of about **$30,754** in net
sales versus the stated non-May weekday-median baseline." It is sensitive to the
baseline chosen: against a trailing-four-week baseline the number would move. Drop
"proven," "exact," "pure incremental," and every "margin" claim. Net sales were
higher during the event window; whether the profit rose, and by how much, is unknown
without cost data.

## 3. The run is Tier 3, not Tier 4.

**Draft claim:** data tier 4, "the deepest tier."

**The error:** the agents' own definition makes Tier 4 require invoices and COGS.
The report declares Tier 4 and then states there are no invoices and no COGS. That
is direct noncompliance with the rule the report is built on.

**Corrected:** this is **Tier 3 (POS plus labor and integrity detail)**. Every
downstream confidence score that leaned on a Tier 4 label should be read one notch
lower.

## 4. The void figure is voided menu value, not proven loss.

**Draft claim:** the post-send void rate is a "loss," and part of it is food that
was "cooked, then binned."

**The error:** a populated kitchen-send timestamp establishes that an item was sent
to the kitchen before it was voided. It does not prove the food was cooked, plated,
or discarded, nor its cost. In an arbitrary POS schema a blank timestamp does not
universally prove a harmless correction either.

**Corrected language:** call the 1.00 percent figure "**post-send voided menu
value**," not loss and not food cost. The pre-send versus post-send split is a
useful workflow signal, but turning it into a dollar loss needs vendor documentation
or a reconciliation the fixture does not contain.

A note on causal language throughout: the drafts say the event "moved" or "drove"
net sales. The defensible statement is associative: net sales were higher during
the event window. Attributing the excess to the event is the owner's interpretation,
reasonable but not proven by the data.

## What the review did not change

The parts of the drafts that survive scrutiny, and that carry the demonstration:

- V1 refused, with no prompting, to turn a high raw void count into an accusation
  ("there is no bad actor here, and I am not going to manufacture one").
- V1 flagged the two-week anomaly and refused to extrapolate it.
- Every number in the drafts traces to a claim and a source row.
- The Q2 filename trap was resolved against the reconciling file, not the most
  official-sounding name.

Those are real, and they are what a reader should take from this. The four
corrections above are what a domain expert removes before any of it reaches a
decision.
