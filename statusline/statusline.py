#!/usr/bin/env python3
"""
Claude Code Status Line - Cost Tracking Script
Displays session cost, daily cost, context usage, and hourly rate in the status line.

Output format:
🤖 Opus 4.5 | 🌿 master | 🟢 [████░░░░░░] 42% | 🔥 $5.23/hr | 💰 $28.03 today
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Cost tracking file location
TRACKING_FILE = Path.home() / '.claude' / 'cost_tracking.json'

# Model pricing (per 1M tokens)
PRICING = {
    'claude-opus-4-5-20251101': {
        'input': 15.00,
        'output': 75.00,
        'cache_write': 18.75,
        'cache_read': 1.50
    },
    'claude-sonnet-4-5-20250514': {
        'input': 3.00,
        'output': 15.00,
        'cache_write': 3.75,
        'cache_read': 0.30
    },
    'claude-haiku-4-5-20251101': {
        'input': 0.25,
        'output': 1.25,
        'cache_write': 0.30,
        'cache_read': 0.03
    },
    # Aliases for partial matching
    'opus': {
        'input': 15.00,
        'output': 75.00,
        'cache_write': 18.75,
        'cache_read': 1.50
    },
    'sonnet': {
        'input': 3.00,
        'output': 15.00,
        'cache_write': 3.75,
        'cache_read': 0.30
    },
    'haiku': {
        'input': 0.25,
        'output': 1.25,
        'cache_write': 0.30,
        'cache_read': 0.03
    },
}


def get_pricing(model_id: str) -> dict:
    """Get pricing for a model, with fallback to Sonnet."""
    model_lower = model_id.lower()

    # Exact match
    if model_lower in PRICING:
        return PRICING[model_lower]

    # Partial match
    if 'opus' in model_lower:
        return PRICING['opus']
    elif 'haiku' in model_lower:
        return PRICING['haiku']
    else:
        return PRICING['sonnet']  # Default


def load_tracking_data() -> dict:
    """Load cost tracking data from file."""
    default_data = {
        'sessions': {},
        'daily': {},
        'current_block': None
    }

    if not TRACKING_FILE.exists():
        return default_data

    try:
        with open(TRACKING_FILE, 'r') as f:
            data = json.load(f)

        # Migrate old format (list -> dict for sessions)
        for date_key, daily_entry in data.get('daily', {}).items():
            sessions = daily_entry.get('sessions', {})
            if isinstance(sessions, list):
                new_sessions = {}
                for sid in sessions:
                    if sid in data.get('sessions', {}):
                        new_sessions[sid] = data['sessions'][sid].get('total_cost', 0.0)
                daily_entry['sessions'] = new_sessions

        return data
    except (json.JSONDecodeError, IOError):
        return default_data


def save_tracking_data(data: dict):
    """Save cost tracking data to file."""
    try:
        with open(TRACKING_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    except IOError:
        pass


def calculate_cost(context_window, model_id: str) -> float:
    """Calculate session cost from token usage."""
    prices = get_pricing(model_id or 'sonnet')

    if not isinstance(context_window, dict):
        return 0.0

    # Cumulative tokens
    input_tokens = context_window.get('total_input_tokens', 0) or 0
    output_tokens = context_window.get('total_output_tokens', 0) or 0

    # Cache tokens (from current_usage)
    current_usage = context_window.get('current_usage') or {}
    cache_creation = current_usage.get('cache_creation_input_tokens', 0) or 0
    cache_read = current_usage.get('cache_read_input_tokens', 0) or 0

    return (
        (input_tokens / 1_000_000) * prices['input'] +
        (output_tokens / 1_000_000) * prices['output'] +
        (cache_creation / 1_000_000) * prices['cache_write'] +
        (cache_read / 1_000_000) * prices['cache_read']
    )


def get_model_display(model) -> str:
    """Get display name for model."""
    if not isinstance(model, dict):
        return "Claude"

    model_id = (model.get('id') or '').lower()
    display_name = model.get('display_name') or 'Claude'

    if 'opus' in model_id or 'Opus' in display_name:
        return "Opus 4.5"
    elif 'haiku' in model_id or 'Haiku' in display_name:
        return "Haiku 4.5"
    elif 'sonnet' in model_id or 'Sonnet' in display_name:
        return "Sonnet 4.5"
    else:
        return display_name if display_name != 'Claude' else "Claude"


def get_git_branch() -> str | None:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def get_context_progress(context_window: dict, max_context: int = 200_000) -> str:
    """Generate context usage progress bar."""
    if not isinstance(context_window, dict):
        return "📊 [░░░░░░░░░░] 0%"

    # Calculate total tokens used
    input_tokens = context_window.get('total_input_tokens', 0) or 0
    output_tokens = context_window.get('total_output_tokens', 0) or 0
    total_used = input_tokens + output_tokens

    # Get max context from data or use default
    max_ctx = context_window.get('max_tokens', max_context) or max_context

    # Calculate percentage
    percent = min(100, (total_used / max_ctx) * 100)

    # Generate progress bar (10 chars)
    filled = int(percent / 10)
    bar = "█" * filled + "░" * (10 - filled)

    # Color indicator based on usage
    if percent >= 80:
        icon = "🔴"
    elif percent >= 60:
        icon = "🟡"
    else:
        icon = "🟢"

    return f"{icon} [{bar}] {percent:.0f}%"


def main():
    try:
        # 1. Read JSON from stdin
        input_data = json.load(sys.stdin)

        # 2. Extract basic info (with None checks)
        model = input_data.get('model') or {}
        session_id = input_data.get('session_id') or 'default'
        context_window = input_data.get('context_window') or {}

        model_id = model.get('id') or 'sonnet'
        model_display = get_model_display(model)

        # 3. Load tracking data
        tracking_data = load_tracking_data()
        now = datetime.now()
        today_str = now.strftime('%Y-%m-%d')

        # 4. Calculate session cost
        session_cost = calculate_cost(context_window, model_id)

        # 5. Update session data
        if session_id not in tracking_data['sessions']:
            tracking_data['sessions'][session_id] = {
                'start_time': now.isoformat(),
                'date': today_str,
                'total_cost': 0.0,
                'last_update': now.isoformat()
            }

        session_data = tracking_data['sessions'][session_id]
        session_data['total_cost'] = session_cost
        session_data['last_update'] = now.isoformat()

        # 6. Update daily data
        if today_str not in tracking_data['daily']:
            tracking_data['daily'][today_str] = {
                'sessions': {},
                'total': 0.0
            }

        daily_data = tracking_data['daily'][today_str]
        daily_data['sessions'][session_id] = session_cost
        today_cost = sum(daily_data['sessions'].values())
        daily_data['total'] = today_cost

        # 7. Calculate session elapsed time for hourly rate
        session_start_str = session_data.get('start_time', now.isoformat())
        try:
            session_start = datetime.fromisoformat(session_start_str)
        except (ValueError, TypeError):
            session_start = now

        elapsed = now - session_start
        elapsed_minutes = elapsed.total_seconds() / 60
        elapsed_hours = elapsed.total_seconds() / 3600

        # 8. Calculate hourly rate (only if 5+ minutes elapsed)
        if elapsed_minutes >= 5 and elapsed_hours > 0:
            hourly_rate = session_cost / elapsed_hours
            rate_str = f"🔥 ${hourly_rate:.2f}/hr"
        else:
            rate_str = f"⏱️ ~{int(elapsed_minutes)}m"

        # 9. Save data
        save_tracking_data(tracking_data)

        # 10. Get git branch
        git_branch = get_git_branch()
        branch_str = f" | 🌿 {git_branch}" if git_branch else ""

        # 11. Get context usage progress
        context_str = get_context_progress(context_window)

        # 12. Output status line
        status = f"🤖 {model_display}{branch_str} | {context_str} | {rate_str} | 💰 ${today_cost:.2f} today"
        print(status)

    except Exception as e:
        # Fallback output on error
        print(f"🤖 Claude | ⚠️ Error: {str(e)[:30]}")


if __name__ == '__main__':
    main()
