"""Shared test fixtures and module loading for the test suite.

Loads the standalone traffic_scout.py script as an importable module so the
tests can exercise its functions directly via ``from .conftest import
traffic_scout as ts``.
"""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
_TRAFFIC_SCOUT_PATH = REPO_ROOT / "performance-audit" / "scripts" / "traffic_scout.py"

_spec = importlib.util.spec_from_file_location("traffic_scout", _TRAFFIC_SCOUT_PATH)
traffic_scout = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(traffic_scout)
