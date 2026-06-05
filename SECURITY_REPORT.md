# Security Report — ApplyPilot

**Audit date:** 2026-06-05  
**Scope:** secrets, credential handling, browser automation, data leakage, API abuse, prompt/form injection, and local file risk.

## Executive risk rating

**Current security posture:** Medium risk for technical local use; High risk if offered as SaaS without major changes.

ApplyPilot handles highly sensitive data: resumes, contact details, work authorization, compensation expectations, job-site credentials, API keys, generated documents, browser sessions, and application history. The local-first model is a strength, but auto-apply and browser control introduce meaningful risk.

## Findings

### 1. Secrets exposure

**Status:** Partially controlled.

Positive controls:

- `.gitignore` excludes common user data and env files.
- `.env.example` does not include real credentials.
- `doctor` reports provider presence without printing key values.

Risks:

- Users may paste credentials into `profile.json`, which is plain JSON.
- Generated prompt files for browser agents may include sensitive profile data.
- Debug logs from scraping or LLM failures could accidentally include page content or generated answers.

Recommendations:

- Add `applypilot redact` or centralized `redact_secret()` for logs.
- Add `applypilot privacy --purge` to delete prompts/logs/generated artifacts.
- Add optional encryption for `profile.json` and `.env` using a user passphrase.
- Avoid storing job-site passwords unless absolutely necessary.

### 2. Credential handling

**Risk:** High.

The setup wizard currently asks for a job-site username/password for login walls. This is sensitive and risky in plain local JSON.

Recommendations:

- Default to not storing passwords.
- Store only username/email by default.
- Prompt users to enter passwords interactively at apply time.
- If persistent credentials are needed, use OS keychain where available or encrypted storage.

### 3. Browser automation risks

**Risk:** High.

Browser agents can:

- Submit incorrect applications.
- Apply to scam/fake jobs.
- Leak PII into third-party forms.
- Trigger anti-bot systems or account locks.
- Follow malicious links in job descriptions.

Recommendations:

- Make review-before-submit the default.
- Add domain allowlist and blocklist enforcement.
- Add screenshot/form summary before final submission.
- Require explicit confirmation for every submit action unless `--auto-submit` is passed.
- Add a maximum daily application cap.

### 4. Data leakage risks

**Risk:** Medium to High.

Data sent to LLM providers can include resume content, contact details, compensation, and work authorization.

Recommendations:

- Add a privacy mode that redacts phone/email/address before job scoring.
- Provide provider-specific privacy warnings.
- Add local LLM setup as the recommended privacy-sensitive path.
- Track which provider processed each generated artifact.

### 5. API abuse and cost risks

**Risk:** Medium.

Scoring/tailoring many jobs can generate high LLM usage and rate limits. Scraping can trigger anti-bot rules.

Recommendations:

- Add per-run budget limits.
- Add provider rate limit settings.
- Cache LLM results by job URL/content hash.
- Add exponential backoff for all network stages, not only LLM calls.

### 6. Injection risks

**Risk:** Medium to High.

Job descriptions are untrusted text. They may contain prompt-injection instructions like "ignore previous instructions" or malicious links. Browser automation prompts may include untrusted page content.

Recommendations:

- Wrap job descriptions as untrusted data in prompts.
- Add prompt-injection detection warnings.
- Never let job text override user profile facts, compensation rules, or work authorization.
- Add tests around malicious job descriptions.

## Security priorities

| Priority | Improvement | Impact |
|---:|---|---|
| P0 | Review-before-submit default | Prevents harmful auto-submits. |
| P0 | Stop storing passwords by default | Reduces credential compromise risk. |
| P1 | Privacy purge command | Gives users control over artifacts/logs. |
| P1 | Prompt-injection guardrails | Reduces LLM/browser manipulation. |
| P1 | Domain allowlist/blocklist | Avoids scam or unsupported application sites. |
| P2 | Encrypted profile store | Needed for SaaS/paid trust. |

## SaaS security requirements

Before SaaS commercialization:

- Encrypt PII at rest and in transit.
- Separate tenant data.
- Add audit logs.
- Implement account deletion/data export.
- Publish privacy policy and data processing terms.
- Add SOC2-style controls if targeting professionals/teams.
- Avoid storing third-party job-site passwords.

## Verdict

ApplyPilot is acceptable for local technical experimentation with careful users. It is not yet safe enough for fully unattended mainstream auto-apply or SaaS operation. The product should shift toward user-reviewed automation and stronger privacy controls before scaling.
