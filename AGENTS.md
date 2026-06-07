# AGENTS.md — ApplyPilot Agent Instructions

## Goal

Make ApplyPilot a practical job application operating system for an Android-first remote worker. Audit the existing repository before changing architecture.

## User Context

- Main device: Android phone.
- Prioritize mobile-first and Termux-friendly workflows.
- Source control: GitHub.
- Web deployment target, if a web layer is added: Vercel.
- Supporting tools: ChatGPT, Codex, GitHub, Vercel, Notion, Gmail, Google Drive, Google Calendar, n8n, and Termux Android.
- Prefer free tools and free tiers.
- Avoid unnecessary backend complexity.

## Critical Rules

- Audit the repository before editing.
- Preserve working code where possible.
- If the repo is CLI-based, do not replace it with a web app without explaining the migration path first.
- Do not add database, authentication, or external service integration for MVP unless already present and required.
- Do not create fake integrations.
- Keep sensitive values out of committed files.
- Prefer local-first storage for MVP.
- If a feature slows launch, move it to later.

## MVP Product Areas

1. Dashboard
2. Job Tracker
3. Application Kit
4. Profile Assets
5. Tool Hub
6. Reports and Export
7. Settings

If the existing repo is CLI-based, map these into commands, local files, markdown reports, or a lightweight web layer only after audit.

## Mobile-First Rules

- Must work well for an Android-first user.
- If building UI, use large tap targets, cards, simple forms, and readable spacing.
- Avoid cramped desktop layouts.
- Add empty, loading, and error states where relevant.
- Keep navigation simple.

## Data Rules

Use local-first storage for MVP.

Conceptual records:

- JobApplication
- ProfileAsset
- ApplicationKitOutput
- ToolEntry
- AppSettings

Every record should include id, createdAt, and updatedAt.

## Tool Workflow Rules

Do not build real integrations for Notion, Gmail, Calendar, Drive, or n8n in the MVP.

Create copy-ready outputs instead:

- Notion-ready application summary
- Email draft text
- Calendar reminder text
- Optional automation ideas

The Tool Hub should organize workflows honestly, not pretend to connect tools.

## Checks

Run checks based on the detected stack.

For Python CLI repo, prefer:

```bash
python -m compileall -q src tests
PYTHONPATH=src pytest tests/ -v
PYTHONPATH=src ruff check src tests
```

For Node or PWA repo, prefer:

```bash
npm install
npm run build
npm run lint
```

If a command is missing or cannot run, report it clearly.

## Final Report

After work, report:

1. Repository audit summary
2. Files changed
3. Features added
4. Bugs fixed
5. Commands run
6. Build, lint, or test result
7. Vercel or Termux run steps
8. Remaining issues
9. Next best feature
