# Restaurant AI Agents

A portfolio multi-agent prompt system for restaurant operators. It packages
three independent agent teams that each turn raw restaurant data into a
decision-ready deliverable, built around one non-negotiable rule: every number
traces to a source, and missing data is declared, never invented.

Brand attribution in the agents is a runtime placeholder (`{{REPORT_BRAND}}`), so anyone can run the system under their own name.

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

Each agent is a markdown prompt file, not executable code. The agents are
designed to run as a small fan-in pipeline: specialists work in parallel, then
a synthesizer agent combines their outputs into the final deliverable.

## The headline engineering point: anti-fabrication discipline

The interesting part is not the agents, it is the discipline that makes their
output trustworthy. Every one of the twelve prompts carries a numbered
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

This is wired into continuous integration. `tests/test_agent_rule_uniformity.py`
fails the build if any prompt loses its ABSOLUTE RULES section, drops below five
numbered rules, removes the anti-fabrication keyword, loses its `## Role`
section, hardcodes a brand string instead of `{{REPORT_BRAND}}`, or if the team
prompt counts drift from four-per-team / twelve total. The anti-hallucination
contract is treated as a testable property, not a guideline.

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

These are reusable prompt templates plus a small data-pull tool. There is no
"paying customer" claim, no "tested on N clients," and no real revenue or labor
numbers anywhere. The samples in `examples/` are explicitly fictional and every
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
