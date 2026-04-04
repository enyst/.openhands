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
    assert (ROOT / ".plugin" / "plugin.json").is_file()
    assert (ROOT / "hooks" / "hooks.json").is_file()
    assert (ROOT / "skills").is_dir()

    for skill in marketplace_manifest["skills"]:
        resolved = ROOT / skill["source"].lstrip("./")
        assert resolved.is_dir(), f"Missing skill source: {resolved}"


def test_plugin_hook_manifest_matches_repo_hook_manifest() -> None:
    repo_hooks = load_json(ROOT / "hooks.json")
    plugin_hooks = load_json(ROOT / "hooks" / "hooks.json")

    assert plugin_hooks == repo_hooks

    commands = [hook["command"] for hook in plugin_hooks["stop"][0]["hooks"]]
    assert "$HOME/.openhands/hooks/deny_stop_on_message.sh" in commands[0]
    assert "$HOME/.openhands/plugins/installed/enyst-workflow/hooks/deny_stop_on_message.sh" in commands[0]
    assert "$HOME/.openhands/hooks/on_stop.sh" in commands[1]
    assert "$HOME/.openhands/plugins/installed/enyst-workflow/hooks/on_stop.sh" in commands[1]
