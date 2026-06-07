"""Optional search API collector adapters.

Supported providers are Brave Search API, Bing Web Search API, SerpAPI, and
Tavily. Collection is skipped when the matching API key is absent.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from applypilot.job_leads.models import JobLead
from applypilot.job_leads.sources import SourceConfig


@dataclass(frozen=True)
class SearchProviderSpec:
    env_key: str
    endpoint: str


PROVIDERS = {
    "brave": SearchProviderSpec("BRAVE_SEARCH_API_KEY", "https://api.search.brave.com/res/v1/web/search"),
    "bing": SearchProviderSpec("BING_SEARCH_API_KEY", "https://api.bing.microsoft.com/v7.0/search"),
    "serpapi": SearchProviderSpec("SERPAPI_API_KEY", "https://serpapi.com/search.json"),
    "tavily": SearchProviderSpec("TAVILY_API_KEY", "https://api.tavily.com/search"),
}


def provider_enabled(provider: str) -> bool:
    spec = PROVIDERS.get(provider.lower())
    return bool(spec and os.environ.get(spec.env_key))


def _extract_results(provider: str, payload: dict[str, Any]) -> list[dict[str, str]]:
    if provider == "brave":
        raw = payload.get("web", {}).get("results", [])
        return [{"title": r.get("title", ""), "url": r.get("url", ""), "description": r.get("description", "")} for r in raw]
    if provider == "bing":
        raw = payload.get("webPages", {}).get("value", [])
        return [{"title": r.get("name", ""), "url": r.get("url", ""), "description": r.get("snippet", "")} for r in raw]
    if provider == "serpapi":
        raw = payload.get("organic_results", [])
        return [{"title": r.get("title", ""), "url": r.get("link", ""), "description": r.get("snippet", "")} for r in raw]
    if provider == "tavily":
        raw = payload.get("results", [])
        return [{"title": r.get("title", ""), "url": r.get("url", ""), "description": r.get("content", "")} for r in raw]
    return []


def _request(provider: str, query: str, limit: int, client: httpx.Client) -> dict[str, Any]:
    spec = PROVIDERS[provider]
    api_key = os.environ.get(spec.env_key, "")
    if provider == "brave":
        response = client.get(spec.endpoint, params={"q": query, "count": limit}, headers={"X-Subscription-Token": api_key})
    elif provider == "bing":
        response = client.get(spec.endpoint, params={"q": query, "count": limit}, headers={"Ocp-Apim-Subscription-Key": api_key})
    elif provider == "serpapi":
        response = client.get(spec.endpoint, params={"q": query, "num": limit, "api_key": api_key})
    elif provider == "tavily":
        response = client.post(spec.endpoint, json={"api_key": api_key, "query": query, "max_results": limit})
    else:
        raise ValueError(f"Unsupported search provider: {provider}")
    response.raise_for_status()
    return response.json()


def collect(source: SourceConfig, client: httpx.Client | None = None) -> list[JobLead]:
    provider = source.provider.lower()
    if not source.enabled or provider not in PROVIDERS or not source.query or not provider_enabled(provider):
        return []
    owns_client = client is None
    http = client or httpx.Client(timeout=20, follow_redirects=True)
    try:
        payload = _request(provider, source.query, source.limit, http)
    finally:
        if owns_client:
            http.close()

    leads: list[JobLead] = []
    for result in _extract_results(provider, payload)[: source.limit]:
        url = result.get("url", "")
        if not url:
            continue
        leads.append(
            JobLead(
                title=result.get("title") or source.query,
                company="Unknown / verify manually",
                source=f"{provider}:{source.name}",
                source_category="search_api",
                location="Remote / verify manually",
                remote_type="unknown",
                apply_url="",
                job_url=url,
                required_skills=source.tags,
                risk_flags=["search_result_verify_source"],
                manual_apply_required=True,
                notes=f"Search API result. Verify company, role, and apply path manually. Snippet: {result.get('description', '')[:240]}",
            )
        )
    return leads
