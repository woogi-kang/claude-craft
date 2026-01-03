---
name: blog-publish
description: |
  Publishing skill for Hashnode blog.
  Publishes approved drafts via Hashnode GraphQL API.
  Activated by: "/blog-publish" or "publish the post"
---

# Blog Publish Skill

Publishes approved blog drafts to woogi's Hashnode blog via GraphQL API.

## Trigger Commands

- `/blog-publish`
- `/blog-publish --draft` (save as draft on Hashnode)
- `publish the post`
- `publish to hashnode`

## Prerequisites

1. Approved draft from **3-review** skill:
   - `work-blog/drafts/{topic-slug}-draft.md`
   - Must have `review_status: "approved"`

2. Hashnode configuration:
   - `HASHNODE_API_KEY` environment variable
   - `HASHNODE_PUBLICATION_ID` environment variable

## Core Functions

### 1. config_validate (Validate Configuration)

Checks all required configuration before publishing.

**Checks:**
```yaml
validation:
  api_key:
    source: "HASHNODE_API_KEY env var"
    status: "valid" | "missing" | "invalid"
  publication_id:
    source: "HASHNODE_PUBLICATION_ID env var"
    status: "valid" | "missing"
  draft:
    path: "work-blog/drafts/{slug}-draft.md"
    status: "found" | "not_found"
    review_status: "approved" | "pending" | "not_reviewed"
```

**Error Handling:**
```
If API key missing:
  "Hashnode API key not found.

   To set up:
   1. Go to hashnode.com → Settings → Developer
   2. Generate new token
   3. Set: export HASHNODE_API_KEY=your_token"

If publication ID missing:
  "Publication ID not found.

   To find yours:
   1. Go to your Hashnode dashboard
   2. URL format: hashnode.com/{publication-id}/dashboard
   3. Set: export HASHNODE_PUBLICATION_ID=your_id"
```

### 2. content_prepare (Prepare Content)

Converts draft markdown to Hashnode-compatible format with SEO optimization.

> **Reference:** See `agents/tech-blog-agent/SEO_GUIDE.md` for Hashnode SEO settings.

**Process:**
- Parse frontmatter for metadata
- Extract title, subtitle, tags
- Apply SEO optimizations
- Clean markdown content
- Validate tag count (max 5)

**Output:**
```yaml
prepared_content:
  # Basic Content
  title: "Understanding React Server Components"
  subtitle: "What RSC is, how it works, and when to use it"
  contentMarkdown: "{full markdown content}"
  slug: "react-server-components-guide"

  # Tags
  tags:
    - slug: "react"
    - slug: "server-components"
    - slug: "javascript"

  # Cover Image
  coverImageOptions:
    coverImageURL: "https://..."  # 1600x840 recommended

  # SEO Settings 🆕
  seo:
    title: "React Server Components Guide 2025"  # Can differ from display title
    description: "Learn how React Server Components work..."

  # Open Graph (Social Sharing) 🆕
  ogMetaData:
    title: "React Server Components: A Practical Guide"
    description: "Master RSC with this comprehensive guide..."
    image: "https://..."  # Social share image

  # Settings
  settings:
    isTableOfContentEnabled: true
    delisted: false  # Set true to hide from Hashnode feed

  # Optional
  canonicalUrl: ""  # If cross-posting from another site
  disableComments: false
```

### 3. api_publish (Publish via API)

Sends content to Hashnode GraphQL API.

**GraphQL Mutation:**
```graphql
mutation PublishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post {
      id
      title
      slug
      url
      publishedAt
    }
  }
}
```

**Input Variables (with SEO):**
```json
{
  "input": {
    "title": "Understanding React Server Components",
    "subtitle": "What RSC is, how it works, and when to use it",
    "slug": "react-server-components-guide",
    "publicationId": "{PUBLICATION_ID}",
    "contentMarkdown": "{content}",
    "tags": [
      { "slug": "react" },
      { "slug": "server-components" }
    ],
    "coverImageOptions": {
      "coverImageURL": "https://your-image-url.png"
    },
    "seo": {
      "title": "React Server Components Guide 2025",
      "description": "Learn how React Server Components work with practical examples and best practices."
    },
    "ogMetaData": {
      "title": "React Server Components: A Practical Guide",
      "description": "Master RSC with this comprehensive guide by woogi",
      "image": "https://your-og-image-url.png"
    },
    "settings": {
      "isTableOfContentEnabled": true
    }
  }
}
```

**cURL Example:**
```bash
curl -X POST https://gql.hashnode.com \
  -H "Content-Type: application/json" \
  -H "Authorization: {API_KEY}" \
  -d '{
    "query": "mutation PublishPost($input: PublishPostInput!) { publishPost(input: $input) { post { id url } } }",
    "variables": {
      "input": {
        "title": "...",
        "publicationId": "...",
        "contentMarkdown": "..."
      }
    }
  }'
```

### 4. draft_save (Save as Draft - Optional)

Saves to Hashnode as draft instead of publishing.

**GraphQL Mutation:**
```graphql
mutation CreateDraft($input: CreateDraftInput!) {
  createDraft(input: $input) {
    draft {
      id
      title
      slug
    }
  }
}
```

**Use case:**
- `/blog-publish --draft`
- Schedule for later publishing via Hashnode UI

### 5. result_handle (Handle Result)

Processes API response and provides feedback.

**Success Response:**
```markdown
## Published Successfully!

**Title:** Understanding React Server Components
**URL:** https://woogi.hashnode.dev/react-server-components
**Published:** 2025-01-04 10:30:00

The post is now live on your Hashnode blog.

---

**Next steps:**
- View your post: [link]
- Share on social media
- Monitor analytics on Hashnode dashboard

**Local copy saved to:**
work-blog/published/react-server-components-final.md
```

**Error Response:**
```markdown
## Publishing Failed

**Error:** {error_message}

**Possible causes:**
- Invalid API key
- Publication ID mismatch
- Content validation error
- Network issue

**Troubleshooting:**
1. Verify your API key: hashnode.com → Settings → Developer
2. Check publication ID in dashboard URL
3. Try again: /blog-publish

**Draft preserved at:**
work-blog/drafts/react-server-components-draft.md
```

### 6. archive_save (Archive Published Post)

Saves final version locally for records.

**Archive Location:**
`work-blog/published/{topic-slug}-final.md`

**Archive Format:**
```markdown
---
title: "Understanding React Server Components"
published_url: "https://woogi.hashnode.dev/react-server-components"
published_at: "2025-01-04T10:30:00Z"
hashnode_post_id: "abc123"
tags: ["react", "server-components", "javascript"]
---

{Full content as published}

---
*Published by woogi via tech-blog-agent*
```

## Publish Flow

```
┌─────────────────────────────────────────┐
│           /blog-publish                 │
└─────────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │ Validate Config  │
         │ (API key, pub ID)│
         └──────────────────┘
                    │
          ┌────────┴────────┐
          │ Missing?        │
          ▼                 ▼
    [Show Setup      [Continue]
     Instructions]        │
                         ▼
              ┌──────────────────┐
              │ Load & Validate  │
              │ Approved Draft   │
              └──────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │ Prepare Content  │
              │ (frontmatter →   │
              │  API format)     │
              └──────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │ Confirm Publish  │
              │ "Publish now?"   │
              └──────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      [User: "yes"]          [User: "draft"]
              │                     │
              ▼                     ▼
       publishPost()         createDraft()
              │                     │
              └──────────┬──────────┘
                         ▼
              ┌──────────────────┐
              │ Handle Result    │
              └──────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │ Archive Locally  │
              └──────────────────┘
                         │
                         ▼
                    [Complete]
```

## Usage Example

```
User: /blog-publish

Agent:
"Preparing to publish...

**Configuration Check:**
- API Key: ✓ Valid
- Publication ID: ✓ Found
- Draft: ✓ Approved (react-server-components)

**Post Details:**
- Title: Understanding React Server Components
- Tags: react, server-components, javascript
- Word count: 1847

**Ready to publish to Hashnode?**
- 'yes' or 'publish' - Publish now
- 'draft' - Save as draft on Hashnode
- 'cancel' - Exit without publishing"

User: "yes"

Agent:
"Publishing to Hashnode...

## Published Successfully!

**Title:** Understanding React Server Components
**URL:** https://woogi.hashnode.dev/react-server-components

Your post is now live!

Local archive saved to:
work-blog/published/react-server-components-final.md"
```

## Error Recovery

### API Key Issues
```
/blog-publish

"API key validation failed.

Your current key may be expired or invalid.
Please generate a new token:
1. hashnode.com → Settings → Developer
2. Generate New Token
3. Update: export HASHNODE_API_KEY=new_token"
```

### Network Issues
```
/blog-publish

"Network error: Could not reach Hashnode API.

Retrying in 5 seconds... (attempt 2/3)

If this persists:
- Check your internet connection
- Verify api.hashnode.com is accessible
- Try again later"
```

## Complete Workflow Summary

```bash
# Full blog writing workflow
/blog-research "React Server Components"  # Research topic
/blog-draft --tone casual                  # Write draft
/blog-review                               # Review & edit
/blog-publish                              # Publish to Hashnode
```
