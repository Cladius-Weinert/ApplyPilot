"""Manual-only job board search URL generator.

This module never fetches or scrapes LinkedIn, Indeed, Glassdoor, Google Jobs,
or ZipRecruiter. It only creates URLs for a human to open and review manually.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus

from applypilot.job_leads.sources import LeadQuery


@dataclass(frozen=True)
class ManualSearchLink:
    board: str
    query_name: str
    url: str
    notes: str = "Manual review only. Do not scrape, bypass login walls, or auto-apply."


def generate_links(queries: list[LeadQuery]) -> list[ManualSearchLink]:
    links: list[ManualSearchLink] = []
    for query in queries:
        q = quote_plus(query.query)
        loc = quote_plus(query.location)
        links.extend(
            [
                ManualSearchLink("LinkedIn", query.name, f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}"),
                ManualSearchLink("Indeed", query.name, f"https://www.indeed.com/jobs?q={q}&l={loc}"),
                ManualSearchLink("Glassdoor", query.name, f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={q}&locT=N&locId=1"),
                ManualSearchLink("Google Jobs", query.name, f"https://www.google.com/search?q={q}+jobs+{loc}"),
                ManualSearchLink("ZipRecruiter", query.name, f"https://www.ziprecruiter.com/jobs-search?search={q}&location={loc}"),
            ]
        )
    return links


def to_markdown(links: list[ManualSearchLink]) -> str:
    lines = [
        "# Manual Job Board Search Links",
        "",
        "These links are for human review only. ApplyPilot does not fetch or scrape login-heavy job boards.",
        "",
    ]
    for link in links:
        lines.append(f"- **{link.board}** ({link.query_name}): {link.url}")
    lines.append("")
    return "\n".join(lines)
