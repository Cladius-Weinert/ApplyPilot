"""Greenhouse public job board collector.

Uses only the public Greenhouse job board endpoint and never submits
applications or accesses authenticated pages.
"""

from __future__ import annotations

import httpx

from applypilot.job_leads.models import JobLead
from applypilot.job_leads.sources import SourceConfig

GREENHOUSE_ENDPOINT = "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"


def _remote_type(location: str) -> str:
    loc = location.lower()
    if "remote" in loc or "anywhere" in loc:
        return "remote"
    if "hybrid" in loc:
        return "hybrid"
    return "onsite_or_unknown"


def collect(source: SourceConfig, client: httpx.Client | None = None) -> list[JobLead]:
    if not source.enabled or not source.board_token:
        return []
    owns_client = client is None
    http = client or httpx.Client(timeout=20, follow_redirects=True)
    try:
        response = http.get(GREENHOUSE_ENDPOINT.format(board_token=source.board_token), params={"content": "true"})
        response.raise_for_status()
        data = response.json()
    finally:
        if owns_client:
            http.close()

    leads: list[JobLead] = []
    for item in data.get("jobs", [])[: source.limit]:
        offices = item.get("offices") or []
        location = ", ".join(str(office.get("name", "")).strip() for office in offices if office.get("name"))
        if not location:
            location = str((item.get("location") or {}).get("name", ""))
        url = str(item.get("absolute_url") or "")
        leads.append(
            JobLead(
                title=str(item.get("title") or "Untitled role"),
                company=source.name,
                source=source.name,
                source_category="public_ats_api",
                location=location,
                remote_type=_remote_type(location),
                apply_url=url,
                job_url=url,
                posted_date=str(item.get("updated_at") or ""),
                required_skills=source.tags,
                manual_apply_required=True,
                notes="Collected from Greenhouse public job board endpoint; human review required.",
            )
        )
    return leads
