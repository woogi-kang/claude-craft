---
name: legal-negotiation-points
description: |
  협상 전략 및 포인트 도출.
  BATNA 분석, 협상 우선순위, Give-and-Take 전략을 수립합니다.
triggers:
  - "협상 전략"
  - "협상 포인트"
  - "BATNA"
  - "협상 준비"
  - "Negotiation"
input:
  - 계약서 텍스트
  - 위험 평가 결과
  - 컨텍스트 문서
output:
  - execution/{project}-negotiation-strategy.md
---

# Negotiation Points Skill

효과적인 계약 협상을 위한 전략과 포인트를 수립합니다.

## BATNA 분석 (Best Alternative To Negotiated Agreement)

### BATNA 프레임워크

```yaml
batna_analysis:
  our_batna:
    alternatives:
      - option: ""           # 대안 1
        feasibility: ""      # 실행 가능성
        outcome: ""          # 예상 결과
      - option: ""           # 대안 2
        feasibility: ""
        outcome: ""

    best_alternative: ""     # 최선의 대안
    reservation_point: ""    # 협상 최저선

  their_batna:
    estimated_alternatives:
      - option: ""
        likelihood: ""
    their_reservation: ""    # 상대방 최저선 추정

  zone_of_possible_agreement:
    our_reservation: ""      # 우리 최저선
    their_reservation: ""    # 상대방 최저선
    overlap: ""              # 합의 가능 영역
```

### BATNA 평가 질문

```
우리의 BATNA:
□ 이 계약이 무산되면 대안이 있는가?
□ 다른 거래처/공급자가 있는가?
□ 내부 수행이 가능한가?
□ 시간적 여유가 있는가?
□ 계약 없이 진행할 수 있는가?

상대방 BATNA:
□ 상대방의 대안은 무엇인가?
□ 우리가 유일한 선택인가?
□ 상대방의 시간 압박은?
□ 상대방의 의사결정권자는?
```

---

## 협상력 평가

### 협상력 요소

```yaml
negotiating_power:
  our_power:
    market_position: ""      # 시장 지위 (강/중/약)
    alternatives: ""         # 대안 보유 (다수/일부/없음)
    time_pressure: ""        # 시간 압박 (낮음/중간/높음)
    information: ""          # 정보 우위 (있음/없음)
    relationship: ""         # 관계 의존도 (낮음/중간/높음)

  their_power:
    market_position: ""
    alternatives: ""
    time_pressure: ""
    information: ""
    relationship: ""

  balance: ""                # 유리/대등/불리
```

### 협상력 매트릭스

```
              상대방 협상력
              낮음    중간    높음
         ┌────────┬────────┬────────┐
    높음 │ 우리   │ 우리   │ 대등   │
    우   │ 우세   │ 유리   │        │
    리   ├────────┼────────┼────────┤
    협 중간│ 우리   │ 대등   │ 상대방 │
    상   │ 유리   │        │ 유리   │
    력   ├────────┼────────┼────────┤
    낮음 │ 대등   │ 상대방 │ 상대방 │
         │        │ 유리   │ 우세   │
         └────────┴────────┴────────┘
```

---

## 협상 목표 설정

### 3단계 목표

```yaml
negotiation_targets:
  ideal:                     # 이상적 목표
    - item: ""
      target: ""
      rationale: ""

  realistic:                 # 현실적 목표
    - item: ""
      target: ""
      rationale: ""

  minimum:                   # 최소 목표 (Walk-away point)
    - item: ""
      target: ""
      rationale: ""
```

### 목표 우선순위

```yaml
priority_matrix:
  must_have:                 # 필수 (포기 불가)
    - item: ""
      reason: ""

  should_have:               # 중요 (강력 협상)
    - item: ""
      reason: ""

  nice_to_have:              # 선호 (양보 가능)
    - item: ""
      reason: ""
```

---

## Give-and-Take 전략

### 양보 가능 항목

```yaml
tradeable_items:
  low_cost_high_value:       # 우리에게 비용↓, 상대방 가치↑
    - item: ""
      our_cost: "낮음"
      their_value: "높음"
      use: "양보 카드"

  high_cost_low_value:       # 우리에게 비용↑, 상대방 가치↓
    - item: ""
      our_cost: "높음"
      their_value: "낮음"
      use: "협상 요구"
```

### 패키지 딜 전략

```yaml
package_deals:
  - give:
      - "{우리 양보 1}"
      - "{우리 양보 2}"
    get:
      - "{획득 목표 1}"
      - "{획득 목표 2}"
    rationale: "{전략적 근거}"

  - give:
      - "{우리 양보 3}"
    get:
      - "{획득 목표 3}"
    rationale: "{전략적 근거}"
```

---

## 조항별 협상 전략

### 손해배상/책임제한

```yaml
liability_negotiation:
  our_position:
    ideal: "직접손해만, 수령금액 1배 상한"
    realistic: "통상손해, 계약금액 2배 상한"
    minimum: "상한 설정 필수"

  arguments:
    - "업계 표준은 계약금액 1-2배 상한"
    - "무제한 책임은 보험 가입 불가"
    - "과도한 리스크로 가격 상승 불가피"

  fallback:
    - "고의/중과실 예외 인정"
    - "특정 위반 항목 예외 인정"
```

### 지적재산권

```yaml
ip_negotiation:
  our_position:
    ideal: "기존 IP 보유, 신규 IP 공동소유"
    realistic: "결과물 양도, 기존 IP + 범용도구 보유"
    minimum: "기존 IP 보유 필수"

  arguments:
    - "기존 IP는 이전 투자 결과물"
    - "범용 도구 제한 시 사업 영위 불가"
    - "공동소유가 양측 이익"

  fallback:
    - "기존 IP 비독점 라이선스 부여"
    - "범용 도구 정의 명확화"
```

### 해지 조건

```yaml
termination_negotiation:
  our_position:
    ideal: "쌍방 동일 해지권, 90일 통지"
    realistic: "쌍방 해지권, 60일 통지"
    minimum: "30일 통지, 시정 기회"

  arguments:
    - "일방적 해지권은 불공정"
    - "투자 회수 기간 필요"
    - "대체 거래처 확보 시간 필요"

  fallback:
    - "즉시 해지 시 손실 보상"
    - "특정 사유에 한해 단축 통지"
```

### 비밀유지

```yaml
confidentiality_negotiation:
  our_position:
    ideal: "3년, 서면 표시 정보만"
    realistic: "5년, 합리적 범위"
    minimum: "영구 비밀유지 거부"

  arguments:
    - "영구 비밀유지는 사업 제약"
    - "업계 표준은 3-5년"
    - "예외 조항 필수"

  fallback:
    - "영업비밀만 장기 유지"
    - "예외 범위 명확화"
```

---

## 협상 전술

### 시작 전술

```yaml
opening_tactics:
  anchoring:
    description: "먼저 높은/낮은 기준점 제시"
    use_when: "협상력 강할 때"
    example: "손해배상 상한 수령금액 50%로 시작"

  bracketing:
    description: "목표의 2배 거리에서 시작"
    use_when: "양보 여지 필요할 때"
    example: "목표 2배 상한 → 상대 반박 → 목표 수렴"
```

### 진행 전술

```yaml
progress_tactics:
  conditional_concession:
    description: "조건부 양보"
    pattern: "~하면 ~하겠다"
    example: "상한을 2배로 하면 기간은 수용"

  package_deal:
    description: "묶음 협상"
    pattern: "A와 B를 함께 논의"
    example: "책임상한 + IP를 패키지로"

  silence:
    description: "침묵 활용"
    use_when: "상대 양보 유도"

  deadline:
    description: "기한 설정"
    use_when: "협상 장기화 시"
```

### 교착 대응

```yaml
deadlock_tactics:
  reframe:
    description: "문제 재정의"
    example: "손해배상 → 보험으로 해결"

  expand_pie:
    description: "새 가치 창출"
    example: "추가 프로젝트 제안"

  third_party:
    description: "제3자 개입"
    example: "전문가 의견 요청"

  break:
    description: "휴식/시간"
    use_when: "감정적 교착"
```

---

## 워크플로우

```
1. 협상 환경 분석
      │
      ├─ BATNA 분석
      ├─ 협상력 평가
      │
      ▼
2. 목표 설정
      │
      ├─ 3단계 목표
      ├─ 우선순위 결정
      │
      ▼
3. 전략 수립
      │
      ├─ Give-and-Take 항목
      ├─ 패키지 딜 구성
      │
      ▼
4. 조항별 전략
      │
      ├─ 포지션 정의
      ├─ 논거 준비
      │
      ▼
5. 전술 선택
      │
      ├─ 시작/진행/교착 전술
      │
      ▼
6. 전략 문서 생성
   → workspace/work-legal/{project}/execution/{project}-negotiation-strategy.md
```

---

## 출력 템플릿

```markdown
# {Project Name} 협상 전략서

## 협상 개요

| 항목 | 내용 |
|------|------|
| 상대방 | {counter_party} |
| 계약 유형 | {contract_type} |
| 예상 계약금액 | {amount} |
| 협상 기한 | {deadline} |
| 우리 역할 | {our_role} |

---

## 1. 협상 환경 분석

### BATNA 분석

#### 우리의 BATNA

| 대안 | 실행가능성 | 예상 결과 |
|------|-----------|----------|
| {alternative_1} | {feasibility} | {outcome} |
| {alternative_2} | {feasibility} | {outcome} |

**최선의 대안:** {best_alternative}
**협상 최저선:** {reservation_point}

#### 상대방 BATNA (추정)

| 대안 | 가능성 | 영향 |
|------|--------|------|
| {their_alt_1} | {likelihood} | {impact} |
| {their_alt_2} | {likelihood} | {impact} |

**추정 최저선:** {their_reservation}

#### 합의 가능 영역 (ZOPA)

```
우리 최저선 ─────────|═══════════════════|───────── 상대 최저선
              우리측 유리      ZOPA      상대측 유리
```

---

### 협상력 평가

| 요소 | 우리 | 상대방 | 우위 |
|------|------|--------|------|
| 시장 지위 | {our} | {their} | {advantage} |
| 대안 보유 | {our} | {their} | {advantage} |
| 시간 압박 | {our} | {their} | {advantage} |
| 정보 우위 | {our} | {their} | {advantage} |
| 관계 의존 | {our} | {their} | {advantage} |
| **종합** | | | **{overall}** |

---

## 2. 협상 목표

### 목표 설정

| 조항 | 이상 목표 | 현실 목표 | 최소 목표 |
|------|----------|----------|----------|
| 손해배상 상한 | 수령금액 1배 | 계약금액 2배 | 상한 설정 |
| IP 귀속 | 공동소유 | 결과물 양도 | 기존IP 보유 |
| 해지 통지 | 90일 | 60일 | 30일 |
| 비밀유지 기간 | 3년 | 5년 | 7년 이내 |

### 우선순위

#### 🔴 Must Have (포기 불가)

| 항목 | 최소 기준 | 근거 |
|------|----------|------|
| {item_1} | {minimum} | {reason} |
| {item_2} | {minimum} | {reason} |

#### 🟠 Should Have (강력 협상)

| 항목 | 목표 | 양보 가능 범위 |
|------|------|---------------|
| {item_3} | {target} | {range} |
| {item_4} | {target} | {range} |

#### 🟢 Nice to Have (양보 가능)

| 항목 | 목표 | 양보 용의 |
|------|------|----------|
| {item_5} | {target} | {willing} |
| {item_6} | {target} | {willing} |

---

## 3. Give-and-Take 전략

### 양보 카드

| 항목 | 우리 비용 | 상대 가치 | 활용 방법 |
|------|----------|----------|----------|
| {give_1} | 낮음 | 높음 | 초기 양보 |
| {give_2} | 중간 | 중간 | 교환 카드 |
| {give_3} | 낮음 | 중간 | 마무리 양보 |

### 요구 항목

| 항목 | 우리 가치 | 상대 비용 | 우선순위 |
|------|----------|----------|----------|
| {get_1} | 높음 | 중간 | 1순위 |
| {get_2} | 높음 | 낮음 | 2순위 |
| {get_3} | 중간 | 낮음 | 3순위 |

### 패키지 딜 시나리오

#### Package A (권장)

| Give | Get |
|------|-----|
| 비밀유지 5년 수용 | 손해배상 상한 확보 |
| 경쟁금지 1년 수용 | IP 공동소유 |

**전략:** 비밀유지/경쟁금지는 실질적 영향 낮음, 핵심 조건 확보

#### Package B (대안)

| Give | Get |
|------|-----|
| 책임상한 2배 수용 | 기존 IP 보유 확보 |
| 해지통지 30일 수용 | 시정기회 확보 |

---

## 4. 조항별 협상 가이드

### 제12조 손해배상

**현재 조항:** 무제한 손해배상

**협상 포지션:**

| 단계 | 포지션 | 논거 |
|------|--------|------|
| 시작 | 수령금액 1배 상한 | 업계 최저 수준 기준 |
| 협상 | 계약금액 2배 상한 | 업계 표준 |
| 최저 | 상한 설정 필수 | 보험 가입 요건 |

**협상 스크립트:**

> "무제한 손해배상은 저희 보험 정책상 수용이 어렵습니다.
> 업계 표준인 계약금액 2배 상한으로 조정을 요청드립니다.
> 이는 저희 가격 경쟁력 유지에도 필수적입니다."

**상대 반박 대응:**

| 상대 주장 | 대응 |
|----------|------|
| "책임 회피" | "상한 내에서 완전 책임, 보험 보완" |
| "업계 관행" | "실제 업계 표준 데이터 제시" |
| "신뢰 문제" | "품질 보증 별도 제안" |

---

### 제8조 지적재산권

**현재 조항:** 전면 IP 양도

**협상 포지션:**

| 단계 | 포지션 | 논거 |
|------|--------|------|
| 시작 | 공동소유 | 공동 투자 |
| 협상 | 결과물만 양도, 기존/범용 보유 | 사업 지속성 |
| 최저 | 기존 IP 보유 필수 | 핵심 자산 보호 |

---

### 제15조 해지

**현재 조항:** 갑만 즉시 해지 가능

**협상 포지션:**

| 단계 | 포지션 | 논거 |
|------|--------|------|
| 시작 | 쌍방 동일, 90일 통지 | 형평성 |
| 협상 | 쌍방 동일, 60일 통지 | 표준 |
| 최저 | 30일 통지, 시정기회 | 최소 보호 |

---

## 5. 협상 전술

### 시작 전술

**선택:** Anchoring

**실행:**
- 첫 제안: 수령금액 50% 상한 (실제 목표의 1/4)
- 근거: 위험 프로파일 분석 결과
- 기대: 2배 상한으로 수렴

### 진행 전술

**주요 전술:**

1. **조건부 양보**
   - "비밀유지 5년을 수용하면, 손해배상 상한 협의 가능"

2. **패키지 딜**
   - 책임/IP/해지를 한 번에 협상

3. **침묵 활용**
   - 핵심 요구 후 상대 반응 대기

### 교착 대응

**시나리오별 대응:**

| 교착 상황 | 대응 전술 |
|----------|----------|
| 손해배상 상한 거부 | 보험 솔루션 제안 |
| IP 양도 고수 | 라이선스백 제안 |
| 시간 압박 | 휴식 요청, 기한 재협의 |

---

## 6. 협상 시나리오

### Best Case (성공)

- 손해배상: 계약금액 2배 상한 ✅
- IP: 기존 IP 보유 + 결과물 양도 ✅
- 해지: 쌍방 60일 통지 ✅
- 비밀유지: 5년 ✅

### Expected Case (표준)

- 손해배상: 계약금액 3배 상한
- IP: 전면 양도, 범용도구 보유
- 해지: 쌍방 30일 통지
- 비밀유지: 5년

### Worst Case (최저선)

- 손해배상: 상한 설정 (금액 협상)
- IP: 기존 IP 보유만 확보
- 해지: 시정기회만 확보
- 비밀유지: 7년 이내

### Walk-Away 조건

다음 중 하나라도 충족 못하면 협상 중단:
- ❌ 손해배상 상한 없음
- ❌ 기존 IP 양도 요구
- ❌ 시정기회 없는 즉시해지

---

## 7. 협상 체크리스트

### 사전 준비

- [ ] BATNA 명확화
- [ ] 권한 범위 확인
- [ ] 의사결정권자 파악
- [ ] 상대방 정보 수집
- [ ] 협상 자료 준비

### 협상 중

- [ ] 의제 순서 합의
- [ ] 기록 담당 지정
- [ ] 감정 관리
- [ ] 양보 추적
- [ ] 시간 관리

### 협상 후

- [ ] 합의 내용 서면화
- [ ] 미결 사항 정리
- [ ] 다음 단계 합의
- [ ] 내부 보고

---

⚠️ 면책: 이 협상 전략은 참고용이며, 실제 협상은 상황에 맞게 조정하세요.
최종 결정은 법률 및 사업 전문가와 상의하세요.
```

## 다음 스킬 연결

협상 전략 수립 후:

1. **수정 제안** → Redline Suggest Skill (협상안 반영)
2. **버전 비교** → Version Compare Skill (협상 결과 추적)
3. **최종 검토** → Final Review Skill (최종 확인)

---

*좋은 협상은 양측 모두 만족하는 합의입니다.*
*협상은 승패가 아닌 가치 창출의 과정입니다.*

⚠️ 면책: 이 전략은 참고용이며, 최종 결정은 전문가와 상의하세요.
