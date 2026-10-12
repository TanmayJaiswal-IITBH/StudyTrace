import json

import httpx
import pytest

from scripts.check_models import main, missing_tiers, run

CONFIGURED = {"nano": "nv/nano-x", "super": "nv/super-y", "ultra": "nv/ultra-z"}
LIVE_MODELS = ["nv/nano-x", "nv/super-y", "nv/ultra-z", "other/llama"]


def _client(models: list[str], posts: list[dict]) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            assert request.url.path == "/v1/models"
            return httpx.Response(200, json={"data": [{"id": m} for m in models]})
        posts.append(json.loads(request.content))
        return httpx.Response(200, json={"choices": [{"message": {"content": "hi"}}]})

    return httpx.Client(base_url="https://tf.example/v1/", transport=httpx.MockTransport(handler))


def test_missing_tiers_flags_empty_and_unknown_ids() -> None:
    configured = {"nano": "nv/nano-x", "super": "", "ultra": "nv/gone"}
    assert missing_tiers(configured, ["nv/nano-x"]) == {"super": "", "ultra": "nv/gone"}


def test_run_pings_every_tier_with_five_tokens(capsys: pytest.CaptureFixture[str]) -> None:
    posts: list[dict] = []
    assert run(_client(LIVE_MODELS, posts), CONFIGURED) == 0
    assert [p["model"] for p in posts] == ["nv/nano-x", "nv/super-y", "nv/ultra-z"]
    assert {p["max_tokens"] for p in posts} == {5}
    out = capsys.readouterr().out
    assert all(tier in out for tier in CONFIGURED)


def test_run_fails_without_pinging_when_a_tier_is_missing(
    capsys: pytest.CaptureFixture[str],
) -> None:
    posts: list[dict] = []
    models = ["nv/nano-x", "nv/super-y", "nvidia/some-nemotron"]
    assert run(_client(models, posts), CONFIGURED) == 1
    assert posts == []
    out = capsys.readouterr().out
    assert "MISSING ultra" in out
    assert "nvidia/some-nemotron" in out


def test_run_reports_http_errors_instead_of_raising(capsys: pytest.CaptureFixture[str]) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(401))
    client = httpx.Client(base_url="https://tf.example/v1/", transport=transport)
    assert run(client, CONFIGURED) == 1
    assert "failed" in capsys.readouterr().out


def test_main_requires_an_api_key(capsys: pytest.CaptureFixture[str]) -> None:
    assert main() == 1
    assert "NEBIUS_API_KEY" in capsys.readouterr().out
