#!/usr/bin/env python3
"""hypatia-git-commit.py — wrap `git commit` with Hypatia's identity.

Per Q-08 (2026-04-22): commits Hypatia authors during save-session use a
distinct identity (`Hypatia <hypatia@local>`) so log readers can tell them
apart from Scholar-authored work. Per Q-decision (2026-05-12): identity is
applied via GIT_AUTHOR_* and GIT_COMMITTER_* env vars in the subprocess,
read from `hypatia.config.yaml`.

Usage (typically invoked by Hypatia in step 6 of the save flow):
    python3 scripts/hypatia-git-commit.py -m "Session save: {session_id}"

All arguments after the script name pass through to `git commit`.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "hypatia.config.yaml"


def load_git_identity() -> dict[str, str]:
    config = yaml.safe_load(CONFIG_PATH.read_text())
    git = config["git"]
    return {
        "GIT_AUTHOR_NAME": git["author_name"],
        "GIT_AUTHOR_EMAIL": git["author_email"],
        "GIT_COMMITTER_NAME": git["committer_name"],
        "GIT_COMMITTER_EMAIL": git["committer_email"],
    }


def main() -> int:
    env = os.environ.copy()
    env.update(load_git_identity())
    result = subprocess.run(
        ["git", "commit", *sys.argv[1:]],
        cwd=REPO_ROOT,
        env=env,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
