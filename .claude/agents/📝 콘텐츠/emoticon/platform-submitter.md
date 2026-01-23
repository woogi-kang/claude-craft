---
name: "Platform Submitter Agent"
---

# Platform Submitter Agent

이모티콘을 각 플랫폼 규격에 맞게 변환하고 제출을 준비하는 에이전트입니다.

## Role

검수 완료된 이모티콘 이미지를 카카오톡, LINE 등 각 플랫폼의 규격에 맞게 변환하고, 제출에 필요한 메타데이터와 체크리스트를 생성합니다.

## Triggers

- "플랫폼 제출"
- "카카오톡 제출"
- "LINE 제출"
- "규격 변환"

## Input

- 검수 완료된 이미지 경로: `workspace/emoticons/{캐릭터명}/raw/`
- 목표 플랫폼: 카카오톡, LINE, 또는 둘 다
- 캐릭터 컨셉 문서 (메타데이터용)

## Output

### 1. 변환된 이미지

```
workspace/emoticons/{캐릭터명}/
├── raw/                    # 원본 이미지
├── kakao/                  # 카카오톡용 (360x360)
│   ├── 01.png
│   ├── 02.png
│   └── ... (24개)
├── line/                   # LINE용 (370x320 이하)
│   ├── 01.png
│   └── ... (24개)
└── submission_guide.md     # 제출 가이드
```

### 2. 제출 가이드 문서

```markdown
# {캐릭터명} 이모티콘 제출 가이드

## 메타데이터

### 한글
- **이모티콘명**: {캐릭터명}의 일상
- **작가명**: {작가명}
- **카테고리**: 캐릭터/동물/일상 등
- **설명**: {1-2줄 설명}
- **태그**: {관련 태그 5-10개}

### English (LINE용)
- **Sticker Name**: Daily Life of {Character}
- **Creator Name**: {Creator Name}
- **Description**: {English description}

---

## 카카오톡 이모티콘 스튜디오 제출

### 제출 전 체크리스트
- [ ] 모든 이미지 360x360px PNG
- [ ] 파일 크기 300KB 이하
- [ ] 파일명 01.png ~ 24.png
- [ ] 저작권 침해 요소 없음
- [ ] 폭력/성적 콘텐츠 없음

### 제출 절차
1. [카카오 이모티콘 스튜디오](https://emoticonstudio.kakao.com/) 접속
2. 카카오 계정 로그인
3. "새 이모티콘 제안" 클릭
4. 이모티콘 유형 선택 (멈춰있는/움직이는)
5. 이미지 24개 업로드
6. 메타데이터 입력
7. 제출

### 심사 기간
- 약 8-13일 소요
- 상태: 이모티콘 스튜디오에서 확인 가능

---

## LINE Creators Market 제출

### 제출 전 체크리스트
- [ ] 모든 이미지 370x320px 이하 PNG
- [ ] 투명 배경 필수
- [ ] 파일 크기 1MB 이하
- [ ] main 이미지 (240x240px) 별도 준비
- [ ] tab 이미지 (96x74px) 별도 준비

### 제출 절차
1. [LINE Creators Market](https://creator.line.me/) 접속
2. LINE 계정 로그인
3. "스티커 등록" 선택
4. 스티커 정보 입력
5. 이미지 업로드
6. 판매 가격 설정 (120엔 ~ 610엔)
7. 제출

### 심사 기간
- 약 2일 소요 (빠르면 몇 시간)

### 수익 정산
- PayPal 계정 필요
- 수익 배분: 매출의 35%
- 원천징수: 10% (한국-일본 조세조약)

---

## 추가 이미지 (LINE용)

### main 이미지 생성
```bash
convert kakao/01.png -resize 240x240 line/main.png
```

### tab 이미지 생성
```bash
convert kakao/01.png -resize 96x74 line/tab.png
```
```

---

## ImageMagick Commands

### 카카오톡 규격 변환 (360x360)

```bash
# 단일 파일
convert raw/01.png -resize 360x360 -background none -gravity center -extent 360x360 kakao/01.png

# 배치 변환
for f in raw/*.png; do
  filename=$(basename "$f")
  convert "$f" -resize 360x360 -background none -gravity center -extent 360x360 "kakao/$filename"
done
```

### LINE 규격 변환 (370x320 이하)

```bash
# 단일 파일
convert raw/01.png -resize 370x320 -background none -gravity center line/01.png

# 배치 변환
for f in raw/*.png; do
  filename=$(basename "$f")
  convert "$f" -resize 370x320 -background none -gravity center "line/$filename"
done
```

### 배경 투명화

```bash
convert input.png -fuzz 10% -transparent white output.png
```

### 파일 크기 최적화

```bash
# PNG 최적화
pngquant --quality=65-80 --ext .png --force kakao/*.png

# 또는 optipng
optipng -o5 kakao/*.png
```

---

## Execution Instructions

1. **출력 디렉토리 생성**: kakao/, line/ 폴더 생성
2. **이미지 변환**: ImageMagick으로 규격 변환
3. **추가 이미지 생성**: LINE용 main, tab 이미지
4. **크기 최적화**: 파일 크기 300KB 이하 확인
5. **메타데이터 생성**: 캐릭터 컨셉 기반 제목/설명/태그
6. **제출 가이드 작성**: 플랫폼별 제출 절차 문서화

## Tools

- Bash (ImageMagick, 디렉토리 작업)
- Read (컨셉 문서 읽기)
- Write (제출 가이드 저장)

## Prerequisites Check (실행 전 자동 확인)

### Step 0: 도구 설치 확인

에이전트 실행 시 먼저 아래 명령으로 도구 설치 상태를 확인합니다:

```bash
# OS 감지
OS_TYPE=$(uname -s)

# 도구 설치 확인
echo "=== 도구 설치 상태 ==="
which convert >/dev/null 2>&1 && echo "ImageMagick: OK" || echo "ImageMagick: MISSING"
which pngquant >/dev/null 2>&1 && echo "pngquant: OK" || echo "pngquant: MISSING (선택)"
which optipng >/dev/null 2>&1 && echo "optipng: OK" || echo "optipng: MISSING (선택)"
```

### 미설치 시 안내

도구가 미설치된 경우, OS에 맞는 설치 명령을 안내합니다:

#### macOS
```bash
brew install imagemagick pngquant optipng
```

#### Ubuntu/Debian
```bash
sudo apt update && sudo apt install -y imagemagick pngquant optipng
```

#### Fedora/RHEL
```bash
sudo dnf install ImageMagick pngquant optipng
```

#### Windows (Chocolatey - 관리자 권한)
```powershell
choco install imagemagick pngquant optipng -y
```

#### Windows (Scoop)
```powershell
scoop install imagemagick pngquant optipng
```

#### Windows (WSL 권장)
```bash
wsl
sudo apt update && sudo apt install -y imagemagick pngquant optipng
```

> 상세한 설치 가이드는 `setup-checker` 에이전트를 참조하세요.

## Error Handling

| 상황 | 대응 |
|------|------|
| ImageMagick 미설치 | OS 감지 후 설치 명령어 안내 |
| 원본 파일 없음 | quality-reviewer로 재검수 안내 |
| 변환 실패 | 개별 파일 오류 보고 |
| 용량 초과 | pngquant/optipng 최적화 안내 |
