# 네이버맵 데이터 스키마 문서

네이버맵 장소 크롤링을 위한 Pydantic v2 데이터 모델 상세 문서.
음식점(메뉴탭 기반)과 병원/서비스(텍스트 기반) 두 가지 장소 유형을 지원.

**파일 위치**: `crawl/naver_map_schema.py`
**의존성**: `crawl/base.py` (공유 모델)

---

## 목차

1. [모델 구조 개요](#1-모델-구조-개요)
2. [Enum 타입](#2-enum-타입)
3. [영업시간 모델](#3-영업시간-모델)
4. [리뷰 통계 모델](#4-리뷰-통계-모델)
5. [메뉴 모델](#5-메뉴-모델)
6. [장소 모델 (Aggregate Root)](#6-장소-모델-aggregate-root)
7. [JSON 파서](#7-json-파서)
8. [필드 매핑표](#8-필드-매핑표)
9. [장소 유형별 데이터 차이](#9-장소-유형별-데이터-차이)

---

## 1. 모델 구조 개요

```
NaverPlace (최상위 Aggregate Root, BasePlace 상속)
├── id: NaverPlaceId (네이버 고유 장소 ID)
├── name, category, road_address ... (BasePlace 상속 필드)
├── coordinates: Coordinates (좌표, base.py)
├── business_hours: list[NaverBusinessHour] (요일별 영업시간)
├── review_stats: NaverReviewStats (리뷰 통계)
│   └── (BaseReviewStats 상속)
├── menu_info: NaverMenuInfo (메뉴 컨테이너)
│   └── items: list[NaverMenuItem] (개별 메뉴 항목)
├── facilities: list[str] (편의시설)
├── image_urls: list[str] (사진 URL)
└── crawl: CrawlMetadata (크롤 메타데이터, base.py)
```

**상속 관계**:
- `NaverPlace` → `BasePlace` (base.py): 이름, 카테고리, 주소, 전화번호, 좌표 공유
- `NaverReviewStats` → `BaseReviewStats` (base.py): 평점 필드 공유

---

## 2. Enum 타입

### DayOfWeek

요일을 나타내는 표준화된 enum. 한국어 요일 파싱 지원.

| 값 | 설명 | 한국어 매핑 |
|----|------|-------------|
| `MON` | 월요일 | `"월"`, `"월요일"` |
| `TUE` | 화요일 | `"화"`, `"화요일"` |
| `WED` | 수요일 | `"수"`, `"수요일"` |
| `THU` | 목요일 | `"목"`, `"목요일"` |
| `FRI` | 금요일 | `"금"`, `"금요일"` |
| `SAT` | 토요일 | `"토"`, `"토요일"` |
| `SUN` | 일요일 | `"일"`, `"일요일"` |
| `HOLIDAY` | 공휴일 | `"공휴일"` |

**한국어 파싱 메서드**:
```python
day = DayOfWeek.from_korean("월요일")  # DayOfWeek.MON
day = DayOfWeek.from_korean("토")      # DayOfWeek.SAT
```

---

### NaverMenuType

메뉴 데이터의 출처 유형.

| 값 | 설명 | 사용 케이스 |
|----|------|-------------|
| `TAB` | 메뉴탭에서 가져온 구조화된 데이터 | 음식점, 카페 등 메뉴 탭이 있는 장소 |
| `TEXT` | 홈/정보 페이지에서 파싱한 텍스트 데이터 | 병원, 미용실 등 가격 정보가 텍스트로 표시되는 장소 |

---

### NaverPlaceId (Annotated Type)

네이버맵 고유 장소 ID에 대한 타입 제약.

| 제약 | 설명 |
|------|------|
| `min_length=1` | 빈 문자열 불가 |
| `pattern=r"^\d+$"` | 숫자로만 구성 |

**예시**: `"1612729816"` (유효), `"abc123"` (ValidationError)

---

## 3. 영업시간 모델

### NaverBusinessHour

특정 요일의 영업시간 정보. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `day_of_week` | `DayOfWeek` | O | - | 요일 (enum) | `DayOfWeek.MON` |
| `open_time` | `Optional[str]` | X | `None` | 영업 시작 시간 (HH:MM) | `"09:30"` |
| `close_time` | `Optional[str]` | X | `None` | 영업 종료 시간 (HH:MM) | `"18:00"` |
| `break_start` | `Optional[str]` | X | `None` | 브레이크타임 시작 | `"13:00"` |
| `break_end` | `Optional[str]` | X | `None` | 브레이크타임 종료 | `"14:00"` |
| `is_day_off` | `bool` | X | `False` | 해당 요일 휴무 여부 | `true` |

**교차 검증 규칙** (model_validator):

1. **휴무일 일관성**: `is_day_off=True`일 때 `open_time`과 `close_time`은 반드시 `None`이어야 함
   - 위반 시: `"open_time and close_time must be None when is_day_off is True"`

2. **브레이크타임 쌍 검증**: `break_start`와 `break_end`는 반드시 함께 제공하거나 둘 다 없어야 함
   - `break_start`만 있고 `break_end` 없음 → ValidationError
   - `break_end`만 있고 `break_start` 없음 → ValidationError

**유효한 데이터 예시**:

```python
# 정상 영업일
NaverBusinessHour(day_of_week=DayOfWeek.MON, open_time="09:30", close_time="18:00")

# 브레이크타임 포함
NaverBusinessHour(
    day_of_week=DayOfWeek.TUE,
    open_time="10:00", close_time="20:30",
    break_start="13:00", break_end="14:00"
)

# 휴무일
NaverBusinessHour(day_of_week=DayOfWeek.SUN, is_day_off=True)
```

---

## 4. 리뷰 통계 모델

### NaverReviewStats

네이버맵 리뷰 통계. `BaseReviewStats`를 상속하여 공통 `rating` 필드 포함. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 범위 | 설명 | 예시 |
|------|------|------|--------|------|------|------|
| `rating` | `Optional[float]` | X | `None` | 0.0~5.0 | 평균 별점 (상속) | `4.3` |
| `visitor_reviews` | `int` | X | `0` | 0 이상 | 방문자 리뷰 수 | `150` |
| `blog_reviews` | `int` | X | `0` | 0 이상 | 블로그 리뷰 수 | `42` |

**프로퍼티**:
- `total_reviews` → `int`: 방문자 리뷰 + 블로그 리뷰 합계
- `has_reviews` → `bool`: 전체 리뷰가 1건 이상인지 여부

**참고**: 네이버맵에서 `rating`은 종종 `null`로 반환됨 (별점이 숨겨져 있는 경우). 이 경우 `None`으로 처리.

---

## 5. 메뉴 모델

### NaverMenuItem

개별 메뉴 항목. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `name` | `str` | O | - | 메뉴명 (최소 1자) | `"김치찌개"` |
| `price` | `str` | O | - | 표시용 가격 문자열 (최소 1자) | `"15,000원"` |
| `price_value` | `Optional[int]` | X | 자동 파싱 | 숫자로 파싱된 가격 (원) | `15000` |
| `description` | `Optional[str]` | X | `None` | 메뉴 설명 | `"2인분부터 주문 가능"` |
| `image_url` | `Optional[str]` | X | `None` | 메뉴 사진 URL | `"http://..."` |
| `is_popular` | `bool` | X | `False` | 인기/추천 메뉴 여부 | `true` |

**가격 자동 파싱 로직** (field_validator):
`price_value`를 명시적으로 제공하지 않으면, `price` 문자열에서 자동으로 숫자를 추출:
- `"15,000원"` → `15000`
- `"4,500"` → `4500`
- `"변동"` → `None` (숫자 없음)
- `"~20,000원"` → `20000`
- `"무료"` → `None`

---

### NaverMenuInfo

메뉴 데이터 컨테이너. 구조화된 메뉴(TAB)와 텍스트 기반 가격정보(TEXT)를 모두 지원. 불변(frozen) 값 객체.

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `menu_type` | `NaverMenuType` | O | - | 메뉴 데이터 출처 유형 | `NaverMenuType.TAB` |
| `items` | `list[NaverMenuItem]` | X | `[]` | 구조화된 메뉴 항목 (TAB일 때 사용) | (위 참조) |
| `price_text` | `Optional[str]` | X | `None` | 원본 가격/메뉴 텍스트 (TEXT일 때 사용) | `"쌍꺼풀 50만원~\n코필러 30만원~"` |

**교차 검증 규칙** (model_validator):

| 조건 | 결과 |
|------|------|
| `menu_type=TAB` + `items`가 비어있음 | ValidationError: `"items must be non-empty when menu_type is TAB"` |
| `menu_type=TEXT` + `price_text`가 없음 | ValidationError: `"price_text must be non-empty when menu_type is TEXT"` |
| `menu_type=TAB` + `items`에 데이터 있음 | 정상 |
| `menu_type=TEXT` + `price_text`에 텍스트 있음 | 정상 |

**사용 예시**:

```python
# 음식점 (구조화된 메뉴)
menu = NaverMenuInfo(
    menu_type=NaverMenuType.TAB,
    items=[
        NaverMenuItem(name="김치찌개", price="9,000원"),
        NaverMenuItem(name="된장찌개", price="9,000원"),
    ]
)

# 병원/클리닉 (텍스트 기반 가격정보)
menu = NaverMenuInfo(
    menu_type=NaverMenuType.TEXT,
    price_text="쌍꺼풀 수술 50만원~\n코필러 30만원~\n보톡스 5만원~"
)
```

---

## 6. 장소 모델 (Aggregate Root)

### NaverPlace

네이버맵 장소의 전체 크롤링 데이터. `BasePlace`를 상속.

#### BasePlace 상속 필드

`base.py`의 `BasePlace`에서 상속받는 공통 필드:

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `name` | `str` | O | - | 상호명 (최소 1자) | `"맛있는 한식당"` |
| `category` | `str` | O | - | 카테고리명 (최소 1자) | `"한식"`, `"피부과"` |
| `road_address` | `Optional[str]` | X | `None` | 도로명 주소 | `"서울특별시 강남구 테헤란로 123"` |
| `parcel_address` | `Optional[str]` | X | `None` | 지번 주소 (구주소) | `"서울특별시 강남구 역삼동 123-45"` |
| `phone` | `Optional[str]` | X | `None` | 전화번호 | `"02-1234-5678"` |
| `coordinates` | `Optional[Coordinates]` | X | `None` | WGS84 좌표 (base.py) | - |

#### NaverPlace 고유 필드

| 필드 | 타입 | 필수 | 기본값 | 설명 | 예시 |
|------|------|------|--------|------|------|
| `id` | `NaverPlaceId` | O | - | 네이버 고유 장소 ID (숫자 문자열) | `"1612729816"` |
| `description` | `Optional[str]` | X | `None` | 장소 소개/설명 텍스트 | `"30년 전통의 한식 전문점"` |
| `homepage_url` | `Optional[str]` | X | `None` | 공식 홈페이지 URL | `"https://example.com"` |
| `image_urls` | `list[str]` | X | `[]` | 장소 사진 URL 목록 | `["http://...", ...]` |
| `facilities` | `list[str]` | X | `[]` | 편의시설 목록 | `["주차", "WiFi", "단체석"]` |
| `business_hours` | `list[NaverBusinessHour]` | X | `[]` | 요일별 영업시간 (위 참조) | - |
| `review_stats` | `NaverReviewStats` | X | (기본값) | 리뷰 통계 (위 참조) | - |
| `menu_info` | `Optional[NaverMenuInfo]` | X | `None` | 메뉴 정보 (위 참조). 메뉴 없는 장소는 `None` | - |
| `crawl` | `CrawlMetadata` | X | (자동 생성) | 크롤 메타데이터 (source=NAVER) | - |

**검증 규칙**:

1. **영업시간 요일 중복 방지**: `business_hours` 내에 같은 요일이 2번 이상 나오면 ValidationError
   ```
   "Duplicate day_of_week entries found"
   ```

2. **이미지 URL 자동 중복 제거**: `image_urls`에 같은 URL이 여러 번 들어오면 자동으로 중복 제거 (순서 유지)

3. **홈페이지 URL 정규화**: 카카오맵과 동일한 로직
   - `//example.com` → `https://example.com`
   - `example.com` → `https://example.com`
   - 빈 문자열 → `None`

---

## 7. JSON 파서

### NaverPlaceParser

네이버맵의 원본 JSON/HTML 데이터를 `NaverPlace` 모델로 변환하는 유틸리티 클래스.

**주요 메서드**:

| 메서드 | 입력 | 출력 | 설명 |
|--------|------|------|------|
| `parse(raw_data, search_query?, source_url?)` | 원본 dict | `NaverPlace` | 전체 파싱 (메인 진입점) |
| `parse_business_hours(raw_hours)` | list[dict] | `list[NaverBusinessHour]` | 영업시간 파싱 (한국어 요일 자동 변환) |
| `parse_menu_info(raw_data)` | 전체 dict | `Optional[NaverMenuInfo]` | 메뉴 정보 파싱 (TAB/TEXT 자동 판별) |
| `parse_review_stats(raw_data)` | 전체 dict | `NaverReviewStats` | 리뷰 통계 파싱 |
| `parse_coordinates(raw_data)` | 전체 dict | `Optional[Coordinates]` | 좌표 파싱 |

**영업시간 파싱 상세**:

파서는 다양한 형식의 요일 데이터를 처리할 수 있음:
- 영문 대문자: `"MON"`, `"TUE"` → 직접 enum 매핑
- 한국어: `"월"`, `"월요일"` → `DayOfWeek.from_korean()` 사용
- 파싱 실패한 항목은 건너뛰고 계속 진행

브레이크타임 파싱:
- `"13:00 - 14:00"` 형식의 문자열을 `break_start`/`break_end`로 자동 분리
- HH:MM 형식이 아닌 경우 `None` 처리

**메뉴 자동 유형 판별**:

파서가 실제 데이터 유무에 따라 `menu_type`을 자동 보정:
- `items`가 있고 `price_text`가 없으면 → `TAB`으로 설정
- `items`가 없고 `price_text`가 있으면 → `TEXT`로 설정

**필드명 호환 처리**:

파서는 camelCase와 snake_case 필드명을 모두 지원:

| snake_case | camelCase | 설명 |
|------------|-----------|------|
| `business_hours` | `businessHours` | 영업시간 |
| `visitor_reviews` | `visitorReviews` | 방문자 리뷰 수 |
| `blog_reviews` | `blogReviews` | 블로그 리뷰 수 |
| `is_day_off` | `isDayOff` | 휴무일 여부 |
| `open_time` | `startTime` | 영업 시작 |
| `close_time` | `endTime` | 영업 종료 |
| `place_id` | `id` | 장소 ID |
| `homepage_url` | `homepage` | 홈페이지 |
| `image_urls` | `images` | 이미지 목록 |

**사용 예시**:

```python
raw_json = await naver_client.fetch_place("1612729816")

place = NaverPlaceParser.parse(
    raw_data=raw_json,
    search_query="강남역 피부과",
    source_url="https://map.naver.com/v5/entry/place/1612729816",
)

print(place.name)                     # "맛있는 한식당"
print(place.review_stats.total_reviews)  # 192
print(place.business_hours[0].day_of_week)  # DayOfWeek.MON
```

**에러 처리**:
- 필수 필드(`id`, `name`) 누락 시 `ValueError` 발생
- `category`가 없으면 `"기타"`로 기본값 설정
- 개별 메뉴/영업시간 파싱 실패 시 해당 항목만 건너뛰고 계속 진행

---

## 8. 필드 매핑표

네이버맵 크롤링 데이터의 필드와 모델 간 전체 매핑.

### 기본 정보

| 소스 필드 | 모델 필드 | 타입 | 필수 | 설명 |
|-----------|-----------|------|------|------|
| `id` / `place_id` | `NaverPlace.id` | NaverPlaceId | O | 고유 장소 ID |
| `name` | `NaverPlace.name` | str | O | 상호명 |
| `category` | `NaverPlace.category` | str | O | 카테고리 |
| `road_address` / `address` | `NaverPlace.road_address` | str? | X | 도로명 주소 |
| `parcel_address` | `NaverPlace.parcel_address` | str? | X | 지번 주소 |
| `phone` | `NaverPlace.phone` | str? | X | 전화번호 |
| `description` | `NaverPlace.description` | str? | X | 소개 텍스트 |
| `homepage_url` / `homepage` | `NaverPlace.homepage_url` | str? | X | 홈페이지 |
| `image_urls` / `images` | `NaverPlace.image_urls` | list[str] | X | 사진 URL 목록 |
| `facilities` | `NaverPlace.facilities` | list[str] | X | 편의시설 목록 |
| `latitude` / `y` | `Coordinates.latitude` | float | X | 위도 |
| `longitude` / `x` | `Coordinates.longitude` | float | X | 경도 |

### 영업시간

| 소스 필드 | 모델 필드 | 타입 | 설명 |
|-----------|-----------|------|------|
| `day` / `day_of_week` | `NaverBusinessHour.day_of_week` | DayOfWeek | 요일 |
| `open_time` / `startTime` | `NaverBusinessHour.open_time` | str? | 시작 시간 |
| `close_time` / `endTime` | `NaverBusinessHour.close_time` | str? | 종료 시간 |
| `break_time` / `breakTime` | → `break_start` + `break_end` | str? | 자동 분리 |
| `is_day_off` / `isDayOff` | `NaverBusinessHour.is_day_off` | bool | 휴무 여부 |

### 리뷰 통계

| 소스 필드 | 모델 필드 | 타입 | 설명 |
|-----------|-----------|------|------|
| `review_stats.visitor_reviews` | `NaverReviewStats.visitor_reviews` | int | 방문자 리뷰 수 |
| `review_stats.blog_reviews` | `NaverReviewStats.blog_reviews` | int | 블로그 리뷰 수 |
| `review_stats.rating` | `NaverReviewStats.rating` | float? | 평균 별점 |

### 메뉴

| 소스 필드 | 모델 필드 | 타입 | 설명 |
|-----------|-----------|------|------|
| `menuInfo.type` / `menu_type` | `NaverMenuInfo.menu_type` | NaverMenuType | 메뉴 유형 |
| `menuInfo.items` / `menuList` | `NaverMenuInfo.items` | list[NaverMenuItem] | 메뉴 항목 |
| `menuInfo.priceText` / `price_text` | `NaverMenuInfo.price_text` | str? | 가격 텍스트 |

---

## 9. 장소 유형별 데이터 차이

네이버맵은 장소 유형에 따라 제공되는 데이터가 다름.

### 음식점/카페

| 특징 | 설명 |
|------|------|
| 메뉴탭 | 있음 → `NaverMenuType.TAB` 사용 |
| 메뉴 구조 | 개별 항목 (`NaverMenuItem`)으로 구조화됨 |
| 사진 | 음식 사진 다수 |
| 리뷰 | 방문자 리뷰가 많음 |
| 영업시간 | 상세하게 제공됨 (브레이크타임 포함) |
| 편의시설 | 주차, WiFi, 단체석, 배달 등 |

```python
# 음식점 예시
NaverPlace(
    id="1612729816",
    name="맛있는 한식당",
    category="한식",
    menu_info=NaverMenuInfo(
        menu_type=NaverMenuType.TAB,
        items=[
            NaverMenuItem(name="김치찌개", price="9,000원"),
            NaverMenuItem(name="불고기", price="15,000원", is_popular=True),
        ]
    ),
    facilities=["주차", "WiFi", "단체석"],
    ...
)
```

### 병원/클리닉

| 특징 | 설명 |
|------|------|
| 메뉴탭 | 없거나 제한적 → `NaverMenuType.TEXT` 또는 `None` 사용 |
| 가격정보 | 텍스트 블록으로 제공됨 |
| 사진 | 내부/외부 사진 위주 |
| 리뷰 | 방문자 리뷰는 적고 블로그 리뷰가 많을 수 있음 |
| 영업시간 | 진료시간, 점심시간 구분 |
| 편의시설 | 주차, 예약 가능 등 |

```python
# 병원/클리닉 예시
NaverPlace(
    id="9876543210",
    name="OO피부과의원",
    category="피부과",
    menu_info=NaverMenuInfo(
        menu_type=NaverMenuType.TEXT,
        price_text="쌍꺼풀 수술 50만원~\n코필러 30만원~\n보톡스 5만원~"
    ),
    business_hours=[
        NaverBusinessHour(
            day_of_week=DayOfWeek.MON,
            open_time="10:00", close_time="19:00",
            break_start="13:00", break_end="14:00",
        ),
        NaverBusinessHour(day_of_week=DayOfWeek.SUN, is_day_off=True),
    ],
    ...
)
```

### 서비스업 (미용실, 네일샵 등)

| 특징 | 설명 |
|------|------|
| 메뉴탭 | 있을 수 있음 → `TAB` 또는 `TEXT` |
| 가격정보 | 서비스별 가격 제공 |
| 영업시간 | 보통 고정 (브레이크타임 없는 경우 많음) |
| 편의시설 | 예약 가능, 주차 등 |

```python
# 미용실 예시
NaverPlace(
    id="5555555555",
    name="스타일 헤어샵",
    category="미용실",
    menu_info=NaverMenuInfo(
        menu_type=NaverMenuType.TAB,
        items=[
            NaverMenuItem(name="커트", price="20,000원"),
            NaverMenuItem(name="염색", price="50,000원~"),
            NaverMenuItem(name="펌", price="70,000원~"),
        ]
    ),
    ...
)
```

### menu_info가 None인 경우

메뉴/가격 정보가 전혀 없는 장소 (관공서, 공원, ATM 등):

```python
NaverPlace(
    id="1111111111",
    name="OO동 주민센터",
    category="관공서",
    menu_info=None,  # 메뉴/가격 정보 없음
    ...
)
```
