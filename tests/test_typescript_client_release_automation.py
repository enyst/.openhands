import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = ROOT / "automations" / "typescript-client-release-maintainer"
AUTOMATION_FILE = (
    AUTOMATION_DIR / "typescript-client-release-maintainer.automation.json"
)
PROMPT_FILE = AUTOMATION_DIR / "prompt.md"
INSTALLER_FILE = AUTOMATION_DIR / "install-local.sh"


def test_import_definition_matches_source_prompt() -> None:
    definition = json.loads(AUTOMATION_FILE.read_text())
    spec = definition["spec"]

    assert definition["version"] == 1
    assert definition["kind"] == "automation"
    assert spec["name"] == "typescript-client Agent Server release maintainer"
    assert spec["repository"] == "https://github.com/OpenHands/typescript-client"
    assert spec["branch"] == "main"
    assert spec["enabled"] is False
    assert spec["timeout"] == 1800
    assert spec["trigger"] == {
        "type": "cron",
        "schedule": "17 * * * *",
        "timezone": "Europe/Stockholm",
    }
    assert spec["prompt"] == PROMPT_FILE.read_text()


def test_prompt_preserves_release_safety_boundaries() -> None:
    prompt = PROMPT_FILE.read_text()

    required_fragments = (
        "Do not create a second bump PR",
        "do not merge anything",
        "do not publish the npm package",
        "Process at most one unprocessed candidate per run",
        "its head repository is `OpenHands/typescript-client`",
        "do not hand-edit `src/generated/agent-server-schema.ts`",
        "re-read the PR's final remote head SHA",
        "status=success",
        "Never expose credentials, tokens, or secret values",
    )

    for fragment in required_fragments:
        assert fragment in prompt


def test_local_installer_has_valid_bash_syntax() -> None:
    bash = shutil.which("bash")
    if bash is None:
        return

    subprocess.run([bash, "-n", str(INSTALLER_FILE)], check=True)
