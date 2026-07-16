# Restaurant AI Agents

Three AI agent teams for restaurant operators. Each turns raw restaurant data
into a decision the operator can act on: whether closing the slowest day
actually saves anything once lost revenue is counted, when the kitchen should
open on Saturday, which ingredient is quietly leaking money. All of it built
around one non-negotiable rule: every number traces to a source, and missing
data is declared, never invented.

Brand attribution in the agents is a runtime placeholder (`{{REPORT_BRAND}}`), so anyone can run the system under their own name.

## Reading order (four minutes)

- `examples/sample-blueprint.md` is the end product: a Next Year Blueprint for
  a fictional bistro, down to the Monday decision math: why the tempting
  "close Monday, save $36,000/year in labor" framing fails contribution-margin
  analysis once lost revenue is counted, and the call that replaces it (sample
  data), with the confidence score attached.
- `FIELD_NOTES.md` is why the rules look the way they do: mislabeled export
  years, UTC-shifted hourly data, stale delivery-platform menus, variance that
  reads like theft but is a mapping failure.
- `performance-audit/agents/blueprint-builder.md` is the densest single
  prompt: synthesis, contradiction handling, confidence scoring, and the
  iteration loop.

## What it does

Three teams, twelve agents (four each), one shared architecture contract:

- **Performance Audit** (`performance-audit/`) turns one operator's historical
  data into a Next Year Blueprint: recommended operating days and hours, an
  SPLH-based staffing template, the top revenue actions ranked by annual dollar
  impact, cost-control flags, and a mandatory data-quality section. A small
  Python tool (`scripts/traffic_scout.py`) pulls public foot-traffic
  (popular-times) data for the venue and nearby competitors.
- **Demo Builder** (`demo-builder/`) generates a personalized Operations
  Intelligence Report for a sales prospect using only public-style data
  (reviews, menu, business profile). It is a pre-sales tool: show a prospect
  what AI analysis looks like before they share anything proprietary.
- **Food Cost Sentinel** (`food-cost-sentinel/`) detects food-cost variance by
  reconciling supplier purchases against theoretical usage
  (`Variance = Actual purchased - Theoretical used`), then ranks money leaks by
  dollar impact with calibrated severity flags.

Each agent is a non-executable Markdown procedure, manually invoked with
Claude Code (which is also how this repository was built). To be precise about
what is and is not here: there is no orchestration runtime, no command that
launches the twelve agents, and no behavioral evaluation suite. The repository
contains the twelve prompt files, one Python data-pull helper
(`scripts/traffic_scout.py`), and static tests that verify the prompt
contracts remain present. Writing the procedures as explicit prompts is still
a deliberate choice for this class of work: the failure mode of restaurant
analysis is not a crash, it is a confident wrong number, and the defense
against that is written constraints, reconciliation steps, and refusal rules.
The intended workflow is a small fan-in: three specialist prompts are run
first (in parallel sessions or one after another), then the synthesizer prompt
combines their output files into the final deliverable.

## Anti-fabrication discipline

The core of this repo is the rule discipline that makes agent output
trustworthy enough to act on. Every one of the twelve prompts carries a numbered
`## ABSOLUTE RULES - VIOLATION = OUTPUT IS WORTHLESS` section enforcing:

- **No invention.** Missing data is declared (`DATA NOT PROVIDED`, `UNREADABLE`,
  `INCOMPUTABLE`, `INSUFFICIENT_DATA`, `UNMAPPED`) and skipped. A blank cell is
  better than a fake number.
- **Source-traced numbers.** Every figure cites a file, cell, row, or computed
  delta.
- **Estimates labeled as estimates,** with the method and inputs stated, and
  ranges when uncertain.
- **A mandatory data-quality section** listing every gap, assumption, and
  limitation.
- **Confidence labels** on every recommendation and every fuzzy mapping.
- **Reconciliation gates** (for example, sales mix must reconcile to the POS
  total before any variance is computed).
- **Patterns, not accusations.** Variance flags describe data and possible
  causes; they never name a person.

This is wired into continuous integration as a structural prompt lint.
`tests/test_agent_rule_uniformity.py` fails the build if any prompt loses its
ABSOLUTE RULES section, drops below five numbered rules, removes the
anti-fabrication keyword, loses its `## Role` section, hardcodes a brand
string instead of `{{REPORT_BRAND}}`, or if the team prompt counts drift from
four-per-team / twelve total. Honest scope: this lint proves the contract is
still written down in every prompt; it does not prove a model follows it.
Behavioral evaluations (feed a prompt broken data, verify it refuses) would be
the next step and are not in this repo.

## Why the rules look the way they do

Each rule targets a specific, well-known way restaurant data goes wrong.
Three examples:

- POS exports named by year can contain a different year's data. The
  trajectory check in `data-analyst.md` (rules 10 and 11) refuses to build
  recommendations on an unverified year label and presents both
  interpretations instead.
- Hourly POS data often arrives in UTC. Presented as local time it invents a
  dead dinner service or a phantom morning rush. `blueprint-builder.md`
  rule 15 drops the hourly table entirely unless the timezone is confirmed.
- Cached delivery-platform menus can be years out of date. Unverified prices
  kill the food-cost section outright (`menu-cost-analyst.md` rule 6)
  rather than quietly degrading it.

The full list, with the failure mode each rule is designed to prevent and the
design call behind it, is in `FIELD_NOTES.md`.

## How an audit is designed to run

The Performance Audit team defines the loop (each step is a manually invoked
prompt session; there is no orchestrator):

1. The operator's exports go in a local `data/` folder (POS, financials,
   labor, the owner questionnaire). Nothing from that folder is ever
   committed.
2. Three specialists run in parallel: the Data Analyst on the files, the Owner
   Calibrator on the questionnaire, the Traffic Scout on public foot traffic
   (via `scripts/traffic_scout.py`).
3. The Blueprint Builder synthesizes. When sources disagree (the data says
   close Monday, the owner says regulars come Monday), it presents all
   perspectives instead of silently picking one. The owner decides.
4. The audit is iterative, not one-shot. `data/config.json` carries calibrated
   parameters (payroll burden, minimum staffing, targets),
   `data/owner-feedback.md` accumulates corrections, and every re-run must
   apply both, open with a "Changes from Previous Version" section, and pass a
   consistency check before the report is final.

## How it is built

- **Python 3.11.** One runtime dependency: `requests` (plus `pytest` for the
  tests). No build system; dependencies are installed ad hoc.
- **Agents are markdown.** Output schemas are inline templates with `[bracketed]`
  fill-ins. Variables flow as files: inputs under `data/`, deliverables under
  `output/`.
- **`traffic_scout.py`** is fully env-parameterized so it is self-documenting
  when run unconfigured. It resolves an API key from the environment or a
  credentials file, uses a submit-then-poll API pattern with linear backoff,
  and caps spend with a call budget. Its docstring and implementation agree on
  return codes: `0` on success or when unconfigured, `1` when no API key is
  found. Transport and unexpected-status errors are caught, logged, and the run
  still completes cleanly.

### Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest requests

# full test suite
python -m pytest tests/ -v

# agent-rule discipline gate only
python -m pytest tests/test_agent_rule_uniformity.py -v

# syntax check the script
python -m py_compile performance-audit/scripts/traffic_scout.py

# smoke run (exits 0 unconfigured, never crashes)
FOOT_TRAFFIC_API_KEY=smoke-test-key python performance-audit/scripts/traffic_scout.py
```

## Honest claims only

These are written agent procedures plus a small data-pull tool. There is no
"paying customer" claim, no "tested on N clients," no field-history claim, and
no real revenue or labor numbers anywhere. What this repo claims is the
discipline encoded in the prompts, nothing more: not a client list, not a
track record. The samples in `examples/` are explicitly fictional and every
figure is round and labeled `(sample data)`.

## No real data

This repository contains zero real client, venue, person, or financial data.
Agent prompts reference data structures (POS exports, financials, owner
questionnaires) but embed no values. Sample outputs are fictional. Brand
attribution is the `{{REPORT_BRAND}}` placeholder, the call-to-action is the
`[CALENDLY_LINK]` placeholder, and the script's venue, city, and cuisine are
`<RESTAURANT_NAME>` / `<CITY>` / `<REGION>` placeholders until configured at
runtime. Real values live in the user's local data folder, never in the repo.

## Security and development

This repository was built clean-room: it contains only synthetic demo data and no real client, venue, or financial information. Two gates keep it that way. A local pre-commit hook blocks any commit that contains a private real-data token, and a CI workflow (`.github/workflows/secret-scan.yml`) runs gitleaks on every push and pull request and fails on any secret or credential finding.

## License

MIT. See `LICENSE`.
