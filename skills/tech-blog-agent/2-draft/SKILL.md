---
name: blog-draft
description: |
  Draft writing skill for tech blog.
  Creates blog post draft based on research, with woogi's voice and selected tone.
  Follows STYLE_GUIDE.md for writing patterns inspired by Dan Abramov, Josh Comeau, and Kent C. Dodds.
  Activated by: "/blog-draft" or "write draft for [topic]"
---

# Blog Draft Skill

Writes blog post drafts for woogi's tech blog based on research output.

> **Important**: Always reference `agents/tech-blog-agent/STYLE_GUIDE.md` for voice, tone, hooks, and structure patterns.

## Trigger Commands

- `/blog-draft`
- `/blog-draft --tone casual`
- `/blog-draft --tone professional`
- `write draft for [topic]`

## Prerequisites

Requires research output from **1-research** skill:
- `work-blog/research/{topic-slug}-research.md`

## Tone Selection

### Casual & Friendly (`--tone casual`)
```
Voice characteristics:
- "Hey folks, let me show you something cool..."
- "I ran into this problem last week and here's how I solved it"
- Uses contractions, direct address
- Personal anecdotes welcome
- Emoji sparingly allowed
```

### Professional (`--tone professional`)
```
Voice characteristics:
- "This article explores the implementation of..."
- "Consider the following approach..."
- Precise technical language
- Structured argumentation
- Focus on best practices
```

### Mixed (Default)
```
Voice characteristics:
- Professional content, friendly delivery
- "I'm going to walk you through..."
- Technical accuracy with accessible tone
- Balance of "I" and educational framing
```

## Core Functions

### 1. research_load (Load Research)

Reads research output and prepares for drafting.

**Process:**
- Load research markdown file
- Parse topic analysis, insights, sources
- Identify key code examples
- Review suggested outline

### 2. structure_create (Article Structure)

Creates the blog post structure with Hashnode-compatible frontmatter.

**Output Template:**
```markdown
---
title: "{Engaging Title}"
subtitle: "{Optional subtitle}"
tags: ["tag1", "tag2", "tag3"]
cover_image: ""
canonical_url: ""
---

# {Title}

{Hook paragraph}

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
...

{Content sections}
```

### 3. intro_write (Write Introduction)

Crafts engaging introduction as woogi.

**Casual Example:**
```markdown
Hey, I'm woogi! If you've been working with React lately,
you've probably heard about Server Components. I was skeptical
at first — "another paradigm shift?" — but after using them
in a real project, I'm convinced they're worth understanding.

Let me show you what I learned.
```

**Professional Example:**
```markdown
React Server Components represent a significant shift in how
we think about component architecture. In this article, I'll
break down the core concepts, demonstrate practical implementations,
and share insights from integrating RSC into production applications.
```

### 4. section_write (Write Content Sections)

Writes each section based on research insights.

**Section Template:**
```markdown
## {Section Title}

{Opening sentence connecting to previous section or main topic}

{Core explanation - 2-3 paragraphs}

{Code example if applicable}
```typescript
// Example code with comments
const example = () => {
  // woogi's tip: always explain why, not just how
};
```

{Key takeaway or transition to next section}
```

### 5. code_format (Format Code Examples)

Formats code examples for readability.

**Guidelines:**
- Language-specific syntax highlighting
- Meaningful variable names
- Comments explaining non-obvious parts
- Keep examples focused (avoid unrelated code)
- Show before/after when applicable

**Example:**
```typescript
// Before: Traditional client-side data fetching
function ClientComponent() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData().then(setData);
  }, []);

  if (!data) return <Loading />;
  return <div>{data}</div>;
}

// After: Server Component approach
async function ServerComponent() {
  const data = await fetchData(); // No loading state needed!
  return <div>{data}</div>;
}
```

### 6. conclusion_write (Write Conclusion)

Wraps up the article with woogi's signature style.

**Template:**
```markdown
## Wrapping Up

{Summary of key points - 1-2 sentences}

{Personal reflection or opinion}

{Call to action or next steps for reader}

---

Thanks for reading! If you found this helpful, let me know
in the comments. Got questions? I'm always happy to chat.

— woogi
```

### 7. seo_optimize (SEO Optimization) 🆕 Enhanced

Comprehensive SEO optimization based on keyword research.

> **Reference:** See `agents/tech-blog-agent/SEO_GUIDE.md` for detailed SEO strategy.

**Process:**

1. **Title Optimization**
   ```yaml
   title:
     display: "Flutter vs React Native in 2025: The Honest Truth"
     seo: "Flutter vs React Native 2025: Complete Comparison"  # Optional shorter version
     length: 56  # Target: 50-60 chars
     keyword_position: "front"  # Primary keyword front-loaded
   ```

2. **Meta Description (Subtitle)**
   ```yaml
   meta_description:
     text: "More developers prefer Flutter, but there are 6x more React Native jobs. Learn which framework to choose based on performance, jobs, and your goals."
     length: 158  # Target: 150-160 chars
     includes_keyword: true
     includes_cta: true  # "Learn which..."
   ```

3. **URL Slug**
   ```yaml
   slug:
     value: "flutter-vs-react-native-2025"
     includes_keyword: true
     word_count: 5  # Target: 3-5 words
   ```

4. **Content SEO**
   ```yaml
   content_seo:
     keyword_in_first_100_words: true
     h2_with_keywords: ["Performance Comparison", "Developer Experience", "Job Market"]
     internal_links: 2  # Links to other woogi posts
     external_links: 5  # Links to authoritative sources
     word_count: 1850
     reading_time: "8 min"
   ```

5. **Image SEO**
   ```yaml
   images:
     cover:
       file_name: "flutter-vs-react-native-cover.png"
       dimensions: "1600x840"
       alt_text: "Flutter vs React Native comparison infographic"
     inline_images:
       - alt: "Diagram comparing Flutter and React Native architecture"
       - alt: "Performance benchmark chart"
   ```

**SEO Output Block (added to draft frontmatter):**
```yaml
seo:
  primary_keyword: "Flutter vs React Native"
  secondary_keywords: ["cross-platform 2025", "mobile framework comparison"]
  meta_description: "More developers prefer Flutter, but..."
  slug: "flutter-vs-react-native-2025"
  word_count: 1850
  internal_links: 2
  external_links: 5
  images_optimized: true
```

**Checklist:**
- [ ] Title: 50-60 chars, keyword front-loaded
- [ ] Meta description: 150-160 chars, keyword + value + CTA
- [ ] Slug: 3-5 words, includes keyword, lowercase
- [ ] Keyword in first 100 words
- [ ] H2s include secondary keywords
- [ ] 2-3 internal links with descriptive anchor text
- [ ] 3-5 external links to authoritative sources
- [ ] All images have descriptive alt text
- [ ] Cover image set (1600x840)
- [ ] Tags relevant and limited to 5

## Draft Output Format

Saved to `work-blog/drafts/{topic-slug}-draft.md`:

```markdown
---
title: "Understanding React Server Components: A Practical Guide"
subtitle: "What RSC is, how it works, and when to use it"
tags: ["react", "server-components", "nextjs", "javascript"]
cover_image: ""
canonical_url: ""
draft: true
tone: "mixed"
word_count: 1847
---

# Understanding React Server Components: A Practical Guide

Hey, I'm woogi! Let me walk you through...

## Table of Contents
...

## What Are React Server Components?
...

## How RSC Works Under the Hood
...

## Practical Example
...

## Best Practices
...

## Common Pitfalls
...

## Wrapping Up
...

---

**Sources:**
- [Source 1](url)
- [Source 2](url)

---
*Draft generated: {date}*
*Ready for review: /blog-review*
```

## Usage Example

```
User: /blog-draft --tone casual

Process:
1. Load research from work-blog/research/react-server-components-research.md
2. Set tone to "casual"
3. Generate structure with Hashnode frontmatter
4. Write intro with woogi's casual voice
5. Write each section with code examples
6. Write conclusion with signature
7. Apply SEO optimization
8. Save to work-blog/drafts/react-server-components-draft.md

Output:
"Draft complete!

Title: Understanding React Server Components: A Practical Guide
Tone: Casual & Friendly
Word count: ~1850 words
Sections: 6

Preview saved to work-blog/drafts/react-server-components-draft.md

Ready to review? Run /blog-review"
```

## Next Step

Draft output feeds into **3-review** skill for user feedback and refinement.
