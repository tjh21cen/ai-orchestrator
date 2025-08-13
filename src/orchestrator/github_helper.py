from __future__ import annotations
import os
from pathlib import Path
from typing import Tuple
from git import Repo, GitCommandError
from github import Github

def _owner_repo_from_url(url: str) -> Tuple[str, str]:
    """
    Accept HTTPS or SSH GitHub remote URLs and return (owner, repo) without .git.
    """
    s = url.strip().replace(".git", "")
    if s.startswith("git@github.com:"):
        s = s.split("git@github.com:")[1]
    elif "github.com/" in s:
        s = s.split("github.com/")[1]
    owner, repo = s.split("/", 1)
    return owner, repo

def ensure_branch_and_push(local_repo: Path, work_branch: str, base_branch: str | None = None) -> tuple[str, str, str]:
    """
    Checkout base, create/switch to work_branch, push to origin.
    Returns (owner, repo, default_base_branch_used).
    """
    repo = Repo(str(local_repo))
    assert not repo.bare, "Local repository appears to be bare."

    origin = repo.remotes.origin
    origin.fetch()

    # Determine base branch if not supplied (prefers 'main' then 'master', else current)
    candidates = ["main", "master", repo.active_branch.name]
    base = base_branch or next((b for b in candidates if b in [h.name.replace("origin/", "") for h in origin.refs]), candidates[-1])

    # Checkout & update base
    repo.git.checkout(base)
    try:
        repo.git.pull("origin", base)
    except GitCommandError:
        pass  # ok if up-to-date

    # Create or switch to work branch
    try:
        repo.git.checkout("-b", work_branch)
    except GitCommandError:
        repo.git.checkout(work_branch)

    # Push work branch
    origin.push(refspec=f"{work_branch}:{work_branch}")

    owner, name = _owner_repo_from_url(origin.url)
    return owner, name, base

def open_pr(owner: str, repo: str, head_branch: str, base_branch: str, title: str, body: str) -> str:
    """
    Open a pull request using GITHUB_TOKEN. Returns PR URL.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is not set. Put it in your ai-orchestrator/.env file.")
    gh = Github(token)
    r = gh.get_repo(f"{owner}/{repo}")
    pr = r.create_pull(title=title, body=body, head=head_branch, base=base_branch)
    return pr.html_url
