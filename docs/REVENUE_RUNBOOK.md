# ApplyPilot Revenue Runbook

## Purpose

This runbook turns ApplyPilot into a practical operating system for remote-work applications and client-ready job application materials.

The strongest use case is not a full SaaS yet. The strongest use case is a supervised workflow that helps create better application packs faster.

## Core offer

**Remote Job Application Pack**

Target buyers:
- Remote job seekers
- AI data annotation workers
- transcription and QA workers
- language evaluators
- freelancers applying to multiple platforms

Deliverables:
- job-fit assessment
- ATS keyword map
- CV summary rewrite
- tailored experience bullets
- cover letter
- screening answer drafts
- follow-up message
- final application checklist

## Pricing ladder

| Package | Price | Deliverables |
|---|---:|---|
| Basic | Rp100.000-Rp150.000 | 1 role, CV summary, cover letter, 3 screening answers |
| Pro | Rp250.000-Rp350.000 | 3 roles, keyword map, CV bullets, cover letters, screening answers |
| Custom | Rp500.000+ | multi-platform pack, profile copy, follow-up messages, delivery checklist |

## Safe operating model

Use ApplyPilot primarily for:
1. discovering opportunities
2. enriching job descriptions
3. scoring role fit
4. tailoring CV/resume content
5. drafting cover letters
6. preparing screening answers
7. exporting materials for manual review

Keep final submission supervised. Manual review protects quality, avoids wrong answers, and reduces account risk.

## Recommended Android/Termux workflow

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
applypilot run discover enrich score tailor cover --validation lenient
applypilot status
```

Use Android/Termux for discovery and material generation. Use manual review before submitting applications.

## Daily workflow

1. Select one target role family.
2. Run discovery and enrichment.
3. Score jobs and keep only strong-fit roles.
4. Generate tailored CV bullets and cover letters.
5. Review outputs manually.
6. Submit the strongest 3-5 applications.
7. Track every submission in Notion or a spreadsheet.
8. Follow up after 3-5 business days.

## Target role families for Cladius Weinert

High-fit role families:
- AI Data Annotator
- QA Reviewer
- Language Evaluator
- Transcription Specialist
- AI Trainer
- LLM/VLM Evaluator
- Remote Bilingual Reviewer

Avoid weak matches unless the job description strongly overlaps with existing experience.

## Quality rules

Do not fabricate:
- degrees
- certificates
- employer names
- dates
- project results
- language fluency
- tool experience

Allowed improvements:
- clearer wording
- better ATS keywords
- stronger bullets based on real experience
- better role alignment
- cleaner summaries
- better screening-answer structure

## Client delivery checklist

Before delivering a paid pack:
- confirm target role
- confirm buyer profile details
- collect current CV/profile
- collect 1-3 job descriptions
- generate fit assessment
- rewrite summary and bullets
- draft cover letter
- draft screening answers
- run final realism check
- deliver in Google Docs or PDF

## Outreach copy

```text
Saya membantu pencari kerja remote membuat paket lamaran yang lebih rapi dan sesuai target role.

Cocok untuk AI Data Annotation, Transcription, QA Review, Language Evaluation, dan remote freelance roles.

Yang Anda dapat:
- CV summary yang lebih kuat
- cover letter sesuai lowongan
- keyword ATS
- jawaban screening awal
- follow-up message

Harga mulai Rp100.000.
```

## Next engineering priorities

1. Add export command for application packs.
2. Add sample output folder.
3. Add supervised-mode documentation in README.
4. Add Notion/spreadsheet tracker template.
5. Add low-RAM Termux troubleshooting.

## Direct verdict

ApplyPilot is useful as a portfolio and service engine now. It is not ready to be sold as a standalone SaaS until the supervised workflow, sample outputs, onboarding, and export format are polished.
