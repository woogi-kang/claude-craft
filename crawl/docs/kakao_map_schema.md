# 카카오맵 데이터 스키마 문서

카카오맵 장소 크롤링을 위한 Pydantic v2 데이터 모델 상세 문서.

**파일 위치**: `crawl/kakao_map_schema.py`
**의존성**: `crawl/base.py` (공유 모델)

---

## 목차

1. [모델 구조 개요](#1-모델-구조-개요)
2. [Enum 타입](#2-enum-타입)
3. [주소 모델](#3-주소-모델)
4. [피드백 및 운영 모델](#4-피드백-및-운영-모델)
5. [메뉴 모델](#5-메뉴-모델)
6. [리뷰 모델](#6-리뷰-모델)
7. [장소 기본정보 모델](#7-장소-기본정보-모델)
8. [최상위 집계 모델](#8-최상위-집계-모델)
9. [JSON 파서](#9-json-파서)
10. [JSON 경로 매핑표](#10-json-경로-매핑표)

---

## 1. 모델 구조 개요

```
KakaoPlaceData (최상위 집계 모델)
├── basic_info: PlaceBasicInfo (장소 기본정보)
│   ├── address: KakaoAddressInfo (주소)
│   │   └── region: RegionInfo (행정구역)
│   ├── coordinates: Coordinates (좌표, base.py)
│   ├── feedback: KakaoFeedbackInfo (평점/리뷰 통계)
│   └── open_hour: OpenHourInfo (실시간 영업 상태)
├── menus: list[KakaoMenuItem] (메뉴 목록)
├── reviews: list[KakaoReviewItem] (리뷰 목록)
└── crawl_metadata: CrawlMetadata (크롤 메타데이터, base.py)
```

---

## 2. Enum 타입

### OpenStatus

카카오맵 API에서 반환하는 영업 상태 값.

| 값 | 설명 |
|----|------|
| `OPEN` | 영업중 |
| `CLOSE` | 영업 종료 |
| `BREAKTIME` | 브레이크타임 (휴식 시간) |
| `N/A` | 정보 없음 |
| `UNKNOWN` | 알 수 없음 (API에서 예상 외 값이 올 때 자동 매핑) |

**특이사항**: `_missing_()` 메서드가 구현되어 있어서, API에서 예상하지 못한 새로운 상태값이 오면 `UNKNOWN`으로 자동 처리됨. 에러 대신 안전하게 fallback.

---

## 3. 주소 모델

### RegionInfo

카카오맵의 행정구역 계층 구조 (시/도 > 구/군 > 동).

| 필드 | 타입 | 필수 | JSON 별칭 | 설명 | 예시 |
|------|------|------|-----------|------|------|
| `province` | `Optional[str]` | X | `name1` | 시/도 (광역시/특별시 포함) | `"서울"` |
| `district` | `Optional[str]` | X | `name2` | 구/군 | `"마포구"` |
| `neighborhood` | `Optional[str]` | X | `name3` | 동/읍/면 | `"서교동"` |

**프로퍼티**:
- `full_region` → `str`: 모든 행정구역을 공백으로 연결한 문자열 (예: `"서울 마포구 서교동"`)

**JSON 경로**: `basicInfo.address.region`

---

### KakaoAddressInfo

도로명 주소, 우편번호, 행정구역 정보를 포함하는 주소 모델.

| 필드 | 타입 | 필수 | JSON 별칭 | 설명 | 예시 |
|------|------|------|-----------|------|------|
| `road_address` | `Optional[str]` | X | `newaddrfull` | 전체 도로명 주소 | `"서울 마포구 홍익로 25"` |
| `zipcode` | `Optional[str]` | X | `bsizonno` | 5자리 우편번호 | `"04039"` |
| `region` | `Optional[RegionInfo]` | X | - | 행정구역 상세 | (위 RegionInfo 참조) |

**검증 규칙**:
- `zipcode`: 정규식 `^\d{5}$` 패턴 검사. 5자리 숫자가 아니면 `None`으로 치환 (에러 대신 graceful 처리)

**프로퍼티**:
- `display_address` → `str`: 표시용 주소. 도로명 주소 우선, 없으면 행정구역 조합

**JSON 경로**: `basicInfo.address`

---

## 4. 피드백 및 운영 모델

### KakaoFeedbackInfo

사용자 평점과 리뷰 수 집계 정보.

| 필드 | 타입 | 필수 | JSON 별칭 | 범위 | 설명 | 예시 |
|------|------|------|-----------|------|------|------|
| `score` | `float` | X (기본 0.0) | - | 0.0~5.0 | 평균 별점 | `4.9` |
| `review_count` | `int` | X (기본 0) | `comntcnt` | 0 이상 | 사용자 리뷰 수 | `128` |
| `blog_review_count` | `int` | X (기본 0) | `blogrvwcnt` | 0 이상 | 블로그 리뷰 수 | `862` |

**프로퍼티**:
- `total_mentions` → `int`: 리뷰 + 블로그 합계
- `has_reviews` → `bool`: 사용자 리뷰가 1건 이상인지 여부

**JSON 경로**: `basicInfo.feedback.all`

---

### OpenHourInfo

카카오맵의 실시간 영업 상태 정보.

| 필드 | 타입 | 필수 | JSON 별칭 | 설명 | 예시 |
|------|------|------|-----------|------|------|
| `status` | `OpenStatus` | X (기본 UNKNOWN) | - | 영업 상태 enum 값 | `"OPEN"` |
| `current_description` | `Optional[str]` | X | `datetime` | 사람이 읽을 수 있는 상태 텍스트 (한국어) | `"진료중"`, `"영업 전"` |

**참고**: JSON 필드명이 `datetime`이지만 실제 내용은 날짜/시간이 아니라 상태 설명 텍스트임. 카카오 API의 네이밍 특이사항.

**JSON 경로**: `basicInfo.openHour.realtime`

---

## 5. 메뉴 모델

### KakaoMenuItem

장소에서 제공하는 개별 메뉴 항목 또는 서비스.

| 필드 | 타입 | 필수 | JSON 별칭 | 설명 | 예시 |
|------|------|------|-----------|------|------|
| `name` | `str` | O | `menu` | 메뉴명 또는 서비스명 (최소 1자) | `"아메리카노"` |
| `price_raw` | `Optional[str]` | X | `price` | 화면에 표시되는 가격 문자열 (원화 형식) | `"4,500"`, `"15,000원"` |
| `photo_url` | `Optional[str]` | X | `photo` | 메뉴 사진 URL | `"http://..."` |
| `is_recommended` | `bool` | X (기본 False) | `recommend` | 추천 메뉴 여부 | `true` |

**프로퍼티**:
- `price_value` → `Optional[int]`: 가격 문자열에서 숫자만 추출한 정수값
  - `"4,500"` → `4500`
  - `"15,000원"` → `15000`
  - `"변동"`, `"무료"` → `None` (숫자가 없는 경우)

**JSON 경로**: `menuInfo.menuList[]`

---

## 6. 리뷰 모델

### KakaoReviewItem

개별 사용자 리뷰.

| 필드 | 타입 | 필수 | JSON 별칭 | 범위 | 설명 | 예시 |
|------|------|------|-----------|------|------|------|
| `content` | `Optional[str]` | X | `contents` | - | 리뷰 본문 텍스트 | `"친절해요..."` |
| `rating` | `int` | O | `point` | 1~5 | 사용자 별점 | `5` |
| `username` | `Optional[str]` | X | - | - | 작성자 닉네임 | `"라이언"` |
| `review_date` | `Optional[str]` | X | `date` | - | 작성일 (API 원본 문자열) | `"2024.01.01"` |

**프로퍼티**:
- `parsed_date` → `Optional[date]`: 날짜 문자열을 Python `date` 객체로 파싱
  - 지원 형식: `YYYY.MM.DD`, `YYYY-MM-DD`, `YY.MM.DD`
  - 파싱 실패 시 `None`
- `has_content` → `bool`: 리뷰 본문이 있는지 여부 (빈 문자열/공백만 있는 경우 False)

**JSON 경로**: `comment.list[]`

---

## 7. 장소 기본정보 모델

### PlaceBasicInfo

카카오맵 장소의 핵심 식별 정보와 메타데이터.

| 필드 | 타입 | 필수 | JSON 별칭 | 설명 | 예시 |
|------|------|------|-----------|------|------|
| `place_id` | `str` | O | `cid` | 카카오 고유 장소 ID (최소 1자) | `"1048722794"` |
| `name` | `str` | O | `placenamefull` | 전체 장소명 (최소 1자) | `"리즈온의원 홍대점"` |
| `short_name` | `Optional[str]` | X | `placename` | 약칭 | `"리즈온의원"` |
| `phone` | `Optional[str]` | X | `phonenum` | 전화번호 | `"02-1234-5678"` |
| `category` | `Optional[str]` | X | `cate1name` | 대분류 카테고리 | `"병원"` |
| `subcategory` | `Optional[str]` | X | `catename` | 소분류 카테고리 | `"피부과"` |
| `homepage` | `Optional[str]` | X | - | 공식 홈페이지 URL | `"https://example.com"` |
| `main_photo_url` | `Optional[str]` | X | `mainphotourl` | 대표 사진 URL | `"http://..."` |
| `tags` | `list[str]` | X (기본 []) | - | 장소 속성 태그 목록 | `["주차가능", "반려동물 동반"]` |
| `address` | `Optional[KakaoAddressInfo]` | X | - | 주소 정보 (위 참조) | - |
| `coordinates` | `Optional[Coordinates]` | X | - | WGS84 좌표 (base.py) | - |
| `feedback` | `KakaoFeedbackInfo` | X (기본값) | - | 평점/리뷰 통계 (위 참조) | - |
| `open_hour` | `Optional[OpenHourInfo]` | X | - | 실시간 영업 상태 (위 참조) | - |

**검증 규칙**:
- `homepage`: URL 정규화 처리
  - `//example.com` → `https://example.com`
  - `example.com` → `https://example.com`
  - 빈 문자열 → `None`

**프로퍼티**:
- `category_path` → `str`: 카테고리 경로 (예: `"병원 > 피부과"`)
- `display_address` → `str`: 표시용 주소 (주소 모델의 display_address 위임)

**JSON 경로**: `basicInfo`

---

## 8. 최상위 집계 모델

### KakaoPlaceData

크롤링한 카카오맵 장소의 모든 데이터를 하나로 합친 최상위 모델.

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `basic_info` | `PlaceBasicInfo` | O | 장소 핵심 정보 (위 참조) |
| `menus` | `list[KakaoMenuItem]` | X (기본 []) | 메뉴 항목 목록 |
| `reviews` | `list[KakaoReviewItem]` | X (기본 []) | 사용자 리뷰 목록 |
| `crawl_metadata` | `CrawlMetadata` | X (자동 생성) | 크롤 메타데이터 (base.py, source=KAKAO) |

**프로퍼티**:
- `place_id` → `str`: `basic_info.place_id`의 단축 접근자
- `average_review_rating` → `Optional[float]`: 리뷰 목록의 실제 평균 별점 (리뷰 없으면 `None`)
- `recommended_menus` → `list[KakaoMenuItem]`: 추천 메뉴만 필터링한 목록

**메서드**:
- `content_hash()` → `str`: 중복 검출용 SHA-256 해시 (place_id + name 기반, 16자)

---

## 9. JSON 파서

### KakaoPlaceParser

카카오맵 API의 원본 JSON 응답을 `KakaoPlaceData` 모델로 변환하는 유틸리티 클래스.

**주요 메서드**:

| 메서드 | 입력 | 출력 | 설명 |
|--------|------|------|------|
| `parse(raw_data, search_query?, source_url?)` | API 원본 dict | `KakaoPlaceData` | 전체 파싱 (메인 진입점) |
| `parse_address(basic_info)` | basicInfo dict | `Optional[KakaoAddressInfo]` | 주소 파싱 |
| `parse_coordinates(basic_info)` | basicInfo dict | `Optional[Coordinates]` | 좌표 파싱 (x→경도, y→위도 변환) |
| `parse_feedback(basic_info)` | basicInfo dict | `KakaoFeedbackInfo` | 피드백 통계 파싱 |
| `parse_open_hour(basic_info)` | basicInfo dict | `Optional[OpenHourInfo]` | 영업 상태 파싱 |
| `parse_menus(raw_data)` | 전체 응답 dict | `list[KakaoMenuItem]` | 메뉴 목록 파싱 |
| `parse_reviews(raw_data)` | 전체 응답 dict | `list[KakaoReviewItem]` | 리뷰 목록 파싱 |

**사용 예시**:

```python
raw_json = await kakao_client.fetch_place("1048722794")

place = KakaoPlaceParser.parse(
    raw_data=raw_json,
    search_query="홍대 피부과",
    source_url="https://place.map.kakao.com/1048722794",
)

print(place.basic_info.name)          # "리즈온의원 홍대점"
print(place.basic_info.category_path) # "병원 > 피부과"
print(place.recommended_menus)        # 추천 메뉴 목록
```

**에러 처리**:
- 필수 필드(`cid`, `placenamefull`) 누락 시 `ValueError` 발생
- 개별 메뉴/리뷰 파싱 실패 시 해당 항목만 건너뛰고 계속 진행 (graceful degradation)

---

## 10. JSON 경로 매핑표

카카오맵 API 응답의 JSON 경로와 모델 필드 간 전체 매핑.

### 장소 식별 정보

| JSON 경로 | 모델 필드 | 타입 | 설명 |
|-----------|-----------|------|------|
| `basicInfo.cid` | `PlaceBasicInfo.place_id` | str | 고유 장소 ID |
| `basicInfo.placenamefull` | `PlaceBasicInfo.name` | str | 전체 장소명 |
| `basicInfo.placename` | `PlaceBasicInfo.short_name` | str? | 약칭 |
| `basicInfo.phonenum` | `PlaceBasicInfo.phone` | str? | 전화번호 |
| `basicInfo.cate1name` | `PlaceBasicInfo.category` | str? | 대분류 |
| `basicInfo.catename` | `PlaceBasicInfo.subcategory` | str? | 소분류 |
| `basicInfo.homepage` | `PlaceBasicInfo.homepage` | str? | 홈페이지 URL |
| `basicInfo.mainphotourl` | `PlaceBasicInfo.main_photo_url` | str? | 대표 사진 |
| `basicInfo.tags` | `PlaceBasicInfo.tags` | list[str] | 속성 태그 |

### 위치 정보

| JSON 경로 | 모델 필드 | 타입 | 설명 |
|-----------|-----------|------|------|
| `basicInfo.address.newaddr.newaddrfull` | `KakaoAddressInfo.road_address` | str? | 도로명 주소 |
| `basicInfo.address.newaddr.bsizonno` | `KakaoAddressInfo.zipcode` | str? | 우편번호 |
| `basicInfo.address.region.name1` | `RegionInfo.province` | str? | 시/도 |
| `basicInfo.address.region.name2` | `RegionInfo.district` | str? | 구/군 |
| `basicInfo.address.region.name3` | `RegionInfo.neighborhood` | str? | 동/읍/면 |
| `basicInfo.y` | `Coordinates.latitude` | float | 위도 (주의: y가 위도) |
| `basicInfo.x` | `Coordinates.longitude` | float | 경도 (주의: x가 경도) |

### 피드백 및 영업 정보

| JSON 경로 | 모델 필드 | 타입 | 설명 |
|-----------|-----------|------|------|
| `basicInfo.feedback.all.score` | `KakaoFeedbackInfo.score` | float | 평균 별점 (0~5) |
| `basicInfo.feedback.all.comntcnt` | `KakaoFeedbackInfo.review_count` | int | 사용자 리뷰 수 |
| `basicInfo.feedback.all.blogrvwcnt` | `KakaoFeedbackInfo.blog_review_count` | int | 블로그 리뷰 수 |
| `basicInfo.openHour.realtime.status` | `OpenHourInfo.status` | OpenStatus | 영업 상태 |
| `basicInfo.openHour.realtime.datetime` | `OpenHourInfo.current_description` | str? | 상태 텍스트 |

### 메뉴

| JSON 경로 | 모델 필드 | 타입 | 설명 |
|-----------|-----------|------|------|
| `menuInfo.menuList[].menu` | `KakaoMenuItem.name` | str | 메뉴명 |
| `menuInfo.menuList[].price` | `KakaoMenuItem.price_raw` | str? | 가격 문자열 |
| `menuInfo.menuList[].photo` | `KakaoMenuItem.photo_url` | str? | 사진 URL |
| `menuInfo.menuList[].recommend` | `KakaoMenuItem.is_recommended` | bool | 추천 여부 |

### 리뷰

| JSON 경로 | 모델 필드 | 타입 | 설명 |
|-----------|-----------|------|------|
| `comment.list[].contents` | `KakaoReviewItem.content` | str? | 리뷰 본문 |
| `comment.list[].point` | `KakaoReviewItem.rating` | int | 별점 (1~5) |
| `comment.list[].username` | `KakaoReviewItem.username` | str? | 작성자 |
| `comment.list[].date` | `KakaoReviewItem.review_date` | str? | 작성일 |
