# Termux Optimization Plan — ApplyPilot

**Audit date:** 2026-06-05  
**Target:** Android 10, 11, 12, 13, and 14 running Termux.

## Executive summary

ApplyPilot can be made genuinely useful on Termux for job discovery, enrichment, scoring, resume tailoring, cover letters, and dashboard/status workflows. Fully unattended browser auto-apply is not reliably portable across Android versions because Playwright/Chrome automation expects a desktop-like browser environment.

The right Termux product strategy is:

> **Mobile job-search command center:** discover roles, score them, generate materials, review from Android, and manually submit or sync to desktop for auto-apply.

## Android version considerations

| Android version | Expected Termux support | Notes |
|---|---|---|
| Android 10 | Good for CLI; browser automation limited | Older devices may have lower RAM and slower Python builds. |
| Android 11 | Good for CLI; storage permissions require care | Use `termux-setup-storage` when importing resumes. |
| Android 12 | Good for CLI; background process limits | Keep workers low and avoid long unattended browser runs. |
| Android 13 | Good for CLI; notification/background restrictions | Use foreground sessions for long jobs. |
| Android 14 | Good for CLI; stricter process/storage behavior | Prefer conservative memory and explicit file paths. |

## Recommended install path

See `docs/TERMUX.md` for user-facing commands. The core path is:

```bash
pkg update && pkg upgrade
pkg install python git clang rust make libxml2 libxslt openssl
python -m pip install --upgrade pip wheel setuptools
python -m pip install -e ".[dev]"
make install-jobspy
applypilot init
applypilot doctor
```

## Required Termux optimizations

### Already improved

- Added Termux setup docs.
- Added Termux-aware Chrome diagnostics.
- Added Termux-safe Chrome user data path fallback.
- Added lightweight Makefile commands.

### Next high-impact improvements

1. **Termux preset command**
   - `applypilot doctor --termux` or `applypilot termux-check`.
   - Report Python, storage, build tools, disk space, RAM, and missing packages.

2. **Mobile-safe defaults**
   - Force `workers=1` on Termux unless explicitly overridden.
   - Recommend `--validation lenient` for lower LLM cost.
   - Add `--max-jobs` for small mobile runs.

3. **Storage import helper**
   - `applypilot import-resume /sdcard/Download/resume.pdf`.
   - Validate `.txt` exists for AI stages.

4. **No-browser mode**
   - Make discovery/tailoring/manual-apply workflow first-class.
   - Add `applypilot export --format csv|html|notion`.

5. **Local dashboard**
   - Generate a mobile-friendly static HTML dashboard.
   - Open with `termux-open` when available.

## Browser automation reality

Playwright + Chrome/Chromium can work in some proot Linux setups but should not be promised as standard Android support. Recommended wording:

- "Termux supports discovery and AI application-material generation."
- "Auto-apply requires desktop Chrome/Chromium or a carefully configured proot environment."

## Termux product opportunity

Very few job-search automation tools optimize for Android power users. ApplyPilot can own this niche by becoming:

- A CLI-first job search assistant.
- A mobile-friendly resume tailoring tool.
- A local/private alternative to SaaS job automation.
- A freelance operator toolkit for managing client job searches from a phone.
