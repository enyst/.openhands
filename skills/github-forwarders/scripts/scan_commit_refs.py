#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REF_RE = re.compile(r"#(\d{1,6})\b")


@dataclass(frozen=True)
class ScanResult:
    max_ref: int
    cap: int
    unique_refs: int
    total_matches: int
    top_refs: list[tuple[int, int]]

    def to_dict(self) -> dict[str, object]:
        return {
            "max_ref": self.max_ref,
            "cap": self.cap,
            "unique_refs": self.unique_refs,
            "total_matches": self.total_matches,
            "top_refs": self.top_refs,
        }


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


def scan_refs(repo_path: Path, rev: str, cap: int) -> ScanResult:
    counts: Counter[int] = Counter()

    for line in iter_git_log_messages(repo_path, rev):
        for match in REF_RE.findall(line):
            n = int(match)
            if 1 <= n <= cap:
                counts[n] += 1

    max_ref = max(counts, default=0)
    top_refs = [(n, c) for n, c in counts.most_common(50)]

    return ScanResult(
        max_ref=max_ref,
        cap=cap,
        unique_refs=len(counts),
        total_matches=sum(counts.values()),
        top_refs=top_refs,
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Scan git commit messages for bare #NNN references and report max/reference counts. "
            "This is used to decide how many forwarder issues to create (dense 1..max_ref)."
        )
    )
    parser.add_argument("--repo-path", type=Path, required=True)
    parser.add_argument("--rev", default="main")
    parser.add_argument("--cap", type=int, default=14000)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)

    repo_path: Path = args.repo_path
    if not repo_path.exists():
        print(f"repo path does not exist: {repo_path}", file=sys.stderr)
        return 2

    result = scan_refs(repo_path=repo_path, rev=args.rev, cap=args.cap)
    payload = result.to_dict()

    out_text = json.dumps(payload, indent=2, sort_keys=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(out_text + "\n", encoding="utf-8")
    print(out_text)

    if result.max_ref == 0:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
