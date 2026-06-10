---
name: brain-sync
description: brain-craft repo를 GBrain PGLite index와 동기화
allowed-tools: ["Bash"]
---

`/Users/woogi/brain-craft`를 GBrain source `brain-craft`와 동기화합니다.

## 절차

1. wrapper로 동기화합니다.
   ```bash
   scripts/brain-memory.sh sync
   ```
2. 상태를 확인합니다.
   ```bash
   scripts/brain-memory.sh status
   ```

wrapper 내부 동작:

```bash
scripts/brain-memory.sh secret-scan
/Users/woogi/.bun/bin/gbrain sync --source brain-craft --repo /Users/woogi/brain-craft --no-embed --no-pull --yes
/Users/woogi/.bun/bin/gbrain extract all --source db
```

커밋되지 않은 변경이 있으면 sync는 중단합니다.

수동으로 상태만 확인할 때:

```bash
cd /Users/woogi/brain-craft && git status --short
```

## 참고

Phase 0에서는 embedding이 비활성화되어 있다. `--no-embed`를 유지한다.
