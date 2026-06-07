# Safe Job Discovery Policy

ApplyPilot's scheduled job lead agent is designed for compliant discovery and human review.

## Allowed automated sources

- Official APIs, such as RemoteOK or Remotive public endpoints when available.
- Public ATS APIs, such as Greenhouse public job board endpoints and Lever public postings endpoints.
- RSS feeds when they are public and allowed.
- Search API results from configured providers such as Brave Search API, Bing Web Search API, SerpAPI, or Tavily.
- Generated manual search URLs.

## Forbidden automated behavior

ApplyPilot must not:

- Scrape LinkedIn, Indeed, Glassdoor, or login-heavy job boards.
- Bypass CAPTCHA, bot protection, login walls, paywalls, or robots restrictions.
- Store passwords, cookies, sessions, browser profiles, or personal account data.
- Auto-apply to jobs.
- Upload resumes/CVs or private profiles to public artifacts unless the files are explicitly public-safe.
- Promise guaranteed jobs, interviews, clients, hiring, or income.

## Human review requirement

All leads are `manual_apply_required=true`. Users must review the company, role, apply URL, pay terms, location eligibility, and scam indicators before applying.

## Anti-scam checks

Treat leads as risky when they mention deposits, paid applications, wire transfers, unrealistic salary claims, unclear company identity, or unclear apply paths.
