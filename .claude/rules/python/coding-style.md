# Python Coding Style

## 포맷팅
- ruff 린터 사용 (Python 3.13 타겟)
- 라인 길이: 100자
- 들여쓰기: 4 spaces

## 패턴
- Type hints 사용 (함수 시그니처)
- dataclass / Pydantic 모델 선호
- async/await 패턴 (FastAPI, Playwright)
- pathlib.Path 사용 (os.path 대신)

## 의존성
- uv 패키지 매니저
- pyproject.toml 기반
- stdlib 우선 (외부 의존성 최소화)
