# Presentation Quality Gate

PPT, HTML deck, PDF 발표자료를 생성할 때는 최종 응답 전에 이 게이트를 반드시 통과한다. 목적은 장표가 "파일은 만들어졌지만 실제 발표에 쓰기 어려운" 상태로 전달되는 일을 막는 것이다.

## 완료 기준

### 1. 인포그래픽 적합성

- 각 슬라이드는 시각 요소의 역할을 명확히 정한다: `none`, `native-diagram`, `chart`, `generated-image`, `screenshot`, `photo/reference`.
- 흐름, 비교, 단계, 구조, 수치, 의사결정 기준을 설명하는 슬라이드는 긴 bullet 대신 다이어그램, 표, 차트, 타임라인, 프로세스 맵 중 하나를 우선 검토한다.
- 생성형 이미지는 장식용 채우기가 아니라 메시지 이해를 돕는 경우에만 사용한다.
- 생성형 이미지 안에는 의도하지 않은 읽을 수 있는 텍스트, 로고, 워터마크가 없어야 한다.
- 이미지나 인포그래픽을 사용한 경우 `slide`, `purpose`, `asset_path`, `prompt_or_source`, `review_status`를 남긴다.

### 2. 레이아웃 전수 검사

- 최종 파일은 모든 슬라이드/페이지를 이미지로 렌더링한 뒤 전수 확인한다.
- 제목, 본문, 각주, 이미지, 도형, 차트가 화면 밖으로 나가거나 서로 겹치면 실패로 본다.
- 텍스트 박스의 overflow, 잘림, 비정상 축소, 불필요한 여백 부족, 페이지 밖 crop을 확인한다.
- contact sheet를 만들어 전체 흐름과 문제 슬라이드를 한 번에 볼 수 있어야 한다.
- 실패 슬라이드는 수정 후 다시 렌더링하고, 마지막 렌더 결과 기준으로만 전달한다.

### 3. Korean Word Breaking

- 한국어 본문에는 `word-break: break-all`, `overflow-wrap: anywhere`를 기본값으로 쓰지 않는다.
- 웹/HTML 기반 장표는 한국어 텍스트에 `word-break: keep-all`을 우선 적용하고, 필요한 줄바꿈은 문장 단위로 직접 설계한다.
- PPTX 텍스트 박스는 조사, 어미, 단위가 줄 첫머리에 홀로 남지 않도록 문장을 짧게 나누거나 명시적 줄바꿈을 넣는다.
- 제목과 큰 본문은 한 줄에 의미 단위가 유지되는지 확인한다.
- 한국어 설명문은 직역투, AI 번역투, 어색한 현업 비사용어를 별도 패스로 다듬는다. 코드 식별자, 파일명, API 이름은 바꾸지 않는다.

### 4. PDF 동시 생성

- PPTX 또는 HTML deck을 납품할 때는 발표용 PDF도 함께 생성한다.
- PDF 페이지 수는 원본 슬라이드 수와 일치해야 한다.
- PDF도 페이지별 이미지로 렌더링해 contact sheet를 만들고, PPTX/HTML 렌더와 별도로 잘림과 overflow를 확인한다.
- PDF 생성이 실패하면 최종 응답에 실패 사유와 재현 명령을 적고, PPT만 성공한 상태를 완료로 처리하지 않는다.

## 필수 산출물

- 편집 가능한 원본: `.pptx` 또는 HTML deck source
- 발표용 PDF: `.pdf`
- 전수 렌더 이미지: slide/page별 PNG 또는 screenshot
- contact sheet: 전체 슬라이드를 한 번에 확인할 수 있는 이미지
- QA report 또는 manual review: 슬라이드별 PASS/FAIL과 수정 이력
- 이미지 manifest: 생성 이미지나 외부 시각 자료를 사용한 경우

## 권장 검증 순서

1. 콘텐츠 구조와 슬라이드별 메시지를 확정한다.
2. 인포그래픽이 필요한 슬라이드를 표시하고 asset manifest를 만든다.
3. PPTX/HTML을 생성한다.
4. 전체 슬라이드를 렌더링하고 contact sheet를 만든다.
5. 레이아웃, overflow, Korean word breaking을 수정한다.
6. PDF를 생성한다.
7. PDF 전체 페이지를 렌더링하고 contact sheet를 만든다.
8. 최종 QA report에 산출물 경로, 페이지 수, 남은 리스크를 기록한다.

## 검증 명령 예시

```bash
soffice --headless --convert-to pdf --outdir <out>/pdf <deck>.pptx
pdfinfo <out>/pdf/<deck>.pdf
pdftoppm -png -r 150 <out>/pdf/<deck>.pdf <out>/qa_pdf_render/png/slide
```

HTML deck을 사용하는 경우 `future-slide-qa` 또는 동등한 Playwright 기반 렌더 QA를 함께 실행한다. PPTX를 직접 생성하는 경우에도 같은 수준의 전체 슬라이드 이미지 렌더와 contact sheet를 남긴다.
