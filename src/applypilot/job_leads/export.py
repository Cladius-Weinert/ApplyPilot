"""Public-safe export helpers for job leads."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from applypilot.job_leads.models import JobLead

PUBLIC_OUTPUT_ROOT = Path("outputs/public")
PRIVATE_OUTPUT_NAMES = {".env", "resume", "cv", "profile", "cookie", "session", "password"}


def ensure_public_output_path(path: str | Path) -> Path:
    output = Path(path)
    normalized_parts = {part.lower() for part in output.parts}
    if any(private in part for private in PRIVATE_OUTPUT_NAMES for part in normalized_parts):
        raise ValueError(f"Refusing private-looking output path: {output}")
    try:
        output.relative_to(PUBLIC_OUTPUT_ROOT)
    except ValueError as exc:
        raise ValueError(f"Job lead outputs must be under {PUBLIC_OUTPUT_ROOT}: {output}") from exc
    output.parent.mkdir(parents=True, exist_ok=True)
    return output


def write_json(leads: Iterable[JobLead], path: str | Path) -> Path:
    output = ensure_public_output_path(path)
    output.write_text(json.dumps([lead.to_dict() for lead in leads], indent=2, ensure_ascii=False), encoding="utf-8")
    return output


def read_json(path: str | Path) -> list[JobLead]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [JobLead.from_dict(item) for item in data]


def write_csv(leads: list[JobLead], path: str | Path = PUBLIC_OUTPUT_ROOT / "job_leads.csv") -> Path:
    output = ensure_public_output_path(path)
    fields = list(JobLead("x", "x", "x", "manual_search_url", job_url="https://example.com").to_dict().keys())
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for lead in leads:
            row = lead.to_dict()
            row["required_skills"] = "; ".join(lead.required_skills)
            row["risk_flags"] = "; ".join(lead.risk_flags)
            writer.writerow(row)
    return output


def write_markdown(leads: list[JobLead], path: str | Path = PUBLIC_OUTPUT_ROOT / "job_leads.md") -> Path:
    output = ensure_public_output_path(path)
    lines = ["# ApplyPilot Job Leads", "", "Human review is required before applying. No auto-apply is performed.", ""]
    for lead in leads:
        lines.extend(
            [
                f"## {lead.title} — {lead.company}",
                f"- Score: {lead.match_score} ({lead.application_priority})",
                f"- Source: {lead.source} / {lead.source_category}",
                f"- Location: {lead.location or 'Not listed'} ({lead.remote_type})",
                f"- Apply URL: {lead.apply_url or 'Manual verification required'}",
                f"- Job URL: {lead.job_url or lead.apply_url}",
                f"- Reason: {lead.reason_for_match}",
                f"- Risk flags: {', '.join(lead.risk_flags) if lead.risk_flags else 'None'}",
                f"- Resume: {lead.recommended_resume_version}",
                f"- Cover letter: {lead.recommended_cover_letter_template}",
                "",
            ]
        )
    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def write_summary(leads: list[JobLead], path: str | Path = PUBLIC_OUTPUT_ROOT / "job_lead_summary.md") -> Path:
    output = ensure_public_output_path(path)
    high = sum(1 for lead in leads if lead.application_priority == "high")
    medium = sum(1 for lead in leads if lead.application_priority == "medium")
    low = sum(1 for lead in leads if lead.application_priority == "low")
    sources = sorted({lead.source for lead in leads})
    lines = [
        "# Job Lead Summary",
        "",
        f"- Total leads: {len(leads)}",
        f"- High priority: {high}",
        f"- Medium priority: {medium}",
        f"- Low priority / review carefully: {low}",
        f"- Sources: {', '.join(sources) if sources else 'None'}",
        "",
        "Public-safe output only. No resumes, profiles, cookies, sessions, passwords, or .env files are included.",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
