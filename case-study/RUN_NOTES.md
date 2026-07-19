FICTIONAL CASE STUDY. SYNTHETIC DATA ONLY.

# Run Notes

This file records what actually happened when the case study was run, including
where reality diverged from the plan and where an adversarial review later caught
the artifact overstating itself. The drafts under `outputs/` were annotated after the
run (a review banner was added, and the client blueprint got a small language pass);
this file and `CORRECTIONS.md` say exactly what was changed. None of the failures
below is hidden.

## What this run was designed to test

Whether a fully synthetic fixture could drive an analyst-to-operator loop: a first
pass (V1) works from data alone, the operator adds context that is not in any file,
the prompts are hardened, and a second pass (V2) produces a better-grounded result.
The design intent was a turnaround caused by operator knowledge. As recorded below,
the run only partly met that intent, and the honest result is smaller than the
design hoped for.

## What actually happened

The V1 specialists were run with `oracle/ground-truth.json`, `owner-feedback.md`,
and each other's outputs excluded from their input sets. That is how the run was set
up; it is asserted by the setup, not independently proven (see "What this does not
prove"). The first V1 run is canonical and is the one recorded here. It was not
re-rolled for a better result.

Three things diverged from the plan. All are recorded rather than hidden.

### 1. The intended false-accusation error did not occur.

The plan expected V1 to see one identifier with an unusually high void count and
reach for allegation language. It did not. The V1 Data Analyst, on the un-amended
prompt, wrote: "There is no bad actor here, and I am not going to manufacture one,"
and read the flat void spread as a process signature. The prompt was already
disciplined enough to refuse the trap. Good for the system, but it means the void
thread is "the analyst read it correctly and the operator added onboarding context,"
not "the analyst accused someone and the operator corrected it."

The void fixture was also weaker than intended: the elevated-count window is 14 days
inside a 365-day file, so on a full-year ranking the signal dilutes to 1.04x the team
average, under any threshold. The trap could not have fired on the full-year view.

Note on the word "theft": it appears in the V1 and V2 drafts, in both cases to argue
the pattern is NOT theft. The draft bodies are the agents' own words, kept unchanged
except that a review banner was added at the top of each file and one client-blueprint
sentence was neutralized in the language pass. The operator review in `CORRECTIONS.md`
is where allegation-adjacent language and every other correction is recorded.

### 2. `owner-answers.md` answered the wrong questionnaire.

The generator populated `owner-answers.md` with answers about audit scope, not the
15 operational questions the Owner Calibrator asks. The V1 Owner Calibrator caught
this and reported 0 of 15 answered rather than inventing context. The blueprints
therefore ran with little owner-operational context. Left as-is and disclosed,
because the agents' handling of the gap is part of what is demonstrated.

### 3. The V2 "reversal" did not survive review.

V2 claimed that, with the exceptional period removed, ordinary H2 was up 2.99 percent
over ordinary H1, and framed operator context as having "unlocked" this. An
adversarial review showed both claims are wrong:

- The 2.99 percent compares totals over unequal periods (181 vs 184 days). Per day
  the figure is about 1.31 percent, inside the POS-transition measurement seam, so
  there is no material reversal. Corrected in `CORRECTIONS.md`.
- V1 had already computed the event dollar figure and built the counterfactual on its
  own. Operator context **confirmed the suspected exceptional-event interpretation and
  justified presenting the counterfactual separately**; it did not unlock a
  calculation. The honest human-in-the-loop value is that operator context prevented
  two false narratives (a spurious "growth" and V1's spurious "decline"), both
  artifacts of unequal-period totals.

## The loop that the evidence actually supports

- V1 surfaced a two-week spike and refused to extrapolate it, flagging it as the top
  owner question.
- The operator supplied two facts absent from every permitted data file: the spike
  coincided with a recurring city event, and the early-August void volume reflected a
  team member new on the POS.
- The prompts were hardened (`diffs/prompt-amendment.diff`): short spikes are not
  baseline; pre-send corrections are separated from post-send voids; allegation
  vocabulary was removed.
- V2 isolated the event and, after review, the ordinary trend is indeterminate across
  the unreconciled POS change (the per-day gap is smaller than the POS overlap
  disagreement). Operator context kept the analysis from turning that artifact into a
  trend in either direction. That is the demonstration, corrected.

## What this does not prove

- No real client, revenue, or impact. Everything is synthetic.
- This is a reconstruction, not a captured live run. There are no raw LLM
  transcripts, no per-invocation input manifests, no runtime or session logs, and no
  external chronology. The output hashes in `runs/` are of the published files, which
  are annotated versions: each carries a review banner added after the agents ran, and
  the client blueprint has one neutralized sentence. No pristine, byte-identical
  capture of the raw model emission was kept, so the original draft cannot be
  reconstructed from what is here. The hashes are an audit trail of the published
  state, not proof of authorship or timing, and could have been generated afterward.
- The operator is the same person who built the fixture and knew the oracle. This is
  simulated operator feedback, not two independent parties. "Not in any file" means
  not in any file the agents were allowed to read; the facts do live in the oracle and
  generator the operator authored.
- V2 re-ran only two agents (Data Analyst and Blueprint Builder); the Owner Calibrator
  and Traffic Scout outputs were carried over unchanged.
- The files under `outputs/` are the agent draft bodies with a review banner added on
  top, plus one neutralized sentence in the client blueprint. They are the reviewed,
  annotated versions, not a pristine capture of the raw model emission; no separate
  byte-identical capture of the original output exists.
- The claims JSON and the HTML renderings are outside the receipt hashes. Both carry a
  review notice pointing to `CORRECTIONS.md`, but a reader parsing only the raw numbers
  should treat them as unreviewed draft values.
- The prompts were hardened twice: once between V1 and V2, and again after the review
  (the de-overfit pass). The archived `runs/v2/*/effective-prompt.txt` capture the
  V2-time prompt, which still instructed a per-person void ranking; the current prompts
  in the repo are the post-review version that reports voids aggregate-only. The
  `diffs/prompt-amendment.diff` shows the V1-to-V2 change, not the later review change.
- Deterministic fixture tests prove the fixture, not that an LLM produced the reports.
- It changes nothing about older commits in this repository's history; it improves the
  evidence from this point forward only.

Given all of the above, this artifact cannot rule out that a polished narrative was
written first and the receipts arranged around it. Read it as a synthetic
demonstration of the system's discipline and of an expert review pass, not as
evidence of an executed client loop.
