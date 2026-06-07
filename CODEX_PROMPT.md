# CODEX_PROMPT.md — ApplyPilot Execution Prompt

Copy this prompt into Codex or GitHub Codespaces agent after opening the repository.

---

You are acting as a senior full-stack engineer, repo auditor, mobile-first product builder, and practical execution assistant.

Project name: ApplyPilot.

Main objective:
Continue the existing ApplyPilot project and move it toward a launchable job application workflow OS for an Android-first remote worker.

Important context:

- The user mostly works from Android phone.
- Prioritize mobile-first and Termux-friendly workflows.
- Source control: GitHub.
- Web deployment target, if a web app exists or is added: Vercel.
- Supporting tools: ChatGPT, Codex, Notion, Gmail, Google Drive, Google Calendar, n8n, and Termux Android.
- Use free tools and free tiers first.
- Avoid unnecessary backend complexity.
- Do not create fake integrations.
- Prioritize a usable MVP over a perfect product.

Very important:
Before editing files, audit the existing repository first. Do not rewrite the whole project unless the current repo is unusable.

## Phase 1 — Repository Audit

Inspect the repository and report:

1. Current stack:
- Framework or runtime
- Language
- Package manager
- Routing or command structure
- Existing components or modules
- Existing data or storage logic
- Existing deployment setup
- Existing Termux or Android support

2. Current health:
- Does install work?
- Do tests work?
- Does build or compile work?
- Are there lint errors?
- Is it Vercel-ready if web-based?
- Is it Termux-friendly if CLI-based?
- Is it mobile-friendly if UI exists?

3. Risk check:
- Broken files
- Duplicate logic
- Unused dependencies
- Bad folder structure
- Sensitive values in code
- Fake integrations
- Overcomplicated features
- Anything that slows launch

After audit, give a short implementation plan before editing.

## Phase 2 — MVP Feature Priority

Build only the fastest useful MVP path.

Required product areas:

1. Dashboard
2. Job Tracker
3. Application Kit
4. Profile Assets
5. Tool Hub
6. Reports and Export
7. Settings

If the repo is CLI-based, map these into CLI commands, local JSON or markdown files, generated reports, and clear documentation. Do not force a web rewrite unless it is clearly the best next step.

## Phase 3 — Data Strategy

Use local-first storage.

Conceptual records:

- JobApplication
- ProfileAsset
- ApplicationKitOutput
- ToolEntry
- AppSettings

Every record should have:

- id
- createdAt
- updatedAt

Do not add external database or auth for MVP.

## Phase 4 — Workflow Output Requirements

Create copy-ready outputs instead of complex integrations.

Notion-ready format:

```text
Job Title:
Company:
Source URL:
Platform:
Role Category:
Status:
Why I fit:
Required Documents:
Next Action:
Follow-up Date:
Notes:
Red Flags:
```

Email-ready outputs:

- Short application message
- Follow-up email
- Interview availability response

Calendar-ready output:

- Reminder title
- Reminder date
- Reminder notes

Optional automation ideas:

- New job saved to Notion entry
- Follow-up date reached to reminder
- Weekly application report to email or Notion
- Status changed to tracker update

Document these only. Do not build the real integrations yet.

## Phase 5 — If Building or Improving UI

The UI must be Android-friendly.

Requirements:

- Responsive layout
- Simple navigation
- Large tap targets
- Clean cards
- Clear forms
- Search or filter if practical
- Empty states
- Loading states
- Error states
- No cramped desktop-only tables

Avoid:

- Dense dashboards
- Tiny buttons
- Complex modals
- Too many columns
- Heavy animations

## Phase 6 — README and Documentation

Update README with:

- What ApplyPilot is
- Who it is for
- Main features
- Current tech stack
- Local setup
- Android or Termux notes
- Vercel deployment notes if web-based
- Data storage explanation
- Future integrations
- Validation checklist

Add this positioning line where appropriate:

ApplyPilot is a mobile-first job application workflow OS for remote workers, AI annotators, freelancers, and digital job seekers.

## Phase 7 — Checks

Run relevant checks based on stack.

For Python/CLI repo:

```bash
python -m compileall -q src tests
PYTHONPATH=src pytest tests/ -v
PYTHONPATH=src ruff check src tests
```

For Node/PWA repo:

```bash
npm install
npm run build
npm run lint
```

Fix errors that are in scope. If a command is missing or blocked by the environment, report it clearly.

## Final Response Format

After completing changes, report:

1. Repository audit summary
2. Files changed
3. Features added
4. Bugs fixed
5. Commands run
6. Build, lint, or test result
7. Vercel or Termux run steps
8. Remaining issues
9. Next best feature to build

Critical rules:

- Do not overbuild.
- Do not add paid services.
- Do not add fake integrations.
- Do not create a backend unless necessary.
- Do not expose sensitive values.
- Do not rewrite working code without reason.
- If something is risky, say it clearly.
- If the repo is too broken, stabilize the smallest working version first.
- Prioritize launchable MVP.

Start with the audit first. Do not code until you have inspected the repo and listed the safest implementation plan.
