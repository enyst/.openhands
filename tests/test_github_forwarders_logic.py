import importlib.util
import json
import sys
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SYNC_PATH = (
    REPO_ROOT / "skills" / "github-forwarders" / "scripts" / "sync_forwarders.py"
)


def _load_sync_module():
    spec = importlib.util.spec_from_file_location("sync_forwarders", SYNC_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


sync = _load_sync_module()


class TestGitHubForwardersLogic(unittest.TestCase):
    def test_prepend_forwarder_inserts_block_and_preserves_original(self) -> None:
        upstream = sync.Repo(owner="OpenHands", name="OpenHands")
        target = sync.Repo(owner="enyst", name="openhands-web")
        forwarder = sync.forwarder_block(
            upstream_repo=upstream,
            target_repo=target,
            number=1,
            canonical_url="https://github.com/OpenHands/OpenHands/pull/1",
            no_linkify_upstream=False,
        )
        expected = sync.forwarder_marker_token(upstream, 1)

        original_body = "hello\nworld\n"
        result = sync.prepend_forwarder(
            original_body,
            forwarder,
            expected_marker_token=expected,
        )

        self.assertTrue(result.startswith("---\n# Forwarder: OpenHands/OpenHands#1\n"))
        self.assertIn("## Original content", result)
        self.assertTrue(result.rstrip().endswith(original_body.rstrip()))

    def test_forwarder_block_no_linkify_uses_code_for_upstream_refs(self) -> None:
        upstream = sync.Repo(owner="OpenHands", name="OpenHands")
        target = sync.Repo(owner="enyst", name="openhands-web")
        url = "https://github.com/OpenHands/OpenHands/pull/10"
        text = sync.forwarder_block(
            upstream_repo=upstream,
            target_repo=target,
            number=10,
            canonical_url=url,
            no_linkify_upstream=True,
        )

        self.assertIn("# Forwarder: `OpenHands/OpenHands#10`", text)
        self.assertIn(f"**Canonical location:** `{url}`", text)
        self.assertNotIn("# Forwarder: OpenHands/OpenHands#10", text)
        self.assertNotIn(f"**Canonical location:** {url}", text)


    def test_prepend_forwarder_noops_on_exact_marker(self) -> None:
        upstream = sync.Repo(owner="OpenHands", name="OpenHands")
        target = sync.Repo(owner="enyst", name="openhands-web")
        expected = sync.forwarder_marker_token(upstream, 2)
        body = "ok\n<!-- forwarder: OpenHands/OpenHands#2 -->\n"
        forwarder = sync.forwarder_block(
            upstream_repo=upstream,
            target_repo=target,
            number=2,
            canonical_url="https://github.com/OpenHands/OpenHands/issues/2",
            no_linkify_upstream=False,
        )

        result = sync.prepend_forwarder(
            body,
            forwarder,
            expected_marker_token=expected,
        )
        self.assertEqual(result, body)

    def test_prepend_forwarder_hard_stops_on_mismatched_marker(self) -> None:
        upstream = sync.Repo(owner="OpenHands", name="OpenHands")
        target = sync.Repo(owner="enyst", name="openhands-web")

        expected = sync.forwarder_marker_token(upstream, 3)
        wrong_body = "oops\n<!-- forwarder: OpenHands/OpenHands#999 -->\n"
        forwarder = sync.forwarder_block(
            upstream_repo=upstream,
            target_repo=target,
            number=3,
            canonical_url="https://github.com/OpenHands/OpenHands/pull/3",
            no_linkify_upstream=False,
        )

        with self.assertRaises(sync.ForwarderMarkerMismatchError) as ctx:
            sync.prepend_forwarder(
                wrong_body,
                forwarder,
                expected_marker_token=expected,
            )

        self.assertIn(expected, str(ctx.exception))

    def test_github_client_enforces_expected_status(self) -> None:
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                if self.path == "/created":
                    payload = {"ok": True}
                    body = json.dumps(payload).encode("utf-8")
                    self.send_response(201)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return

                payload = {"ok": True}
                body = json.dumps(payload).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: object) -> None:  # noqa: A003
                return

        with HTTPServer(("127.0.0.1", 0), Handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_port}"

            client = sync.GitHubClient(token="test-token")
            good = client.request("GET", base_url + "/ok", expected=(200,))
            self.assertEqual(good, {"ok": True})

            with self.assertRaises(RuntimeError):
                client.request("GET", base_url + "/created", expected=(200,))

            created = client.request("GET", base_url + "/created", expected=(201,))
            self.assertEqual(created, {"ok": True})

    def test_github_client_retries_on_primary_rate_limit(self) -> None:
        class Handler(BaseHTTPRequestHandler):
            calls = 0

            def do_GET(self) -> None:  # noqa: N802
                Handler.calls += 1

                if self.path == "/rate":
                    if Handler.calls == 1:
                        payload = {"message": "API rate limit exceeded"}
                        body = json.dumps(payload).encode("utf-8")
                        self.send_response(403)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("X-RateLimit-Remaining", "0")
                        self.send_header("X-RateLimit-Reset", str(int(time.time()) - 1))
                        self.send_header("Content-Length", str(len(body)))
                        self.end_headers()
                        self.wfile.write(body)
                        return

                    payload = {"ok": True}
                    body = json.dumps(payload).encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return

                self.send_response(404)
                self.end_headers()

            def log_message(self, format: str, *args: object) -> None:  # noqa: A003
                return

        sleep_calls: list[float] = []

        def fake_sleep(seconds: float) -> None:
            sleep_calls.append(seconds)

        with HTTPServer(("127.0.0.1", 0), Handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_port}"

            client = sync.GitHubClient(
                token="test-token",
                max_retries=2,
                backoff_base_seconds=0.0,
                reset_buffer_seconds=0,
                sleep_fn=fake_sleep,
            )
            result = client.request("GET", base_url + "/rate", expected=(200,))

        self.assertEqual(result, {"ok": True})
        self.assertEqual(Handler.calls, 2)
        self.assertGreaterEqual(len(sleep_calls), 1)



if __name__ == "__main__":
    unittest.main()
