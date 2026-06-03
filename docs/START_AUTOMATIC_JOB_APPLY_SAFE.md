# Start Automatic Job Apply Safely

Repository: `Cladius-Weinert/ApplyPilot`

Use ApplyPilot in a controlled way. Start with discovery, scoring, tailored documents, and dry-run form filling. Do not start with mass real submissions.

## Relevant target roles

Use these roles first because they fit a remote AI/language freelance profile:

- AI Data Annotator Indonesian
- Indonesian AI Trainer
- Bilingual Indonesian English Evaluator
- LLM Response Evaluator Indonesian
- Transcription QA Indonesian
- Remote Content Evaluator
- Balinese Linguist Remote
- Malay Indonesian Language Evaluator

## Local requirements

Install locally on your computer:

- Python 3.11+
- Node.js 18+
- Chrome or Chromium
- Gemini API key
- Claude Code CLI only if using browser-based auto-apply

## Install

```bash
pip install applypilot
pip install --no-deps python-jobspy
pip install pydantic tls-client requests markdownify regex
```

## Initialize locally

```bash
applypilot init
applypilot doctor
```

During setup, use your private data only on your own computer. Do not commit the generated `.env`, real `profile.json`, resume files, phone number, full address, passwords, API keys, or job-board login credentials.

## Recommended safe sequence

Generate job matches and documents first:

```bash
applypilot run --min-score 8 --validation lenient
```

Test form filling without submitting:

```bash
applypilot apply --dry-run --workers 1
```

Only after manual review, run real submission with low speed:

```bash
applypilot apply --workers 1
```

## Rule

Use real facts only. Do not fabricate degrees, certificates, work history, companies, dates, or credentials.
