# Keyword Validation Snapshot (2026-02-23 JST)

## Method
- Source: x.com live search (`f=live`)
- Runner: Playwright persistent burner session
- Sampling: load + 2 scrolls
- Metrics:
  - `articles`: number of tweet cards in DOM
  - `recent_30d`: count of tweets within 30 days among first 25 cards

## Existing Pool Highlights
- Strong: `レーザー治療 (16)`, `ピコレーザー (14)`, `韓国クリニック (11)`, `韓国皮膚科 (10)`
- Strong hashtag: `#韓国美容 (10)`, `#韓国肌管理 (8)`
- Weak in this sample: `#渡韓美容`, `#ポテンツァ`, `#ピコレーザー`

## Persona Candidate Highlights
- Price: `韓国 美容 コスパ (10)`, `韓国 美容 料金 (9)`, `韓国 施術 価格 (8)`
- Beginner: `韓国 皮膚科 初めて (10)`, `初渡韓 美容 (9)`, `韓国 皮膚科 おすすめ (7)`
- Procedure: `ポテンツァ (17)`, `ピコトーニング (13)`, `リジュラン 韓国 (9)`
- Risk: `韓国 追加料金 (5)`, `韓国 皮膚科 トラブル (4)`
- Lifestyle: `韓国 美容 よかった (10)`, `渡韓美容 レポ (7)`

## Notes
- `recent_30d = 0`인 키워드는 완전 제거 대신 secondary로 보관.
- 키워드는 월 1회 동일 방식 재검증 권장.
