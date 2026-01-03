---
name: blog-research
description: |
  Research skill for tech blog writing.
  Gathers information from web searches and local codebase analysis.
  Activated by: "/blog-research [topic]" or "research [topic] for blog"
---

# Blog Research Skill

Researches topics for woogi's tech blog posts using web search and code analysis.

## Trigger Commands

- `/blog-research [topic]`
- `research [topic] for blog`
- `gather info about [topic]`

## Core Functions

### 1. topic_analysis (Topic Understanding)

Breaks down the topic into researchable components.

**Input:** Topic keyword or phrase
**Process:**
- Identify main concept and sub-topics
- Define scope (beginner/intermediate/advanced)
- List key questions to answer

**Output:**
```yaml
topic_analysis:
  main_topic: "React Server Components"
  sub_topics:
    - "What are RSC"
    - "How RSC differs from SSR"
    - "When to use RSC"
    - "RSC vs Client Components"
  target_audience: "intermediate"
  key_questions:
    - "What problem does RSC solve?"
    - "How does it work under the hood?"
    - "What are the trade-offs?"
```

### 2. web_research (Web Information Gathering)

Searches the web for relevant information, tutorials, and documentation.

**Sources to prioritize:**
1. Official documentation
2. Author/maintainer blog posts
3. Reputable tech blogs (dev.to, css-tricks, smashing magazine)
4. GitHub discussions/issues
5. Conference talks/videos

**Output structure:**
```yaml
web_research:
  - id: "W001"
    title: "React Server Components RFC"
    url: "https://..."
    type: "documentation"
    key_points:
      - "RSC run only on the server"
      - "Zero bundle size for RSC"
    credibility: "high"
    date: "2024-01-15"
```

### 3. code_research (Codebase Analysis)

Analyzes local codebase for relevant examples and patterns.

**Process:**
- Search for related files/functions
- Extract code patterns
- Identify real-world usage examples

**Output structure:**
```yaml
code_research:
  - id: "C001"
    file: "src/components/ServerData.tsx"
    pattern: "Server Component data fetching"
    code_snippet: |
      async function ServerData() {
        const data = await fetchData();
        return <div>{data}</div>;
      }
    notes: "Direct async/await in component"
```

### 4. insight_extraction (Key Insights)

Synthesizes research into actionable insights for the blog post.

**Categories:**
- **Pain points:** What problems does this solve?
- **How it works:** Core mechanism/concept
- **Best practices:** Recommended patterns
- **Pitfalls:** Common mistakes to avoid
- **Real examples:** Practical use cases

### 5. outline_suggestion (Draft Outline)

Based on research, suggests a blog post structure.

**Template:**
```markdown
# Suggested Outline

## Hook
[Engaging opening based on pain point]

## Sections
1. Introduction - What and Why
2. Core Concept - How it works
3. Practical Example - Code walkthrough
4. Best Practices - Tips from research
5. Common Pitfalls - What to avoid
6. Conclusion - Summary and next steps

## Estimated Length
~1500-2000 words

## Code Examples Needed
- [ ] Basic example
- [ ] Real-world example
- [ ] Comparison example
```

## Research Output Format

All research is saved to `work-blog/research/{topic-slug}-research.md`:

```markdown
# Research: {Topic}

**Date:** {date}
**Author:** woogi
**Status:** Ready for Draft

## Topic Analysis
{topic_analysis output}

## Web Research
{web_research output with sources}

## Code Research
{code_research output if applicable}

## Key Insights
{insight_extraction output}

## Suggested Outline
{outline_suggestion output}

## Sources
- [Source 1](url)
- [Source 2](url)
...
```

## Usage Example

```
User: /blog-research React Server Components

Process:
1. Analyze topic: "React Server Components"
2. Web search for official docs, tutorials, best practices
3. Search local codebase for RSC usage examples
4. Extract key insights and patterns
5. Generate suggested outline
6. Save to work-blog/research/react-server-components-research.md

Output:
"Research complete! I've gathered:
- 8 web sources including React official docs
- 3 code examples from your codebase
- Suggested outline: 6 sections, ~1800 words

Ready to draft? Run /blog-draft"
```

## Next Step

Research output feeds into **2-draft** skill for article writing.
