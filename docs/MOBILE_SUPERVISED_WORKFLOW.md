# Mobile Supervised Workflow

## Goal

Use ApplyPilot from Android/Termux for the parts that work best on mobile:

1. discover jobs
2. enrich job data
3. score fit
4. tailor resume/CV content
5. generate cover letters
6. review and submit manually

This is safer and more realistic than trying to run full browser automation from Android.

## Recommended command

```bash
applypilot run discover enrich score tailor cover --validation lenient
applypilot status
```

## Android/Termux setup

```bash
pkg update && pkg upgrade -y
pkg install git python python-pip clang make rust -y
git clone https://github.com/Cladius-Weinert/ApplyPilot.git
cd ApplyPilot
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel setuptools
pip install -e ".[dev]"
applypilot init
applypilot doctor
```

## Safe review process

Before submitting any application:

- check the company name
- check the role title
- check the CV summary
- check tailored bullets for accuracy
- remove any unverifiable claim
- check cover letter tone
- check screening answers
- confirm salary, location, remote status, and availability answers

## What to avoid on mobile

Avoid relying on Android for full browser-driven submission unless you have a stable browser environment and have verified the target site allows this workflow.

Do not submit applications automatically without manual review.

## Best use case

This workflow is strongest for preparing high-quality application materials quickly. It can support a paid service such as Remote Job Application Pack.