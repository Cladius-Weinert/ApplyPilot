# AGENTS.md

## Owner Context
This repository is maintained by Cladius Weinert. The owner works mobile-first using Android/HP, GitHub, Termux, ChatGPT/Codex, Vercel, Notion, n8n, and web tools.

## Main Objective
Make this project practical, buildable, secure, documented, and ready for deployment or APK/PWA packaging when possible.

## Work Priorities
1. Inspect the full repository before editing.
2. Fix build errors, dependency issues, broken scripts, missing files, and setup problems.
3. Make the project easy to run from Android/Termux when possible.
4. Prepare the project for GitHub, Vercel, PWA, APK, Expo, Capacitor, Flutter, or native Android depending on the stack.
5. Improve README.md, setup guide, installation guide, build guide, and troubleshooting.
6. Keep changes simple, safe, and reviewable.
7. Do not add unnecessary backend services.
8. Avoid Supabase, Firebase, paid services, or complex infrastructure unless explicitly requested.
9. Never expose API keys, tokens, credentials, private URLs, or secrets.
10. Add or improve .env.example if environment variables are required.

## Code Review Rules
When reviewing code, check for:
- Build errors
- Broken dependencies
- Security risks
- Hardcoded secrets
- Bad file structure
- Missing .gitignore coverage
- Missing README instructions
- Broken mobile/Termux setup
- APK/PWA/deployment blockers
- Unclear scripts
- Unused or risky files
- Poor error handling
- UI bugs
- Incomplete features

## Mobile / Termux Rules
When relevant, always document:
- Termux install commands
- GitHub mobile workflow
- Build commands
- Deployment steps
- APK/PWA packaging path
- Known Android limitations

## Testing Rules
Before finalizing, run available checks when possible:
- install command
- build command
- test command
- lint command
- typecheck command

If a command fails, explain the exact cause and fix it if safe.

## Review Guidance
For code review, also follow `code_review.md` when it exists.

## Final Report Format
Always respond with:
1. What was inspected
2. What was changed
3. Commands run
4. Build/test result
5. Remaining blockers
6. Exact next action from Android/HP
