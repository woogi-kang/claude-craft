# API Document Template

## Structure

```markdown
# [API 이름] API Reference

| 속성 | 값 |
|------|-----|
| 🏷️ 태그 | API, Reference |
| 👤 담당자 | @name |
| 📅 상태 | 작성중 / 배포됨 |
| 📆 최종수정 | YYYY-MM-DD |
| 🔖 API 버전 | v1.0.0 |

## Overview

[API 개요 1-2문장]

**Base URL**
```
https://api.example.com/v1
```

## Authentication

[인증 방식 설명]

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" ...
```

💡 토큰은 [발급 방법/위치]에서 발급받을 수 있습니다.

## Endpoints

### [카테고리명]

#### `METHOD /path`

**설명**: [엔드포인트 설명]

**Headers**
| 이름 | 필수 | 타입 | 설명 |
|------|------|------|------|
| Authorization | ✅ | string | Bearer 토큰 |
| Content-Type | ✅ | string | application/json |

**Path Parameters**
| 이름 | 타입 | 설명 |
|------|------|------|
| id | string | 리소스 ID |

**Query Parameters**
| 이름 | 필수 | 타입 | 기본값 | 설명 |
|------|------|------|--------|------|
| page | ❌ | int | 1 | 페이지 번호 |
| limit | ❌ | int | 20 | 페이지당 항목 수 |

**Request Body**
```json
{
  "field": "value",
  "nested": {
    "key": "value"
  }
}
```

**Response** `200 OK`
```json
{
  "data": {
    "id": "123",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

▶️ Error Responses
   **`400 Bad Request`**
   ```json
   {"error": "validation_error", "message": "field is required"}
   ```
   
   **`401 Unauthorized`**
   ```json
   {"error": "unauthorized", "message": "Invalid token"}
   ```

⚠️ Rate Limit: 100 requests/minute

---

## Error Codes

| 코드 | 이름 | 설명 | 해결방법 |
|------|------|------|----------|
| 400 | Bad Request | 잘못된 요청 | 요청 파라미터 확인 |
| 401 | Unauthorized | 인증 실패 | 토큰 재발급 |
| 429 | Too Many Requests | Rate limit 초과 | 1분 후 재시도 |

## SDK Examples

▶️ Dart/Flutter
   ```dart
   // 파일: lib/api/client.dart
   final response = await client.get('/resource');
   ```

▶️ JavaScript
   ```javascript
   // 파일: src/api.js
   const response = await fetch('/resource');
   ```

---
📝 **유지보수 노트**
- API 버전 변경 시 업데이트 필요
- 새 엔드포인트 추가 시 업데이트 필요
```

## Key Elements

1. **메타데이터**: API 버전 포함 필수
2. **Base URL**: 환경별(dev/staging/prod) 구분 시 테이블로
3. **인증**: 토큰 발급 방법 링크 필수
4. **엔드포인트**: METHOD + path 형식, 카테고리별 그룹화
5. **파라미터**: 필수 여부 이모지로 표시 (✅/❌)
6. **에러**: 토글로 접어서 가독성 확보
7. **SDK**: 주요 언어별 예시 (토글 사용)
