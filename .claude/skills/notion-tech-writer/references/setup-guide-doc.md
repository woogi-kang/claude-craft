# Setup Guide Template

## Structure

```markdown
# [프로젝트명] Development Environment Setup

| 속성 | 값 |
|------|-----|
| 🏷️ 태그 | Setup, Onboarding, DevEnv |
| 👤 담당자 | @name |
| 📅 상태 | 배포됨 |
| 📆 최종수정 | YYYY-MM-DD |
| ⏱️ 예상 소요 시간 | 30분 - 1시간 |

## Prerequisites

### 필수 요구사항

| 항목 | 최소 버전 | 권장 버전 | 확인 명령어 |
|------|----------|----------|------------|
| OS | macOS 12+ / Ubuntu 22.04+ / Windows 11 | Latest | - |
| Git | 2.30+ | 2.40+ | `git --version` |
| Node.js | 18.x | 20.x LTS | `node -v` |
| Flutter | 3.19+ | 3.22+ | `flutter --version` |

### 선택 요구사항

| 항목 | 용도 | 필요 상황 |
|------|------|----------|
| Docker | 로컬 DB/서비스 | 백엔드 개발 시 |
| Android Studio | Android 에뮬레이터 | 모바일 개발 시 |
| Xcode | iOS 시뮬레이터 | macOS + iOS 개발 시 |

## Quick Start

💡 **5분 빠른 시작** - 이미 환경이 갖춰진 경우

```bash
# 1. 저장소 클론
git clone https://github.com/org/repo.git
cd repo

# 2. 의존성 설치
flutter pub get

# 3. 환경변수 설정
cp .env.example .env

# 4. 실행
flutter run
```

✅ `http://localhost:3000` 접속 시 앱 화면이 보이면 성공

---

## Step-by-Step Setup

### Step 1: Git 설정

```bash
# Git 설치 확인
git --version

# 사용자 정보 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
```

▶️ SSH 키 설정 (선택)
   ```bash
   # SSH 키 생성
   ssh-keygen -t ed25519 -C "your.email@company.com"
   
   # 공개키 복사
   cat ~/.ssh/id_ed25519.pub
   # → GitHub Settings > SSH Keys에 추가
   ```

### Step 2: Flutter 설치

#### macOS

```bash
# Homebrew로 설치
brew install flutter

# 또는 공식 설치
# https://docs.flutter.dev/get-started/install/macos
```

#### Windows

```powershell
# Chocolatey로 설치
choco install flutter

# 또는 공식 설치
# https://docs.flutter.dev/get-started/install/windows
```

#### Linux

```bash
# Snap으로 설치
sudo snap install flutter --classic
```

**설치 확인**:
```bash
flutter doctor
```

⚠️ `flutter doctor`에서 모든 항목이 ✓ 표시되어야 합니다.

▶️ flutter doctor 문제 해결
   | 문제 | 해결 방법 |
   |------|----------|
   | Android toolchain 오류 | `flutter doctor --android-licenses` |
   | Xcode 오류 | `sudo xcode-select --switch /Applications/Xcode.app` |
   | VS Code 확장 없음 | VS Code에서 Flutter 확장 설치 |

### Step 3: 프로젝트 클론

```bash
# HTTPS (권장)
git clone https://github.com/org/repo.git

# SSH
git clone git@github.com:org/repo.git

cd repo
```

### Step 4: 의존성 설치

```bash
# Flutter 패키지
flutter pub get

# 코드 생성 (필요시)
flutter pub run build_runner build --delete-conflicting-outputs
```

💡 `build_runner`는 Freezed, JSON Serializable 등 코드 생성에 필요합니다.

### Step 5: 환경변수 설정

```bash
# 템플릿 복사
cp .env.example .env

# 편집
nano .env  # 또는 선호하는 에디터
```

**필수 환경변수**:

| 변수 | 설명 | 예시 |
|------|------|------|
| `API_BASE_URL` | API 서버 주소 | `https://api-dev.example.com` |
| `API_KEY` | API 인증 키 | Slack #dev-secrets 참조 |

🚨 `.env` 파일은 절대 Git에 커밋하지 마십시오!

▶️ 환경변수 발급 방법
   1. Slack `#dev-secrets` 채널 참조
   2. 또는 @admin에게 요청
   3. 1Password "Dev Secrets" vault 참조

### Step 6: 로컬 서비스 실행 (선택)

```bash
# Docker로 로컬 DB 실행
docker-compose up -d

# 상태 확인
docker-compose ps
```

### Step 7: 앱 실행

```bash
# 디바이스 목록 확인
flutter devices

# 실행
flutter run

# 특정 디바이스 지정
flutter run -d chrome
flutter run -d "iPhone 15 Pro"
```

✅ **성공 확인**: 앱이 정상적으로 실행되고 로그인 화면 표시

## IDE Setup

### VS Code (권장)

**필수 확장**:
- Flutter
- Dart
- Error Lens

**권장 확장**:
- GitLens
- Thunder Client
- TODO Highlight

**설정** (`.vscode/settings.json`):
```json
{
  "dart.flutterSdkPath": "~/.flutter",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  }
}
```

### Android Studio

**필수 플러그인**:
- Flutter
- Dart

## Verification Checklist

설정 완료 후 확인:

- [ ] `flutter doctor` - 모든 항목 ✓
- [ ] `flutter run` - 앱 정상 실행
- [ ] 로그인 - 테스트 계정으로 로그인 성공
- [ ] API 호출 - 데이터 정상 로드
- [ ] Hot Reload - 코드 변경 시 즉시 반영

## Troubleshooting

### "CocoaPods not installed" (macOS)

```bash
sudo gem install cocoapods
cd ios && pod install
```

### "Android SDK not found"

```bash
flutter config --android-sdk /path/to/android/sdk
```

### "Port 3000 already in use"

```bash
# 프로세스 확인
lsof -i :3000

# 종료
kill -9 <PID>
```

▶️ 더 많은 문제 해결
   [트러블슈팅 가이드 링크]

## Next Steps

설정 완료 후:

1. 📖 [코드 컨벤션](link) 읽기
2. 🔀 [Git 워크플로우](link) 확인
3. 🎫 첫 번째 이슈 할당받기
4. 💬 Slack `#dev-general` 인사하기

## Support

문제 발생 시:
- Slack: `#dev-help`
- 담당자: @onboarding-buddy

---
📝 **유지보수 노트**
- Flutter/도구 버전 업그레이드 시 업데이트
- 환경변수 변경 시 업데이트
- 분기별 링크 유효성 검증
```

## Key Elements

1. **Prerequisites 테이블**: 버전 + 확인 명령어
2. **Quick Start**: 경험자용 5분 설정
3. **Step-by-Step**: 초보자용 상세 가이드
4. **토글**: 선택적 상세 내용 (SSH, 문제해결)
5. **Verification Checklist**: 체크박스로 확인
6. **Next Steps**: 설정 후 행동 안내
