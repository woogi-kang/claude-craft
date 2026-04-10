#!/usr/bin/env bash
# k-skill 의존성 설치 및 환경 설정 스크립트
# Usage: bash scripts/k-skill-setup.sh

set -euo pipefail

echo "=== k-skill 의존성 설치 ==="

# 1. Node.js 패키지 (전역)
echo ""
echo "[1/3] Node.js 패키지 설치..."
npm install -g \
  @ohah/hwpjs \
  kbo-game \
  kleague-results \
  lck-analytics \
  toss-securities \
  hipass-receipt \
  k-lotto \
  coupang-product-search \
  used-car-price-search \
  cheap-gas-nearby \
  korean-law-mcp \
  daiso \
  bunjang-cli 2>&1 || echo "  [warn] 일부 npm 패키지 설치 실패 - 개별 확인 필요"

# 2. Python 패키지
echo ""
echo "[2/3] Python 패키지 설치..."
python3 -m pip install SRTrain korail2 pycryptodome 2>&1 || echo "  [warn] 일부 Python 패키지 설치 실패"

# 3. secrets.env 템플릿 생성
echo ""
echo "[3/3] secrets.env 설정..."
SECRETS_DIR="$HOME/.config/k-skill"
SECRETS_FILE="$SECRETS_DIR/secrets.env"

if [ -f "$SECRETS_FILE" ]; then
  echo "  이미 존재: $SECRETS_FILE"
  echo "  기존 파일을 유지합니다."
else
  mkdir -p "$SECRETS_DIR"
  cat > "$SECRETS_FILE" <<'EOF'
# k-skill 시크릿 설정
# 필요한 항목만 replace-me를 실제 값으로 교체하세요.
# 사용하지 않는 서비스는 replace-me 그대로 두면 됩니다.

# === 로그인 필요 서비스 ===
KSKILL_SRT_ID=replace-me
KSKILL_SRT_PASSWORD=replace-me
KSKILL_KTX_ID=replace-me
KSKILL_KTX_PASSWORD=replace-me

# === API 키 ===
LAW_OC=replace-me
KIPRIS_PLUS_API_KEY=replace-me
AIR_KOREA_OPEN_API_KEY=replace-me

# === 프록시 서버 ===
# 서울지하철, 날씨 등에 필요. 자체 호스팅 또는 공개 프록시 URL.
KSKILL_PROXY_BASE_URL=replace-me
EOF
  chmod 0600 "$SECRETS_FILE"
  echo "  생성됨: $SECRETS_FILE (퍼미션 0600)"
  echo "  필요한 값을 편집하세요: \$EDITOR $SECRETS_FILE"
fi

echo ""
echo "=== 설치 완료 ==="
echo ""
echo "다음 서비스는 추가 설정 없이 바로 사용 가능합니다:"
echo "  - 부동산 실거래가, 주식 시세, 주유소, 한강 수위 (호스팅 프록시)"
echo "  - 로또, 배송추적, 우편번호, KBO, K리그, 맞춤법 검사"
echo "  - HWP 문서 변환, 다이소/올리브영/쿠팡/번개장터 검색"
echo ""
echo "로그인/API키 필요 서비스:"
echo "  - SRT/KTX 예약 → KSKILL_SRT_ID, KSKILL_KTX_ID"
echo "  - 법률 검색(로컬) → LAW_OC"
echo "  - 특허 검색 → KIPRIS_PLUS_API_KEY"
echo "  - 미세먼지 → AIR_KOREA_OPEN_API_KEY 또는 KSKILL_PROXY_BASE_URL"
echo "  - 날씨/지하철 → KSKILL_PROXY_BASE_URL"
echo "  - Toss 증권 → brew 별도 설치 필요"
echo "  - HiPass → 브라우저 세션 기반"
