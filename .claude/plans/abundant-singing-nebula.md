# AI 캐릭터 이모티콘 사업 시스템 설계 계획

> **결정 사항**
> - 캐릭터 스타일: 귀여운 SD(2-3등신)
> - 구현 방식: 전용 에이전트 구성 (Option A)
> - 메인 AI 도구: **Leonardo.ai** (게임/캐릭터 특화, 일관성 우수)

## 1. 사업 구조 분석

### 1.1 플랫폼별 수익 구조

| 플랫폼 | 수익 배분 | 심사 기간 | 특징 |
|--------|----------|----------|------|
| **카카오톡** | 약 30-35% (추정) | 8-13일 | 구독 모델(이모티콘 플러스) 250만 구독자, 시장규모 1.2조원 |
| **LINE** | 35% (매출×0.7×0.5) | 약 2일 | PayPal 필요, 원천징수 10%(조세조약) |

### 1.2 제작 규격

- **카카오톡**: 360×360px, PNG/GIF, 24개 세트
- **LINE**: PNG, 짝수 사이즈, 72dpi 이상, RGB

---

## 2. AI 캐릭터 일관성 유지 기술 스택 (2026년 1월 최신)

### 2.1 2026년 최신 도구 비교

| 도구 | 일관성 | SD 캐릭터 적합도 | 장점 | 단점 |
|------|--------|-----------------|------|------|
| **Hunyuan Image 3.0** | ★★★★★ | ★★★★★ | 캐릭터/애니메이션 일관성 1위 | 중국 서비스 |
| **FLUX.2 Max** | ★★★★★ | ★★★★☆ | 참조 이미지 10개, 오픈웨이트 | 유료 API |
| **Midjourney v7** | ★★★★☆ | ★★★★☆ | --cref 기능, 최고 품질 | 월 구독 |
| **Leonardo.ai** | ★★★★★ | ★★★★★ | 게임/캐릭터 특화, 일관성 우수 | 유료 |
| **나노바나나/씨드림** | ★★★★★ | ★★★★★ | 아시안 캐릭터 강점, 일관성 탁월 | 신규 서비스 |
| **OpenArt.ai Bulk Create** | ★★★★☆ | ★★★★☆ | 여러 각도 한번에 생성 | 유료 |
| **ComfyUI + LoRA** | ★★★★★ | ★★★★★ | 완전 커스텀, 무료, 로컬 | 학습 곡선 |

### 2.2 선택된 도구 조합 (SD 캐릭터용)

**Primary**: Leonardo.ai (캐릭터 컨셉, 이모티콘 생성, 일관성 유지)
**Secondary**: ComfyUI + LoRA (대량 생산 필요시, 완전 제어)
**Backup**: Midjourney v7 --cref (빠른 변형, 고품질 필요시)

### 2.3 권장 파이프라인

```
[Phase 1: 캐릭터 설계]
    ├─ 컨셉 정의 (성격, 색상 팔레트, 비율)
    ├─ 레퍼런스 이미지 15-30장 생성
    └─ LoRA 트레이닝 (Network Rank: 32, Alpha: 16)

[Phase 2: 캐릭터 시트 생성]
    ├─ 다양한 각도 (정면, 측면, 3/4)
    ├─ 다양한 표정 (기쁨, 슬픔, 화남, 놀람 등)
    └─ 다양한 포즈 (앉기, 서기, 점프 등)

[Phase 3: 이모티콘 생성]
    ├─ ComfyUI 워크플로우로 배치 생성
    ├─ 배경 제거 및 규격 맞춤
    └─ 품질 검수 및 수정

[Phase 4: 플랫폼 제출]
    ├─ 플랫폼별 규격 변환
    ├─ 메타데이터 작성
    └─ 심사 제출
```

### 2.3 LoRA 트레이닝 권장 설정

```yaml
training_config:
  network_rank: 32
  network_alpha: 16
  learning_rate: 1e-4
  epochs: 12
  image_repeats: 15
  batch_size: 1
  expected_loss: 0.05-0.10
```

---

## 3. 전용 에이전트 시스템 설계 (Option A 선택)

### 3.1 중요: 에이전트 역할 범위

> **Claude Code 에이전트의 한계**: 에이전트는 이미지를 직접 생성할 수 없습니다.
> 에이전트는 **가이드 제공, 프롬프트 생성, 품질 검수, 문서화**를 담당하고,
> **실제 이미지 생성은 사용자가 Leonardo.ai 등 외부 도구에서 직접 수행**합니다.

### 3.2 실제 워크플로우 (사용자 + 에이전트 협업)

```
[사용자] "고양이 캐릭터 이모티콘 만들고 싶어"
    ↓
[concept-designer 에이전트]
    → 캐릭터 컨셉 문서 생성
    → Leonardo.ai용 프롬프트 24개 생성
    ↓
[사용자] Leonardo.ai에서 프롬프트로 이미지 생성
    ↓
[사용자] 생성된 이미지를 프로젝트 폴더에 저장
    ↓
[quality-reviewer 에이전트]
    → 이미지 검수 (규격, 일관성 체크)
    → 수정 필요 항목 피드백
    ↓
[사용자] 피드백 반영하여 이미지 수정/재생성
    ↓
[platform-submitter 에이전트]
    → 플랫폼별 규격 변환 (ImageMagick)
    → 제출 체크리스트 및 메타데이터 생성
```

### 3.3 에이전트 아키텍처

```
.claude/agents/emoticon/
├── emoticon-orchestrator.md   # 워크플로우 가이드 및 에이전트 호출
├── concept-designer.md        # 컨셉 기획 + 프롬프트 생성
├── prompt-engineer.md         # AI 도구별 최적화 프롬프트 생성
├── quality-reviewer.md        # 이미지 품질 검수 (파일 분석)
└── platform-submitter.md      # 규격 변환 + 제출 준비
```

### 3.4 각 에이전트 역할 상세

#### emoticon-orchestrator (오케스트레이터)
```yaml
역할: 전체 워크플로우 가이드 및 에이전트 호출
트리거: "이모티콘 만들어줘", "캐릭터 생성", "스티커 제작"
워크플로우:
  1. concept-designer 호출 → 컨셉 확정 + 프롬프트 생성
  2. [사용자 작업] → Leonardo.ai에서 이미지 생성
  3. quality-reviewer 호출 → 품질 검수
  4. [사용자 작업] → 피드백 반영
  5. platform-submitter 호출 → 제출 준비
도구: Task (에이전트 호출)
```

#### concept-designer (컨셉 디자이너)
```yaml
역할: 캐릭터 컨셉 기획 및 AI 프롬프트 생성
입력: 사용자 아이디어 (텍스트 또는 레퍼런스 이미지 경로)
출력:
  - 캐릭터 프로필 문서 (이름, 성격, 배경 스토리)
  - 시각적 DNA (색상 팔레트 HEX, 비율, 특징)
  - 24개 이모티콘 표정/포즈 목록
  - Leonardo.ai용 프롬프트 24개 (복사해서 바로 사용 가능)
도구: WebSearch, Read, Write
```

#### prompt-engineer (프롬프트 엔지니어)
```yaml
역할: AI 도구별 최적화 프롬프트 생성
지원 도구:
  - Leonardo.ai (기본)
  - Midjourney v7 (--cref, --sref 포함)
  - FLUX.2 (참조 이미지 설정 포함)
입력: 캐릭터 시각적 DNA, 표정/포즈 목록
출력: 도구별 최적화된 프롬프트 세트
도구: Read, Write
```

#### quality-reviewer (품질 검수자)
```yaml
역할: 생성된 이미지 품질 검수 (파일 분석)
체크리스트:
  - 규격 준수 (360x360px, PNG/GIF) - 파일 메타데이터 확인
  - 파일 크기 적정성
  - 파일명 규칙 준수
  - (시각적 일관성은 사용자가 직접 확인)
입력: 이미지 파일 경로 (workspace/emoticons/)
출력: 검수 리포트, 규격 미달 항목 목록
도구: Read (이미지 메타데이터), Bash (file, identify 명령)
```

#### platform-submitter (플랫폼 제출자)
```yaml
역할: 플랫폼별 규격 변환 및 제출 준비
지원 플랫폼:
  - 카카오톡 이모티콘 스튜디오
  - LINE Creators Market
기능:
  - 규격 변환 (ImageMagick: 리사이즈, 포맷 변환, 배경 제거)
  - 메타데이터 생성 (제목, 설명, 태그 제안)
  - 제출 체크리스트 생성
입력: 검수 완료된 이미지 폴더 경로
출력:
  - 변환된 이미지 (kakao/, line/ 폴더)
  - 제출 가이드 문서
도구: Bash (ImageMagick), Write
```

### 3.5 MCP 서버 연동 (선택사항 - 향후 확장)

```yaml
# .mcp.json에 추가
mcp-comfyui:
  description: ComfyUI API 연동
  tools:
    - generate_image      # 이미지 생성
    - run_workflow        # 워크플로우 실행
    - train_lora          # LoRA 트레이닝
    - batch_generate      # 배치 생성
```

---

## 4. 구현 로드맵

### Phase 1: 에이전트 기반 구축
- [ ] `.claude/agents/emoticon/` 디렉토리 생성
- [ ] emoticon-orchestrator.md 작성 (메인 에이전트)
- [ ] concept-designer.md 작성 (컨셉 기획)
- [ ] CLAUDE.md에 에이전트 등록

### Phase 2: 이미지 생성 파이프라인
- [ ] image-generator.md 작성
- [ ] AI 도구 API 연동 테스트 (Leonardo.ai 또는 FLUX.2)
- [ ] consistency-keeper.md 작성
- [ ] 캐릭터 시트 생성 워크플로우 구축

### Phase 3: 품질 관리 & 제출 시스템
- [ ] quality-reviewer.md 작성
- [ ] 품질 검수 체크리스트 정의
- [ ] platform-submitter.md 작성
- [ ] 플랫폼별 규격 변환 스크립트 (ImageMagick)

### Phase 4: 통합 테스트 & 첫 제작
- [ ] 전체 워크플로우 통합 테스트
- [ ] 첫 캐릭터 컨셉 기획 및 생성
- [ ] 24개 이모티콘 세트 제작
- [ ] 카카오톡 이모티콘 스튜디오 제출

### Phase 5: 최적화 (선택)
- [ ] ComfyUI MCP 서버 구축 (로컬 생성용)
- [ ] LoRA 트레이닝 자동화
- [ ] 배치 생성 워크플로우 최적화

---

## 5. 핵심 기술 요소

### 5.1 캐릭터 일관성 유지 기법

1. **LoRA 트레이닝**: 15-30장의 고품질 이미지로 캐릭터 임베딩
2. **시드 고정**: `--seed` 파라미터로 변동 최소화
3. **캐릭터 DNA 프롬프트**: 상세한 외형 설명 재사용
4. **IPAdapter 가중치**: 0.7 정도로 70% 일관성 유지
5. **OpenPose**: 포즈 안정성 확보

### 5.2 스타일 일관성 요소

```
색상 팔레트:
  - Primary: #XXXXXX
  - Secondary: #XXXXXX
  - Accent: #XXXXXX

선 두께: 일정하게 유지 (예: 3px)
명암 비율: 하이라이트 20%, 미드톤 60%, 섀도우 20%
비율: SD 캐릭터의 경우 2-3등신 유지
```

---

## 6. 예상 비용 및 ROI

### 6.1 Leonardo.ai 비용 (메인 도구)

| 플랜 | 월 비용 | 토큰 | 특징 |
|------|--------|------|------|
| **Free** | 무료 | 150/일 | 테스트용, 대기시간 5-20분 |
| **Apprentice** | $12 (연 $10) | 8,500/월 | 상업적 사용 가능 |
| **Artisan** | $30 (연 $24) | 25,000/월 | Relaxed Generation 포함 |
| **Maestro** | $60 (연 $48) | 60,000/월 | 최고 우선순위 |

> **권장**: Artisan 플랜 (월 $24-30) - 이모티콘 24개 세트 제작에 충분

### 6.2 기타 비용 (선택)
- GPU (로컬 ComfyUI): RTX 3060+ 보유시 무료, 미보유시 클라우드 월 10-30만원
- Midjourney: 월 $10-30
- ComfyUI: 무료 (오픈소스)

### 6.3 예상 수익
- 카카오톡 이모티콘 1개 세트: 월 10-100만원 (평균)
- 누적 매출 1억원 이상 이모티콘: 2,885개 존재
- 10억원 이상: 146개
- 100억원 이상: 17개

---

## 7. 검증 방법

### 7.1 에이전트 단위 테스트

```bash
# 1. 컨셉 디자이너 테스트
claude "concept-designer 에이전트로 귀여운 고양이 캐릭터 컨셉 기획해줘"
# 예상 출력: 캐릭터 프로필 + 색상 팔레트 + 24개 프롬프트

# 2. 프롬프트 엔지니어 테스트
claude "prompt-engineer 에이전트로 Leonardo.ai용 프롬프트 최적화해줘"
# 예상 출력: 도구별 최적화 프롬프트

# 3. 품질 검수자 테스트 (이미지 파일 필요)
claude "quality-reviewer 에이전트로 workspace/emoticons/ 폴더 검수해줘"
# 예상 출력: 규격 검수 리포트

# 4. 플랫폼 제출자 테스트
claude "platform-submitter 에이전트로 카카오톡 제출 준비해줘"
# 예상 출력: 변환된 이미지 + 제출 가이드
```

### 7.2 통합 워크플로우 테스트

```bash
# 전체 워크플로우 (오케스트레이터)
claude "귀여운 토끼 캐릭터 이모티콘 24개 만들고 싶어"
```

**예상 흐름**:
1. concept-designer가 컨셉 + 프롬프트 생성
2. 사용자에게 "Leonardo.ai에서 이미지를 생성하세요" 안내
3. 사용자가 이미지 저장 후 검수 요청
4. quality-reviewer가 파일 검수
5. platform-submitter가 규격 변환 및 제출 준비

### 7.3 품질 체크리스트 (사용자 확인용)
- [ ] 캐릭터 일관성: 모든 이모티콘에서 동일한 얼굴/색상/비율
- [ ] 규격 준수: 360x360px, PNG 포맷, 투명 배경
- [ ] 표현력: 24개 감정이 명확히 구분됨
- [ ] 플랫폼 가이드라인: 폭력/성적/저작권 침해 콘텐츠 없음
- [ ] 파일명 규칙: 01.png ~ 24.png 순서대로

### 7.4 성공 기준
- [ ] Phase 1: 에이전트 4개 작성 완료 및 개별 테스트 통과
- [ ] Phase 2: 통합 워크플로우 테스트 완료
- [ ] Phase 3: 첫 캐릭터 컨셉 기획 → 프롬프트 24개 생성
- [ ] Phase 4: Leonardo.ai에서 이모티콘 24개 생성 (사용자 작업)
- [ ] Phase 5: 카카오톡 이모티콘 스튜디오 심사 제출
- [ ] Phase 6: 첫 이모티콘 승인 획득

---

## 8. 참고 자료

### 카카오톡 이모티콘
- [카카오 이모티콘 스튜디오](https://emoticonstudio.kakao.com/)
- [카카오 이모티콘 스튜디오 전면 개편 (2025.11)](https://www.kakaocorp.com/page/detail/11821)
- [카톡 이모티콘 출시 14주년 - 머니투데이](https://www.mt.co.kr/tech/2025/05/22/2025052214360496713)
- [이모티콘 등록 프로세스 - 이모티팡](https://creator.emotipang.com/blog/kakaotalk-emoticon-process)

### LINE 스티커
- [LINE Creators Market](https://creator.line.me/ko/)
- [LINE 스티커 가이드라인](https://creator.line.me/ko/guideline/sticker/)

### 2026년 최신 AI 이미지 생성 도구
- [Best AI Image Generators 2026 - WaveSpeedAI](https://wavespeed.ai/blog/posts/best-ai-image-generators-2026/)
- [Top 10 AI Image Generation Models January 2026 - ThePromptBuddy](https://www.thepromptbuddy.com/prompts/top-10-ai-image-generation-models-dominating-january-2026)
- [Best AI Image Tools 2026 - Jim MacLeod](https://jimmacleod.medium.com/the-best-ai-image-tools-for-2026-compared-and-evaluated-4dee99b4b565)
- [이미지 생성 AI 추천 2026 - 캐럿](https://carat.im/blog/image-generation-ai-recommendation)

### AI 캐릭터 일관성 기법
- [Character Consistency Guide - Human Academy](https://www.humanacademy.ai/en/blog/consistency-character-image-video-ai)
- [Anime Character Consistency Guide 2025 - Apatero](https://apatero.com/blog/anime-character-consistency-complete-guide-2025)
- [LoRA Training Best Practices - Apatero](https://apatero.com/blog/lora-training-best-practices-flux-stable-diffusion-2025)
- [AI Character Sticker Pack Tutorial - Lovart](https://www.lovart.ai/blog/ai-character-sticker-pack)
- [OpenArt.ai Bulk Create - GPTers](https://www.gpters.org/marketing/post/create-images-character-angle-HmwgElQVxyTWgEU)

### FLUX.2 & 최신 모델
- [FLUX.2 - Black Forest Labs](https://bfl.ai/)
- [FLUX.2 on NVIDIA RTX](https://blogs.nvidia.com/blog/rtx-ai-garage-flux-2-comfyui/)
- [Hunyuan Image 3.0 - 캐릭터 일관성 1위](https://www.bentoml.com/blog/a-guide-to-open-source-image-generation-models)
- [Leonardo.ai - 게임/캐릭터 특화](https://leonardo.ai/)

### ComfyUI & LoRA
- [ComfyUI Realtime LoRA - GitHub](https://github.com/shootthesound/comfyUI-Realtime-Lora)
- [ComfyUI FLUX LoRA Training - RunComfy](https://www.runcomfy.com/comfyui-workflows/comfyui-flux-lora-training-detailed-guides)
- [Flux Consistent Characters Workflow - RunComfy](https://www.runcomfy.com/comfyui-workflows/flux-consistent-characters-input-image)
