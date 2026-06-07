"""Remotive public API collector.

Uses Remotive's public remote jobs API only. It does not submit applications or
store account/session data.
"""

from __future__ import annotations

import httpx

from applypilot.job_leads.models import JobLead
from applypilot.job_leads.sources import SourceConfig

REMOTIVE_ENDPOINT = "https://remotive.com/api/remote-jobs"


def collect(source: SourceConfig, client: httpx.Client | None = None) -> list[JobLead]:
    if not source.enabled:
        return []
    owns_client = client is None
    http = client or httpx.Client(timeout=20, follow_redirects=True, headers={"User-Agent": "ApplyPilot-safe-job-leads/1.0"})
    try:
        params = {"search": source.query} if source.query else None
        response = http.get(source.url or REMOTIVE_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
    finally:
        if owns_client:
            http.close()

    leads: list[JobLead] = []
    for item in data.get("jobs", [])[: source.limit]:
        url = str(item.get("url") or "")
        leads.append(
            JobLead(
                title=str(item.get("title") or "Untitled role"),
                company=str(item.get("company_name") or "Unknown / verify manually"),
                source=source.name,
                source_category="official_api",
                location=str(item.get("candidate_required_location") or "Remote / verify eligibility"),
                remote_type="remote",
                apply_url=url,
                job_url=url,
                posted_date=str(item.get("publication_date") or ""),
                salary_or_rate=str(item.get("salary") or ""),
                contract_type=str(item.get("job_type") or ""),
                required_skills=[*source.tags, str(item.get("category") or "")],
                manual_apply_required=True,
                notes="Collected from Remotive public API; human review required before applying.",
            )
        )
    return leads
