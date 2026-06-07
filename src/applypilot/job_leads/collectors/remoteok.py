"""RemoteOK public API collector.

Uses RemoteOK's public JSON API only. It does not log in, scrape protected
pages, or submit applications.
"""

from __future__ import annotations

import httpx

from applypilot.job_leads.models import JobLead
from applypilot.job_leads.sources import SourceConfig

REMOTEOK_ENDPOINT = "https://remoteok.com/api"


def _remote_type(location: str) -> str:
    text = location.lower()
    if "remote" in text or "worldwide" in text or "anywhere" in text:
        return "remote"
    return "remote_or_unknown"


def collect(source: SourceConfig, client: httpx.Client | None = None) -> list[JobLead]:
    if not source.enabled:
        return []
    owns_client = client is None
    http = client or httpx.Client(timeout=20, follow_redirects=True, headers={"User-Agent": "ApplyPilot-safe-job-leads/1.0"})
    try:
        response = http.get(source.url or REMOTEOK_ENDPOINT)
        response.raise_for_status()
        data = response.json()
    finally:
        if owns_client:
            http.close()

    leads: list[JobLead] = []
    for item in data:
        if not isinstance(item, dict) or not item.get("position"):
            continue
        location = str(item.get("location") or "Remote / verify eligibility")
        apply_url = str(item.get("apply_url") or item.get("url") or "")
        job_url = str(item.get("url") or apply_url)
        tags = item.get("tags") if isinstance(item.get("tags"), list) else []
        leads.append(
            JobLead(
                title=str(item.get("position") or "Untitled role"),
                company=str(item.get("company") or "Unknown / verify manually"),
                source=source.name,
                source_category="official_api",
                location=location,
                remote_type=_remote_type(location),
                apply_url=apply_url,
                job_url=job_url,
                posted_date=str(item.get("date") or ""),
                salary_or_rate=str(item.get("salary") or ""),
                required_skills=[*source.tags, *[str(tag) for tag in tags]],
                manual_apply_required=True,
                notes="Collected from RemoteOK public API; human review required before applying.",
            )
        )
        if len(leads) >= source.limit:
            break
    return leads
