# 공유 베이스 스키마 문서

카카오맵과 네이버맵에서 공통으로 사용하는 기반 모델 상세 문서.

**파일 위치**: `crawl/base.py`

---

## 목차

1. [설계 원칙](#1-설계-원칙)
2. [공유 Annotated 타입](#2-공유-annotated-타입)
3. [공유 Enum](#3-공유-enum)
4. [좌표 모델](#4-좌표-모델)
5. [크롤 메타데이터 모델](#5-크롤-메타데이터-모델)
6. [장소 베이스 모델](#6-장소-베이스-모델)
7. [API 응답 모델](#7-api-응답-모델)
8. [크롤 작업 모델](#8-크롤-작업-모델)
9. [패키지 구조](#9-패키지-구조)

---

## 1. 설계 원칙

- **단일 소스**: 중복 정의 방지. 좌표, 크롤 메타데이터 등 공통 개념은 `base.py`에만 정의
- **플랫폼 구분**: `CrawlSource` enum으로 카카오/네이버 데이터 출처 명확히 구분
- **확장성**: `BasePlace`, `BaseReviewStats`를 상속하여 플랫폼별 모델 확장
- **불변 값 객체**: 좌표, 메타데이터 등은 `frozen=True`로 생성 후 변경 불가

---

## 2. 공유 Annotated 타입

재사용 가능한 타입 제약 정의.

### KoreanPhone

한국 전화번호 형식 검증.

| 속성 | 값 |
|------|-----|
| 정규식 | `^0\d{1,2}-?\d{3,4}-?\d{4}$` |
| 유효 예시 | `"02-1234-5678"`, `"010-9876-5432"`, `"0311234567"` |
| 무효 예시 | `"+82-2-1234-5678"` (국제번호 미지원), `"1588-1234"` (대표번호 미지원) |

**참고**: 하이픈은 선택사항. 있어도 되고 없어도 됨.

---

### TimeStr

HH:MM 형식의 시간 문자열 검증.

| 속성 | 값 |
|------|-----|
| 정규식 | `^([01]\d\|2[0-3]):[0-5]\d$` |
| 유효 예시 | `"09:30"`, `"18:00"`, `"23:59"`, `"00:00"` |
| 무효 예시 | `"25:00"`, `"9:30"` (앞자리 0 필수), `"abc"` |

---

## 3. 공유 Enum

### CrawlSource

크롤링 데이터의 플랫폼 출처.

| 값 | 설명 | 사용처 |
|----|------|--------|
| `NAVER` | 네이버맵 | `NaverPlace.crawl.source` |
| `KAKAO` | 카카오맵 | `KakaoPlaceData.crawl_metadata.source` |

향후 구글맵 등 추가 플랫폼 지원 시 여기에 값 추가.

---

### CrawlJobStatus

크롤 작업의 생명주기 상태.

| 값 | 설명 | 전이 가능 상태 |
|----|------|----------------|
| `PENDING` | 대기 중 (생성됨) | → RUNNING |
| `RUNNING` | 실행 중 | → COMPLETED, FAILED, PARTIAL |
| `COMPLETED` | 정상 완료 | (종료) |
| `FAILED` | 실패 | (종료) |
| `PARTIAL` | 일부 성공, 일부 실패 | (종료) |

---

## 4. 좌표 모델

### Coordinates

WGS84 좌표계 기반 위도/경도. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 범위 | 설명 | 예시 |
|------|------|------|------|------|------|
| `latitude` | `float` | O | 33.0~39.0 | 위도 (한국 범위) | `37.5665` |
| `longitude` | `float` | O | 124.0~132.0 | 경도 (한국 범위) | `126.9780` |

**범위 제한 근거**:
- 한국 최남단 (마라도): 약 33.1N
- 한국 최북단 (강원도): 약 38.6N
- 한국 최서단 (백령도): 약 124.6E
- 한국 최동단 (독도): 약 131.9E

**팩토리 메서드**:

| 메서드 | 설명 |
|--------|------|
| `from_kakao(x, y)` | 카카오 API 형식 변환. **주의**: 카카오에서 `x`는 경도, `y`는 위도 (일반적인 (위도, 경도) 순서의 반대) |

**유틸리티 메서드**:

| 메서드 | 반환 | 설명 |
|--------|------|------|
| `to_tuple()` | `tuple[float, float]` | `(위도, 경도)` 튜플 반환 |

**카카오맵 좌표 변환 주의사항**:
```
카카오 API: x = 126.92 (경도), y = 37.555 (위도)
              ↓ from_kakao(x, y)
Coordinates: latitude = 37.555, longitude = 126.92
```

---

## 5. 크롤 메타데이터 모델

### CrawlMetadata

크롤링 작업에 대한 메타 정보. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `source` | `CrawlSource` | O | - | 데이터 출처 플랫폼 | `CrawlSource.NAVER` |
| `crawled_at` | `datetime` | X | 현재 UTC 시간 | 크롤링 시점 (UTC, timezone-aware) | `2024-01-15T09:30:00+00:00` |
| `source_url` | `Optional[str]` | X | `None` | 크롤링한 원본 URL | `"https://map.naver.com/..."` |
| `search_query` | `Optional[str]` | X | `None` | 이 장소를 찾은 검색어 | `"홍대 피부과"` |
| `raw_data_hash` | `Optional[str]` | X | `None` | 원본 응답의 SHA-256 해시 접두사 (중복 검출용) | `"a1b2c3d4e5f6..."` |
| `crawl_duration_ms` | `Optional[int]` | X | `None` | 크롤링 소요 시간 (밀리초, 0 이상) | `1250` |

**`crawled_at` 관련 주의사항**:
- `datetime.utcnow()`는 Python 3.12에서 deprecated. 대신 `datetime.now(timezone.utc)` 사용
- 항상 timezone-aware datetime 생성

---

## 6. 장소 베이스 모델

### BasePlace

카카오맵과 네이버맵에서 공통으로 사용하는 장소 기본 필드.

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `name` | `str` | O | - | 상호명 (최소 1자) | `"맛있는 한식당"` |
| `category` | `str` | O | - | 카테고리명 (최소 1자) | `"한식"` |
| `road_address` | `Optional[str]` | X | `None` | 도로명 주소 | `"서울 강남구 테헤란로 123"` |
| `parcel_address` | `Optional[str]` | X | `None` | 지번 주소 (구주소) | `"서울 강남구 역삼동 123"` |
| `phone` | `Optional[str]` | X | `None` | 전화번호 | `"02-1234-5678"` |
| `coordinates` | `Optional[Coordinates]` | X | `None` | WGS84 좌표 | - |

**설정(ConfigDict)**:
- `str_strip_whitespace=True`: 문자열 앞뒤 공백 자동 제거
- `extra="ignore"`: 모델에 정의되지 않은 필드는 무시 (크롤링 데이터의 예상 외 필드 안전 처리)

**상속 구조**:
```
BasePlace
├── NaverPlace (naver_map_schema.py)
└── (KakaoPlaceData는 직접 상속하지 않고 PlaceBasicInfo를 사용)
```

---

### BaseReviewStats

공통 리뷰 통계 기반 모델. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 범위 | 설명 |
|------|------|------|--------|------|------|
| `rating` | `Optional[float]` | X | `None` | 0.0~5.0 | 평균 별점 |

**상속 구조**:
```
BaseReviewStats
└── NaverReviewStats (+visitor_reviews, +blog_reviews)
```

---

## 7. API 응답 모델

### PlaceSummary

목록 API 엔드포인트용 경량 장소 요약. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `id` | `str` | O | - | 장소 ID |
| `name` | `str` | O | - | 상호명 |
| `category` | `str` | O | - | 카테고리 |
| `road_address` | `Optional[str]` | X | `None` | 도로명 주소 |
| `rating` | `Optional[float]` | X | `None` | 평균 별점 |
| `total_reviews` | `int` | X | `0` | 전체 리뷰 수 |
| `source` | `CrawlSource` | O | - | 데이터 출처 (NAVER/KAKAO) |
| `coordinates` | `Optional[Coordinates]` | X | `None` | 좌표 |

**용도**: 검색 결과 목록, 지도 마커 표시 등 전체 데이터가 필요 없는 경우에 사용.

---

### PaginatedResponse

페이지네이션이 적용된 API 응답 래퍼. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 범위 | 설명 |
|------|------|------|------|------|
| `items` | `list[PlaceSummary]` | O | - | 현재 페이지의 항목 목록 |
| `total` | `int` | O | 0 이상 | 전체 항목 수 |
| `page` | `int` | O | 1 이상 | 현재 페이지 번호 |
| `page_size` | `int` | O | 1~100 | 페이지당 항목 수 |
| `has_next` | `bool` | O | - | 다음 페이지 존재 여부 |

**프로퍼티**:
- `total_pages` → `int`: 전체 페이지 수 계산

**팩토리 메서드**:
```python
response = PaginatedResponse.create(
    items=place_summaries,
    total=150,
    page=1,
    page_size=20,
)
# has_next가 자동 계산됨 (1 * 20 < 150 → True)
```

---

## 8. 크롤 작업 모델

### CrawlError

개별 크롤링 에러 기록. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `place_id` | `Optional[str]` | X | `None` | 에러 발생 장소 ID | `"1612729816"` |
| `url` | `Optional[str]` | X | `None` | 에러 발생 URL | `"https://..."` |
| `error_type` | `str` | O | - | 에러 클래스명 | `"TimeoutError"` |
| `message` | `str` | O | - | 사람이 읽을 수 있는 에러 메시지 | `"Connection timed out after 30s"` |
| `timestamp` | `datetime` | X | 현재 UTC | 에러 발생 시점 | - |

---

### CrawlJob

배치 크롤링 작업 추적 모델.

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `job_id` | `str` | O | - | 고유 작업 ID | `"job-20240115-001"` |
| `source` | `CrawlSource` | O | - | 크롤링 대상 플랫폼 | `CrawlSource.NAVER` |
| `status` | `CrawlJobStatus` | X | `PENDING` | 작업 상태 | `CrawlJobStatus.RUNNING` |
| `query` | `Optional[str]` | X | `None` | 검색 쿼리 | `"강남역 피부과"` |
| `region` | `Optional[str]` | X | `None` | 대상 지역 | `"서울 강남구"` |
| `total_places` | `int` | X | `0` | 발견된 전체 장소 수 | `45` |
| `completed_places` | `int` | X | `0` | 성공적으로 크롤링된 장소 수 | `40` |
| `failed_places` | `int` | X | `0` | 크롤링 실패한 장소 수 | `5` |
| `errors` | `list[CrawlError]` | X | `[]` | 발생한 에러 목록 | - |
| `started_at` | `Optional[datetime]` | X | `None` | 작업 시작 시간 | - |
| `completed_at` | `Optional[datetime]` | X | `None` | 작업 완료 시간 | - |
| `created_at` | `datetime` | X | 현재 UTC | 작업 생성 시간 | - |

**프로퍼티**:
- `progress_pct` → `float`: 진행률 퍼센트 (`completed_places / total_places * 100`)
- `success_rate` → `float`: 성공률 퍼센트 (`completed / (completed + failed) * 100`)

---

### CrawlResult

개별 장소 크롤링 시도 결과. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `success` | `bool` | O | - | 크롤링 성공 여부 |
| `place_data` | `Optional[dict]` | X | `None` | 크롤링된 장소 데이터 (성공 시) |
| `error` | `Optional[CrawlError]` | X | `None` | 에러 정보 (실패 시) |

**교차 검증 규칙**:
- `success=True`이면 `place_data`는 반드시 존재해야 함
- `success=False`이면 `error`는 반드시 존재해야 함

---

## 9. 패키지 구조

```
crawl/
├── __init__.py              # 패키지 진입점, 주요 모델 re-export
├── base.py                  # 이 문서: 공유 베이스 모델
├── kakao_map_schema.py      # 카카오맵 전용 모델 + 파서
├── naver_map_schema.py      # 네이버맵 전용 모델 + 파서
└── docs/
    ├── base_schema.md       # 이 문서
    ├── kakao_map_schema.md  # 카카오맵 스키마 문서
    └── naver_map_schema.md  # 네이버맵 스키마 문서
```

**import 예시**:

```python
# 공유 모델 직접 import
from crawl.base import Coordinates, CrawlMetadata, CrawlSource

# 카카오맵 모델
from crawl.kakao_map_schema import KakaoPlaceData, KakaoPlaceParser

# 네이버맵 모델
from crawl.naver_map_schema import NaverPlace, NaverPlaceParser

# 패키지 레벨 import (편의용)
from crawl import KakaoPlaceData, NaverPlace, CrawlSource
```
