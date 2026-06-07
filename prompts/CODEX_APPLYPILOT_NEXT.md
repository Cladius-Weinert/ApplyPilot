# Codex Task: Improve ApplyPilot supervised workflow

You are working on the ApplyPilot repository.

## Objective
Improve ApplyPilot as a safe, mobile-first, supervised remote-work application workflow. The goal is to make the repository more useful for job seekers and for a service called Remote Job Application Pack.

## Context
The owner works primarily from Android/HP using Termux, GitHub, Codex, Notion, Gmail, Google Drive, and Vercel when relevant. This repository is a Python CLI project, not a Vercel web app. Do not force web deployment unless a separate web UI is explicitly requested.

## Critical direction
Prioritize supervised workflows:
- discover jobs
- enrich job data
- score fit
- tailor CV/resume content
- generate cover letters
- prepare screening answers
- export materials
- allow manual review before submission

Treat browser-driven submission as optional and advanced. Keep Android/Termux focused on discovery, scoring, tailoring, and export.

## Tasks

### 1. Inspect repository
Inspect the current structure before editing. Identify:
- CLI commands
- config files
- docs
- tests
- export capabilities
- Termux blockers
- existing README claims that should be softened or clarified

### 2. Add supervised workflow docs
Add or improve documentation for a supervised flow:

```bash
applypilot run discover enrich score tailor cover --validation lenient
applypilot status
```

Explain that final application submission should be reviewed manually.

### 3. Add application pack export plan
If export functionality exists, document it clearly.
If not, propose and implement the smallest safe export feature:
- Markdown export
- one folder per job
- includes fit score, keyword map, CV bullets, cover letter, screening answers, and checklist

Do not add a database migration unless necessary.

### 4. Improve Termux guide
Improve Android/Termux docs:
- minimum requirements
- low-RAM warnings
- commands that work on mobile
- commands that need desktop/browser automation
- common errors and fixes
- safe manual submission workflow

### 5. Add sample outputs
Add sample Markdown files under:

```text
samples/application-packs/
```

Create sample packs for:
- AI Data Annotator
- QA Reviewer
- Language Evaluator

Use realistic generic examples. Do not invent fake certificates, fake degrees, fake employers, or unverifiable claims.

### 6. README improvement
Update README to make the safest path clear:
- mobile-friendly supervised mode first
- full automation optional
- API keys stay in `.env`
- manual review recommended before final submission

### 7. Testing
Run available checks:

```bash
python -m compileall -q src tests
PYTHONPATH=src pytest tests -v
PYTHONPATH=src ruff check src tests
```

If dependency installation fails because of the environment, document that clearly and still run what is possible with `PYTHONPATH=src`.

## Output expected
When finished, report:
1. Files changed
2. New commands added or documented
3. Tests run
4. Remaining blockers
5. Exact next Android/HP action

## Do not
- Do not add paid infrastructure.
- Do not add Supabase/Firebase.
- Do not expose secrets.
- Do not overbuild a web dashboard.
- Do not claim that ApplyPilot guarantees jobs.
- Do not encourage submitting applications without review.
