"""YAML configuration loading for safe job lead sources and queries."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from applypilot.job_leads.models import SOURCE_TYPES


@dataclass(frozen=True)
class SourceConfig:
    name: str
    type: str
    enabled: bool = True
    board_token: str = ""
    company_slug: str = ""
    url: str = ""
    query: str = ""
    provider: str = ""
    limit: int = 25
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceConfig":
        source_type = str(data.get("type", "")).strip()
        if source_type not in SOURCE_TYPES:
            raise ValueError(f"Unsupported source type '{source_type}' for {data.get('name', 'unknown')}")
        return cls(
            name=str(data.get("name", "")).strip(),
            type=source_type,
            enabled=bool(data.get("enabled", True)),
            board_token=str(data.get("board_token", "")).strip(),
            company_slug=str(data.get("company_slug", "")).strip(),
            url=str(data.get("url", "")).strip(),
            query=str(data.get("query", "")).strip(),
            provider=str(data.get("provider", "")).strip().lower(),
            limit=int(data.get("limit", 25) or 25),
            tags=[str(tag) for tag in data.get("tags", [])],
        )


@dataclass(frozen=True)
class LeadQuery:
    name: str
    query: str
    location: str = "remote"
    remote: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LeadQuery":
        return cls(
            name=str(data.get("name", data.get("query", "search"))).strip(),
            query=str(data.get("query", "")).strip(),
            location=str(data.get("location", "remote")).strip(),
            remote=bool(data.get("remote", True)),
        )


def _read_yaml(path: str | Path) -> dict[str, Any]:
    cfg_path = Path(path)
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config not found: {cfg_path}")
    return yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}


def load_source_configs(path: str | Path) -> list[SourceConfig]:
    data = _read_yaml(path)
    return [SourceConfig.from_dict(item) for item in data.get("sources", [])]


def load_queries(path: str | Path) -> list[LeadQuery]:
    data = _read_yaml(path)
    return [LeadQuery.from_dict(item) for item in data.get("queries", [])]
