from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_wtf_has_no_unbundled_compound_skill_routing() -> None:
    skill = (ROOT / "skills/wtf/SKILL.md").read_text()
    assert not re.search(r"\bce-[a-z-]+\b", skill)
    assert "relevant project workflow" in skill


def test_learning_retirement_adaptation_link_resolves() -> None:
    assert (ROOT / "skills/learning-retirement/SKILL.md").is_file()
    assert "../learning-retirement/SKILL.md" in (
        ROOT / "skills/adapt-yourself/SKILL.md"
    ).read_text()
