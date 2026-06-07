<!-- logo here -->

> **⚠️ ApplyPilot** is the original open-source project, created by [Pickle-Pixel](https://github.com/Pickle-Pixel) and first published on GitHub on **February 17, 2026**. We are **not affiliated** with applypilot.app, useapplypilot.com, or any other product using the "ApplyPilot" name. These sites are **not associated with this project** and may misrepresent what they offer.

# ApplyPilot

**A practical job-search workflow assistant for remote jobseekers, AI data workers, freelancers, and application tracking users.**

[![PyPI version](https://img.shields.io/pypi/v/applypilot?color=blue)](https://pypi.org/project/applypilot/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Pickle-Pixel/ApplyPilot?style=social)](https://github.com/Pickle-Pixel/ApplyPilot)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/S6S01UL5IO)




https://github.com/user-attachments/assets/7ee3417f-43d4-4245-9952-35df1e77f2df


---

## 📱 Mobile Setup
See [docs/TERMUX_SETUP.md](docs/TERMUX_SETUP.md) for Android/Termux installation instructions.

---

## What It Does

ApplyPilot helps remote AI workers discover better job opportunities, organize applications, tailor resumes, build proof-of-work portfolio assets, and apply more consistently. It does **not** guarantee jobs, interviews, hiring, clients, or income.

Core workflow commands:

```bash
pip install applypilot
pip install --no-deps python-jobspy && pip install pydantic tls-client requests markdownify regex
applypilot init          # one-time setup: resume, profile, preferences, API keys
applypilot doctor        # verify your setup — shows what's installed and what's missing
applypilot pricing       # view subscription tiers
applypilot run discover  # discover job leads within the active plan limit
applypilot run score     # Starter+ job match scoring
applypilot run tailor    # Pro+ resume tailoring workflow
```

> **Why two install commands?** `python-jobspy` pins an exact numpy version in its metadata that conflicts with pip's resolver, but works fine at runtime with any modern numpy. The `--no-deps` flag bypasses the resolver; the second command installs jobspy's actual runtime dependencies. Everything except `python-jobspy` installs normally.

---

## Two Paths

### Free/manual workflow
**Requires:** Python 3.11+.

Use discovery, the basic tracker/dashboard, basic CV and cover letter templates, and a manual job-board checklist. Free is limited to 5 job leads per day.

### Paid AI workflow
**Requires:** Python 3.11+ and an LLM key for AI-assisted scoring, suggestions, and tailoring.

Starter unlocks saved-search style workflows, match scoring, cover/CV suggestions, CSV export, and a 14-day income sprint plan. Pro unlocks portfolio-building, premium prompts, resume tailoring, RWS/AOP workflow templates, freelance gig generation, and priority scoring workflows. Agency unlocks multi-profile and team/client pipeline features.

---

## The Pipeline

| Stage | What Happens |
|-------|-------------|
| **1. Discover** | Scrapes 5 job boards (Indeed, LinkedIn, Glassdoor, ZipRecruiter, Google Jobs) + 48 Workday employer portals + 30 direct career sites |
| **2. Enrich** | Fetches full job descriptions via JSON-LD, CSS selectors, or AI-powered extraction |
| **3. Score** | AI rates every job 1-10 based on your resume and preferences. Only high-fit jobs proceed |
| **4. Tailor** | AI rewrites your resume per job: reorganizes, emphasizes relevant experience, adds keywords. Never fabricates |
| **5. Cover Letter** | AI generates a targeted cover letter per job |
| **6. Review/track** | Review generated materials, submit manually where appropriate, and track outcomes |

Each stage is independent. Run them all or pick what you need.

---

## ApplyPilot vs The Alternatives

| Feature | ApplyPilot | AIHawk | Manual |
|---------|-----------|--------|--------|
| Job discovery | 5 boards + Workday + direct sites | LinkedIn only | One board at a time |
| AI scoring | 1-10 fit score per job | Basic filtering | Your gut feeling |
| Resume tailoring | Per-job AI rewrite | Template-based | Hours per application |
| Application tracking | Local tracker + dashboard | LinkedIn-focused | Spreadsheets/manual notes |
| Supported sites | Indeed, LinkedIn, Glassdoor, ZipRecruiter, Google Jobs, 46 Workday portals, 28 direct sites | LinkedIn | Whatever you open |
| License | AGPL-3.0 | MIT | N/A |

---

## Requirements

| Component | Required For | Details |
|-----------|-------------|---------|
| Python 3.11+ | Everything | Core runtime |
| Gemini/OpenAI/local LLM key | Scoring, tailoring, cover letters | Required for AI stages only |

**Gemini API key is free.** Get one at [aistudio.google.com](https://aistudio.google.com). OpenAI and local models (Ollama/llama.cpp) are also supported.

### Optional job lead search APIs

| Component | What It Does |
|-----------|-------------|
| Brave/Bing/SerpAPI/Tavily key | Enables optional search API collection for safe public job lead discovery. Leave blank to disable. |

> **Note:** python-jobspy is installed separately with `--no-deps` because it pins an exact numpy version in its metadata that conflicts with pip's resolver. It works fine with modern numpy at runtime.

---

## Configuration

All generated by `applypilot init`:

### `profile.json`
Your personal data in one structured file: contact info, work authorization, compensation, experience, skills, resume facts (preserved during tailoring), and EEO defaults. Powers scoring, tailoring, and form auto-fill.

### `searches.yaml`
Job search queries, target titles, locations, boards. Run multiple searches with different parameters.

### `.env`
API keys and runtime config: `GEMINI_API_KEY`, `LLM_MODEL`, and optional safe job lead search API keys. Subscription/pricing data is product documentation only in this MVP.

### Package configs (shipped with ApplyPilot)
- `config/employers.yaml` - Workday employer registry (48 preconfigured)
- `config/sites.yaml` - Direct career sites (30+), blocked sites, base URLs, manual ATS domains
- `config/searches.example.yaml` - Example search configuration

---

## How Stages Work

### Discover
Queries Indeed, LinkedIn, Glassdoor, ZipRecruiter, Google Jobs via JobSpy. Scrapes 48 Workday employer portals (configurable in `employers.yaml`). Hits 30 direct career sites with custom extractors. Deduplicates by URL.

### Enrich
Visits each job URL and extracts the full description. 3-tier cascade: JSON-LD structured data, then CSS selector patterns, then AI-powered extraction for unknown layouts.

### Score
AI scores every job 1-10 against your profile. 9-10 = strong match, 7-8 = good, 5-6 = moderate, 1-4 = skip. Only jobs above your threshold proceed to tailoring.

### Tailor
Generates a custom resume per job: reorders experience, emphasizes relevant skills, incorporates keywords from the job description. Your `resume_facts` (companies, projects, metrics) are preserved exactly. The AI reorganizes but never fabricates.

### Cover Letter
Writes a targeted cover letter per job referencing the specific company, role, and how your experience maps to their requirements.

### Review/track
Use the local tracker and dashboard to review generated materials, record manual submissions, and track outcomes. Respect each job board's terms and protections; do not store job-board passwords or bypass LinkedIn, Indeed, Glassdoor, or similar protections.

```bash
# Utility tracking modes
applypilot apply --mark-applied URL    # manually mark a job as applied
applypilot apply --mark-failed URL     # manually mark a job as failed
applypilot apply --reset-failed        # reset failed jobs for manual retry
```

---

## CLI Reference

```
applypilot init                         # First-time setup wizard
applypilot doctor                       # Verify setup, diagnose missing requirements
applypilot run [stages...]              # Run pipeline stages (or 'all')
applypilot run --workers 4              # Parallel discovery/enrichment
applypilot run --stream                 # Concurrent stages (streaming mode)
applypilot run --min-score 8            # Override score threshold
applypilot run --dry-run                # Preview without executing
applypilot run --validation lenient     # Relax validation (recommended for Gemini free tier)
applypilot run --validation strict      # Strictest validation (retries on any banned word)
applypilot pricing                      # Show subscription tiers
applypilot apply --mark-applied URL     # Manually mark a job as applied
applypilot apply --mark-failed URL      # Manually mark a job as failed
applypilot status                       # Pipeline statistics
applypilot dashboard                    # Open HTML results dashboard
```

---

## Monetization Model

ApplyPilot includes subscription tiers for a hosted SaaS-style product. Pricing values are placeholders until validated with customers.

| Tier | Monthly placeholder | Included |
|------|---------------------|----------|
| Free | $0/mo | 5 job leads/day, basic application tracker, basic CV template, basic cover letter template, manual job-board checklist |
| Starter | $19/mo placeholder | Saved job search queries, job match scoring, CV/cover suggestions, daily discovery workflow, CSV export, 14-day income sprint plan |
| Pro | $49/mo placeholder | AI evaluator portfolio builder, premium prompt library, resume tailoring, RWS/AOP templates, freelance gig generator, priority scoring for Mercor, Outlier, TELUS, Mindrift, OneForma, RWS, and Prolific |
| Agency | $149/mo placeholder | Multiple profiles, client/application pipelines, reusable templates, team notes, export reports |

See [`web/pricing.html`](web/pricing.html), [`docs/SUBSCRIPTION_MODEL.md`](docs/SUBSCRIPTION_MODEL.md), and [`docs/PRICING_STRATEGY.md`](docs/PRICING_STRATEGY.md).

### Subscription/pricing MVP boundary

The Free/Starter/Pro/Agency tiers are product documentation and pricing placeholders only. This MVP does not include Stripe checkout, payment webhooks, card storage, or hosted paid-feature authorization. Add payment later only with server-side billing code and verified provider webhooks.

### Privacy and no-guarantee disclaimer

ApplyPilot stores local job-search data in `~/.applypilot` by default. Hosted deployments should publish a privacy policy before collecting user data. ApplyPilot does not guarantee jobs, interviews, hiring, clients, or income.

---

## Safe Scheduled Job Lead Discovery

ApplyPilot includes a safe job lead agent for scheduled discovery every 24 hours by default. It is designed for public-safe lead collection and human review only.

### Automated sources

The scheduled agent may collect from:

- Greenhouse public job board endpoints.
- Lever public postings endpoints.
- RemoteOK and Remotive public APIs when available.
- Optional search APIs when keys are configured: Brave Search API, Bing Web Search API, SerpAPI, or Tavily.

The search API collector is disabled automatically when no matching API key exists.

### Manual-only sources

ApplyPilot does **not** scrape LinkedIn, Indeed, Glassdoor, Google Jobs, or ZipRecruiter. It only generates manual search links for these sites so a human can open and review them:

```bash
applypilot job-leads links --config config/job_lead_queries.yaml
```

### Job lead commands

```bash
applypilot job-leads collect --config config/job_lead_sources.yaml
applypilot job-leads score --input outputs/public/job_leads_raw.json
applypilot job-leads export --format csv,md
applypilot job-leads links --config config/job_lead_queries.yaml
```

Public-safe outputs are written to `outputs/public/`:

- `job_leads.csv`
- `job_leads.md`
- `manual_search_links.md`
- `job_lead_summary.md`

### Android / Termux usage

```bash
pkg update && pkg install python git
cd ApplyPilot
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
applypilot job-leads collect --config config/job_lead_sources.yaml
applypilot job-leads score --input outputs/public/job_leads_raw.json
applypilot job-leads export --format csv,md
applypilot job-leads links --config config/job_lead_queries.yaml
```

If editable install is blocked, use `PYTHONPATH=src python -m applypilot.cli job-leads ...`.

### Codex Cloud usage

In Codex Cloud or any non-interactive container, run the same commands with `PYTHONPATH=src` if the package is not installed. Keep generated files under `outputs/public/` only and do not upload resumes, profiles, `.env` files, cookies, sessions, or passwords.

### GitHub Actions schedule

The workflow `.github/workflows/job-leads.yml` supports manual `workflow_dispatch` and a default 24-hour cron schedule. To enable it, push the workflow to GitHub and confirm Actions are enabled for the repository. To run every 6 hours, edit the workflow cron from `0 3 * * *` to `0 */6 * * *`.

The workflow uploads only public-safe files from `outputs/public/` and must not upload `.env`, resumes/CVs, profiles, cookies, sessions, passwords, or browser data.

### Privacy, anti-scam, and no-auto-apply rules

- No auto-apply is performed.
- Human review is required before every application.
- The agent does not store passwords, cookies, sessions, browser profiles, or personal account data.
- The agent does not bypass CAPTCHA, bot protection, login walls, paywalls, or robots restrictions.
- Treat deposits, paid applications, wire transfers, suspicious companies, unrealistic salary claims, and unclear apply paths as scam risks.
- ApplyPilot does not guarantee jobs, interviews, hiring, clients, or income.

See [`docs/JOB_LEAD_AGENT.md`](docs/JOB_LEAD_AGENT.md) and [`docs/SAFE_JOB_DISCOVERY_POLICY.md`](docs/SAFE_JOB_DISCOVERY_POLICY.md).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding standards, and PR guidelines.

---

## License

ApplyPilot is licensed under the [GNU Affero General Public License v3.0](LICENSE).

You are free to use, modify, and distribute this software. If you deploy a modified version as a service, you must release your source code under the same license.
