# Git Workflow

## 커밋
- 사용자가 명시적으로 요청할 때만 커밋
- Conventional Commits 형식: feat/fix/refactor/docs/test/chore
- Co-Authored-By 헤더 포함
- .env, credentials 등 민감 파일 커밋 금지

## 브랜치
- PR은 master 브랜치 기준
- 파괴적 git 명령(force push, reset --hard) 사용 전 확인
- amend 대신 새 커밋 생성 (기본)

## PR
- 제목 70자 이내
- 본문에 Summary + Test plan 포함
