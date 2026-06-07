"""Lever public postings collector.

Uses only Lever's public postings endpoint and never submits applications.
"""

from __future__ import annotations

import httpx

from applypilot.job_leads.models import JobLead
from applypilot.job_leads.sources import SourceConfig

LEVER_ENDPOINT = "https://api.lever.co/v0/postings/{company_slug}"


def _remote_type(item: dict) -> str:
    workplace = str(item.get("workplaceType") or "").lower()
    location = str((item.get("categories") or {}).get("location", "")).lower()
    if "remote" in workplace or "remote" in location:
        return "remote"
    if "hybrid" in workplace or "hybrid" in location:
        return "hybrid"
    return "onsite_or_unknown"


def collect(source: SourceConfig, client: httpx.Client | None = None) -> list[JobLead]:
    if not source.enabled or not source.company_slug:
        return []
    owns_client = client is None
    http = client or httpx.Client(timeout=20, follow_redirects=True)
    try:
        response = http.get(LEVER_ENDPOINT.format(company_slug=source.company_slug), params={"mode": "json"})
        response.raise_for_status()
        data = response.json()
    finally:
        if owns_client:
            http.close()

    leads: list[JobLead] = []
    for item in data[: source.limit]:
        categories = item.get("categories") or {}
        url = str(item.get("hostedUrl") or item.get("applyUrl") or "")
        leads.append(
            JobLead(
                title=str(item.get("text") or "Untitled role"),
                company=source.name,
                source=source.name,
                source_category="public_ats_api",
                location=str(categories.get("location") or ""),
                remote_type=_remote_type(item),
                apply_url=url,
                job_url=url,
                contract_type=str(categories.get("commitment") or ""),
                required_skills=source.tags,
                manual_apply_required=True,
                notes="Collected from Lever public postings endpoint; human review required.",
            )
        )
    return leads
