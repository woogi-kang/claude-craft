# X Post Templates

Templates and voice guide for generating @ask.nandemo Japanese X posts about Korean dermatology.
Based on actual 渡韓美容 community writing patterns and the existing @ask.nandemo voice.

## Voice Guide

### Persona
- Korean dermatology data researcher who shares what they find
- NOT a clinic, NOT an influencer, NOT a medical professional
- "全部調べてまとめてる人" (the person who researched and compiled everything)
- Honest about risks and downsides, not just hype

### Tone: カジュアル常体 (Casual Plain Form)

The @ask.nandemo voice uses **常体 (plain form) as base** with occasional です/ます for softening.
This matches the 渡韓美容 X community where users post like talking to friends.

**Base form**: 常体 (plain/casual)
- ～だよ、～だった、～してきた、～かも、～よね
- ～って知ってた？ ～なんだけど、～してみた

**Softening (occasional)**: ます/です mix
- Only for CTA or friendly advice: ～してね、～だよ、～どうぞ

**NEVER use**: Full です/ます throughout (sounds like a clinic ad or press release)

### Sentence Patterns (実際の渡韓美容コミュニティから)

**Hooks (1st line - must stop the scroll)**:
- ～って知ってた？ (Did you know ~?)
- ～の価格差がエグい (The price gap for ~ is insane)
- ～、受ける前にこれ読んで (Read this before getting ~)
- ～調べたら面白いことわかった (Found something interesting researching ~)
- 正直に言う。～ (I'll be honest. ~)

**Data presentation**:
- 約X万円 / 約X,000円 (abbreviated yen format)
- X万ウォン（約Y円） (won with yen conversion in parentheses)
- X倍の差 (X times difference)
- X%オフ (X% off)

**Pain descriptions (擬態語 required)**:
- チクチク (prickling - needles)
- ヒリヒリ (stinging - post-treatment)
- ピリピリ (tingling - mild sensation)
- ジンジン (throbbing - deeper pain)
- ズキズキ (pulsing - acute pain)
- Comparison format: "インフルワクチンほどではない" "我慢できるレベル"

**Effect descriptions (美容SNS定型)**:
- ツルツル (smooth skin texture)
- もちもち (bouncy/plump)
- ぷるぷる (dewy/hydrated)
- つやつや / ツヤ肌 (glossy/radiant)
- 肌のキメが整う (skin texture evens out)

**Casual emphasis**:
- めっちゃ / めちゃくちゃ (very/extremely)
- マジで (seriously)
- ガチで (genuinely/for real)
- 全然違う (completely different)
- 顔面課金 (face investment - popular slang)

**Line breaks**: Use generously. One idea per line. Mobile readability first.

### What NOT to Do

- 【brackets】for every section - looks like a clinic brochure
- Full です/ます polite form throughout - sounds like corporate PR
- "ご紹介します" "ご覧ください" - too formal for X
- "施術をお受けになる前に" - honorific keigo is wrong register
- Long unbroken paragraphs - unreadable on mobile
- 4+ emoji per post - looks spammy
- "絶対" "必ず効く" "確実に" - absolute claims are both wrong and untrustworthy

## Character Counting Rules

**Account tier: FREE (280 weighted character hard limit)**

X character limits for Japanese (weighted):
- Japanese full-width characters (hiragana, katakana, kanji, full-width symbols): weight 2
- ASCII half-width characters (a-z, 0-9, basic punctuation): weight 1
- Weighted total must NOT exceed 280 (FREE account hard limit)
- Hashtags: include # (weight 1) + text in character count
- URLs: always count as 23 weight regardless of length
- Line breaks: weight 1 each

**Target: 200-250 weighted characters (strict buffer for free account)**
- Under 250: safe to post
- 250-270: acceptable but tight
- Over 270: MUST trim before posting
- Over 280: WILL BE REJECTED by X

**Validation step (REQUIRED before finalizing any post)**:
1. Count each line's weighted characters
2. Add line break weights (1 per \n)
3. Sum total and confirm under 250 (ideal) or 270 (max)
4. If over limit: shorten lines, reduce hashtags to 2, remove filler words

Note: This is the X API weighting system. "約2万円" = 約(2)+2(1)+万(2)+円(2) = 7 weighted.

## Content Pillars

### Pillar 1: 施術なるほどメモ (Treatment Deep-dive)

Specific treatment info in digestible format.

**Template 1A: Quick Explainer**
```
{treatment_jp}ってなに？

簡単に言うと、{one_line_principle_casual}

痛み: {onomatopoeia}（{pain_level}/5）
ダウンタイム: {downtime}
韓国価格: 約{price_jpy}円
持続: {duration}

{one_relatable_fact}

#渡韓美容 #{treatment_hashtag}
```

**Template 1B: Before You Get This**
```
{treatment_jp}、受ける前にこれだけは知っておいて

・{point_1_casual}
・{point_2_casual}
・{point_3_casual}

知らずに受けて後悔してる人、結構いる

#渡韓美容 #韓国皮膚科
```

**Template 1C: VS Comparison**
```
{treatment_A} vs {treatment_B}、どっちがいい？

{treatment_A}→{key_point_A_casual}
{treatment_B}→{key_point_B_casual}

{concern}なら{recommendation}の方がいいかも

#渡韓美容 #{hashtag}
```

**Template 1D: Pain Reality**
```
{treatment_jp}の痛み、正直に言う

{pain_description_with_onomatopoeia}

{comparison_to_relatable_experience}

でも{positive_tradeoff}から我慢できるレベル

#渡韓美容 #{treatment_hashtag}
```

### Pillar 2: データで見る韓国皮膚科 (Price/Data Comparison)

Numbers-first format that builds credibility.

**Template 2A: Price Gap**
```
{treatment_jp}の日韓価格差

日本: 約{price_jp}円
韓国: 約{price_kr_jpy}円

{savings}円の差。{percent}%オフ

麻酔・アフターケア込みでこの値段

#渡韓美容 #韓国美容
```

**Template 2B: Bundle Math**
```
韓国で{treatment_1}+{treatment_2}受けた場合

施術: 約{total_kr}円
航空券+ホテル: 約{travel}円
合計: 約{grand_total}円

日本で{treatment_1}だけで{jp_price}円するから
{treatment_2}が実質タダ以下になる計算

#渡韓美容 #韓国皮膚科
```

**Template 2C: Price List**
```
韓国の皮膚科、だいたいこんな値段

シュリンク 300shot: 約{price}円
リジュラン 1cc: 約{price}円
ボトックス(額): 約{price}円
ピコスポット(1個): 約{price}円

クリニックで結構差あるから比較大事

#渡韓美容 #韓国美容医療
```

**Template 2D: Data Surprise**
```
{number_or_stat}

調べてて「マジか」ってなったデータ

{context_and_explanation}

#渡韓美容 #{relevant_hashtag}
```

### Pillar 3: それ誤解かも (Myth-busting)

Correct misconceptions with data.

**Template 3A: Common Myth**
```
「{common_myth_in_quotes}」

これ、よくある誤解

実際は{truth_casual}

{supporting_data_or_number}

#渡韓美容 #韓国皮膚科
```

**Template 3B: Honest Take**
```
正直に言う。{topic}について

{honest_opinion_with_data}

{balanced_conclusion}

気になることあればリプかDMで聞いて

#渡韓美容 #{hashtag}
```

### Pillar 4: はじめての渡韓美容 (Clinic Tips)

Practical info for first-timers.

**Template 4A: Tips List**
```
韓国の皮膚科で{topic}するときのコツ

・{tip_1_casual}
・{tip_2_casual}
・{tip_3_casual}

知ってるかどうかで全然違う

#渡韓美容 #韓国皮膚科
```

**Template 4B: Warning**
```
韓国の皮膚科選び、ここだけは注意

{red_flag_casual}

見分け方: {how_to_check_casual}

DB作ってるからこそ見えてくること

#渡韓美容 #韓国美容
```

**Template 4C: Quick FAQ**
```
よく聞かれるから書いとく

Q: {question_casual}
A: {answer_casual}

{additional_one_liner}

他にも聞きたいことあったらリプで

#渡韓美容 #{hashtag}
```

### Pillar 5: トレンドメモ (Seasonal/Trend)

What's hot and timely.

**Template 5A: Trending Treatment**
```
今韓国で一番人気の施術、{treatment_jp}

理由↓
・{reason_1_casual}
・{reason_2_casual}

韓国価格: 約{price}円

#渡韓美容 #{treatment_hashtag}
```

**Template 5B: Seasonal**
```
{season}に受けるなら{treatment_jp}がいい理由

{seasonal_reason_casual}

ダウンタイム{downtime}だから{season}なら{recovery_context}

#渡韓美容 #韓国皮膚科
```

### Pillar 6: みんなに聞いてみた (Engagement)

Drive replies and interaction.

**Template 6A: Poll-style Question**
```
韓国で施術受けるとき一番不安なのは？

1. {option_1}
2. {option_2}
3. {option_3}
4. {option_4}

リプで教えて！

#渡韓美容 #韓国美容
```

**Template 6B: Open Question**
```
{open_question_casual}

リプで教えてくれたら調べてまとめるよ

#渡韓美容
```

## Hashtag Strategy

### Tier 1: Anchor (every post, pick 1-2)
- `#渡韓美容` (REQUIRED - community anchor tag, never skip)
- `#韓国皮膚科` or `#韓国美容` (pick based on topic)

### Tier 2: Topic (pick 1 when relevant)
Treatment: `#ポテンツァ` `#シュリンク` `#リジュラン` `#ボトックス` `#フィラー` `#ピコレーザー` `#ダーマペン` `#水光注射` `#アートメイク` `#ジュベルック` `#サーマージュ` `#ウルセラ` `#インモード`
Area: `#江南美容` `#明洞美容`
General: `#韓国美容医療` `#韓国クリニック` `#韓国肌管理`

### Tier 3: Discovery (initial growth phase only, pick 0-1)
- `#美容垢さんと繋がりたい` (community building)

### Total: 2-4 hashtags per post. Less is more.

## Post Generation Checklist

1. **Weighted character count under 250** (FREE account, 280 hard limit)
2. First line is a hook (question, surprising fact, or direct address)
3. Contains 1+ specific data point (price, percentage, number)
4. Uses 常体 (casual plain form) as base, NOT full です/ます
5. Pain/effect descriptions use 擬態語 (onomatopoeia)
6. Line breaks between every thought (mobile-first)
7. 2-3 hashtags with `#渡韓美容` always present (fewer hashtags = more content space)
8. No absolute medical claims
9. Reads like a person, not a clinic brochure
10. 0-2 emoji maximum (less is better for this account)
11. **Final validation**: show weighted character count breakdown in post rationale
