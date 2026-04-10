#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REF_RE = re.compile(r"#(\d{1,6})\b")
MARKER_RE = re.compile(r"<!--\s*forwarder:\s*([^\n]+?)\s*-->")


class ForwarderMarkerMismatchError(RuntimeError):
    def __init__(self, *, expected: str, found: list[str]) -> None:
        super().__init__(
            "Forwarder marker mismatch: expected marker "
            f"{expected!r} but found {found!r}. Stopping for safety."
        )
        self.expected = expected
        self.found = found




def utc_now_iso() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def get_auth_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    try:
        out = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "No GITHUB_TOKEN set and 'gh auth token' failed. "
            "Set GITHUB_TOKEN or authenticate gh."
        ) from exc

    if not out:
        raise RuntimeError("Empty token from 'gh auth token'")
    return out


@dataclass(frozen=True)
class Repo:
    owner: str
    name: str

    @classmethod
    def parse(cls, value: str) -> "Repo":
        if "/" not in value:
            raise ValueError("repo must be OWNER/NAME")
        owner, name = value.split("/", 1)
        if not owner or not name:
            raise ValueError("repo must be OWNER/NAME")
        return cls(owner=owner, name=name)


class GitHubClient:
    def __init__(self, token: str):
        self._token = token

    def request(
        self,
        method: str,
        url: str,
        *,
        json_body: dict[str, Any] | None = None,
        expected: tuple[int, ...] = (200,),
    ) -> dict[str, Any] | list[Any] | None:
        data = None
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "github-forwarders-script",
        }

        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
                status = getattr(resp, "status", 200)
                raw = resp.read().decode("utf-8")

                if status not in expected:
                    snippet = raw[:5000] if raw else ""
                    raise RuntimeError(
                        f"Unexpected HTTP {status} for {method} {url} "
                        f"(expected {expected}): {snippet}"
                    )

                if not raw:
                    return None
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None

            body = None
            try:
                body = e.read().decode("utf-8")
            except Exception:  # noqa: BLE001
                body = None

            msg = f"HTTP {e.code} for {method} {url}"
            if body:
                msg = f"{msg}: {body[:5000]}"
            raise RuntimeError(msg) from e


def iter_git_log_messages(repo_path: Path, rev: str) -> Iterable[str]:
    proc = subprocess.Popen(
        ["git", "-C", str(repo_path), "log", "--format=%B", rev],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        yield line
    _, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(stderr.strip() or "git log failed")


def compute_max_ref_from_git(repo_path: Path, rev: str, cap: int) -> int:
    max_ref = 0
    for line in iter_git_log_messages(repo_path, rev):
        for match in REF_RE.findall(line):
            n = int(match)
            if 1 <= n <= cap and n > max_ref:
                max_ref = n
    return max_ref


def forwarder_marker_token(upstream_repo: Repo, number: int) -> str:
    return f"{upstream_repo.owner}/{upstream_repo.name}#{number}"


def forwarder_issue_title(
    *,
    upstream_repo: Repo,
    number: int,
    upstream_found: bool,
    no_linkify_upstream: bool,
) -> str:
    if no_linkify_upstream:
        suffix = "" if upstream_found else ", upstream missing"
        return f"Forwarder {number} ({upstream_repo.owner}/{upstream_repo.name}{suffix})"

    if upstream_found:
        return f"Forwarder: {upstream_repo.owner}/{upstream_repo.name}#{number}"

    return f"Forwarder (missing upstream): {upstream_repo.owner}/{upstream_repo.name}#{number}"


def forwarder_marker_comment(marker_token: str) -> str:
    return f"<!-- forwarder: {marker_token} -->\n"


def find_forwarder_marker_tokens(body: str) -> list[str]:
    return MARKER_RE.findall(body)


def forwarder_block(
    *,
    upstream_repo: Repo,
    target_repo: Repo,
    number: int,
    canonical_url: str | None,
    no_linkify_upstream: bool,
) -> str:
    marker_token = forwarder_marker_token(upstream_repo, number)

    title_token = f"`{marker_token}`" if no_linkify_upstream else marker_token
    title = f"Forwarder: {title_token}"

    if canonical_url is None:
        canonical_target = "(upstream item not found)"
    else:
        canonical_target = f"`{canonical_url}`" if no_linkify_upstream else canonical_url

    canonical_line = f"**Canonical location:** {canonical_target}"

    return (
        "---\n"
        f"# {title}\n\n"
        f"This item exists in **{target_repo.owner}/{target_repo.name}** to preserve historical `#{number}` references in commit messages.\n\n"
        f"{canonical_line}\n\n"
        "> This is an auto-generated forwarder. Please do not rely on discussion here.\n"
        "---\n\n"
        + forwarder_marker_comment(marker_token)
    )


def prepend_forwarder(
    existing_body: str | None,
    forwarder: str,
    *,
    expected_marker_token: str,
) -> str:
    existing = existing_body or ""

    found = find_forwarder_marker_tokens(existing)
    if found:
        if expected_marker_token in found:
            return existing
        raise ForwarderMarkerMismatchError(expected=expected_marker_token, found=found)

    if not existing.strip():
        return forwarder

    return (
        forwarder
        + "\n---\n\n## Original content\n\n(kept below)\n\n---\n\n"
        + existing
    )


def load_state(state_path: Path) -> dict[str, Any]:
    if not state_path.exists():
        return {}
    return json.loads(state_path.read_text(encoding="utf-8"))


def save_state(state_path: Path, state: dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def repo_issue_url(repo: Repo, number: int) -> str:
    return f"https://api.github.com/repos/{repo.owner}/{repo.name}/issues/{number}"


def ensure_label_exists(client: GitHubClient, repo: Repo, label: str, *, dry_run: bool) -> None:
    url = f"https://api.github.com/repos/{repo.owner}/{repo.name}/labels/{urllib.parse.quote(label)}"
    existing = client.request("GET", url)
    if existing is not None:
        return

    if dry_run:
        return

    create_url = f"https://api.github.com/repos/{repo.owner}/{repo.name}/labels"
    client.request(
        "POST",
        create_url,
        json_body={
            "name": label,
            "color": "ededed",
            "description": "Auto-generated forwarders for commit-history #NNN references",
        },
        expected=(201,),
    )


def add_label(client: GitHubClient, repo: Repo, number: int, label: str, *, dry_run: bool) -> None:
    if dry_run:
        return
    url = f"https://api.github.com/repos/{repo.owner}/{repo.name}/issues/{number}/labels"
    client.request("POST", url, json_body={"labels": [label]}, expected=(200, 201))


def create_issue(
    client: GitHubClient,
    repo: Repo,
    *,
    title: str,
    body: str,
    labels: list[str],
    dry_run: bool,
) -> dict[str, Any]:
    if dry_run:
        return {"number": -1, "title": title, "body": body, "labels": labels}

    url = f"https://api.github.com/repos/{repo.owner}/{repo.name}/issues"
    resp = client.request(
        "POST",
        url,
        json_body={
            "title": title,
            "body": body,
            "labels": labels,
        },
        expected=(201,),
    )
    assert isinstance(resp, dict)
    return resp


def patch_issue_body(client: GitHubClient, repo: Repo, number: int, body: str, *, dry_run: bool) -> None:
    if dry_run:
        return
    url = repo_issue_url(repo, number)
    client.request("PATCH", url, json_body={"body": body}, expected=(200,))


def run_sync(
    *,
    upstream: Repo,
    target: Repo,
    git_repo_path: Path,
    rev: str,
    start: int,
    max_cap: int,
    max_number: int | None,
    dry_run: bool,
    no_linkify_upstream: bool,
    sleep_s: float,
    state_path: Path,
    log_path: Path,
) -> None:
    token = get_auth_token()
    client = GitHubClient(token=token)

    ensure_label_exists(client, target, "forwarder", dry_run=dry_run)

    if max_number is None:
        computed = compute_max_ref_from_git(git_repo_path, rev=rev, cap=max_cap)
        max_number = min(computed, max_cap)

    state = load_state(state_path)
    next_number = int(state.get("next_number", start))
    max_number = int(max_number)

    if next_number < start:
        next_number = start

    if max_number > max_cap:
        max_number = max_cap

    for n in range(next_number, max_number + 1):
        upstream_item = client.request("GET", repo_issue_url(upstream, n))
        canonical_url = None
        upstream_found = False
        upstream_kind = "missing"

        if isinstance(upstream_item, dict):
            upstream_found = True
            canonical_url = str(upstream_item.get("html_url") or "") or None
            upstream_kind = "pull" if "pull_request" in upstream_item else "issue"

        target_item = client.request("GET", repo_issue_url(target, n))
        action = "noop"
        created = False
        updated = False

        if target_item is None:
            title = forwarder_issue_title(
                upstream_repo=upstream,
                number=n,
                upstream_found=upstream_found,
                no_linkify_upstream=no_linkify_upstream,
            )
            body = forwarder_block(
                upstream_repo=upstream,
                target_repo=target,
                number=n,
                canonical_url=canonical_url,
                no_linkify_upstream=no_linkify_upstream,
            )
            resp = create_issue(
                client,
                target,
                title=title,
                body=body,
                labels=["forwarder"],
                dry_run=dry_run,
            )
            created = True
            action = "create"

            if not dry_run:
                created_number = int(resp.get("number"))
                if created_number != n:
                    raise RuntimeError(
                        f"Created wrong issue number: expected {n}, got {created_number}. "
                        "STOPPING to avoid number drift."
                    )
        else:
            assert isinstance(target_item, dict)
            existing_body = target_item.get("body")
            expected_marker = forwarder_marker_token(upstream, n)
            forwarder = forwarder_block(
                upstream_repo=upstream,
                target_repo=target,
                number=n,
                canonical_url=canonical_url,
                no_linkify_upstream=no_linkify_upstream,
            )

            try:
                new_body = prepend_forwarder(
                    existing_body
                    if isinstance(existing_body, str) or existing_body is None
                    else str(existing_body),
                    forwarder,
                    expected_marker_token=expected_marker,
                )
            except ForwarderMarkerMismatchError as exc:
                append_jsonl(
                    log_path,
                    {
                        "ts": utc_now_iso(),
                        "n": n,
                        "action": "error_marker_mismatch",
                        "dry_run": dry_run,
                        "upstream_found": upstream_found,
                        "upstream_kind": upstream_kind,
                        "canonical_url": canonical_url,
                        "expected_marker": exc.expected,
                        "found_markers": exc.found,
                    },
                )
                raise

            if new_body != (existing_body or ""):
                patch_issue_body(client, target, n, new_body, dry_run=dry_run)
                updated = True
                action = "update"

            add_label(client, target, n, "forwarder", dry_run=dry_run)

        record = {
            "ts": utc_now_iso(),
            "n": n,
            "action": action,
            "created": created,
            "updated": updated,
            "dry_run": dry_run,
            "upstream_found": upstream_found,
            "upstream_kind": upstream_kind,
            "canonical_url": canonical_url,
        }
        append_jsonl(log_path, record)

        state = {
            "updated_at": utc_now_iso(),
            "upstream": f"{upstream.owner}/{upstream.name}",
            "target": f"{target.owner}/{target.name}",
            "rev": rev,
            "max_cap": max_cap,
            "max_number": max_number,
            "next_number": n + 1,
        }
        save_state(state_path, state)

        if not dry_run:
            time.sleep(sleep_s)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Create/update dense forwarder issues in a target repo so that bare #NNN commit references resolve. "
            "This script does NOT rewrite git history."
        )
    )

    parser.add_argument("--upstream", type=Repo.parse, required=True)
    parser.add_argument("--target", type=Repo.parse, required=True)
    parser.add_argument("--git-repo-path", type=Path, required=True)
    parser.add_argument("--rev", default="main")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--max", type=int)
    parser.add_argument("--max-cap", type=int, default=14000)
    parser.add_argument("--sleep", type=float, default=1.25)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--no-linkify-upstream",
        action="store_true",
        help=(
            "Render upstream references (owner/repo#N and canonical URL) as code so they do not "
            "autolink/cross-reference on GitHub. Useful for initial staging runs."
        ),
    )
    parser.add_argument("--state-file", type=Path, default=Path(".forwarders/state.json"))
    parser.add_argument("--log-file", type=Path, default=Path(".forwarders/run.jsonl"))

    args = parser.parse_args(argv)

    if args.start < 1:
        print("--start must be >= 1", file=sys.stderr)
        return 2

    if not args.git_repo_path.exists():
        print(f"--git-repo-path does not exist: {args.git_repo_path}", file=sys.stderr)
        return 2

    try:
        run_sync(
            upstream=args.upstream,
            target=args.target,
            git_repo_path=args.git_repo_path,
            rev=args.rev,
            start=args.start,
            max_cap=args.max_cap,
            max_number=args.max,
            dry_run=args.dry_run,
            no_linkify_upstream=args.no_linkify_upstream,
            sleep_s=args.sleep,
            state_path=args.state_file,
            log_path=args.log_file,
        )
    except KeyboardInterrupt:
        print("Interrupted. State file preserved for resume.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
