"""Deduplication helpers for job leads."""

from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from applypilot.job_leads.models import JobLead

_TRACKING_PREFIXES = ("utm_",)
_TRACKING_KEYS = {"fbclid", "gclid", "msclkid", "ref", "src"}


def normalize_url(url: str) -> str:
    if not url:
        return ""
    split = urlsplit(url.strip())
    query = [
        (key, value)
        for key, value in parse_qsl(split.query, keep_blank_values=True)
        if key.lower() not in _TRACKING_KEYS and not key.lower().startswith(_TRACKING_PREFIXES)
    ]
    path = re.sub(r"/+$", "", split.path)
    return urlunsplit((split.scheme.lower(), split.netloc.lower(), path, urlencode(query), ""))


def dedupe_key(lead: JobLead) -> str:
    url = normalize_url(lead.apply_url or lead.job_url)
    if url:
        return url
    return f"{lead.company.lower()}::{lead.title.lower()}::{lead.location.lower()}"


def dedupe_leads(leads: list[JobLead]) -> list[JobLead]:
    seen: set[str] = set()
    unique: list[JobLead] = []
    for lead in leads:
        key = dedupe_key(lead)
        if key in seen:
            continue
        seen.add(key)
        unique.append(lead)
    return unique
