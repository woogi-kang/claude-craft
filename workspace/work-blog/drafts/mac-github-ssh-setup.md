# Mac에서 GitHub SSH 키 설정하기: 완벽 가이드

매번 GitHub에 push할 때마다 비밀번호를 입력하는 것이 번거로우신가요? SSH 키를 설정하면 보안도 강화하고 인증 과정도 간소화할 수 있습니다. 이 글에서는 Mac에서 GitHub SSH 키를 설정하는 방법을 단계별로 알아보겠습니다.

## SSH 키란?

SSH(Secure Shell) 키는 공개키 암호화 방식을 사용하는 인증 방법입니다. 비밀번호 대신 키 쌍(공개키와 개인키)을 사용하여 안전하게 인증할 수 있습니다.

- **개인키(Private Key)**: 내 컴퓨터에만 저장되는 비밀 키
- **공개키(Public Key)**: GitHub에 등록하는 키

## 1단계: SSH 키 생성하기

터미널을 열고 다음 명령어를 입력합니다:

```bash
ssh-keygen -t ed25519 -C "본인의_이메일_주소@example.com"
```

### 옵션 설명
- `-t ed25519`: Ed25519 알고리즘 사용 (현재 가장 권장되는 알고리즘)
- `-C "이메일"`: 키에 주석(comment) 추가 (식별용)

### 실행 과정

```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/Users/username/.ssh/id_ed25519):
```
**Enter**를 눌러 기본 경로를 사용합니다.

```
Enter passphrase (empty for no passphrase):
```
추가 보안을 위한 비밀번호를 입력합니다. (선택사항이지만 권장)

```
Enter same passphrase again:
```
비밀번호를 다시 입력합니다.

완료되면 `~/.ssh/` 디렉토리에 두 개의 파일이 생성됩니다:
- `id_ed25519`: 개인키 (절대 공유하면 안 됨!)
- `id_ed25519.pub`: 공개키 (GitHub에 등록할 키)

## 2단계: SSH Agent 실행하기

SSH Agent는 SSH 키를 메모리에 저장하여 매번 비밀번호를 입력하지 않아도 되게 해줍니다.

```bash
eval "$(ssh-agent -s)"
```

실행 결과:
```
Agent pid 12345
```

## 3단계: SSH 키를 Agent에 등록하기

생성한 SSH 키를 Agent에 추가합니다. `--apple-use-keychain` 옵션을 사용하면 Mac의 키체인에 비밀번호가 저장되어 재부팅 후에도 비밀번호를 다시 입력할 필요가 없습니다.

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

> **참고**: macOS Monterey(12.0) 이전 버전에서는 `--apple-use-keychain` 대신 `-K` 옵션을 사용합니다.

## 4단계: SSH Config 파일 설정 (선택사항)

재부팅 후에도 SSH Agent가 키체인의 키를 자동으로 로드하도록 설정합니다.

```bash
# ~/.ssh/config 파일 생성 또는 편집
nano ~/.ssh/config
```

다음 내용을 추가합니다:

```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

## 5단계: 공개키 복사하기

GitHub에 등록할 공개키를 클립보드에 복사합니다:

```bash
pbcopy < ~/.ssh/id_ed25519.pub
```

이제 클립보드에 공개키가 복사되었습니다. `pbcopy`는 Mac의 클립보드에 내용을 복사하는 명령어입니다.

## 6단계: GitHub에 SSH 키 등록하기

1. [GitHub](https://github.com)에 로그인합니다.
2. 우측 상단 프로필 사진 클릭 → **Settings**
3. 좌측 메뉴에서 **SSH and GPG keys** 클릭
4. **New SSH key** 버튼 클릭
5. 다음 정보를 입력합니다:
   - **Title**: 키를 식별할 수 있는 이름 (예: "MacBook Pro 2024")
   - **Key type**: Authentication Key (기본값)
   - **Key**: `Cmd + V`로 복사한 공개키 붙여넣기
6. **Add SSH key** 버튼 클릭

## 7단계: 연결 테스트하기

모든 설정이 완료되었는지 테스트합니다:

```bash
ssh -T git@github.com
```

처음 연결 시 다음과 같은 메시지가 나타날 수 있습니다:

```
The authenticity of host 'github.com (IP주소)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

`yes`를 입력합니다.

성공하면 다음 메시지가 표시됩니다:

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

## 기존 HTTPS 저장소를 SSH로 변경하기

이미 HTTPS로 clone한 저장소가 있다면 SSH로 변경할 수 있습니다:

```bash
# 현재 원격 저장소 URL 확인
git remote -v

# SSH URL로 변경
git remote set-url origin git@github.com:사용자명/저장소명.git
```

## 문제 해결

### Permission denied (publickey) 오류

```bash
# SSH Agent에 키가 등록되어 있는지 확인
ssh-add -l

# 키가 없다면 다시 추가
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### SSH 키가 여러 개인 경우

`~/.ssh/config` 파일에서 각 서비스별로 다른 키를 지정할 수 있습니다:

```
# GitHub
Host github.com
  IdentityFile ~/.ssh/id_ed25519_github

# GitLab
Host gitlab.com
  IdentityFile ~/.ssh/id_ed25519_gitlab
```

## 마무리

SSH 키 설정이 완료되었습니다! 이제 GitHub에 push/pull할 때 비밀번호 없이 안전하게 인증됩니다.

### 요약

| 단계 | 명령어 |
|------|--------|
| 키 생성 | `ssh-keygen -t ed25519 -C "이메일"` |
| Agent 실행 | `eval "$(ssh-agent -s)"` |
| 키 등록 | `ssh-add --apple-use-keychain ~/.ssh/id_ed25519` |
| 키 복사 | `pbcopy < ~/.ssh/id_ed25519.pub` |
| 연결 테스트 | `ssh -T git@github.com` |

SSH 키는 한 번 설정해두면 계속 사용할 수 있으니, 새 Mac을 설정할 때 이 가이드를 참고하세요!
