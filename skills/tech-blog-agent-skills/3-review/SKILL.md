---
name: blog-review
description: |
  Interactive review skill for blog post drafts.
  Presents draft for feedback, processes edits, and refines content.
  Activated by: "/blog-review" or "review the draft"
---

# Blog Review Skill

Interactive review process for woogi's blog drafts. Collects feedback, processes edits, and refines until approval.

## Trigger Commands

- `/blog-review`
- `/blog-review [specific-draft]`
- `review the draft`
- `let me see the draft`

## Prerequisites

Requires draft from **2-draft** skill:
- `work-blog/drafts/{topic-slug}-draft.md`

## Review Workflow

```
┌─────────────────────────────────────────┐
│           /blog-review                  │
└─────────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  Present Draft   │
         │  (section by     │
         │   section)       │
         └──────────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  Collect         │◄─────┐
         │  Feedback        │      │
         └──────────────────┘      │
                    │              │
                    ▼              │
         ┌──────────────────┐      │
         │  Apply Edits     │      │
         └──────────────────┘      │
                    │              │
                    ▼              │
         ┌──────────────────┐      │
         │  Show Changes    │──────┘
         │  (more edits?)   │
         └──────────────────┘
                    │ (approved)
                    ▼
         ┌──────────────────┐
         │  Ready for       │
         │  /blog-publish   │
         └──────────────────┘
```

## Core Functions

### 1. draft_present (Present Draft)

Shows the draft to user in digestible sections.

**Presentation Format:**
```markdown
## Draft Review: {Title}

**Metadata:**
- Tone: {tone}
- Word count: {count}
- Reading time: ~{minutes} min

---

### Section 1: Introduction

{intro content}

---

**Feedback for this section?**
- Type your edits or suggestions
- Type "ok" or "next" to approve and continue
- Type "skip" to move to next section without approving

---
```

### 2. feedback_collect (Collect Feedback)

Processes user feedback in various formats.

**Accepted Feedback Types:**

| Input | Action |
|-------|--------|
| `ok` / `good` / `next` | Approve section, move to next |
| `skip` | Move to next without marking approved |
| Free text | Interpret as edit request |
| `"change X to Y"` | Direct replacement |
| `"make it more casual"` | Tone adjustment |
| `"add example for Z"` | Content addition |
| `"remove the part about..."` | Content deletion |
| `"shorter"` / `"longer"` | Length adjustment |

### 3. edit_apply (Apply Edits)

Applies requested changes to the draft.

**Edit Categories:**

**Content Edits:**
- Add/remove paragraphs
- Expand/condense explanations
- Add/modify code examples

**Tone Edits:**
- Adjust formality level
- Add/remove personality
- Modify woogi's voice intensity

**Structure Edits:**
- Reorder sections
- Split/merge sections
- Modify headers

**Technical Edits:**
- Fix code syntax
- Update outdated information
- Add clarifications

### 4. change_show (Show Changes)

Displays what was changed after each edit.

**Format:**
```markdown
### Changes Applied

**Section: Introduction**

~~Old:~~
> Hey, I'm woogi! Let me show you something...

**New:**
> Hey, I'm woogi! I've been working with RSC for the past
> few months, and I want to share what I've learned...

---

**Continue reviewing?**
- "ok" - approve this change
- "undo" - revert this change
- Continue with more feedback
```

### 5. quality_check (Quality Checklist)

Runs automatic quality checks before approval.

**Checklist:**
```markdown
## Pre-Publish Quality Check

### Content
- [ ] Title is engaging and includes keyword
- [ ] Introduction hooks the reader
- [ ] All sections have clear purpose
- [ ] Code examples are tested/valid
- [ ] Conclusion has clear takeaway

### Voice (as woogi)
- [ ] Consistent tone throughout
- [ ] Personal touch present
- [ ] Not overly formal/robotic
- [ ] Signature closing included

### Technical
- [ ] No broken code syntax
- [ ] Links are valid
- [ ] No placeholder text
- [ ] Images have alt text (if any)

### SEO
- [ ] Tags are relevant (max 5)
- [ ] Subtitle is compelling
- [ ] Headers are descriptive
```

### 6. final_approval (Get Final Approval)

Presents final version for publishing approval.

**Format:**
```markdown
## Final Review

**Title:** {title}
**Subtitle:** {subtitle}
**Tags:** {tags}
**Word Count:** {count}
**Reading Time:** ~{minutes} min

---

{Full article preview}

---

**Ready to publish?**
- Type "publish" or "yes" to proceed to /blog-publish
- Type "edit [section]" to make more changes
- Type "save" to save as draft and exit
```

## Review Session Output

Updates draft file with changes and adds review metadata:

```markdown
---
title: "..."
# ... existing frontmatter ...
review_status: "approved"
review_date: "2025-01-04"
review_notes:
  - "Made intro more personal"
  - "Added real-world example in section 3"
  - "Shortened conclusion"
---

{Updated content}
```

## Usage Example

```
User: /blog-review

Agent:
"Let's review your draft!

## Draft Review: Understanding React Server Components

**Metadata:**
- Tone: Casual & Friendly
- Word count: 1847
- Reading time: ~8 min

---

### Section 1: Introduction

Hey, I'm woogi! If you've been working with React lately...
[shows intro]

---

**Feedback for this section?**"

User: "make it mention that I struggled with this at first"

Agent:
"Got it! Here's the updated intro:

**New:**
> Hey, I'm woogi! If you've been working with React lately,
> you've probably heard about Server Components. I'll be honest —
> I struggled to understand them at first. But after diving deep
> and building a few projects, it finally clicked.
>
> Let me share what I learned so you don't have to struggle like I did.

**Continue with this change?**"

User: "ok"

Agent:
"Great! Moving to Section 2: What Are React Server Components?
[shows section 2]

**Feedback?**"

...

User: "publish"

Agent:
"All sections approved!

Ready to publish to Hashnode.
Run /blog-publish to continue."
```

## Next Step

Approved draft proceeds to **4-publish** skill for Hashnode publication.
