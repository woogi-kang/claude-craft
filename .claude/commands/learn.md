---
name: learn
description: 현재 세션에서 재사용 가능한 패턴을 추출하여 스킬로 저장
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "AskUserQuestion"]
---

$ARGUMENTS

현재 세션에서 발견된 패턴을 스킬로 저장합니다.

## 절차

### 1. 패턴 식별
세션을 분석하여 다음 유형의 패턴을 찾습니다:
- 에러 해결 패턴 (문제 → 원인 → 해결)
- 디버깅 기법
- 워크어라운드
- 프로젝트 고유 패턴
- 반복되는 워크플로우

### 2. 품질 게이트 (중복 체크)
저장 전 반드시 확인:
- `.claude/skills/` 에서 유사 스킬 존재 여부 Grep
- `.claude/memory/MEMORY.md` 에서 중복 확인
- `CLAUDE.md` 규칙과 겹치는지 확인

### 3. 판정
각 패턴에 대해 하나를 선택:
- **Save**: 새 스킬로 저장
- **Improve**: 기존 스킬에 내용 추가
- **Absorb**: 기존 스킬/메모리에 흡수 (별도 파일 불필요)
- **Drop**: 일회성이라 저장 불필요

### 4. 저장
판정이 Save인 패턴을 `.claude/skills/learned/` 에 저장:

파일명: `{pattern-name}/SKILL.md`

```yaml
---
name: {pattern-name}
description: |
  {한 줄 설명}
metadata:
  category: "learned"
  version: "1.0.0"
  source: "session-learning"
  learned_date: "{YYYY-MM-DD}"
---

# {Pattern Name}

## 문제
{어떤 상황에서 발생하는지}

## 해결
{해결 방법}

## 예시
{구체적 코드/명령 예시}

## 적용 시점
{언제 이 패턴을 사용해야 하는지}
```

### 5. 사용자 확인
생성된 스킬 목록과 내용을 보여주고 확인받기.

---

## EXECUTION DIRECTIVE

1. 인자를 확인합니다:
   - 인자가 없으면: 세션 전체를 분석하여 모든 재사용 가능한 패턴 추출
   - 인자가 있으면: 해당 주제/키워드에 관련된 패턴만 추출

2. 패턴 식별 후, 품질 게이트를 통과시킵니다:
   ```bash
   # 유사 스킬 검색
   find .claude/skills/ -name "SKILL.md" -exec grep -l "{pattern-keyword}" {} \;
   ```

3. 각 패턴에 대해 판정(Save/Improve/Absorb/Drop)을 내립니다.

4. 판정 결과를 사용자에게 표로 보여줍니다:
   ```
   | 패턴 | 판정 | 사유 |
   |------|------|------|
   | {name} | Save | 새로운 패턴 |
   | {name} | Drop | 일회성 |
   ```

5. AskUserQuestion으로 확인:
   - Question: "위 판정대로 스킬을 저장할까요?"
   - Options:
     - Label: "저장", Description: "판정대로 스킬을 저장합니다"
     - Label: "수정", Description: "판정을 수정하겠습니다"
     - Label: "취소", Description: "저장하지 않습니다"

6. 확인 후 Save 판정 패턴을 `.claude/skills/learned/{pattern-name}/SKILL.md` 에 저장합니다.

7. Improve 판정 패턴은 기존 스킬 파일에 내용을 추가합니다.

8. 저장 완료 후 요약을 출력합니다:
   ```
   ## 학습 완료
   - 저장: {N}개 스킬
   - 개선: {N}개 스킬
   - 흡수: {N}개
   - 드롭: {N}개
   ```

---

## 사용 예시

```
/learn                    # 세션 전체에서 패턴 추출
/learn auth workaround    # 특정 주제 패턴만 추출
/learn debugging          # 디버깅 관련 패턴 추출
```

---

Version: 1.0.0
Last Updated: 2026-03-16
Core: Session pattern extraction and skill creation
