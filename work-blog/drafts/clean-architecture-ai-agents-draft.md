---
title: "Why Your AI Writes Great Code Until Your Project Gets Big"
slug: vibe-coding-trap-clean-architecture
tags: ["vibe-coding", "clean-architecture", "ai-agents", "context-engineering", "feature-based"]
seo_description: "I spent weeks debugging AI-generated code that worked perfectly in small projects. Here's what I learned about why Vibe Coding breaks at scale, and how Feature-based Clean Architecture fixes it."
---

# Why Your AI Writes Great Code Until Your Project Gets Big

I still remember the first time I used Claude to build something.

"Make me a simple TODO app with a REST API." Thirty seconds later, I had working code. Clean code. Code with proper error handling and everything.

I thought: "Wait, do we even need developers anymore?"

Andrej Karpathy called this "Vibe Coding" back in February 2025. You describe what you want, the AI builds it, you run it and vibe. No need to understand every line. It just... works.

**Then my project hit 10,000 lines, and everything fell apart.**

## The Hangover Is Real

I'm not alone in this. In 2025, people started calling it "Vibe Coding Hangover."

The numbers are brutal:
- 45% of AI-generated code has security vulnerabilities (Veracode, 2025)
- 41% more debugging time for systems over 50,000 lines
- 16 out of 18 CTOs surveyed experienced production disasters from AI code

One CTO's story hit close to home:

> "The AI-generated database queries worked perfectly in tests. Syntax was correct, so my developer approved it. Then real traffic came in. The system nearly froze. What worked on small datasets completely collapsed at production scale. Debugging took a week."

I've been there. I've stared at AI-generated code that looked right, tested fine locally, then burned everything down in production.

## Here's What I Finally Understood

The problem isn't that AI is dumb. It's actually scary smart. The problem is that **AI can't see your whole codebase at once.**

Even the best LLMs today have a 128K-200K token context window. Sounds like a lot until you do the math:

```
Project size vs tokens:
├── MVP (5,000 lines): ~25,000 tokens ✅ Easy
├── Medium project (30,000 lines): ~150,000 tokens ⚠️ Tight
├── Large project (100,000 lines): ~500,000 tokens ❌ Impossible
```

When you ask AI to "fix the order feature," here's what happens in a messy codebase:

```
Unstructured project:
├── Files AI has to scan: 47
├── Actually relevant: 9 (19%)
├── Wasted tokens: ~35,000
└── Result: AI gets confused, edits the wrong things

Structured project:
├── Files AI has to scan: 9
├── Actually relevant: 9 (100%)
├── Tokens used: ~5,000
└── Result: Precise changes
```

FlowHunt's research proved something I suspected:

> "300 focused tokens outperform 113,000 scattered tokens."

That hit me hard.

## The Frustrations I Know You've Felt

Working with AI on an unstructured project, you've probably experienced:

**Context amnesia.** Yesterday, I spent an hour explaining our JWT refresh token logic. Today I asked for "add social login" and the AI created a completely new auth module, ignoring everything we discussed.

**Helpful overreach.** I asked to change a button color. The AI "helpfully" refactored the PaymentController comments and changed return types. Broke all our tests.

**Pattern blindness.** Our entire codebase uses `Result<T, E>` for error handling. The AI sprinkled its own `try-except` blocks everywhere.

**Scope creep.** "Just optimize this one function." The AI modified every caller of that function. 300-line PR for a one-line fix.

The AI isn't broken. **We're not giving it clear boundaries to work within.**

## Why Standard Clean Architecture Isn't Enough

"Just use Clean Architecture, right?"

That's what I thought at first:

```
src/
├── domain/          # Pure business logic
├── application/     # Use cases
├── infrastructure/  # External systems
└── presentation/    # API layer
```

It helped. But as the project grew, new problems showed up.

**Problem 1: Cohesion breaks down.**

Add 'orders', 'users', 'payments', 'shipping' and suddenly:

```
src/
├── domain/
│   └── entities/
│       ├── user.py
│       ├── order.py
│       ├── payment.py
│       └── ... (20+ files)
```

When you ask AI about "orders," it has to wade through everything else too.

**Problem 2: Cross-contamination.**

With `Order` and `User` in the same folder, AI optimizing orders might casually add a `last_order_id` field to the User entity. I've seen this happen more than once.

```python
# AI "improving" order lookup
@dataclass
class User:
    id: str
    email: str
    name: str
    last_order_id: str = None  # 👈 Touched User while working on orders
```

**Problem 3: The "core" folder becomes a graveyard.**

```python
core/
├── result.py
├── failure.py
├── validators.py      # Everything validates here
├── formatters.py      # Multiple features dump stuff here
├── helpers.py         # "Put it here for now" cemetery
└── common_models.py   # Who owns these?
```

AI treats all of this as relevant context. For everything.

## What Actually Works: Feature-Based Architecture

The fix is straightforward once you see it: **give AI physical boundaries it can't ignore.**

Feature-based architecture combines vertical layers with horizontal feature separation:

```
src/
├── features/                      # 👈 Everything lives here, isolated
│   ├── auth/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.py        # Only auth's User
│   │   │   └── ports/
│   │   ├── application/
│   │   │   └── use_cases/
│   │   ├── infrastructure/
│   │   └── api.py                 # Public interface
│   │
│   ├── order/
│   │   ├── domain/
│   │   ├── application/
│   │   └── api.py
│   │
│   └── payment/
│       └── ...
│
└── core/                          # 👈 Truly generic only
    ├── result.py
    └── failure.py
```

The difference in context efficiency:

```
Layer-based "fix orders":
├── domain/entities/* (all entities)     ~8,000 tokens
├── application/use_cases/* (all)        ~15,000 tokens
└── Total context                        ~27,000 tokens ❌

Feature-based "fix orders":
├── features/order/domain/*              ~2,000 tokens
├── features/order/application/*         ~3,000 tokens
└── Total context                        ~5,000 tokens ✅
```

**5x more efficient.** That's not a small improvement.

## Making Features Talk to Each Other

When features are isolated, they still need to communicate. Here's what works.

**Rule: Never import another feature's internals.**

```python
# ❌ Don't do this
from src.features.auth.application.use_cases.get_user import GetUserUseCase

# ✅ Do this
from src.features.auth.api import get_current_user_id
```

**Solution 1: Public APIs (Facades)**

```python
# src/features/auth/api.py - The only file other features can import
from .presentation.dependencies import get_current_active_user

def get_current_user_id(user = Depends(get_current_active_user)) -> str:
    return user.id

def validate_user_exists(user_id: str) -> bool:
    # Implementation hidden
    ...
```

**Solution 2: Event-driven communication**

```python
# src/features/payment/application/use_cases/complete_payment.py
class CompletePaymentUseCase:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def execute(self, payment_id: str):
        payment = self.complete_payment(payment_id)

        # Notification feature subscribes to this
        self.event_bus.publish(PaymentCompletedEvent(
            payment_id=payment.id,
            user_id=payment.user_id,
            amount=payment.amount
        ))
```

## How I Prompt AI Now

Here's what my prompts look like these days:

```
You're a Python expert working on a feature-based clean architecture project.

**Feature:** order (order processing)
**Scope:** All changes stay in `src/features/order/`

**Task:** Add inventory restoration when users cancel orders.

**Relevant files:**
- src/features/order/application/use_cases/cancel_order.py (modify this)
- src/features/order/domain/ports/inventory_port.py (use this interface)
- src/features/order/domain/entities/order.py (reference)

**Rules:**
- Don't import from other features' internals
- Need data from another feature? Use their api.py
- New ports go in src/features/order/domain/ports/

Go ahead and update cancel_order.py.
```

Clear boundaries. Specific files. Explicit rules.

## What Changed for Me

Addy Osmani nailed it:

> "Vibe coding is not the same as AI-Assisted Engineering."

| Vibe Coding | AI-Assisted Engineering |
|-------------|------------------------|
| "If it works, ship it" | "It needs to be maintainable" |
| No structure, just generate | Generate within clear architecture |
| Works only at small scale | Scales indefinitely |
| AI owns everything | AI works within boundaries |

My role shifted from "how do I write this code" to "where should this code live."

```
[Vibe Coding]
Developer → Ask AI → Get code → 🤞 Hope it works

[AI-Assisted Engineering]
Developer → Set boundaries → AI generates → Validate boundaries → Ship
            (Feature +        (execute)      (guardrails)
             layers)
```

## The Takeaway

Vibe Coding doesn't fail because AI is bad at coding. It fails because **AI can't see clear boundaries when we don't provide them.**

Feature-based Clean Architecture gives you:

1. **Context isolation** - AI only sees what it needs
2. **Predictable changes** - Modifications stay within feature boundaries
3. **No cross-contamination** - Physical separation prevents "helpful" overreach
4. **Sustainable scaling** - Works at 10,000 lines and 100,000 lines

---

300 focused tokens beat 113,000 scattered ones.

That's the power of structured context.

The magic of Vibe Coding doesn't have to disappear. **Inside the right structure, it becomes sustainable.**

---

**References**

- [Vibe Coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)
- [Vibe Coding is not AI-Assisted Engineering - Addy Osmani](https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98)
- [The Rise of Vibe Coding in 2025 - Emil](https://ecoemil.medium.com/the-rise-of-vibe-coding-in-2025-a-revolution-or-a-reckoning-4c2f7053ceef)
- [How AI Vibe Coding Is Destroying Junior Developers' Careers - Final Round AI](https://www.finalroundai.com/blog/ai-vibe-coding-destroying-junior-developers-careers)
- [The Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Context Engineering - FlowHunt](https://www.flowhunt.io/blog/context-engineering/)

— woogi
