import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "skills" / "openhands-conversation-export" / "scripts"


class TestOpenHandsConversationExportScripts(unittest.TestCase):
    def test_truncate_json_redacts_and_truncates(self) -> None:
        token = "ghu_abcdefghijklmnopqrstuvwxyz123456"
        payload = {
            "session_api_key": "session-secret",
            "nested": {
                "api_key": "api-secret",
                "text": f"Authorization: Bearer {token}",
            },
            "long": "x" * 160,
        }

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            input_path = td_path / "input.json"
            output_path = td_path / "output.json"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "truncate_json.py"),
                    "--input-path",
                    str(input_path),
                    "--output-path",
                    str(output_path),
                    "--max-len",
                    "60",
                    "--head",
                    "10",
                    "--tail",
                    "10",
                ],
                check=True,
            )

            result = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(result["session_api_key"], "<redacted>")
        self.assertEqual(result["nested"]["api_key"], "<redacted>")
        self.assertIn("<truncated", result["long"])
        self.assertIn("Authorization: Bearer <redacted>", result["nested"]["text"])
        self.assertNotIn(token, result["nested"]["text"])

    def test_render_markdown_outputs_transcript_and_redacts_tokens(self) -> None:
        token = "ghp_abcdefghijklmnopqrstuvwxyz123456"
        payload = {
            "conversation": {
                "conversation_id": "conv-123",
                "title": "Demo conversation",
                "selected_repository": "enyst/.openhands",
                "selected_branch": "main",
                "created_at": "2026-01-01T00:00:00Z",
                "last_updated_at": "2026-01-01T00:01:00Z",
                "status": "RUNNING",
            },
            "events": [
                {
                    "id": 1,
                    "source": "environment",
                    "action": "run",
                    "timestamp": "2026-01-01T00:00:01Z",
                    "args": {"command": "echo hi"},
                },
                {
                    "id": 2,
                    "source": "environment",
                    "observation": "run",
                    "cause": 1,
                    "timestamp": "2026-01-01T00:00:02Z",
                    "content": f"Authorization: Bearer {token}",
                },
                {
                    "id": 3,
                    "source": "user",
                    "action": "message",
                    "timestamp": "2026-01-01T00:00:03Z",
                    "args": {"content": "please export this"},
                },
                {
                    "id": 4,
                    "source": "agent",
                    "action": "message",
                    "timestamp": "2026-01-01T00:00:04Z",
                    "content": "done",
                },
            ],
        }

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            input_path = td_path / "input.json"
            output_path = td_path / "output.md"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "render_markdown.py"),
                    "--input-path",
                    str(input_path),
                    "--output-path",
                    str(output_path),
                    "--head",
                    "20",
                    "--tail",
                    "20",
                ],
                check=True,
            )

            markdown = output_path.read_text(encoding="utf-8")

        self.assertIn("# Demo conversation", markdown)
        self.assertIn("- Conversation ID: `conv-123`", markdown)
        self.assertIn("<details>", markdown)
        self.assertIn("### User · 2026-01-01T00:00:03Z · id=3", markdown)
        self.assertIn("### Assistant · 2026-01-01T00:00:04Z · id=4", markdown)
        self.assertIn("Authorization: Bearer <redacted>", markdown)
        self.assertNotIn(token, markdown)


if __name__ == "__main__":
    unittest.main()
