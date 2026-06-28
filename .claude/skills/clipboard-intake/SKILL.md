---
name: clipboard-intake
description: "Capture clipboard text, terminal logs, screenshots paths, pasted stack traces, and large copied artifacts into a local redacted intake folder for lazy reading. Use when the user says they copied something, has a long log, wants to drop a screenshot/text blob, or asks to inspect clipboard content."
license: MIT
metadata:
  category: "Standalone"
  version: "0.1.0"
  tags: "clipboard, logs, intake, redaction, debugging"
---

# Clipboard Intake

Use this skill when the user wants you to inspect copied text, logs, stack traces, or pasted artifacts without flooding the conversation.

## Capture

On macOS, capture text with:

```bash
mkdir -p "$HOME/.claude-craft/clipboard-drops/$(date +%Y%m%d)"
pbpaste > "$HOME/.claude-craft/clipboard-drops/$(date +%Y%m%d)/drop-$(date +%H%M%S).txt"
```

If the clipboard contains an image or file reference, save the path or ask the user to provide the file path. Do not guess binary clipboard formats.

## Manifest

For each drop, record:

- path
- byte size and line count
- detected kind: log, stack trace, markdown, JSON, shell, unknown
- redaction status
- short preview with secrets removed

Do not print raw secrets. For long files, read focused slices with `rg`, `sed`, or structured parsers.

## Reading Strategy

- Under 20 KB: read directly after redaction check.
- 20 KB to 1 MB: search for errors, timestamps, exception names, request IDs, or user-mentioned terms before reading chunks.
- Over 1 MB: summarize structure first and inspect only focused slices.

## Safety

- Keep drops in `$HOME/.claude-craft/clipboard-drops/`, not the repo.
- Do not commit drops.
- Ask before sending clipboard content to external tools or hosted services.
