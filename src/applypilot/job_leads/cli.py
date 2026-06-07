"""CLI commands for safe scheduled job lead discovery."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from applypilot.job_leads import export as lead_export
from applypilot.job_leads.collectors import greenhouse, lever, manual_search_links, remoteok, remotive, search_api
from applypilot.job_leads.dedupe import dedupe_leads
from applypilot.job_leads.scoring import score_leads
from applypilot.job_leads.sources import load_queries, load_source_configs

app = typer.Typer(name="job-leads", help="Safe public job lead discovery. No auto-apply.", no_args_is_help=True)
console = Console()

DEFAULT_RAW = Path("outputs/public/job_leads_raw.json")
DEFAULT_SCORED = Path("outputs/public/job_leads_scored.json")
DEFAULT_LINKS = Path("outputs/public/manual_search_links.md")


def _collect_from_source(source) -> list:
    if source.type == "public_ats_api" and source.board_token:
        return greenhouse.collect(source)
    if source.type == "public_ats_api" and source.company_slug:
        return lever.collect(source)
    if source.type == "official_api" and source.provider == "remoteok":
        return remoteok.collect(source)
    if source.type == "official_api" and source.provider == "remotive":
        return remotive.collect(source)
    if source.type == "search_api":
        return search_api.collect(source)
    return []


@app.command()
def collect(
    config: Path = typer.Option(Path("config/job_lead_sources.yaml"), "--config", help="Safe source config YAML."),
    output: Path = typer.Option(DEFAULT_RAW, "--output", help="Public-safe raw JSON output path."),
) -> None:
    """Collect leads from safe public ATS/API/search sources only."""

    sources = load_source_configs(config)
    leads = []
    for source in sources:
        if not source.enabled:
            continue
        try:
            source_leads = _collect_from_source(source)
            leads.extend(source_leads)
            console.print(f"[green]{source.name}[/green]: {len(source_leads)} lead(s)")
        except Exception as exc:
            console.print(f"[yellow]{source.name} skipped/error:[/yellow] {exc}")
    unique = dedupe_leads(leads)
    path = lead_export.write_json(unique, output)
    console.print(f"[bold]Wrote {len(unique)} public-safe raw leads:[/bold] {path}")


@app.command()
def score(
    input: Path = typer.Option(DEFAULT_RAW, "--input", help="Raw leads JSON."),
    output: Path = typer.Option(DEFAULT_SCORED, "--output", help="Public-safe scored JSON output path."),
) -> None:
    """Score collected leads with transparent local rules."""

    leads = lead_export.read_json(input)
    scored = score_leads(dedupe_leads(leads))
    path = lead_export.write_json(scored, output)
    console.print(f"[bold]Wrote {len(scored)} scored leads:[/bold] {path}")


@app.command("export")
def export_cmd(
    input: Path = typer.Option(DEFAULT_SCORED, "--input", help="Scored leads JSON."),
    format: str = typer.Option("csv,md", "--format", help="Comma-separated formats: csv,md"),
) -> None:
    """Export scored leads to public-safe CSV and/or Markdown."""

    leads = lead_export.read_json(input)
    formats = {part.strip().lower() for part in format.split(",") if part.strip()}
    written: list[Path] = []
    if "csv" in formats:
        written.append(lead_export.write_csv(leads))
    if "md" in formats or "markdown" in formats:
        written.append(lead_export.write_markdown(leads))
    written.append(lead_export.write_summary(leads))
    if not written:
        raise typer.BadParameter("Use --format csv,md")
    for path in written:
        console.print(f"[green]Wrote[/green] {path}")


@app.command()
def links(
    config: Path = typer.Option(Path("config/job_lead_queries.yaml"), "--config", help="Manual search query config."),
    output: Path = typer.Option(DEFAULT_LINKS, "--output", help="Public-safe manual links Markdown output path."),
) -> None:
    """Generate manual-only search links for login-heavy job boards."""

    queries = load_queries(config)
    generated = manual_search_links.generate_links(queries)
    out_path = lead_export.ensure_public_output_path(output)
    out_path.write_text(manual_search_links.to_markdown(generated), encoding="utf-8")
    console.print(f"[bold]Wrote {len(generated)} manual search links:[/bold] {out_path}")
