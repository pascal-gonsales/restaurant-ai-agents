"""Structural prompt lint.

These tests fail the build if any agent prompt loses its anti-fabrication
ABSOLUTE RULES section, drops its Role section, hardcodes a brand attribution
string instead of the {{REPORT_BRAND}} placeholder, or if the team prompt
counts drift. They verify the written contract is present in every prompt;
they do not test model behavior against the contract.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TEAMS = ["performance-audit", "demo-builder", "food-cost-sentinel"]

_ABSOLUTE_RULES_HEADER_RE = re.compile(r"^##\s+ABSOLUTE\s+RULES", re.MULTILINE)
_ABSOLUTE_RULES_SECTION_RE = re.compile(
    r"^##\s+ABSOLUTE\s+RULES[^\n]*\n(.*?)(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL,
)
_NUMBERED_RULE_RE = re.compile(r"^\s*\d+\.\s+", re.MULTILINE)
_ROLE_HEADER_RE = re.compile(r"^##\s+Role\s*$", re.MULTILINE)


def _all_agent_prompts():
    """Yield (team, prompt_path) for every agent prompt, sorted."""
    for team in TEAMS:
        agents_dir = REPO_ROOT / team / "agents"
        for prompt_path in sorted(agents_dir.glob("*.md")):
            yield team, prompt_path


def _extract_absolute_rules_section(text):
    match = _ABSOLUTE_RULES_SECTION_RE.search(text)
    return match.group(1) if match else ""


_PROMPTS = list(_all_agent_prompts())
_PROMPT_IDS = [str(p.relative_to(REPO_ROOT)) for _, p in _PROMPTS]


def test_every_team_has_agents_dir():
    for team in TEAMS:
        agents_dir = REPO_ROOT / team / "agents"
        assert agents_dir.is_dir(), f"{team} is missing an agents/ directory"
        md_files = list(agents_dir.glob("*.md"))
        assert len(md_files) >= 1, f"{team}/agents has no .md prompt files"


def test_team_count_matches_readme():
    counts = {
        team: len(list((REPO_ROOT / team / "agents").glob("*.md"))) for team in TEAMS
    }
    assert counts["performance-audit"] == 4, counts
    assert counts["demo-builder"] == 4, counts
    assert counts["food-cost-sentinel"] == 4, counts
    assert sum(counts.values()) == 12, counts


@pytest.mark.parametrize("team, prompt_path", _PROMPTS, ids=_PROMPT_IDS)
def test_each_agent_has_absolute_rules_header(team, prompt_path):
    text = prompt_path.read_text(encoding="utf-8")
    assert _ABSOLUTE_RULES_HEADER_RE.search(text), (
        f"{prompt_path} is missing an '## ABSOLUTE RULES' header"
    )


@pytest.mark.parametrize("team, prompt_path", _PROMPTS, ids=_PROMPT_IDS)
def test_each_agent_absolute_rules_has_at_least_five_rules(team, prompt_path):
    text = prompt_path.read_text(encoding="utf-8")
    body = _extract_absolute_rules_section(text)
    rules = _NUMBERED_RULE_RE.findall(body)
    assert len(rules) >= 5, (
        f"{prompt_path} ABSOLUTE RULES has only {len(rules)} numbered rules "
        "(expected >= 5)"
    )


@pytest.mark.parametrize("team, prompt_path", _PROMPTS, ids=_PROMPT_IDS)
def test_each_agent_absolute_rules_mentions_no_invention_or_no_fabrication(
    team, prompt_path
):
    text = prompt_path.read_text(encoding="utf-8")
    body = _extract_absolute_rules_section(text).lower()
    keywords = ("invent", "fabricat", "never invent", "no fabrication")
    assert any(keyword in body for keyword in keywords), (
        f"{prompt_path} ABSOLUTE RULES does not mention any anti-fabrication "
        f"keyword {keywords}"
    )


@pytest.mark.parametrize("team, prompt_path", _PROMPTS, ids=_PROMPT_IDS)
def test_each_agent_has_role_section(team, prompt_path):
    text = prompt_path.read_text(encoding="utf-8")
    assert _ROLE_HEADER_RE.search(text), f"{prompt_path} is missing a '## Role' section"


def test_no_brand_hardcoded_attribution():
    forbidden = ["AI Resto Tools Performance Audit", "AI Resto Tools - AI Tools"]
    for _team, prompt_path in _PROMPTS:
        text = prompt_path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text, (
                f"{prompt_path} contains hardcoded brand attribution '{needle}'; "
                "use the {{REPORT_BRAND}} placeholder instead"
            )


def test_report_builder_uses_placeholder_brand():
    path = REPO_ROOT / "demo-builder" / "agents" / "report-builder.md"
    text = path.read_text(encoding="utf-8")
    assert "{{REPORT_BRAND}}" in text


def test_blueprint_builder_uses_placeholder_brand():
    path = REPO_ROOT / "performance-audit" / "agents" / "blueprint-builder.md"
    text = path.read_text(encoding="utf-8")
    assert "{{REPORT_BRAND}}" in text
