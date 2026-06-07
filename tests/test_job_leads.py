import json
from pathlib import Path

import pytest

from applypilot.job_leads.collectors.manual_search_links import generate_links
from applypilot.job_leads.dedupe import dedupe_leads
from applypilot.job_leads.export import ensure_public_output_path, write_csv
from applypilot.job_leads.models import JobLead
from applypilot.job_leads.scoring import score_lead
from applypilot.job_leads.sources import LeadQuery


def test_job_lead_schema_validation_requires_supported_source_category():
    lead = JobLead(
        title="LLM Evaluator",
        company="Example",
        source="test",
        source_category="public_ats_api",
        job_url="https://example.com/job",
    )

    assert lead.manual_apply_required is True
    assert lead.to_dict()["title"] == "LLM Evaluator"

    with pytest.raises(ValueError):
        JobLead(title="Bad", company="Example", source="x", source_category="scraped_board", job_url="https://x.test")


def test_scoring_prefers_remote_indonesian_ai_contract_work():
    lead = JobLead(
        title="Remote Indonesian-English LLM Evaluation Contract",
        company="AI Work Co",
        source="test",
        source_category="public_ats_api",
        location="Remote Worldwide Indonesia eligible",
        remote_type="remote",
        apply_url="https://example.com/apply",
        job_url="https://example.com/job",
        contract_type="freelance contract",
        required_language="Indonesian, English",
        required_skills=["AI data annotation", "LLM evaluation"],
    )

    scored = score_lead(lead)

    assert scored.match_score >= 75
    assert scored.application_priority == "high"
    assert scored.recommended_resume_version == "ai_data_worker"


def test_scoring_flags_paid_application_and_unclear_apply_path():
    lead = JobLead(
        title="Onsite Senior Software Engineer",
        company="Suspicious Co",
        source="search",
        source_category="search_api",
        location="US only onsite",
        job_url="https://example.com/job",
        salary_or_rate="Pay deposit before interview",
        notes="paid application fee required",
    )

    scored = score_lead(lead)

    assert scored.match_score < 50
    assert scored.application_priority == "low"
    assert "deposit" in scored.risk_flags
    assert "application_fee" in scored.risk_flags
    assert "unclear_apply_path" in scored.risk_flags


def test_dedupe_normalizes_tracking_query_params():
    first = JobLead(
        title="AI Evaluator",
        company="Example",
        source="a",
        source_category="public_ats_api",
        apply_url="https://example.com/jobs/1?utm_source=x",
    )
    second = JobLead(
        title="AI Evaluator Copy",
        company="Example",
        source="b",
        source_category="public_ats_api",
        apply_url="https://example.com/jobs/1",
    )

    assert len(dedupe_leads([first, second])) == 1


def test_manual_links_generate_without_fetching_login_heavy_boards():
    links = generate_links([LeadQuery(name="LLM", query="LLM evaluator", location="Remote")])

    boards = {link.board for link in links}
    assert {"LinkedIn", "Indeed", "Glassdoor", "Google Jobs", "ZipRecruiter"} <= boards
    assert all(link.url.startswith("https://") for link in links)


def test_public_output_guard_blocks_private_paths(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("outputs/public").mkdir(parents=True)
    safe = ensure_public_output_path("outputs/public/job_leads.csv")
    assert safe == Path("outputs/public/job_leads.csv")

    with pytest.raises(ValueError):
        ensure_public_output_path("outputs/private/job_leads.csv")
    with pytest.raises(ValueError):
        ensure_public_output_path("outputs/public/resume_leads.csv")


def test_write_csv_outputs_public_safe_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    lead = JobLead(
        title="Search Evaluator",
        company="Example",
        source="manual",
        source_category="manual_search_url",
        job_url="https://example.com/search",
    )

    path = write_csv([lead], "outputs/public/job_leads.csv")

    assert path.exists()
    assert "Search Evaluator" in path.read_text(encoding="utf-8")
    assert not list(Path("outputs/public").glob("*.env"))


def test_json_round_trip_schema(tmp_path, monkeypatch):
    from applypilot.job_leads.export import read_json, write_json

    monkeypatch.chdir(tmp_path)
    lead = JobLead(
        title="RWS Research Evaluator",
        company="Example",
        source="test",
        source_category="public_ats_api",
        job_url="https://example.com/job",
        required_skills=["RWS", "AOP research"],
    )

    out = write_json([lead], "outputs/public/job_leads_raw.json")
    raw = json.loads(out.read_text(encoding="utf-8"))
    restored = read_json(out)

    assert raw[0]["manual_apply_required"] is True
    assert restored[0].title == "RWS Research Evaluator"
