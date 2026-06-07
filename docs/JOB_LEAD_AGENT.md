# ApplyPilot Safe Scheduled Job Lead Agent

The job lead agent collects public-safe job leads for remote jobseekers, AI data workers, freelancers, and application tracking users. It is discovery-only: it never auto-applies and never stores job-board credentials.

## What it collects automatically

- Greenhouse public job board postings.
- Lever public postings.
- RemoteOK and Remotive public APIs when available.
- Optional search API results when one of these keys exists:
  - `BRAVE_SEARCH_API_KEY`
  - `BING_SEARCH_API_KEY`
  - `SERPAPI_API_KEY`
  - `TAVILY_API_KEY`

Search API collection is skipped when keys are missing.

## Manual-only sources

The agent only generates search links for these boards and never fetches or scrapes them:

- LinkedIn
- Indeed
- Glassdoor
- Google Jobs
- ZipRecruiter

## Commands

```bash
applypilot job-leads collect --config config/job_lead_sources.yaml
applypilot job-leads score --input outputs/public/job_leads_raw.json
applypilot job-leads export --format csv,md
applypilot job-leads links --config config/job_lead_queries.yaml
```

Outputs are written under `outputs/public/`:

- `job_leads_raw.json`
- `job_leads_scored.json`
- `job_leads.csv`
- `job_leads.md`
- `manual_search_links.md`
- `job_lead_summary.md`

## Termux / Android

```bash
pkg update && pkg install python git
cd ApplyPilot
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
applypilot job-leads links --config config/job_lead_queries.yaml
applypilot job-leads collect --config config/job_lead_sources.yaml
applypilot job-leads score --input outputs/public/job_leads_raw.json
applypilot job-leads export --format csv,md
```

If editable install is blocked, run with `PYTHONPATH=src python -m applypilot.cli ...`.

## Codex Cloud / container usage

Use `PYTHONPATH=src python -m applypilot.cli job-leads ...` when editable installs are unavailable. Keep all generated outputs under `outputs/public/` and never upload private files.

## GitHub Actions schedule

`.github/workflows/job-leads.yml` runs once every 24 hours by default and can be started manually from the Actions tab. To run every 6 hours, change the cron comment in the workflow from `0 3 * * *` to `0 */6 * * *`.

The workflow uploads only public-safe files from `outputs/public/` and explicitly avoids `.env`, profile, resume/CV, cookies, sessions, passwords, and browser data.
