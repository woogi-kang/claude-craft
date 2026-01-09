# Tech Blog SEO Guide

> Comprehensive SEO optimization guide for woogi's Hashnode blog.
> Covers keyword research, on-page SEO, technical SEO, and Hashnode-specific settings.

---

## Table of Contents
- [1. Keyword Research](#1-keyword-research)
- [2. Title Optimization](#2-title-optimization)
- [3. Meta Description](#3-meta-description)
- [4. URL Slug](#4-url-slug)
- [5. Content Structure](#5-content-structure)
- [6. Image SEO](#6-image-seo)
- [7. Internal & External Links](#7-internal--external-links)
- [8. Hashnode SEO Settings](#8-hashnode-seo-settings)
- [9. Schema Markup](#9-schema-markup)
- [10. SEO Checklist](#10-seo-checklist)

---

## 1. Keyword Research

### Before Writing: Find Your Keywords

Every blog post should target **1 primary keyword** and **2-3 secondary keywords**.

### Keyword Research Process

```yaml
keyword_research:
  step_1_brainstorm:
    - What would someone search to find this content?
    - What problem are they trying to solve?
    - What terms do developers actually use?

  step_2_validate:
    tools:
      - Google Search (autocomplete suggestions)
      - Google Trends (compare terms)
      - AnswerThePublic (question-based keywords)
      - Also Asked (related questions)

  step_3_analyze_intent:
    informational: "what is React Server Components"
    tutorial: "how to use React Server Components"
    comparison: "React Server Components vs SSR"
    troubleshooting: "React Server Components not working"
```

### Keyword Placement Strategy

| Location | Priority | Example |
|----------|----------|---------|
| **Title (H1)** | Must have | "Flutter vs React Native in 2025" |
| **First 100 words** | Must have | Mention primary keyword naturally |
| **URL slug** | Must have | `/flutter-vs-react-native-2025` |
| **Meta description** | Must have | Include keyword + value proposition |
| **H2 headings** | Should have | Use secondary keywords |
| **Image alt text** | Should have | Descriptive + keyword if natural |
| **Throughout content** | Natural | Don't force it; 1-2% density max |

### Keyword Research Output Template

```yaml
seo_keywords:
  primary: "Flutter vs React Native"
  secondary:
    - "cross-platform development 2025"
    - "Flutter or React Native which to choose"
    - "mobile app framework comparison"
  long_tail:
    - "Flutter vs React Native performance benchmark"
    - "Flutter vs React Native job market"
  search_intent: "comparison"
  estimated_difficulty: "medium"
```

---

## 2. Title Optimization

### Title Formula

```
[Primary Keyword] + [Value/Hook] + [Year if relevant]
```

### Title Rules

| Rule | Good | Bad |
|------|------|-----|
| **Length** | 50-60 characters | Too long gets truncated |
| **Keyword position** | Front-loaded | Buried at the end |
| **Numbers** | Odd numbers (5, 7, 9) | Round numbers less effective |
| **Power words** | "Honest", "Complete", "Essential" | Generic words |

### Title Examples for Tech Blogs

```markdown
✓ "Flutter vs React Native in 2025: The Honest Truth"
✓ "7 TypeScript Patterns Every Developer Should Know"
✓ "Understanding React Server Components: A Practical Guide"
✓ "Why I Stopped Using Redux (And What I Use Instead)"

✗ "A Blog Post About Flutter and React Native Comparison for Developers"
✗ "Some Tips for TypeScript"
✗ "React Server Components Explained"
```

### SEO Title vs Display Title

Hashnode allows separate SEO title. Use this for:
- Longer display title on the page
- Shorter, keyword-optimized SEO title for search

```yaml
display_title: "Flutter vs React Native in 2025: The Honest Truth About Choosing Your Framework"
seo_title: "Flutter vs React Native 2025: Complete Comparison"
```

---

## 3. Meta Description

### Meta Description Formula

```
[Pain point/Question] + [What you'll learn] + [CTA/Hook]
```

### Rules

| Aspect | Guideline |
|--------|-----------|
| **Length** | 150-160 characters |
| **Keyword** | Include primary keyword once |
| **Action words** | "Learn", "Discover", "Find out" |
| **Unique value** | What makes this post different? |

### Examples

```markdown
✓ "Flutter has more stars but React Native has 6x more jobs.
   Learn which framework to choose in 2025 based on your goals."
   (147 characters)

✓ "Struggling to choose between Flutter and React Native?
   I break down performance, jobs, and real-world usage to help you decide."
   (138 characters)

✗ "This is a blog post about Flutter vs React Native comparison."
   (Too generic, no value proposition)
```

### Hashnode Subtitle = Meta Description

In Hashnode, the `subtitle` field becomes the meta description:

```yaml
---
title: "Flutter vs React Native in 2025: The Honest Truth"
subtitle: "More developers prefer Flutter, but there are 6x more React Native jobs. Here's how to think about this."
---
```

---

## 4. URL Slug

### Slug Rules

| Rule | Example |
|------|---------|
| **Include keyword** | `/flutter-vs-react-native` |
| **Keep it short** | 3-5 words ideal |
| **Use hyphens** | Not underscores |
| **Lowercase only** | Never mixed case |
| **Remove stop words** | Remove "the", "a", "in", etc. |
| **No dates in URL** | Update content, keep URL |

### Good vs Bad Slugs

```markdown
✓ /flutter-vs-react-native-2025
✓ /react-server-components-guide
✓ /typescript-patterns-developers

✗ /flutter-vs-react-native-in-2025-the-honest-truth-about-choosing
✗ /blog-post-about-flutter
✗ /post-12345
```

---

## 5. Content Structure

### Heading Hierarchy

```markdown
# H1: Title (only one per page - Hashnode handles this)

## H2: Main Sections
- Include secondary keywords
- Should outline the article structure

### H3: Subsections
- Break down complex topics
- Improve scannability

#### H4: Rare, for nested details
```

### SEO-Optimized Structure

```markdown
# Flutter vs React Native in 2025: The Honest Truth

## The Current State of Cross-Platform Development
[Intro + context - mention keyword naturally]

## Performance Comparison: Flutter vs React Native
[H2 with secondary keyword]

### How Flutter Achieves Better Performance
[H3 for details]

### React Native's New Architecture
[H3 for details]

## Developer Experience Comparison
[Another H2 section]

## Job Market: React Native vs Flutter
[H2 with keyword variation]

## Which Should You Choose?
[Conclusion with clear takeaways]
```

### Content Length Guidelines

| Type | Word Count | SEO Impact |
|------|------------|------------|
| Quick answer | 500-800 | Lower ranking potential |
| Standard post | 1,200-1,800 | Good balance |
| Comprehensive guide | 2,000-3,000 | Higher ranking potential |
| Ultimate guide | 3,000+ | Pillar content |

> **Tip:** For competitive keywords like "Flutter vs React Native", aim for 2,000+ words with comprehensive coverage.

---

## 6. Image SEO

### Image Optimization Checklist

```yaml
image_seo:
  file_name:
    good: "flutter-vs-react-native-architecture.png"
    bad: "IMG_12345.png" or "screenshot.png"

  alt_text:
    good: "Diagram comparing Flutter and React Native architecture"
    bad: "" (empty) or "image" or "flutter react native"

  format:
    diagrams: PNG or SVG
    photos: WebP or JPEG
    screenshots: PNG

  size:
    max_width: 1200px
    max_file_size: 200KB (compress!)

  lazy_loading: true (Hashnode handles this)
```

### Alt Text Best Practices

```markdown
✓ "Code snippet showing React Native bridge architecture"
✓ "Performance benchmark chart comparing Flutter and React Native startup times"
✓ "Screenshot of Flutter DevTools profiler"

✗ "image1"
✗ "flutter react native comparison image"
✗ "" (empty)
```

### Cover Image

- **Dimensions:** 1600x840px (Hashnode recommended)
- **Include text:** Title or key message
- **Branding:** Consistent style for woogi's blog
- **File name:** `flutter-vs-react-native-cover.png`

---

## 7. Internal & External Links

### Internal Linking Strategy

```yaml
internal_links:
  purpose:
    - Keep readers on your blog
    - Distribute page authority
    - Improve navigation

  rules:
    - Link to 2-3 related posts per article
    - Use descriptive anchor text
    - Link naturally within content

  example:
    good: "I covered [React hooks in detail](/react-hooks-guide) previously"
    bad: "Click [here](/react-hooks-guide) for more"
```

### External Linking Strategy

```yaml
external_links:
  purpose:
    - Add credibility (cite sources)
    - Provide additional resources
    - Show expertise through curation

  rules:
    - Link to authoritative sources (official docs, research)
    - Open in new tab (Hashnode default)
    - 3-5 external links per post
    - Avoid linking to competitors' similar content

  good_sources:
    - Official documentation (flutter.dev, reactnative.dev)
    - GitHub repositories
    - Research papers / surveys
    - Reputable tech blogs (confirmed stats)
```

### Anchor Text Optimization

```markdown
✓ "According to the [Stack Overflow 2024 survey](url)..."
✓ "Check the [official Flutter documentation](url) for details"
✓ "I wrote about [state management patterns](/state-management) before"

✗ "Click [here](url) for more info"
✗ "[Link](url)"
✗ "Read more at [https://flutter.dev/docs/...](url)"
```

---

## 8. Hashnode SEO Settings

### Hashnode-Specific SEO Fields

```yaml
hashnode_seo:
  # Basic SEO
  title: "Flutter vs React Native 2025"  # SEO title (can differ from display)
  subtitle: "Meta description here..."    # Becomes meta description
  slug: "flutter-vs-react-native-2025"   # URL path

  # Open Graph (Social Sharing)
  og_image: "url-to-cover-image"         # Social share image
  og_title: "Flutter vs React Native"    # Social title
  og_description: "..."                  # Social description

  # Advanced
  canonical_url: ""                       # If cross-posting from another site
  no_index: false                         # Keep false for SEO

  # Tags (also affect discoverability)
  tags:
    - "flutter"
    - "react-native"
    - "mobile-development"
    - "cross-platform"
```

### GraphQL Mutation with SEO

```graphql
mutation PublishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post {
      id
      url
      seo {
        title
        description
      }
    }
  }
}

# Input variables
{
  "input": {
    "title": "Flutter vs React Native in 2025: The Honest Truth",
    "subtitle": "More developers prefer Flutter, but there are 6x more React Native jobs.",
    "slug": "flutter-vs-react-native-2025",
    "publicationId": "YOUR_PUB_ID",
    "contentMarkdown": "...",
    "tags": [
      { "slug": "flutter" },
      { "slug": "react-native" }
    ],
    "coverImageOptions": {
      "coverImageURL": "https://..."
    },
    "settings": {
      "isTableOfContentEnabled": true
    },
    "seo": {
      "title": "Flutter vs React Native 2025: Complete Comparison",
      "description": "Compare Flutter and React Native in 2025..."
    }
  }
}
```

---

## 9. Schema Markup

### Article Schema (Hashnode Auto-generates)

Hashnode automatically adds basic Article schema. For enhanced SEO, ensure:

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Flutter vs React Native in 2025: The Honest Truth",
  "author": {
    "@type": "Person",
    "name": "woogi"
  },
  "datePublished": "2025-01-04",
  "dateModified": "2025-01-04",
  "description": "Compare Flutter and React Native...",
  "image": "cover-image-url",
  "publisher": {
    "@type": "Organization",
    "name": "woogi's Tech Blog"
  }
}
```

### FAQ Schema (Manual - for Q&A style posts)

If your post answers common questions, add FAQ schema:

```markdown
## Frequently Asked Questions

### Which is better, Flutter or React Native?
It depends on your team's expertise and project needs...

### Is Flutter faster than React Native?
Yes, Flutter typically performs better due to...
```

This can be marked up for rich snippets in search results.

---

## 10. SEO Checklist

### Pre-Writing

- [ ] Primary keyword identified
- [ ] Secondary keywords (2-3) identified
- [ ] Search intent understood (informational/tutorial/comparison)
- [ ] Competitor content analyzed

### Title & Meta

- [ ] Title is 50-60 characters
- [ ] Primary keyword in title (front-loaded)
- [ ] Meta description is 150-160 characters
- [ ] Meta description includes keyword + value prop
- [ ] URL slug is short, includes keyword

### Content

- [ ] Keyword in first 100 words
- [ ] H2s include secondary keywords
- [ ] Content is comprehensive (word count appropriate)
- [ ] Headers create logical structure
- [ ] Content matches search intent

### Images

- [ ] Cover image set (1600x840px)
- [ ] All images have descriptive alt text
- [ ] Image file names are descriptive
- [ ] Images are compressed (<200KB)

### Links

- [ ] 2-3 internal links to related posts
- [ ] 3-5 external links to authoritative sources
- [ ] Anchor text is descriptive (not "click here")

### Hashnode Settings

- [ ] SEO title set (if different from display title)
- [ ] Subtitle/meta description optimized
- [ ] Slug is clean and keyword-rich
- [ ] Tags are relevant (max 5)
- [ ] Table of contents enabled (for long posts)

### Post-Publish

- [ ] Google Search Console: Request indexing
- [ ] Share on social media
- [ ] Monitor Search Console for impressions/clicks
- [ ] Update content if rankings plateau

---

## Quick Reference: SEO Output Template

```yaml
seo_optimization:
  keywords:
    primary: "Flutter vs React Native"
    secondary: ["cross-platform 2025", "mobile framework comparison"]

  title:
    display: "Flutter vs React Native in 2025: The Honest Truth"
    seo: "Flutter vs React Native 2025: Complete Comparison"
    length: 56

  meta_description: "More developers prefer Flutter, but there are 6x more React Native jobs. Learn which framework to choose based on performance, jobs, and your goals."
  meta_length: 158

  slug: "flutter-vs-react-native-2025"

  headings:
    h2_count: 6
    keywords_in_h2: ["Performance", "Developer Experience", "Job Market"]

  images:
    cover: "flutter-vs-react-native-cover.png"
    alt_texts_complete: true

  links:
    internal: 2
    external: 5

  word_count: 1850
  estimated_read_time: "8 min"
```
