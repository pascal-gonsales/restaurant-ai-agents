FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

# Case Study: a synthetic reconstructed demonstration

This is a reproducible demonstration of the Performance Audit agents working a
realistic, fully synthetic dataset, followed by an operator review that catches
what the agents got wrong. It exists to answer one question a reader of this
repository has: does this system run end to end and produce disciplined,
source-traced output, and does a human in the loop actually add value?

Read the next paragraph before anything else, because it sets the honesty bar.

## What this is, and what it is not

It is a **reconstruction**, not a captured live run. The agents were invoked with
an LLM runtime and their outputs saved, but the artifact does not carry the
independent evidence that would let a stranger prove an LLM produced these exact
files at these exact times (no raw transcripts, no per-invocation input manifests,
no external chronology). The operator who supplied the feedback is the same person
who built the fixture, so the human-in-the-loop step is **simulated operator
feedback**, not two independent parties. The receipts under `runs/` are an audit
trail, not proof. `RUN_NOTES.md` lists every one of these gaps in plain language.

So read this as: "here is what the agent system produces, and here is the review
discipline applied to it," not "here is proof of a live client engagement."

## Read it in a few minutes

1. `outputs/v1/final/blueprint-commerce-01.md` is the first-pass blueprint from data
   alone. Its top open question is a two-week revenue spike it can measure but not
   explain, which it correctly refuses to extrapolate.
2. `owner-feedback.md` is the operator context: two facts that were not in any data
   file the agents were given (they do live in the oracle the designer authored).
3. `outputs/v2/final/blueprint-commerce-01.md` is the second pass, informed by that
   context and by three hardened prompt rules.
4. **`CORRECTIONS.md` is the most important file.** It is the operator review that
   catches four substantive errors the agent drafts made, including a headline
   "growth" claim that does not survive an equal-day comparison. The drafts are kept
   with their errors on purpose; catching them is the point.
5. `RUN_NOTES.md` is the honest record of how the run diverged from its own plan and
   what it cannot prove.

The honest takeaway is narrower than a triumphant one, and truer: the agents produce
structured, fully traced output; they refuse to over-extrapolate and refuse to
accuse; and a domain expert removes four real errors before any of it reaches a
decision. That last step is the job this repository is a portfolio for.

## The traps in the fixture

The data is built to contain the failure modes the agent rules target, so running
the agents exercises the rules rather than asserting them:

- A mid-year POS system change: two column schemas in one year, with two overlap
  days a naive total double-counts.
- Four contradictory versions of the same quarter, where the reassuring filename is
  not the authoritative one.
- A two-week revenue spike with no label explaining it.
- A window where one identifier shows a high raw void count that is mostly pre-send
  corrections, not voided sales.

Which rule targets each trap is in `fixture-spec.md`.

## Reproduce it

```bash
python3 case-study/generate_fixture.py --output case-study/inputs
python3 case-study/scripts/verify_fixture.py
python -m pytest case-study/tests/ -q
```

The fixture is deterministic and seed-locked, so it rebuilds byte for byte. The
agent runs are not re-executed by these commands; `runs/` holds the effective prompt
and output hash per invocation as an audit trail, with the limits described above.

## Honest limits

Synthetic throughout. Reconstruction, not a captured live run. Simulated operator,
not an independent second party. Receipts are an audit trail, not cryptographic
proof. The four corrected errors are in `CORRECTIONS.md`; the full list of what this
does not prove is in `RUN_NOTES.md`.
