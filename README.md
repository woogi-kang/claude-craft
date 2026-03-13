# Claude Craft

Claude Code용 커스텀 자산 저장소입니다. 현재는 `moai` 코어 오케스트레이션을 제거하고, 도메인 에이전트/스킬과 커맨드, 경량 `statusline`만 유지합니다.

## 포함 항목

- `.claude/agents/` 도메인 에이전트
- `.claude/skills/` 도메인 스킬
- `.claude/commands/` 커스텀 커맨드
- `.claude/hooks/` 일반 훅 스크립트
- `.claude/statusline.py` 상태줄

## 제거된 항목

- `.moai/` 설정 및 산출물
- `.claude/agents/moai/`
- `.claude/skills/moai*`
- `.claude/hooks/moai/`
- `.claude/rules/moai/`
- `.claude/output-styles/moai/`

## 설치

```bash
git clone https://github.com/woogi-kang/claude-craft.git ~/.claude-craft
cd ~/.claude-craft
./scripts/install.sh
```

설치 스크립트는 `~/.claude` 아래에 `agents`, `skills`, `hooks`, `commands`, `statusline.py`를 설치합니다. `~/.claude/settings.json`이 없으면 기본 `statusLine` 설정만 생성합니다.

## 제거

```bash
rm -rf ~/.claude/agents ~/.claude/skills ~/.claude/hooks ~/.claude/commands
rm -f ~/.claude/statusline.py
```
