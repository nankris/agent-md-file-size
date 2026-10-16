# A 619-byte CLAUDE.md cut output 40%. The bill moved 10%.

*Draft. Tech in General experiments #004/#009. 20 headless Claude Code runs (Opus 5.5, Pro), 2026-10-15 IST.*

The claim: a tiny rules file ("be terse, no recap, smallest change") cuts Claude Code's tokens by ~40%. I tried it on 5 small bug fixes, next to no file, a normal 25-line project file, and a 38 KB "engineering handbook".

Every run fixed its bug without touching the tests.

| CLAUDE.md | Output tokens | Final reply | Est. cost |
|---|---|---|---|
| none | 671 | 106 words | 12.5¢ |
| 619-byte concise rules | 403 (−40%) | 17 words | 11.3¢ (−10%) |
| 25-line project notes | 432 (−36%) | 40 words | 13.8¢* |
| 38 KB handbook | 653 | 87 words | 21.9¢ (+75%) |

*\*two runs paid fresh cache writes; noise.*

**The claim holds, for output.** −40% output tokens, almost exactly the cited number, and the summaries went from paragraphs to one line.

**But output isn't the bill.** Each call re-sends ~16K tokens of system prompt and tools. Output is maybe a fifth of the cost, so −40% output ≈ −10% total.

**The real danger is the other direction.** A bloated CLAUDE.md rides along on every call. 38 KB of boilerplate added ~11K tokens per call and 75% to the cost, and didn't make the answers any shorter.

**Takeaway.** Keep CLAUDE.md short and specific. A few concise-output rules are worth having; a handbook is a tax.

*$ are API-equivalent estimates from Claude Code's `total_cost_usd`; Pro isn't billed per token.*
