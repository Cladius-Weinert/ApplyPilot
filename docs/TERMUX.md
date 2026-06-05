# ApplyPilot on Termux Android

ApplyPilot can run its lightweight CLI, setup wizard, discovery, enrichment, scoring, resume tailoring, and cover-letter generation from Termux. Full browser-driven auto-apply is harder on Android because it depends on Claude Code, Node.js, and a controllable Chrome/Chromium binary.

## Recommended Termux path

Use Termux for **discovery + AI-assisted application materials**, then submit applications manually from your Android browser or desktop.

```bash
pkg update && pkg upgrade
pkg install python git clang rust make libxml2 libxslt openssl
python -m pip install --upgrade pip wheel setuptools

# From a cloned repo
cd ApplyPilot
python -m pip install -e ".[dev]"

# Optional job-board scraper support
python -m pip install --no-deps python-jobspy
python -m pip install pydantic tls-client requests markdownify regex

# Prepare user config
mkdir -p ~/.applypilot
cp .env.example ~/.applypilot/.env
applypilot init
applypilot doctor
```

## Environment file

Edit `~/.applypilot/.env` and set one LLM provider:

```bash
nano ~/.applypilot/.env
```

At minimum, set `GEMINI_API_KEY` for the recommended low-cost path. Keep this file private and do not commit it.

## Run a safe workflow

```bash
applypilot doctor
applypilot run discover enrich
applypilot run score tailor cover --validation lenient
applypilot status
```

If you only want to verify command wiring without contacting job sites or LLM providers, use:

```bash
applypilot run discover --dry-run
```

## Auto-apply limitations on Android

`applypilot apply` requires Claude Code, Node.js/`npx`, and Chrome/Chromium automation. On Android Termux this may require a proot Linux environment with Chromium installed and `CHROME_PATH` pointing to that Chromium binary.

Example only if you have a working Chromium inside proot:

```bash
export CHROME_PATH=/usr/bin/chromium
applypilot doctor
applypilot apply --dry-run --limit 1
```

If `applypilot doctor` reports Chrome/Chromium as missing, use ApplyPilot for discovery and tailoring on Termux, then apply manually.

## Troubleshooting

- If a Python wheel fails to build, run `pkg install clang rust make` and retry.
- If YAML or JSON config fails to load, fix the line reported by the error or re-run `applypilot init`.
- If job-board discovery dependencies conflict, install `python-jobspy` with `--no-deps` and then install the runtime dependencies shown above.
- If storage access is needed for resume files, run `termux-setup-storage` and copy your resume into `~/.applypilot/`.
