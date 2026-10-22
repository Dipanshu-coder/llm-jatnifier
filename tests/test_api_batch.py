"""Contract tests for the optional batch API."""
import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from llm_output_polisher import api


client = TestClient(api.app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_batch_format_only_does_not_need_model(monkeypatch):
    def unexpected_call(*args, **kwargs):
        raise AssertionError("format-only mode must not call the model")

    monkeypatch.setattr(api.polisher, "polish", unexpected_call)
    response = client.post(
        "/polish/batch",
        json={"texts": ["###heading", "• item"], "format_only": True},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    assert [item["text"] for item in payload["results"]] == ["### heading", "- item"]


def test_batch_rejects_empty_list():
    response = client.post("/polish/batch", json={"texts": []})
    assert response.status_code == 422


def test_batch_rejects_blank_item():
    response = client.post(
        "/polish/batch",
        json={"texts": ["valid", "  "], "format_only": True},
    )
    assert response.status_code == 400
    assert "texts[1]" in response.json()["detail"]


def test_batch_limit_is_twenty():
    response = client.post(
        "/polish/batch",
        json={"texts": ["ok"] * 21, "format_only": True},
    )
    assert response.status_code == 422
