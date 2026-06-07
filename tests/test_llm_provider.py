import importlib

import pytest


_PROVIDER_ENVS = [
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "OPENROUTER_API_KEY",
    "DEEPSEEK_API_KEY",
    "ANTHROPIC_API_KEY",
    "CLAUDE_API_KEY",
    "LLM_URL",
    "LLM_API_KEY",
    "LLM_MODEL",
    "LLM_PROVIDER",
]


def reload_llm(monkeypatch):
    for name in _PROVIDER_ENVS:
        monkeypatch.delenv(name, raising=False)
    import applypilot.llm as llm

    return importlib.reload(llm)


def test_openrouter_provider_detection(monkeypatch):
    llm = reload_llm(monkeypatch)
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    config = llm._detect_provider_config()

    assert config.name == "openrouter"
    assert config.base_url == "https://openrouter.ai/api/v1"
    assert config.model == "google/gemini-2.0-flash-001"


def test_deepseek_provider_detection(monkeypatch):
    llm = reload_llm(monkeypatch)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")

    config = llm._detect_provider_config()

    assert config.name == "deepseek"
    assert config.base_url == "https://api.deepseek.com/v1"
    assert config.model == "deepseek-chat"


def test_claude_provider_detection(monkeypatch):
    llm = reload_llm(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    config = llm._detect_provider_config()

    assert config.name == "claude"
    assert config.api_style == "anthropic-messages"
    assert config.model == "claude-3-5-haiku-latest"


def test_llm_provider_can_force_available_provider(monkeypatch):
    llm = reload_llm(monkeypatch)
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-key")
    monkeypatch.setenv("OPENROUTER_API_KEY", "openrouter-key")
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")

    config = llm._detect_provider_config()

    assert config.name == "openrouter"
    assert config.api_key == "openrouter-key"


def test_requested_provider_requires_matching_secret(monkeypatch):
    llm = reload_llm(monkeypatch)
    monkeypatch.setenv("LLM_PROVIDER", "deepseek")

    with pytest.raises(RuntimeError, match="LLM_PROVIDER='deepseek'"):
        llm._detect_provider_config()
