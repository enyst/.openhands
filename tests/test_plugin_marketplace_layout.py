import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / ".plugin" / "plugin.json"
MARKETPLACE_MANIFEST = ROOT / ".plugin" / "marketplace.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def test_marketplace_exposes_root_plugin_and_existing_skills() -> None:
    plugin_manifest = load_json(PLUGIN_MANIFEST)
    marketplace_manifest = load_json(MARKETPLACE_MANIFEST)

    assert plugin_manifest["name"] == "enyst-workflow"
    assert marketplace_manifest["name"] == "enyst-workflow"

    plugin_entry = next(
        entry
        for entry in marketplace_manifest["plugins"]
        if entry["name"] == "enyst-workflow"
    )

    assert plugin_entry["source"] in {".", "./"}
    assert plugin_entry["version"] == plugin_manifest["version"]
    assert marketplace_manifest["metadata"]["version"] == plugin_manifest["version"]
    assert (ROOT / ".plugin" / "plugin.json").is_file()
    assert (ROOT / "hooks" / "hooks.json").is_file()

    skills_root = (ROOT / "skills").resolve()
    assert skills_root.is_dir()

    for skill in marketplace_manifest["skills"]:
        source = Path(skill["source"])
        assert not source.is_absolute(), f"Absolute skill source not allowed: {source}"
        resolved = (ROOT / source).resolve()
        assert resolved.is_dir(), f"Missing skill source: {resolved}"
        assert resolved.is_relative_to(skills_root), (
            f"Skill source must stay under skills/: {source} -> {resolved}"
        )


def test_plugin_hook_manifest_matches_repo_hook_manifest() -> None:
    repo_hooks = load_json(ROOT / "hooks.json")
    plugin_hooks = load_json(ROOT / "hooks" / "hooks.json")

    assert plugin_hooks == repo_hooks

    commands = [hook["command"] for hook in plugin_hooks["stop"][0]["hooks"]]
    deny_command = next(command for command in commands if "deny_stop_on_message.sh" in command)
    on_stop_command = next(command for command in commands if "on_stop.sh" in command)

    assert "$HOME/.openhands/hooks/deny_stop_on_message.sh" in deny_command
    assert "$HOME/.openhands/plugins/installed/enyst-workflow/hooks/deny_stop_on_message.sh" in deny_command
    assert "$HOME/.openhands/hooks/on_stop.sh" in on_stop_command
    assert "$HOME/.openhands/plugins/installed/enyst-workflow/hooks/on_stop.sh" in on_stop_command
