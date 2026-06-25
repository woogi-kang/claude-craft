# Evaluation Result Schema

Eval 결과를 기록할 때 사용하는 표준 스키마. 도메인별 프리셋은 기존 Markdown 리포트를 유지할 수 있지만, model-based grader나 자동 집계가 필요한 결과는 이 구조로도 남긴다.

## 사용 시점

- 평가 기준이 주관적이거나 LLM 판단을 포함할 때
- 여러 축 점수, 감점, 가점, hard fail을 분리해야 할 때
- 평가 입력에 개인정보, 브랜드/학교/회사 인지도, 추측성 맥락처럼 점수에 쓰면 안 되는 신호가 섞여 있을 때
- 이후 benchmark, 회귀 비교, 리뷰 합의에 재사용할 결과가 필요할 때

## 평가 순서

1. Evidence Packet을 먼저 만든다.
2. `excluded_signals`를 분리하고 점수 산정에서 제외한다.
3. 축별 base score를 매긴다.
4. deductions, bonus, hard_failures를 base score와 분리해서 기록한다.
5. hard failure가 있으면 weighted score와 무관하게 `result.status`를 `fail` 또는 `needs_review`로 둔다.

## JSON 구조

```json
{
  "schema": "evaluation-result-v1",
  "rubric": "api-backend|ui-design|content-quality|custom",
  "evidence_packet": {
    "source_coverage": "complete|partial|unknown",
    "included_signals": [
      {
        "id": "E1",
        "source": "file, command, browser flow, screenshot, log, user-provided artifact",
        "summary": "평가에 사용한 관찰 가능한 근거",
        "supports": ["correctness", "security"]
      }
    ],
    "excluded_signals": [
      {
        "signal": "점수에 쓰면 안 되는 정보",
        "reason": "privacy|identity|prestige|unsupported|out_of_scope|unverified"
      }
    ],
    "missing_evidence": [
      "평가에 필요하지만 확인하지 못한 근거"
    ]
  },
  "scores": {
    "axis_name": {
      "score": 0,
      "max": 10,
      "weight": 0.25,
      "evidence": ["E1"],
      "rationale": "점수 근거"
    }
  },
  "adjustments": {
    "bonus": [
      {
        "points": 0,
        "reason": "base score 밖에서 더한 근거",
        "evidence": ["E1"]
      }
    ],
    "deductions": [
      {
        "points": 0,
        "reason": "base score 밖에서 뺀 근거",
        "evidence": ["E1"]
      }
    ],
    "hard_failures": [
      {
        "reason": "점수와 무관하게 실패시키는 조건",
        "evidence": ["E1"]
      }
    ]
  },
  "result": {
    "weighted_score": 0,
    "adjusted_score": 0,
    "status": "pass|fail|needs_review",
    "confidence": 0.0,
    "summary": "한 문단 평가 요약"
  }
}
```

## 작성 규칙

- `included_signals`는 실제로 본 파일, 명령 출력, 브라우저 플로우, 스크린샷, 로그, 사용자 제공 자료만 적는다.
- `excluded_signals`는 평가 대상에 포함되어 있었지만 점수에 쓰지 않은 정보를 기록한다. 기록했다는 이유로 감점하지 않는다.
- 개인정보, 시크릿, API 키, 직접 연락처, 결제 정보는 원문을 복사하지 말고 `redacted` 또는 범주명으로만 남긴다.
- 축별 `evidence`는 `included_signals[].id`를 참조한다. 근거 없는 점수는 `needs_review`로 낮춘다.
- `deductions`와 `bonus`는 축별 base score에 섞지 않는다.
- `hard_failures`는 보안 취약점, 핵심 기능 불능, 사실 오류처럼 합격 기준을 직접 깨는 조건에만 쓴다.
- `confidence`는 근거 완전성 기준이다. 실행 증거가 충분하면 0.8 이상, 일부만 확인했으면 0.5-0.7, 추정이 많으면 0.5 미만으로 둔다.

## 최소 예시

```json
{
  "schema": "evaluation-result-v1",
  "rubric": "api-backend",
  "evidence_packet": {
    "source_coverage": "partial",
    "included_signals": [
      {
        "id": "E1",
        "source": "curl POST /auth/login",
        "summary": "valid credentials return 200 with token fields",
        "supports": ["correctness"]
      }
    ],
    "excluded_signals": [
      {
        "signal": "developer name in commit metadata",
        "reason": "identity"
      }
    ],
    "missing_evidence": ["authorization edge cases were not exercised"]
  },
  "scores": {
    "correctness": {
      "score": 7,
      "max": 10,
      "weight": 0.4,
      "evidence": ["E1"],
      "rationale": "happy path works, but edge cases are incomplete"
    }
  },
  "adjustments": {
    "bonus": [],
    "deductions": [],
    "hard_failures": []
  },
  "result": {
    "weighted_score": 2.8,
    "adjusted_score": 2.8,
    "status": "needs_review",
    "confidence": 0.6,
    "summary": "Login happy path is verified, but coverage is too partial for PASS."
  }
}
```
