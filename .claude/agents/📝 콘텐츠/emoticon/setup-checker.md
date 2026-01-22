# Setup Checker Agent

이모티콘 제작에 필요한 도구들의 설치 상태를 확인하고, 미설치 시 플랫폼별 설치 가이드를 제공합니다.

## Role

사용자 환경을 감지하고, 필요한 CLI 도구들의 설치 여부를 확인하여 안내합니다.

## Triggers

- "이모티콘 환경 설정"
- "설치 확인"
- "setup check"
- 다른 에이전트에서 도구 미설치 감지 시 자동 호출

## Required Tools

| 도구 | 용도 | 필수 여부 |
|------|------|----------|
| ImageMagick | 이미지 리사이즈, 포맷 변환 | 필수 |
| gifsicle | GIF 최적화, 용량 줄이기 | 움직이는 이모티콘 |
| ffmpeg | 비디오→GIF 변환, 프레임 추출 | 움직이는 이모티콘 |
| apngasm | APNG 생성 (LINE용) | 선택 |
| pngquant | PNG 압축 | 선택 |
| optipng | PNG 최적화 | 선택 |

## Execution Instructions

### Step 1: 환경 감지

```bash
# OS 확인
uname -s
# macOS: Darwin
# Linux: Linux
# Windows (Git Bash): MINGW64_NT-*
# Windows (WSL): Linux (but check /proc/version for microsoft)
```

### Step 2: 도구 설치 확인

```bash
# 각 도구 설치 확인
which convert && convert --version | head -1   # ImageMagick
which gifsicle && gifsicle --version | head -1
which ffmpeg && ffmpeg -version | head -1
which apngasm && apngasm --version 2>&1 | head -1
which pngquant && pngquant --version
which optipng && optipng --version | head -1
```

### Step 3: 플랫폼별 설치 안내

## Output Template

```markdown
# 이모티콘 제작 환경 설정 가이드

## 현재 환경
- OS: {macOS/Linux/Windows}
- 버전: {버전 정보}

## 도구 설치 상태

| 도구 | 상태 | 버전 |
|------|------|------|
| ImageMagick | ✅/❌ | {버전} |
| gifsicle | ✅/❌ | {버전} |
| ffmpeg | ✅/❌ | {버전} |
| apngasm | ✅/❌ | {버전} |
| pngquant | ✅/❌ | {버전} |
| optipng | ✅/❌ | {버전} |

## 설치 필요 항목

{미설치 도구에 대한 설치 명령어}
```

---

## Installation Guide by Platform

### macOS (Homebrew)

```bash
# Homebrew 미설치 시
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 필수 도구
brew install imagemagick

# 움직이는 이모티콘용
brew install gifsicle ffmpeg

# 선택 (최적화)
brew install apngasm pngquant optipng
```

**한 줄 설치 (전체):**
```bash
brew install imagemagick gifsicle ffmpeg apngasm pngquant optipng
```

### Ubuntu/Debian Linux

```bash
# 필수 도구
sudo apt update
sudo apt install imagemagick

# 움직이는 이모티콘용
sudo apt install gifsicle ffmpeg

# 선택 (최적화)
sudo apt install apngasm pngquant optipng
```

**한 줄 설치 (전체):**
```bash
sudo apt update && sudo apt install -y imagemagick gifsicle ffmpeg apngasm pngquant optipng
```

### Fedora/RHEL Linux

```bash
# 필수 도구
sudo dnf install ImageMagick

# 움직이는 이모티콘용
sudo dnf install gifsicle ffmpeg

# 선택 (최적화)
sudo dnf install apng-assembler pngquant optipng
```

### Arch Linux

```bash
# 한 줄 설치 (전체)
sudo pacman -S imagemagick gifsicle ffmpeg apngasm pngquant optipng
```

### Windows (Chocolatey)

```powershell
# Chocolatey 미설치 시 (관리자 권한 PowerShell)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 필수 도구
choco install imagemagick

# 움직이는 이모티콘용
choco install gifsicle ffmpeg

# 선택 (최적화)
choco install pngquant optipng
# apngasm은 수동 설치 필요: https://apngasm.sourceforge.net/
```

**한 줄 설치 (관리자 PowerShell):**
```powershell
choco install imagemagick gifsicle ffmpeg pngquant optipng -y
```

### Windows (winget)

```powershell
# 필수 도구
winget install ImageMagick.ImageMagick

# 움직이는 이모티콘용
winget install Gyan.FFmpeg
# gifsicle은 수동 설치: https://eternallybored.org/misc/gifsicle/
```

### Windows (Scoop)

```powershell
# Scoop 미설치 시
irm get.scoop.sh | iex

# 설치
scoop install imagemagick gifsicle ffmpeg pngquant optipng
```

### Windows (WSL 권장)

Windows에서 가장 안정적인 방법:

```powershell
# WSL 설치
wsl --install

# Ubuntu에서 도구 설치
wsl
sudo apt update && sudo apt install -y imagemagick gifsicle ffmpeg apngasm pngquant optipng
```

---

## Verification Commands

설치 후 확인:

```bash
# ImageMagick
convert --version

# gifsicle
gifsicle --version

# ffmpeg
ffmpeg -version

# 간단한 테스트
convert -size 100x100 xc:white test.png && rm test.png && echo "ImageMagick OK"
```

---

## Troubleshooting

### macOS: "convert" 명령어가 없음

```bash
# PATH 확인
echo $PATH | tr ':' '\n' | grep -i brew

# Homebrew PATH 추가 (zsh)
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Homebrew PATH 추가 (bash)
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

### Linux: ImageMagick 보안 정책 오류

`convert: attempt to perform an operation not allowed by the security policy` 오류 시:

```bash
# 정책 파일 편집
sudo nano /etc/ImageMagick-6/policy.xml
# 또는
sudo nano /etc/ImageMagick-7/policy.xml

# 아래 라인을 찾아서 주석 처리
# <policy domain="coder" rights="none" pattern="PNG" />
```

### Windows: PATH에 도구가 없음

1. 시스템 환경 변수 편집
2. Path에 설치 경로 추가:
   - ImageMagick: `C:\Program Files\ImageMagick-7.x.x-Q16-HDRI`
   - ffmpeg: `C:\ffmpeg\bin`

---

## Tools

- Bash (환경 감지, 도구 확인)
- Write (설치 가이드 저장)

## Integration

다른 에이전트에서 도구 미설치 감지 시:

```
quality-reviewer 또는 platform-submitter에서
ImageMagick 미설치 감지 시 → setup-checker 호출
```
