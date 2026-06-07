# ApplyPilot MVP Scope

## Positioning

ApplyPilot is a mobile-first job application workflow OS for remote workers, AI annotators, freelancers, and digital job seekers.

## Main Users

- Remote job seekers
- AI data annotators
- Transcription and QA workers
- Language evaluators
- Content writers
- Freelancers
- Digital workers applying to many platforms

## Main Problem

The user applies to many remote work opportunities across platforms. Without a system, job links, CV versions, cover letters, follow-up dates, screening answers, and platform notes become scattered.

ApplyPilot should become a practical command center for applications.

## MVP Goal

Build the smallest useful version that helps the user:

1. Save job opportunities.
2. Track application status.
3. Generate reusable application material from templates.
4. Store profile assets.
5. Organize workflow tools.
6. Export or copy data to Notion, email, and other tools.
7. Run from Android or Termux where practical.

## Core MVP Features

### 1. Dashboard

Show:

- Total applications
- Active applications
- Assessment stage
- Interview stage
- Follow-up needed
- Accepted
- Rejected
- Archived
- Recent applications
- Quick actions

Suggested quick actions:

- Add Job
- Generate Kit
- Export Data
- Open Tool Hub

### 2. Job Tracker

Fields:

- Job title
- Company
- Job URL
- Platform or source
- Role category
- Status
- Deadline
- Salary or rate
- Notes
- Red flags
- Required documents
- Created date
- Updated date

Platform options:

- Indeed
- LinkedIn
- Greenhouse
- Workday
- Telus
- Outlier
- Appen
- RWS
- OneForma
- Mercor
- Prolific
- Other

Role category options:

- AI Annotation
- Transcription
- QA
- Language Evaluation
- Content Writing
- Marketing
- Software or Automation
- Other

Status options:

- Saved
- Preparing
- Applied
- Assessment
- Interview
- Follow-up
- Accepted
- Rejected
- Archived

### 3. Application Kit

For a selected job, generate:

- CV focus points
- Cover letter outline
- Short application message
- Screening answer draft
- Follow-up email draft
- Interview preparation notes
- Notion-ready application summary

Rules:

- Use local templates first.
- No paid API required for MVP.
- If an AI provider is already supported by the repo, keep usage optional and documented.
- If no AI integration exists, do not add it yet.

### 4. Profile Assets

Store reusable career materials:

- Profile summary
- Skills
- Experience bullets
- Certifications
- Portfolio links
- CV versions
- Cover letter versions
- Prompt templates
- Common answers

Suggested default categories:

- AI Data Annotation
- Transcription
- QA
- Language Evaluation
- Content Writing
- Marketing
- Software or Automation
- General Remote Work

### 5. Tool Hub

Workflow cards for:

- ChatGPT
- Codex
- GitHub
- Vercel
- Notion
- Gmail
- Google Drive
- Google Calendar
- n8n
- Termux Android

Each card should include:

- Tool name
- Purpose
- Recommended use
- Setup status
- Link
- Notes

Setup status options:

- Not Started
- In Progress
- Ready
- Optional
- Later

Do not create real OAuth integrations in MVP.

### 6. Reports and Export

Include:

- Copy job summary
- Copy cover letter draft
- Copy follow-up draft
- Copy Notion-ready job entry
- Export all data as JSON
- Import JSON backup if safe and simple
- CSV export only if practical

### 7. Settings

Include:

- App info
- Storage explanation
- Export/import controls
- Theme setting if simple
- Future integration notes

## Notion-Ready Format

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

## Email-Ready Outputs

- Short application message
- Follow-up email
- Interview availability response
- Recruiter response
- Assessment clarification message

## Calendar-Ready Output

```text
Reminder Title:
Reminder Date:
Reminder Notes:
Related Job:
Company:
Next Action:
```

## Optional Automation Ideas

Document only. Do not build yet.

- New job saved to Notion entry
- Follow-up date reached to reminder
- Weekly application report to email or Notion
- Status changed to tracker update
- New CV version saved to Drive backup

## Later Features

Move these to later:

- Real Notion API
- Gmail OAuth
- Google Calendar OAuth
- Google Drive sync
- n8n webhook automation
- External database
- Multi-user accounts
- Authentication
- Team collaboration
- Paid subscription features
- Browser extension
- Scraping job sites

## MVP Success Criteria

The MVP is successful if:

- The project builds or passes relevant tests.
- It works from Android or Termux where practical.
- The user can add and manage job applications.
- The user can generate template-based application material.
- The user can store profile assets.
- The user can copy or export data.
- The README explains setup clearly.
