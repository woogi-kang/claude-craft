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

> **Important**: Always reference `../STYLE_GUIDE.md` for voice, tone, hooks, and structure patterns.

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

### 7. seo_optimize (SEO Optimization)

Optimizes for discoverability.

**Checklist:**
- [ ] Title includes main keyword
- [ ] Meta description (subtitle) is compelling
- [ ] Headers use relevant keywords naturally
- [ ] Internal structure is scannable
- [ ] Alt text for images (if any)
- [ ] Relevant tags (max 5)

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
