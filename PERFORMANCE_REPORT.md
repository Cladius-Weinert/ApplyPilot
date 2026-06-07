# Performance Report — ApplyPilot

**Audit date:** 2026-06-05  
**Method:** static code review, dependency review, CLI smoke checks, compile checks, and pipeline architecture assessment. Full live benchmarks were not run because job-board scraping and LLM calls require external services and credentials.

## Executive summary

ApplyPilot's likely bottlenecks are network I/O, browser automation, LLM calls, and repeated scraping/enrichment. CPU-bound work is secondary. The best performance improvements are caching, concurrency limits, deduplication, resumability, and avoiding unnecessary browser launches.

## Current bottleneck map

| Area | Likely bottleneck | Impact | Recommendation |
|---|---|---:|---|
| Discovery via JobSpy/direct sites | Network latency, anti-bot throttling, parsing large pages | High | Cache results, cap per-site requests, backoff, better source health metrics. |
| Workday/direct enrichment | Browser startup and page rendering | High | Prefer HTTP/JSON-LD extraction before Playwright; pool browser contexts. |
| LLM scoring/tailoring | API latency, rate limits, token cost | High | Batch where safe, cache by job hash, set per-run budget, support cheaper providers. |
| PDF generation | Document rendering overhead | Medium | Generate only for shortlisted jobs; reuse unchanged files. |
| SQLite writes | Serialized writes under parallel discovery | Low/Medium | Batch inserts and use WAL mode if high concurrency is added. |
| Dashboard | HTML generation from DB | Low | Paginate or filter if DB grows beyond thousands of jobs. |

## Slow function candidates

Based on code structure and naming, the highest-risk functions are:

1. `discover_smartextract` / direct-site scraping paths.
2. Workday scraping/enrichment functions.
3. Detail enrichment that escalates from HTTP to Playwright.
4. LLM-powered scoring, tailoring, cover-letter generation, and extraction.
5. Browser auto-apply launcher and per-worker Chrome sessions.

## Memory usage risks

- Storing full page HTML for extraction can use significant memory on large sites.
- LLM prompts built from full descriptions/resumes can become large.
- Parallel browser workers multiply memory usage quickly, especially on Termux/mobile.

Recommendations:

- Truncate page HTML aggressively before LLM extraction.
- Store compressed raw artifacts only when debug mode is enabled.
- Default Termux workers to 1.
- Add `--max-jobs` and `--max-llm-calls` options for safe runs.

## Network bottlenecks

- External job boards and ATS pages are variable and rate-limited.
- Some sources block headless browsers.
- LLM providers rate-limit free tiers.

Recommendations:

- Add source-level timeout and retry configuration.
- Track per-source success/failure/latency.
- Cache failed detail fetches for a cooldown period.
- Use OpenRouter/DeepSeek/local model routing for cost/performance flexibility. This PR adds provider foundation.

## Browser bottlenecks

- Launching a full Chrome instance per worker is expensive.
- Browser automation is fragile on Android/Termux.
- `--workers` should be conservative by default.

Recommendations:

- Keep `workers=1` default.
- Reuse browser contexts where safe.
- Add browser health checks.
- Add screenshot capture only on failure/debug to reduce disk use.

## Implemented in this PR

- Added multi-provider LLM routing so users can select lower-cost/faster providers without changing pipeline code.
- Added documentation that recommends conservative Termux workflow and warns about browser automation limits.
- Added Makefile smoke commands so performance regressions can be checked more easily.

## Benchmark plan for next PR

Add `scripts/benchmark_pipeline.py` with:

- `--sample-db` for synthetic jobs.
- Per-stage wall-clock timing.
- Peak memory via `tracemalloc`.
- LLM call count and token estimate.
- Browser launch timing.
- CSV/JSON output for before/after comparisons.

Suggested metrics:

| Metric | Target |
|---|---:|
| Doctor command | < 2 seconds |
| Synthetic score prompt build | < 200 ms/job |
| SQLite insert batch | > 1,000 jobs/sec local |
| Termux memory at idle | < 250 MB excluding browser |
| Termux recommended workers | 1 |

## Verdict

The biggest performance win is not micro-optimization. It is reducing unnecessary network/browser/LLM work through caching, budgets, and source health metrics.
