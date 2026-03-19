#!/usr/bin/env python3
"""orchestrate-dashboard.py — Web dashboard for orchestration sessions.

Zero-dependency web server (stdlib only) that monitors .orchestration/ sessions
and displays real-time DAG status with worker states.

Usage:
    python3 scripts/orchestrate-dashboard.py                    # port 8080
    python3 scripts/orchestrate-dashboard.py --port 3000        # custom port
    python3 scripts/orchestrate-dashboard.py --open             # auto-open browser
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs


# ---------------------------------------------------------------------------
# Helpers (duplicated from orchestrate-worktrees.py to stay standalone)
# ---------------------------------------------------------------------------

KNOWN_STATES = frozenset({"not_started", "waiting", "running", "completed", "failed"})


def get_repo_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def slugify(text: str, fallback_index: int = 0) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_only = nfkd.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_only.lower()).strip("-")
    return slug if slug else f"w{fallback_index}"


def read_status(path: Path) -> str:
    if not path.exists():
        return "unknown"
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return "unknown"
    try:
        data = json.loads(text)
        state = data.get("state", "unknown")
    except (json.JSONDecodeError, AttributeError):
        state = text
    return state if state in KNOWN_STATES else "unknown"


def detect_tmux_panes(session_name: str) -> dict[str, dict]:
    """Return {window_name: {dead: bool, exit_code: int}} from tmux."""
    if not shutil.which("tmux"):
        return {}
    try:
        result = subprocess.run(
            ["tmux", "has-session", "-t", session_name],
            capture_output=True, check=False,
        )
        if result.returncode != 0:
            return {}
        result = subprocess.run(
            ["tmux", "list-panes", "-s", "-t", session_name,
             "-F", "#{window_name} #{pane_dead} #{pane_dead_status}"],
            capture_output=True, text=True, check=False,
        )
        panes = {}
        if result.returncode == 0:
            for line in result.stdout.strip().splitlines():
                parts = line.split(None, 2)
                if len(parts) >= 2:
                    name = parts[0]
                    dead = parts[1] == "1"
                    exit_code = int(parts[2]) if len(parts) == 3 else 0
                    panes[name] = {"dead": dead, "exit_code": exit_code}
        return panes
    except FileNotFoundError:
        return {}


# ---------------------------------------------------------------------------
# Session data collection
# ---------------------------------------------------------------------------

REPO_ROOT = get_repo_root()
ORCH_DIR = REPO_ROOT / ".orchestration"


def list_sessions() -> list[dict]:
    """List all orchestration sessions."""
    sessions = []
    if not ORCH_DIR.exists():
        return sessions
    for d in sorted(ORCH_DIR.iterdir()):
        if not d.is_dir():
            continue
        plan_file = d / "plan.json"
        if not plan_file.exists():
            # Try to find plan.json by scanning for worker dirs
            worker_dirs = [x for x in d.iterdir() if x.is_dir()]
            sessions.append({
                "name": d.name,
                "has_plan": False,
                "worker_count": len(worker_dirs),
            })
        else:
            try:
                plan = json.loads(plan_file.read_text(encoding="utf-8"))
                sessions.append({
                    "name": d.name,
                    "has_plan": True,
                    "worker_count": len(plan.get("workers", [])),
                })
            except (json.JSONDecodeError, KeyError):
                sessions.append({"name": d.name, "has_plan": False, "worker_count": 0})
    return sessions


def get_session_detail(session_name: str) -> dict | None:
    """Get detailed status for a session."""
    session_dir = ORCH_DIR / session_name
    if not session_dir.exists():
        return None

    # Try plan.json first
    plan_file = session_dir / "plan.json"
    if not plan_file.exists():
        return {"session": session_name, "error": "plan.json not found"}

    try:
        plan = json.loads(plan_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"session": session_name, "error": "Invalid plan.json"}

    tmux_name = f"orch-{session_name}"
    panes = detect_tmux_panes(tmux_name)

    workers = []
    for i, w in enumerate(plan.get("workers", [])):
        name = w["name"]
        slug = slugify(name, fallback_index=i)
        status_file = session_dir / slug / "status.md"
        state = read_status(status_file)

        # Infer from tmux if available
        if state == "running" and slug in panes and panes[slug]["dead"]:
            exit_code = panes[slug]["exit_code"]
            state = "completed" if exit_code == 0 else "failed"

        depends_on = w.get("depends_on", [])
        workers.append({
            "name": name,
            "slug": slug,
            "state": state,
            "depends_on": depends_on,
            "task": w.get("task", "")[:200],  # truncate for display
            "in_tmux": slug in panes,
            "pane_dead": panes.get(slug, {}).get("dead", False),
        })

    # Compute layers for DAG visualization
    name_to_deps = {w["name"]: w["depends_on"] for w in workers}
    layers = compute_layers(workers, name_to_deps)

    # Summary
    state_counts: dict[str, int] = {}
    for w in workers:
        state_counts[w["state"]] = state_counts.get(w["state"], 0) + 1

    tmux_alive = bool(panes)

    return {
        "session": session_name,
        "tmux_alive": tmux_alive,
        "tmux_session": tmux_name,
        "workers": workers,
        "layers": layers,
        "summary": state_counts,
        "total": len(workers),
    }


def compute_layers(workers: list[dict], name_to_deps: dict) -> list[list[str]]:
    """Compute topological layers for DAG visualization (cycle-safe)."""
    depths: dict[str, int] = {}
    VISITING = -1

    def depth_of(name: str) -> int:
        if name in depths:
            return 0 if depths[name] == VISITING else depths[name]  # cycle → break
        depths[name] = VISITING
        deps = name_to_deps.get(name, [])
        if not deps:
            depths[name] = 0
        else:
            depths[name] = 1 + max(depth_of(d) for d in deps)
        return depths[name]

    for w in workers:
        depth_of(w["name"])

    max_depth = max(depths.values(), default=0)
    layers: list[list[str]] = [[] for _ in range(max_depth + 1)]
    for name, d in depths.items():
        layers[d].append(name)
    return layers


# ---------------------------------------------------------------------------
# HTML Template
# ---------------------------------------------------------------------------

HTML_PAGE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Craft Orchestra Dashboard</title>
<style>
:root {
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #e6edf3; --text-dim: #8b949e; --text-bright: #ffffff;
  --green: #3fb950; --cyan: #58a6ff; --yellow: #d29922;
  --red: #f85149; --purple: #bc8cff; --gray: #484f58;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, 'SF Mono', monospace; background: var(--bg); color: var(--text); min-height: 100vh; }
.header { padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 16px; }
.header h1 { font-size: 18px; font-weight: 600; }
.header .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
.container { max-width: 1200px; margin: 0 auto; padding: 24px; }
.sessions { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.session-btn { padding: 6px 14px; border: 1px solid var(--border); border-radius: 6px; background: var(--surface); color: var(--text); cursor: pointer; font-size: 13px; transition: all 0.2s; }
.session-btn:hover { border-color: var(--cyan); }
.session-btn.active { border-color: var(--cyan); background: #1f2937; color: var(--cyan); }
.summary { display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }
.stat { padding: 12px 16px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; min-width: 100px; }
.stat .label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; }
.stat .value { font-size: 24px; font-weight: 700; margin-top: 4px; }
.dag { display: flex; gap: 24px; align-items: flex-start; overflow-x: auto; padding: 16px 0; }
.layer { display: flex; flex-direction: column; gap: 12px; min-width: 200px; }
.layer-label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.worker-card { padding: 14px 16px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; border-left: 3px solid var(--gray); transition: all 0.3s; }
.worker-card.completed { border-left-color: var(--green); }
.worker-card.running { border-left-color: var(--cyan); animation: glow 2s infinite; }
.worker-card.waiting { border-left-color: var(--yellow); }
.worker-card.failed { border-left-color: var(--red); }
.worker-card.not_started { border-left-color: var(--gray); }
@keyframes glow { 0%,100% { box-shadow: 0 0 0 0 rgba(88,166,255,0); } 50% { box-shadow: 0 0 8px 0 rgba(88,166,255,0.15); } }
.worker-name { font-size: 14px; font-weight: 600; }
.worker-state { font-size: 12px; margin-top: 4px; padding: 2px 8px; border-radius: 10px; display: inline-block; }
.worker-state.completed { background: rgba(63,185,80,0.15); color: var(--green); }
.worker-state.running { background: rgba(88,166,255,0.15); color: var(--cyan); }
.worker-state.waiting { background: rgba(210,153,34,0.15); color: var(--yellow); }
.worker-state.failed { background: rgba(248,81,73,0.15); color: var(--red); }
.worker-state.not_started { background: rgba(72,79,88,0.15); color: var(--gray); }
.worker-state.unknown { background: rgba(188,140,255,0.15); color: var(--purple); }
.worker-deps { font-size: 11px; color: var(--text-dim); margin-top: 6px; }
.worker-task { font-size: 11px; color: var(--text-dim); margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 180px; }
.arrows { display: flex; gap: 4px; margin-top: 6px; }
.arrow { font-size: 10px; color: var(--text-dim); }
.tmux-info { font-size: 12px; color: var(--text-dim); margin-bottom: 16px; padding: 8px 12px; background: var(--surface); border-radius: 6px; border: 1px solid var(--border); }
.tmux-info .alive { color: var(--green); } .tmux-info .dead { color: var(--red); }
.empty { text-align: center; color: var(--text-dim); padding: 80px 24px; }
.empty h2 { font-size: 16px; margin-bottom: 8px; }
.footer { text-align: center; color: var(--text-dim); font-size: 11px; padding: 24px; border-top: 1px solid var(--border); margin-top: 48px; }
</style>
</head>
<body>
<div class="header">
  <div class="dot" id="pulse-dot"></div>
  <h1>Craft Orchestra</h1>
  <span style="color:var(--text-dim);font-size:12px" id="last-update"></span>
</div>
<div class="container">
  <div class="sessions" id="sessions"></div>
  <div id="content">
    <div class="empty"><h2>Select a session</h2><p>Or waiting for sessions to appear...</p></div>
  </div>
</div>
<div class="footer">Polling every 2s &middot; Craft Orchestra Dashboard</div>
<script>
let currentSession = null;
let pollTimer = null;

async function fetchJSON(url) {
  const r = await fetch(url);
  return r.json();
}

async function loadSessions() {
  const sessions = await fetchJSON('/api/sessions');
  const el = document.getElementById('sessions');
  if (!sessions.length) { el.innerHTML = '<span style="color:var(--text-dim)">No sessions found in .orchestration/</span>'; return; }
  el.innerHTML = sessions.map(s =>
    `<button class="session-btn ${s.name===currentSession?'active':''}" onclick="selectSession('${s.name}')">${s.name} <span style="color:var(--text-dim)">(${s.worker_count})</span></button>`
  ).join('');
  if (!currentSession && sessions.length) selectSession(sessions[0].name);
}

function selectSession(name) {
  currentSession = name;
  loadSessions();
  loadDetail();
}

async function loadDetail() {
  if (!currentSession) return;
  const d = await fetchJSON('/api/sessions/' + currentSession);
  if (d.error) { document.getElementById('content').innerHTML = `<div class="empty"><h2>${d.error}</h2></div>`; return; }
  let html = '';
  // tmux info
  html += `<div class="tmux-info">tmux: <span class="${d.tmux_alive?'alive':'dead'}">${d.tmux_alive?'alive':'not running'}</span> &middot; ${d.tmux_session}</div>`;
  // summary
  html += '<div class="summary">';
  html += `<div class="stat"><div class="label">Total</div><div class="value">${d.total}</div></div>`;
  for (const [state, count] of Object.entries(d.summary || {})) {
    const color = {completed:'var(--green)',running:'var(--cyan)',waiting:'var(--yellow)',failed:'var(--red)',not_started:'var(--gray)',unknown:'var(--purple)'}[state]||'var(--text)';
    html += `<div class="stat"><div class="label">${state}</div><div class="value" style="color:${color}">${count}</div></div>`;
  }
  html += '</div>';
  // DAG layers
  html += '<div class="dag">';
  const workerMap = {};
  d.workers.forEach(w => workerMap[w.name] = w);
  d.layers.forEach((layer, i) => {
    html += `<div class="layer"><div class="layer-label">Layer ${i}</div>`;
    layer.forEach(name => {
      const w = workerMap[name]; if (!w) return;
      const deps = w.depends_on.length ? `← ${w.depends_on.join(', ')}` : 'root';
      const task = w.task.replace(/</g,'&lt;').replace(/\\n/g,' ').substring(0,80);
      html += `<div class="worker-card ${w.state}">
        <div class="worker-name">${w.name}</div>
        <span class="worker-state ${w.state}">${w.state}</span>
        <div class="worker-deps">${deps}</div>
        <div class="worker-task" title="${task}">${task}</div>
      </div>`;
    });
    html += '</div>';
  });
  html += '</div>';
  document.getElementById('content').innerHTML = html;
  document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
}

async function poll() {
  try { await loadSessions(); if (currentSession) await loadDetail(); } catch(e) {}
}

poll();
pollTimer = setInterval(poll, 2000);
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# HTTP Server
# ---------------------------------------------------------------------------

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "":
            self._html(HTML_PAGE)
        elif path == "/api/sessions":
            self._json(list_sessions())
        elif path.startswith("/api/sessions/"):
            session_name = path.split("/api/sessions/", 1)[1].strip("/")
            # Path traversal protection
            if not re.fullmatch(r'[a-zA-Z0-9_-]+', session_name):
                self._json({"error": "Invalid session name"}, 400)
                return
            data = get_session_detail(session_name)
            if data:
                self._json(data)
            else:
                self._json({"error": "Session not found"}, 404)
        else:
            self._json({"error": "Not found"}, 404)

    def _html(self, content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _json(self, data, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        # No CORS header needed — same-origin requests from embedded HTML
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress default request logging
        pass


def main():
    parser = argparse.ArgumentParser(description="Web dashboard for orchestration sessions.")
    parser.add_argument("--port", type=int, default=8080, help="Server port (default: 8080)")
    parser.add_argument("--bind", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--open", action="store_true", help="Auto-open browser")
    args = parser.parse_args()

    server = HTTPServer((args.bind, args.port), DashboardHandler)
    url = f"http://localhost:{args.port}"

    print(f"\033[36m▸\033[0m Craft Orchestra Dashboard")
    print(f"  URL:  {url}")
    print(f"  Root: {REPO_ROOT}")
    print(f"  Orch: {ORCH_DIR}")
    print()
    print(f"  Press Ctrl+C to stop")
    print()

    if args.open:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[36m▸\033[0m Dashboard stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
