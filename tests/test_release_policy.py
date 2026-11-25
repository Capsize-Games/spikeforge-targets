"""Release-policy convergence guards for issue #2."""

import re
from pathlib import Path
from typing import List, Match, Optional

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_PYPROJECT = _ROOT / "pyproject.toml"
_WORKFLOW = _ROOT / ".github" / "workflows" / "ci.yml"
_README = _ROOT / "README.md"
_POLICY = _ROOT / "docs" / "release-policy.md"

_PIN = re.compile(r"spikeforge~=(?P<version>\d+\.\d+\.\d+)")
_STRICT = re.compile(r"^spikeforge~=\d+\.\d+\.\d+$")


def _first_pin(text: str) -> Optional[str]:
    """Return the first core compatible-release pin in text, if any."""
    found: Optional[Match[str]] = _PIN.search(text)
    if found is None:
        return None
    return "spikeforge~=" + found.group("version")


def _all_pins(text: str) -> List[str]:
    """Return every core compatible-release pin found in text."""
    return ["spikeforge~=" + found.group("version")
            for found in _PIN.finditer(text)]


def _is_strict_pin(value: str) -> bool:
    """Return True only for an exact ``spikeforge~=X.Y.Z`` pin."""
    return _STRICT.match(value.strip()) is not None


def test_pyproject_and_ci_pins_agree() -> None:
    """The family core pin is identical in packaging and CI."""
    pyproject_pin = _first_pin(_PYPROJECT.read_text(encoding="utf-8"))
    workflow_pin = _first_pin(_WORKFLOW.read_text(encoding="utf-8"))
    assert pyproject_pin is not None
    assert workflow_pin is not None
    assert pyproject_pin == workflow_pin
    assert _is_strict_pin(pyproject_pin)


def test_core_pin_tracks_matrix_line() -> None:
    """The pin stays on the documented matrix core line."""
    pins = _all_pins(_PYPROJECT.read_text(encoding="utf-8"))
    assert pins == ["spikeforge~=0.6.3"]


def test_release_docs_name_monorepo_provenance() -> None:
    """README and policy state the monorepo publish authority."""
    readme = _README.read_text(encoding="utf-8")
    policy = _POLICY.read_text(encoding="utf-8")
    for text in (readme, policy):
        assert "Capsize-Games/spikeforge" in text
        assert "compatibility.json" in text
    assert "spikeforge~=0.6.3" in policy
    assert "does not publish" in policy or "not from this" in readme


def test_missing_pin_returns_none() -> None:
    """A file without a core pin yields no pin instead of crashing."""
    assert _first_pin('name = "spikeforge-targets"\n') is None
    assert _all_pins('dependencies = ["numpy>=1.26"]\n') == []


@pytest.mark.parametrize("value", [
    "spikeforge==0.6.3",
    "spikeforge>=0.6",
    "spikeforge~=0.6",
    "spikeforge~=0.6.3.1",
    "spikeforge",
    "",
    "spikeforge~=0.6.3; os.system('x')",
])
def test_malformed_pins_rejected(value: str) -> None:
    """Non-conforming specifiers never pass as the family core pin."""
    assert _is_strict_pin(value) is False
