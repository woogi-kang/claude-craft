#!/usr/bin/env python3
"""MoAI Rank Session Hook (Global)

This hook submits Claude Code session token usage to the MoAI Rank service.
It is installed globally at ~/.claude/hooks/moai/ and runs for all projects.

Opt-out: Configure ~/.moai/rank/config.yaml to exclude specific projects:
    rank:
      enabled: true
      exclude_projects:
        - "/path/to/private-project"
        - "*/confidential/*"
"""

import json
import sys

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return

        session_data = json.loads(input_data)

        # Lazy import to avoid startup delay
        from moai_adk.rank.hook import is_project_excluded, submit_session_hook

        # Check if this project is excluded
        project_path = session_data.get("projectPath") or session_data.get("cwd")
        if is_project_excluded(project_path):
            return  # Silently skip excluded projects

        result = submit_session_hook(session_data)

        if result["success"]:
            print("Session submitted to MoAI Rank", file=sys.stderr)
        elif result["message"] != "Not registered with MoAI Rank":
            print(f"MoAI Rank: {result['message']}", file=sys.stderr)

    except json.JSONDecodeError:
        pass
    except ImportError:
        # moai-adk not installed, silently skip
        pass
    except Exception as e:
        print(f"MoAI Rank hook error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
