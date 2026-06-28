---
name: official-docs-guide
description: "Official documentation lookup route for libraries, SDKs, APIs, frameworks, standards, MCPs, model/tool docs, package versions, and implementation questions where docs may have changed. Use this before relying on memory or third-party tutorials for technical guidance."
license: MIT
metadata:
  category: "Standalone"
  version: "0.1.0"
  tags: "docs, llms-txt, api-docs, sdk, versioning, technical-research"
---

# Official Docs Guide

Use this skill for technical questions where the correct answer depends on current docs, package versions, or provider-specific behavior.

## Source Order

1. **Local truth**
   - Inspect the repository's installed versions: `package.json`, lockfiles, `pyproject.toml`, `requirements.txt`, `pubspec.yaml`, SDK config, generated clients, and existing wrappers.
   - If code already encodes the contract, prefer code over generic docs.

2. **Official docs**
   - Use the vendor's docs domain, source repository, RFC/standard, package registry, or release notes.
   - Look for `llms.txt` or `llms-full.txt` at the docs root.
   - For GitHub-hosted docs, prefer raw markdown and tagged release docs when version matters.

3. **Version match**
   - Match docs to the installed major/minor version when possible.
   - If installed and latest docs differ, say which one you are using and why.

4. **Fallbacks**
   - Use sitemap, search restricted to the official domain, package registry metadata, examples in the official repo, or changelog entries.
   - Use third-party articles only as pointers, never as final authority for API shape.

## Output Contract

For implementation guidance, report:

- package/provider and version used
- official source URL
- exact API or config shape to apply
- drift risk if docs are current but local dependency is older
- verification command or focused test

## When to Pair

- Pair with `web-access-ladder` when official docs are hard to fetch.
- Pair with `context-pack-gate` before sending a docs-derived prompt to an external model or worker.
- Pair with `verification-loop` when the docs change should be proven by tests.
