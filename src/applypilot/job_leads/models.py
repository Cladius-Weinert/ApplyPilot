"""Normalized public-safe job lead schema."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

SOURCE_TYPES = {"official_api", "public_ats_api", "rss_feed", "search_api", "manual_search_url"}
PRIORITIES = {"low", "medium", "high"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.replace(";", ",").split(",") if part.strip()]
    return [str(value).strip()] if str(value).strip() else []


@dataclass
class JobLead:
    title: str
    company: str
    source: str
    source_category: str
    location: str = ""
    remote_type: str = "unknown"
    apply_url: str = ""
    job_url: str = ""
    posted_date: str = ""
    detected_at: str = field(default_factory=utc_now_iso)
    salary_or_rate: str = ""
    contract_type: str = ""
    required_language: str = ""
    required_skills: list[str] = field(default_factory=list)
    match_score: int = 0
    reason_for_match: str = ""
    application_priority: str = "medium"
    recommended_resume_version: str = "general_remote_ai_worker"
    recommended_cover_letter_template: str = "basic_remote_work"
    risk_flags: list[str] = field(default_factory=list)
    manual_apply_required: bool = True
    notes: str = "Human review required before applying."

    def __post_init__(self) -> None:
        self.title = str(self.title or "").strip()
        self.company = str(self.company or "").strip()
        self.source = str(self.source or "").strip()
        self.source_category = str(self.source_category or "").strip()
        self.location = str(self.location or "").strip()
        self.remote_type = str(self.remote_type or "unknown").strip().lower()
        self.apply_url = str(self.apply_url or "").strip()
        self.job_url = str(self.job_url or "").strip()
        self.posted_date = str(self.posted_date or "").strip()
        self.detected_at = str(self.detected_at or utc_now_iso()).strip()
        self.salary_or_rate = str(self.salary_or_rate or "").strip()
        self.contract_type = str(self.contract_type or "").strip()
        self.required_language = str(self.required_language or "").strip()
        self.required_skills = _as_list(self.required_skills)
        self.match_score = max(0, min(100, int(self.match_score or 0)))
        self.application_priority = str(self.application_priority or "medium").lower()
        if self.application_priority not in PRIORITIES:
            self.application_priority = "medium"
        self.risk_flags = _as_list(self.risk_flags)
        self.manual_apply_required = bool(self.manual_apply_required)
        if self.source_category not in SOURCE_TYPES:
            raise ValueError(f"Unsupported source_category: {self.source_category}")
        if not self.title:
            raise ValueError("JobLead.title is required")
        if not self.company:
            raise ValueError("JobLead.company is required")
        if not (self.apply_url or self.job_url):
            raise ValueError("JobLead requires apply_url or job_url")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "JobLead":
        return cls(**data)
