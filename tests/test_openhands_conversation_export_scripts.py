import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "skills" / "openhands-conversation-export" / "scripts"
SCANNER_SAFE_BEARER = "scanner_safe_bearer_token_for_tests_only"


class TestOpenHandsConversationExportScripts(unittest.TestCase):
    def _run_script(
        self,
        script_name: str,
        *args: str,
        check: bool = True,
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.update(kwargs.pop("env", {}))
        return subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / script_name), *args],
            check=check,
            timeout=30,
            text=True,
            env=env,
            **kwargs,
        )

    def test_truncate_json_redacts_and_truncates(self) -> None:
        payload = {
            "session_api_key": "session-secret",
            "nested": {
                "api_key": "api-secret",
                "text": f"Authorization: Bearer {SCANNER_SAFE_BEARER}",
            },
            "long": "x" * 160,
        }

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            input_path = td_path / "input.json"
            output_path = td_path / "output.json"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

            self._run_script(
                "truncate_json.py",
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
            )

            result = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(result["session_api_key"], "<redacted>")
        self.assertEqual(result["nested"]["api_key"], "<redacted>")
        self.assertIn("<truncated", result["long"])
        self.assertIn("Authorization: Bearer <redacted>", result["nested"]["text"])
        self.assertNotIn(SCANNER_SAFE_BEARER, result["nested"]["text"])

    def test_render_markdown_outputs_transcript_and_redacts_tokens(self) -> None:
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
                    "content": f"Authorization: Bearer {SCANNER_SAFE_BEARER}",
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

            self._run_script(
                "render_markdown.py",
                "--input-path",
                str(input_path),
                "--output-path",
                str(output_path),
                "--head",
                "20",
                "--tail",
                "20",
            )

            markdown = output_path.read_text(encoding="utf-8")

        self.assertIn("# Demo conversation", markdown)
        self.assertIn("- Conversation ID: `conv-123`", markdown)
        self.assertIn("<details>", markdown)
        self.assertIn("### User · 2026-01-01T00:00:03Z · id=3", markdown)
        self.assertIn("### Assistant · 2026-01-01T00:00:04Z · id=4", markdown)
        self.assertIn("Authorization: Bearer <redacted>", markdown)
        self.assertNotIn(SCANNER_SAFE_BEARER, markdown)

    def test_render_markdown_keeps_tool_only_transcripts(self) -> None:
        payload = {
            "conversation": {
                "conversation_id": "conv-tools-only",
                "title": "Tool only conversation",
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
                    "content": "hi\n",
                },
            ],
        }

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            input_path = td_path / "input.json"
            output_path = td_path / "output.md"
            input_path.write_text(json.dumps(payload), encoding="utf-8")

            self._run_script(
                "render_markdown.py",
                "--input-path",
                str(input_path),
                "--output-path",
                str(output_path),
            )

            markdown = output_path.read_text(encoding="utf-8")

        self.assertIn("# Tool only conversation", markdown)
        self.assertIn("Tool calls / results (2 events)", markdown)
        self.assertIn("action=run", markdown)
        self.assertIn("observation=run", markdown)

    def test_export_conversation_rejects_missing_id_on_non_terminal_page(self) -> None:
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                parsed = urlparse(self.path)
                if parsed.path == "/api/conversations/conv-123":
                    payload = {
                        "conversation_id": "conv-123",
                        "title": "Demo export",
                        "status": "RUNNING",
                    }
                elif parsed.path == "/api/conversations/conv-123/events":
                    start_id = parse_qs(parsed.query).get("start_id", ["0"])[0]
                    if start_id == "0":
                        payload = {
                            "events": [
                                {
                                    "source": "user",
                                    "action": "message",
                                    "args": {"content": "hi"},
                                }
                            ],
                            "has_more": True,
                        }
                    else:
                        payload = {"events": [], "has_more": False}
                else:
                    self.send_response(404)
                    self.end_headers()
                    return

                body = json.dumps(payload).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: object) -> None:  # noqa: A003
                return

        with HTTPServer(("127.0.0.1", 0), Handler) as server, tempfile.TemporaryDirectory() as td:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            output_path = Path(td) / "export.json"

            result = self._run_script(
                "export_conversation.py",
                "--base-url",
                f"http://127.0.0.1:{server.server_port}",
                "--conversation-id",
                "conv-123",
                "--out",
                str(output_path),
                check=False,
                capture_output=True,
                env={"OPENHANDS_API_KEY": "test-api-key"},
            )
            output_exists = output_path.exists()

            server.shutdown()
            thread.join(timeout=5)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "Expected integer id on last event when has_more=true",
            result.stderr,
        )
        self.assertFalse(output_exists)


if __name__ == "__main__":
    unittest.main()
