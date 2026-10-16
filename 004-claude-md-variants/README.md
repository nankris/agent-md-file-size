# #004 (+ #009-style) A 619-byte CLAUDE.md vs none / project notes / bloated (Claude Code CLI)

**Question.** Does a tiny "be concise" CLAUDE.md cut tokens, and what do a normal 25-line project file and a bloated handbook do? Grade quality, not just tokens.

**Short answer.** 5 tasks × 4 variants = 20 runs, **all passed, no test files touched** (quality held in every arm). The ~619-byte concise-output file (`short619.md`, 621 B) cut **output tokens 40%** (671 → 403 per task) — the same −40% as the cited known result — and the final reply shrank from **106 words to 17**. But output is a small part of the bill: **API-equivalent cost fell only 10%** ($0.125 → $0.113). The 25-line project-notes file (`agents25.md`, 736 B) cut output 36% and model calls 4.0 → 3.4, but cost +11% because two of its runs paid fresh cache writes (cache noise, see caveats). The **bloated 38 KB handbook** added ~11K tokens to every call and **raised cost 75%** ($0.219) with no output saving.

## Setup
- Claude Code 2.1.300, `claude-opus-5-5`, default effort, Pro; headless `claude -p "Make \`node test.js\` pass by fixing the code. Do not edit test.js." --output-format stream-json --verbose --dangerously-skip-permissions --strict-mcp-config --no-session-persistence`; fresh package copy per run with the variant copied in as `./CLAUDE.md`.
- Variants (`scripts/claude_md/`): **none**; **short619** (621 B: terse, no recap, smallest change, test once, one-line final reply, never edit tests); **agents25** (736 B, ~25 lines: layout, commands, conventions, 5-step workflow — the #009 "short AGENTS.md" analogue); **bloated** (37,871 B: 20 generic handbook sections × 6 boilerplate rules + one relevant line).
- Tasks: N01_median, N02_duration, N03_csv, T05_stale, T07_multihunk. 1 run per cell, 2 at a time, 2026-10-14 ~20:04–20:06 UTC.
- Quality = test passes, test.js unchanged, plus final-reply length. Est. $ = `total_cost_usd`, **API-equivalent estimate; Pro isn't billed per token.**

## Exact commands
```bash
source /workspace/tools/setup.sh
scripts/harness/driver_cc.sh scripts/jobs.txt 2 results/driver.log
/workspace/tools/mlenv/bin/python scripts/analyze.py
```

## Results (means over 5 tasks)
| Variant | Size | Passed | First-call prompt | Output tokens | Δ output | Final reply words | Model calls | Est. $ | Δ cost |
|---|---|---|---|---|---|---|---|---|---|
| none | 0 B | 5/5 | 16,470 | 671 | — | 106 | 4.0 | $0.125 | — |
| short619 | 621 B | 5/5 | 16,808 | 403 | **−40%** | **17** | 4.0 | $0.113 | **−10%** |
| agents25 | 736 B | 5/5 | 16,900 | 432 | −36% | 40 | 3.4 | $0.138 | +11% |
| bloated | 37,871 B | 5/5 | 27,519 | 653 | −3% | 87 | 4.4 | $0.219 | **+75%** |

`results/summary.csv`, `results/runs.csv`, raw in `results/raw/`. Chart: `results/chart.png`.

## Caveats
- 5 tasks, 1 run each. agents25's cost is skewed by two runs (N01, N02) that wrote 17–19K tokens to cache instead of reading them; its token total was actually the lowest (71K). Treat its cost delta as noise; the output delta is solid.
- Tiny tasks, so the "test once / read less" rules had little room to cut calls; on bigger tasks they may matter more.
- Code-quality grading is pass/fail + untouched tests; I didn't diff-review style.
