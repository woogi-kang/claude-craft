#!/usr/bin/env python3
"""orchestrate-worktrees.py — tmux worktree orchestration for parallel Claude Code instances.

Creates git worktrees and tmux panes so multiple Claude instances can work on
independent tasks simultaneously.

Usage:
    python3 scripts/orchestrate-worktrees.py plan.json              # dry-run
    python3 scripts/orchestrate-worktrees.py plan.json --execute    # run
    python3 scripts/orchestrate-worktrees.py plan.json --status     # check
    python3 scripts/orchestrate-worktrees.py plan.json --cleanup    # teardown
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
import unicodedata
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str, fallback_index: int = 0) -> str:
    """Convert text to a filesystem/branch-safe slug.

    ASCII text is lowercased and cleaned.  Non-ASCII (e.g. Korean) is dropped;
    if the result is empty we fall back to ``w{fallback_index}``.
    """
    # Normalize unicode, strip accents
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_only = nfkd.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_only.lower()).strip("-")
    return slug if slug else f"w{fallback_index}"


def run(cmd: list[str], *, check: bool = True, capture: bool = True, **kw) -> subprocess.CompletedProcess:
    """Run a subprocess with sensible defaults."""
    return subprocess.run(
        cmd,
        check=check,
        capture_output=capture,
        text=True,
        **kw,
    )


def git(*args: str, **kw) -> subprocess.CompletedProcess:
    return run(["git", *args], **kw)


def tmux(*args: str, **kw) -> subprocess.CompletedProcess:
    return run(["tmux", *args], **kw)


def ensure_command(name: str) -> None:
    if shutil.which(name) is None:
        die(f"'{name}' is not installed or not in PATH.")


def die(msg: str, code: int = 1) -> None:
    print(f"\033[31mError:\033[0m {msg}", file=sys.stderr)
    sys.exit(code)


def info(msg: str) -> None:
    print(f"\033[36m▸\033[0m {msg}")


def success(msg: str) -> None:
    print(f"\033[32m✓\033[0m {msg}")


def warn(msg: str) -> None:
    print(f"\033[33m!\033[0m {msg}")


# ---------------------------------------------------------------------------
# Plan loading & validation
# ---------------------------------------------------------------------------

def load_plan(path: str) -> dict:
    plan_path = Path(path)
    if not plan_path.is_file():
        die(f"Plan file not found: {path}")
    try:
        with open(plan_path, encoding="utf-8") as f:
            plan = json.load(f)
    except json.JSONDecodeError as exc:
        die(f"Invalid JSON in {path}: {exc}")

    # Required fields
    for key in ("session", "workers"):
        if key not in plan:
            die(f"Plan is missing required key: '{key}'")

    if not isinstance(plan["workers"], list) or len(plan["workers"]) == 0:
        die("Plan must have at least one worker.")

    for i, w in enumerate(plan["workers"]):
        if "name" not in w or "task" not in w:
            die(f"Worker #{i} is missing 'name' or 'task'.")

    # Defaults
    plan.setdefault("base_ref", "HEAD")
    plan.setdefault(
        "launcher",
        "claude --dangerously-skip-permissions -p '{task}' --cwd {worktree}",
    )

    return plan


# ---------------------------------------------------------------------------
# Derived paths / names
# ---------------------------------------------------------------------------

class WorkerInfo:
    """Derived names and paths for a single worker."""

    def __init__(self, worker: dict, index: int, plan: dict, repo_root: Path):
        self.name: str = worker["name"]
        self.task: str = worker["task"]
        self.slug: str = slugify(self.name, fallback_index=index)
        self.session: str = plan["session"]
        self.tmux_session: str = f"orch-{self.session}"
        self.branch: str = f"orch-{self.session}-{self.slug}"
        self.repo_name: str = repo_root.name
        self.worktree_path: Path = repo_root.parent / f"{self.repo_name}-{self.session}-{self.slug}"
        self.coord_dir: Path = repo_root / ".orchestration" / self.session / self.slug
        self.task_file: Path = self.coord_dir / "task.md"
        self.handoff_file: Path = self.coord_dir / "handoff.md"
        self.status_file: Path = self.coord_dir / "status.md"
        self.base_ref: str = plan.get("base_ref", "HEAD")
        self.launcher_template: str = plan.get(
            "launcher",
            "claude --dangerously-skip-permissions -p '{task}' --cwd {worktree}",
        )

    def launcher_cmd(self) -> str:
        """Expand template variables in the launcher string."""
        # Read task from file to avoid shell quoting issues with Korean text
        task_escaped = self.task.replace("'", "'\\''")
        return (
            self.launcher_template
            .replace("{worker}", self.name)
            .replace("{session}", self.session)
            .replace("{worktree}", str(self.worktree_path))
            .replace("{branch}", self.branch)
            .replace("{task}", task_escaped)
            .replace("{task_file}", str(self.task_file))
            .replace("{handoff_file}", str(self.handoff_file))
        )


def build_workers(plan: dict, repo_root: Path) -> list[WorkerInfo]:
    return [
        WorkerInfo(w, i, plan, repo_root)
        for i, w in enumerate(plan["workers"])
    ]


# ---------------------------------------------------------------------------
# Coordination files
# ---------------------------------------------------------------------------

TASK_TEMPLATE = textwrap.dedent("""\
    # Task: {worker_name}

    ## Session
    - Session: {session}
    - Worker: {worker_name}
    - Branch: {branch}
    - Worktree: {worktree_path}

    ## Objective
    {task_description}

    ## Coordination
    - Status: .orchestration/{session}/{worker_slug}/status.md
    - Handoff: .orchestration/{session}/{worker_slug}/handoff.md

    ## Instructions
    - Focus only on your assigned task
    - Do not modify files outside your scope
    - Write a summary of your work when done
""")

HANDOFF_TEMPLATE = textwrap.dedent("""\
    # Handoff: {worker_name}

    ## Summary
    _Pending_

    ## Files Changed
    _Pending_

    ## Tests/Verification
    _Pending_

    ## Follow-up Items
    _Pending_
""")


def write_coordination_files(worker: WorkerInfo) -> None:
    worker.coord_dir.mkdir(parents=True, exist_ok=True)

    worker.task_file.write_text(
        TASK_TEMPLATE.format(
            worker_name=worker.name,
            session=worker.session,
            branch=worker.branch,
            worktree_path=worker.worktree_path,
            task_description=worker.task,
            worker_slug=worker.slug,
        ),
        encoding="utf-8",
    )

    worker.handoff_file.write_text(
        HANDOFF_TEMPLATE.format(worker_name=worker.name),
        encoding="utf-8",
    )

    worker.status_file.write_text("not_started\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Git worktree management
# ---------------------------------------------------------------------------

def create_worktree(worker: WorkerInfo) -> None:
    if worker.worktree_path.exists():
        warn(f"Worktree already exists: {worker.worktree_path}")
        return
    git(
        "worktree", "add",
        "-b", worker.branch,
        str(worker.worktree_path),
        worker.base_ref,
    )
    success(f"Worktree created: {worker.worktree_path}")


def remove_worktree(worker: WorkerInfo) -> None:
    if worker.worktree_path.exists():
        git("worktree", "remove", "--force", str(worker.worktree_path), check=False)
        info(f"Removed worktree: {worker.worktree_path}")
    else:
        info(f"Worktree already gone: {worker.worktree_path}")

    # Delete the branch if it still exists
    result = git("branch", "--list", worker.branch)
    if worker.branch in result.stdout:
        git("branch", "-D", worker.branch, check=False)
        info(f"Deleted branch: {worker.branch}")


# ---------------------------------------------------------------------------
# tmux management
# ---------------------------------------------------------------------------

def tmux_session_exists(name: str) -> bool:
    result = tmux("has-session", "-t", name, check=False)
    return result.returncode == 0


def create_tmux_session(workers: list[WorkerInfo]) -> None:
    session_name = workers[0].tmux_session

    if tmux_session_exists(session_name):
        die(f"tmux session '{session_name}' already exists. Use --cleanup first or pick a different session name.")

    # Create session with the first worker
    first = workers[0]
    first.status_file.write_text("running\n", encoding="utf-8")
    tmux(
        "new-session",
        "-d",                        # detached
        "-s", session_name,          # session name
        "-n", first.slug,            # first window name
    )

    # Send the launch command to the first pane
    cmd = first.launcher_cmd()
    tmux("send-keys", "-t", f"{session_name}:{first.slug}", cmd, "Enter")
    success(f"Started worker: {first.name} ({first.slug})")

    # Create additional windows for remaining workers
    for w in workers[1:]:
        w.status_file.write_text("running\n", encoding="utf-8")
        tmux("new-window", "-t", session_name, "-n", w.slug)
        cmd = w.launcher_cmd()
        tmux("send-keys", "-t", f"{session_name}:{w.slug}", cmd, "Enter")
        success(f"Started worker: {w.name} ({w.slug})")


def kill_tmux_session(session_name: str) -> None:
    if tmux_session_exists(session_name):
        tmux("kill-session", "-t", session_name)
        info(f"Killed tmux session: {session_name}")
    else:
        info(f"tmux session not found: {session_name}")


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

def mode_dry_run(plan: dict, workers: list[WorkerInfo]) -> None:
    """Print what would happen without executing anything."""
    session = plan["session"]
    tmux_name = f"orch-{session}"

    print()
    print(f"{'='*60}")
    print(f"  Orchestration Plan: {session}")
    print(f"{'='*60}")
    print()
    print(f"  tmux session : {tmux_name}")
    print(f"  base ref     : {plan.get('base_ref', 'HEAD')}")
    print(f"  workers      : {len(workers)}")
    print(f"  launcher     : {plan.get('launcher', '(default)')}")
    print()
    print(f"  {'Worker':<16} {'Slug':<16} {'Branch':<32} Worktree")
    print(f"  {'─'*15:<16} {'─'*15:<16} {'─'*31:<32} {'─'*40}")

    for w in workers:
        print(f"  {w.name:<16} {w.slug:<16} {w.branch:<32} {w.worktree_path}")

    print()
    print(f"  Coordination dir: .orchestration/{session}/")
    print()
    print("  Run with --execute to start, or --status / --cleanup for existing sessions.")
    print()


def mode_execute(plan: dict, workers: list[WorkerInfo], repo_root: Path) -> None:
    """Full execution: coordination files, worktrees, tmux session."""
    session = plan["session"]

    info(f"Starting orchestration: {session}")
    print()

    # 1. Coordination files
    info("Creating coordination files...")
    for w in workers:
        write_coordination_files(w)
    success(f"Coordination directory: .orchestration/{session}/")
    print()

    # 2. Git worktrees
    info("Creating git worktrees...")
    for w in workers:
        create_worktree(w)
    # Prune stale worktree references
    git("worktree", "prune")
    print()

    # 3. Copy coordination files into each worktree
    info("Syncing coordination files to worktrees...")
    for w in workers:
        dst = w.worktree_path / ".orchestration" / session / w.slug
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(w.task_file, dst / "task.md")
        shutil.copy2(w.handoff_file, dst / "handoff.md")
        shutil.copy2(w.status_file, dst / "status.md")
    print()

    # 4. tmux
    info("Creating tmux session...")
    create_tmux_session(workers)
    print()

    tmux_name = f"orch-{session}"
    success(f"Orchestration running!")
    print()
    print(f"  Attach: tmux attach -t {tmux_name}")
    print(f"  Status: python3 scripts/orchestrate-worktrees.py {sys.argv[1]} --status")
    print(f"  Cleanup: python3 scripts/orchestrate-worktrees.py {sys.argv[1]} --cleanup")
    print()


def mode_status(plan: dict, workers: list[WorkerInfo]) -> None:
    """Show status of a running session."""
    session = plan["session"]
    tmux_name = f"orch-{session}"

    print()
    print(f"=== Session: {session} ===")
    print()

    # Check tmux session
    session_alive = tmux_session_exists(tmux_name)
    if not session_alive:
        warn(f"tmux session '{tmux_name}' is not running.")
        print()

    # Get pane info from tmux if alive
    pane_map: dict[str, str] = {}
    if session_alive:
        result = tmux(
            "list-windows", "-t", tmux_name,
            "-F", "#{window_name} #{pane_id}",
            check=False,
        )
        if result.returncode == 0:
            for line in result.stdout.strip().splitlines():
                parts = line.split(None, 1)
                if len(parts) == 2:
                    pane_map[parts[0]] = parts[1]

    print(f"  {'Worker':<16} {'Branch':<32} {'Status':<14} Pane")
    print(f"  {'─'*15:<16} {'─'*31:<32} {'─'*13:<14} {'─'*8}")

    for w in workers:
        status = "unknown"
        if w.status_file.exists():
            status = w.status_file.read_text(encoding="utf-8").strip()
        pane = pane_map.get(w.slug, "-")
        print(f"  {w.name:<16} {w.branch:<32} {status:<14} {pane}")

    print()
    print(f"  Coordination: .orchestration/{session}/")
    if session_alive:
        print(f"  Attach: tmux attach -t {tmux_name}")
    print()


def mode_cleanup(plan: dict, workers: list[WorkerInfo], repo_root: Path, *, force: bool = False) -> None:
    """Kill session, remove worktrees and branches, optionally remove coordination dir."""
    session = plan["session"]
    tmux_name = f"orch-{session}"

    info(f"Cleaning up session: {session}")
    print()

    # 1. Kill tmux
    kill_tmux_session(tmux_name)

    # 2. Remove worktrees and branches
    for w in workers:
        remove_worktree(w)
    git("worktree", "prune", check=False)
    print()

    # 3. Coordination directory
    coord_root = repo_root / ".orchestration" / session
    if coord_root.exists():
        if force:
            shutil.rmtree(coord_root)
            info(f"Removed coordination directory: {coord_root}")
        else:
            info(f"Coordination directory kept: {coord_root}")
            info("Use --force to also remove it.")

    # Clean up empty .orchestration parent
    orch_root = repo_root / ".orchestration"
    if orch_root.exists() and not any(orch_root.iterdir()):
        orch_root.rmdir()

    print()
    success("Cleanup complete.")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def get_repo_root() -> Path:
    try:
        result = git("rev-parse", "--show-toplevel")
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        die("Not inside a git repository.")
        return Path()  # unreachable, satisfies type checker


def main() -> None:
    parser = argparse.ArgumentParser(
        description="tmux worktree orchestration for parallel Claude Code instances.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              %(prog)s plan.json              # dry-run — show plan
              %(prog)s plan.json --execute    # create worktrees & tmux session
              %(prog)s plan.json --status     # check running session
              %(prog)s plan.json --cleanup    # teardown everything
        """),
    )
    parser.add_argument("plan", help="Path to plan JSON file")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true", help="Execute the plan (create worktrees & tmux)")
    mode.add_argument("--status", action="store_true", help="Show status of running session")
    mode.add_argument("--cleanup", action="store_true", help="Kill session and remove worktrees")

    parser.add_argument("--force", action="store_true", help="With --cleanup, also remove .orchestration dir")

    args = parser.parse_args()

    # Validate environment
    ensure_command("git")
    repo_root = get_repo_root()
    plan = load_plan(args.plan)
    workers = build_workers(plan, repo_root)

    # tmux is only required for modes that interact with it
    needs_tmux = args.execute or args.status or args.cleanup
    if needs_tmux:
        ensure_command("tmux")

    if args.execute:
        mode_execute(plan, workers, repo_root)
    elif args.status:
        mode_status(plan, workers)
    elif args.cleanup:
        mode_cleanup(plan, workers, repo_root, force=args.force)
    else:
        mode_dry_run(plan, workers)


if __name__ == "__main__":
    main()
