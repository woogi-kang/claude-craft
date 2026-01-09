# woogi's Tech Blog Style Guide

> Research-based writing guide for woogi's English tech blog on Hashnode.
> Based on analysis of successful tech bloggers including Dan Abramov, Josh Comeau, Kent C. Dodds, and best practices from dev.to, freeCodeCamp, and Smashing Magazine.

---

## Table of Contents
- [1. Core Philosophy](#1-core-philosophy)
- [2. Voice & Tone](#2-voice--tone)
- [3. Article Structure](#3-article-structure)
- [4. Writing Hooks](#4-writing-hooks)
- [5. Headlines & Titles](#5-headlines--titles)
- [6. Code Examples](#6-code-examples)
- [7. Teaching Approach](#7-teaching-approach)
- [8. Common Mistakes to Avoid](#8-common-mistakes-to-avoid)
- [9. Reference Examples](#9-reference-examples)

---

## 1. Core Philosophy

### The woogi Approach

Inspired by the best tech bloggers:

| Blogger | Key Trait | woogi Takeaway |
|---------|-----------|----------------|
| **Dan Abramov** | Philosophical depth + accessibility | Explain the "why", not just "how" |
| **Josh Comeau** | Interactive + visual + whimsical | Build mental models, use diagrams |
| **Kent C. Dodds** | Practical + exercise-driven | Focus on real problems, be concise |

### Core Principles

1. **Teach concepts, not just code**
   - Readers should understand *why* something works
   - Build mental models, not just memorization

2. **Be authentically helpful**
   - Share what you wish you knew earlier
   - Admit what you struggled with

3. **Respect the reader's time**
   - Get to the point quickly
   - Remove anything that doesn't contribute

4. **Lower the barrier**
   - Make complex topics accessible
   - Use analogies and real-world comparisons

---

## 2. Voice & Tone

### woogi's Voice

```
Authentic + Knowledgeable + Approachable
```

**Characteristics:**
- First person ("I", "I've learned", "I struggled with")
- Conversational but not sloppy
- Confident but not arrogant
- Technical but not intimidating

### Tone Spectrum

```
← Casual ─────────────── Mixed ─────────────── Professional →

"Let me show you      "Here's what I        "This article explores
 this cool trick..."   learned about..."      the implementation of..."
```

### Language Patterns

**DO Use:**
```
✓ "Let me show you..."
✓ "Here's what I learned..."
✓ "I struggled with this at first, but..."
✓ "The key insight is..."
✓ "Think of it like..."
✓ "In my experience..."
```

**AVOID:**
```
✗ "In this article, we will discuss..."  (too formal)
✗ "As everyone knows..."                  (condescending)
✗ "Simply do X..."                        (dismissive)
✗ "Obviously..."                          (alienating)
✗ "It's easy, just..."                    (minimizing)
```

### Contractions

Use contractions for a natural flow:
- "you'll" instead of "you will"
- "it's" instead of "it is"
- "don't" instead of "do not"
- "I've" instead of "I have"

---

## 3. Article Structure

### Optimal Length

| Type | Word Count | Read Time |
|------|------------|-----------|
| Quick tip | 500-800 | 2-3 min |
| Tutorial | 1200-2000 | 5-8 min |
| Deep dive | 2000-3000 | 10-15 min |

> **Best performing posts**: 5-10 minute read time (1200-2000 words)

### Standard Structure

```markdown
# [Engaging Title]

[Hook - 2-3 sentences max]

[Brief context - what this post covers]

## Table of Contents (optional, for longer posts)

## Section 1: The Problem / Context
[Why this matters]

## Section 2: The Core Concept
[Main explanation with examples]

## Section 3: Practical Implementation
[Code walkthrough]

## Section 4: Best Practices / Tips
[Actionable advice]

## Section 5: Common Pitfalls (optional)
[What to avoid]

## Wrapping Up
[Summary + next steps]

---
[Signature]
```

### Section Guidelines

**Each section should:**
- Have a clear, descriptive heading
- Start with a transition from the previous section
- End with a bridge to the next section
- Be scannable (use sub-headers, lists, code blocks)

---

## 4. Writing Hooks

### The First 2 Sentences Are Everything

> 73% of people skim blog posts. If your intro doesn't hook them, they're gone.

### Hook Formulas for woogi

#### 1. The Struggle Hook (Most Authentic)
```markdown
I spent three days debugging a React re-render issue. The fix?
One line of code. Let me save you those three days.
```

#### 2. The Question Hook
```markdown
What if I told you that most developers use useEffect wrong?
I was one of them—until I understood this one concept.
```

#### 3. The Surprising Stat Hook
```markdown
67% of React components re-render unnecessarily.
Here's how to find and fix them in your app.
```

#### 4. The "Here's What I Learned" Hook
```markdown
After building five production apps with Server Components,
I finally understand when to use them. Let me share what clicked.
```

#### 5. The Empathy Hook (Morrow Opening)
```markdown
You've read the docs. You've watched the tutorials.
But somehow, it still doesn't click. I've been there.
```

### Hook Rules

1. **Keep it short** - Under 100 words for the entire intro
2. **Create curiosity** - Promise value, don't deliver it yet
3. **Be specific** - "67%" beats "most", "three days" beats "a long time"
4. **Connect emotionally** - Address a pain point

---

## 5. Headlines & Titles

### Title Formulas That Work

| Formula | Example |
|---------|---------|
| How to [Achieve X] | How to Debug React Re-renders |
| [Number] [Things] for [Outcome] | 5 Patterns for Cleaner React Code |
| Why [Counterintuitive Truth] | Why Your useEffect Is Probably Wrong |
| [X] vs [Y]: [Question] | Server vs Client Components: When to Use Each |
| The [Adjective] Guide to [Topic] | The Practical Guide to React Suspense |
| Understanding [Concept] | Understanding the React Fiber Architecture |
| What I Learned [Doing X] | What I Learned Building My First Rust CLI |

### Title Best Practices

- **Length**: 50-60 characters (avoid search cutoff)
- **Keywords first**: Place main topic at the beginning
- **Odd numbers**: Perform 20% better than even (7 > 6)
- **Power words**: "Essential", "Complete", "Practical", "Real-world"

### Examples for woogi

```
✓ "How I Finally Understood React Server Components"
✓ "5 TypeScript Patterns I Wish I Learned Earlier"
✓ "Why I Stopped Using Redux (And What I Use Instead)"
✓ "The Mental Model That Made CSS Click for Me"
✓ "Debugging React: A Practical Guide"
```

---

## 6. Code Examples

### Code Philosophy

> "Code examples should work when copy-pasted."

### Formatting Rules

1. **Use syntax highlighting** - Always specify the language
2. **Add meaningful comments** - Explain the "why"
3. **Keep examples focused** - Remove unrelated code
4. **Show before/after** - When refactoring or improving

### Example Format

```typescript
// Before: What most developers do
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  if (!user) return <Loading />;
  return <div>{user.name}</div>;
}

// After: A cleaner approach with React Query
function UserProfile({ userId }) {
  const { data: user, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Loading />;
  return <div>{user.name}</div>;
}

// Why this is better:
// - Automatic caching and deduplication
// - Built-in loading and error states
// - No cleanup needed
```

### Code Block Guidelines

| Aspect | Guideline |
|--------|-----------|
| Max lines | 20-30 lines per block |
| Comments | Focus on "why", not "what" |
| Naming | Use realistic, meaningful names |
| Imports | Include if they help understanding |

---

## 7. Teaching Approach

### Kent C. Dodds' Insights Applied

1. **Exercises before concepts**
   - Show the problem before explaining the solution
   - "Try this first, then I'll explain what's happening"

2. **Build on previous knowledge**
   - Reference earlier sections
   - "Remember how we said X? Here's why that matters now."

3. **Encourage self-reflection**
   - "Pause and think: why might this be a problem?"
   - "Before reading on, try to guess what happens."

### Josh Comeau's Insights Applied

1. **Pop the hood**
   - Don't just show the API, explain the mechanism
   - "Here's what's actually happening under the hood"

2. **Build mental models**
   - Use analogies: "Think of it like a..."
   - Use diagrams when helpful

3. **Add whimsy**
   - Make technical content enjoyable
   - Use creative examples (but stay professional)

### Dan Abramov's Insights Applied

1. **Philosophical depth**
   - Explore the design decisions behind tools
   - "The React team designed it this way because..."

2. **Personal anecdotes**
   - "When I first started, I thought..."
   - "A common misconception I had was..."

3. **Acknowledge complexity**
   - Don't oversimplify when accuracy matters
   - "This is nuanced—here's the full picture"

---

## 8. Common Mistakes to Avoid

### The Biggest Mistake: Meandering

> "Often, the author has some valuable insight to share, but they squander their first seven paragraphs on the history of functional programming. By the time they get to the interesting part, everyone has closed the tab."

### Mistakes Checklist

| Mistake | Fix |
|---------|-----|
| Long intros with history | Get to the point in 2-3 sentences |
| "In this article we will..." | Just start with the hook |
| Over-explaining basics | Know your audience level |
| Walls of text | Use headers, lists, code blocks |
| Generic examples | Use realistic, specific scenarios |
| No code comments | Explain the "why" in comments |
| Jargon without explanation | Define terms or link to resources |
| "Simply do X" | Show empathy for complexity |

### Self-Edit Checklist

Before publishing, ask:

- [ ] Does the first sentence hook the reader?
- [ ] Can someone skim and understand the main points?
- [ ] Is every paragraph necessary?
- [ ] Do code examples work when copy-pasted?
- [ ] Is the conclusion actionable?
- [ ] Would I want to read this?

---

## 9. Reference Examples

### woogi Article Template

```markdown
# How I Finally Understood [Topic]

I spent [time] struggling with [problem]. Every tutorial I found
either oversimplified it or assumed knowledge I didn't have.

Then something clicked. Let me share the mental model that made
it all make sense.

## The Problem

[Describe the pain point - what's confusing or hard]

When I first encountered [topic], I thought [common misconception].
Here's what I was missing.

## The Key Insight

[The "aha" moment - explain the core concept]

Think of it like [analogy]. Just as [comparison], [concept] works by...

## Let's See It in Action

[Practical code example with explanation]

```typescript
// Your code here with comments
```

Notice how [key observation]. This is because [explanation].

## Tips from Experience

Here's what I wish someone told me earlier:

1. **[Tip 1]** - [Brief explanation]
2. **[Tip 2]** - [Brief explanation]
3. **[Tip 3]** - [Brief explanation]

## Common Pitfalls

Watch out for these:

- **[Pitfall 1]** - [How to avoid]
- **[Pitfall 2]** - [How to avoid]

## Wrapping Up

[1-2 sentence summary]

The key takeaway: [main insight in one sentence].

If you found this helpful, let me know in the comments.
Got questions? I'm always happy to chat.

— woogi
```

---

## Sources

### Bloggers Studied
- [Dan Abramov - Overreacted](https://overreacted.io/)
- [Josh Comeau](https://www.joshwcomeau.com/)
- [Kent C. Dodds](https://kentcdodds.com/blog)

### Writing Guides
- [freeCodeCamp - How to Write a Great Technical Blog Post](https://www.freecodecamp.org/news/how-to-write-a-great-technical-blog-post-414c414b67f6/)
- [dev.to - The Ultimate Guide to Writing Technical Blog Posts](https://dev.to/blackgirlbytes/the-ultimate-guide-to-writing-technical-blog-posts-5464)
- [Hashnode - 13 Blogging Tips for Developers](https://hashnode.com/post/13-blogging-tips-for-developers-ckqkuqem8009ed7s15zpidiob)
- [Draft.dev - Technical Blogs](https://draft.dev/learn/technical-blogs)
- [Refactoring English - Write Blog Posts Developers Read](https://refactoringenglish.com/chapters/write-blog-posts-developers-read/)

### Headline & Hook Research
- [CoSchedule - Catchy Blog Titles](https://coschedule.com/headlines/catchy-blog-titles)
- [Siege Media - Blog Title Examples](https://www.siegemedia.com/creation/blog-title-examples)
- [SmartWriter - Blog Intros That Hook Readers](https://www.smartwriter.ai/blog/blog-intros-that-emotionally-hook-readers-and-reduce-bounce-rate)
