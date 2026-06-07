"""Rule-based, explainable scoring for safe job leads."""

from __future__ import annotations

from datetime import datetime, timezone

from applypilot.job_leads.models import JobLead

POSITIVE_KEYWORDS = {
    "remote": 8,
    "worldwide": 8,
    "anywhere": 8,
    "indonesia": 10,
    "indonesian": 10,
    "english": 4,
    "ai data": 10,
    "data annotation": 10,
    "llm evaluation": 10,
    "ai trainer": 8,
    "transcription qa": 8,
    "search evaluation": 8,
    "rws": 7,
    "aop": 7,
    "research": 5,
    "freelance": 7,
    "contract": 6,
    "part-time": 4,
}
NEGATIVE_KEYWORDS = {
    "onsite": -12,
    "on-site": -12,
    "hybrid": -5,
    "us only": -12,
    "u.s. only": -12,
    "eu only": -10,
    "senior software engineer": -8,
    "deposit": -25,
    "application fee": -25,
    "paid application": -25,
    "wire transfer": -25,
    "too good to be true": -12,
}
LANGUAGE_HINTS = ("indonesian", "bahasa", "english")


def _combined_text(lead: JobLead) -> str:
    return " ".join(
        [
            lead.title,
            lead.company,
            lead.location,
            lead.remote_type,
            lead.contract_type,
            lead.required_language,
            " ".join(lead.required_skills),
            lead.salary_or_rate,
            lead.notes,
        ]
    ).lower()


def _posted_days_ago(posted_date: str) -> int | None:
    if not posted_date:
        return None
    try:
        parsed = datetime.fromisoformat(posted_date.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return max(0, (datetime.now(timezone.utc) - parsed).days)


def score_lead(lead: JobLead) -> JobLead:
    text = _combined_text(lead)
    score = 45
    reasons: list[str] = []
    risk_flags = set(lead.risk_flags)

    for keyword, points in POSITIVE_KEYWORDS.items():
        if keyword in text:
            score += points
            reasons.append(f"+{points} {keyword}")

    for keyword, points in NEGATIVE_KEYWORDS.items():
        if keyword in text:
            score += points
            reasons.append(f"{points} {keyword}")
            if points <= -20:
                risk_flags.add(keyword.replace(" ", "_"))

    if lead.apply_url:
        score += 8
        reasons.append("+8 clear apply URL")
    else:
        score -= 10
        reasons.append("-10 unclear apply path")
        risk_flags.add("unclear_apply_path")

    days = _posted_days_ago(lead.posted_date)
    if days is not None:
        if days <= 7:
            score += 8
            reasons.append("+8 recent posting")
        elif days > 45:
            score -= 5
            reasons.append("-5 older posting")

    if lead.required_language and not any(lang in lead.required_language.lower() for lang in LANGUAGE_HINTS):
        score -= 8
        reasons.append("-8 language mismatch risk")
        risk_flags.add("language_mismatch_review")

    lead.match_score = max(0, min(100, score))
    lead.risk_flags = sorted(risk_flags)
    lead.reason_for_match = "; ".join(reasons[:12]) or "General remote job lead; review manually."
    if lead.match_score >= 75 and not lead.risk_flags:
        lead.application_priority = "high"
    elif lead.match_score < 50 or lead.risk_flags:
        lead.application_priority = "low"
    else:
        lead.application_priority = "medium"
    if "llm" in text or "ai" in text or "annotation" in text:
        lead.recommended_resume_version = "ai_data_worker"
        lead.recommended_cover_letter_template = "ai_data_annotation"
    elif "research" in text or "rws" in text or "aop" in text:
        lead.recommended_resume_version = "research_operations"
        lead.recommended_cover_letter_template = "research_workflow"
    return lead


def score_leads(leads: list[JobLead]) -> list[JobLead]:
    return [score_lead(lead) for lead in leads]
