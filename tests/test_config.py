import importlib
import json

import pytest


def reload_config(monkeypatch, tmp_path):
    monkeypatch.setenv("APPLYPILOT_DIR", str(tmp_path / "appdata"))
    import applypilot.config as config

    return importlib.reload(config)


def test_load_profile_reports_invalid_json(monkeypatch, tmp_path):
    config = reload_config(monkeypatch, tmp_path)
    config.ensure_dirs()
    config.PROFILE_PATH.write_text('{"name": ', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        config.load_profile()


def test_load_search_config_reports_invalid_yaml(monkeypatch, tmp_path):
    config = reload_config(monkeypatch, tmp_path)
    config.ensure_dirs()
    config.SEARCH_CONFIG_PATH.write_text("defaults: [", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid YAML"):
        config.load_search_config()


def test_load_profile_reads_valid_json(monkeypatch, tmp_path):
    config = reload_config(monkeypatch, tmp_path)
    config.ensure_dirs()
    config.PROFILE_PATH.write_text(json.dumps({"name": "Test User"}), encoding="utf-8")

    assert config.load_profile()["name"] == "Test User"
