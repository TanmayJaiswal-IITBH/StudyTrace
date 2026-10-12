"""Manual check of the Nemotron model IDs on Nebius Token Factory. Never run in CI.

Uses httpx rather than the openai client on purpose: CLAUDE.md allows that client only inside
llm.py, and this script has to verify the raw IDs before llm.py is trusted.
"""

import sys
import time

import httpx

from memory_service.config import get_settings


def missing_tiers(configured: dict[str, str], available: list[str]) -> dict[str, str]:
    """Tiers whose configured model ID is empty or absent from the live model list."""
    return {tier: model for tier, model in configured.items() if model not in available}


def _ping(client: httpx.Client, model: str) -> tuple[str, float]:
    start = time.perf_counter()
    resp = client.post(
        "/chat/completions",
        json={"model": model, "max_tokens": 5, "messages": [{"role": "user", "content": "Hi"}]},
    )
    resp.raise_for_status()
    reply = resp.json()["choices"][0]["message"]["content"] or ""
    return reply.strip(), time.perf_counter() - start


def _check(client: httpx.Client, configured: dict[str, str]) -> int:
    resp = client.get("/models")
    resp.raise_for_status()
    available = [model["id"] for model in resp.json()["data"]]

    missing = missing_tiers(configured, available)
    if missing:
        for tier, model in missing.items():
            print(f"MISSING {tier}: {model or '(not set)'}")
        print("Nemotron models on this account:")
        for model_id in sorted(m for m in available if "nemotron" in m.lower()):
            print(f"  {model_id}")
        return 1

    for tier, model in configured.items():
        reply, seconds = _ping(client, model)
        print(f"{tier:<6}{model}  {seconds:.2f}s  reply: {reply!r}")
    return 0


def run(client: httpx.Client, configured: dict[str, str]) -> int:
    try:
        return _check(client, configured)
    except httpx.HTTPError as exc:
        print(f"Token Factory request failed: {exc}")
        return 1


def main() -> int:
    settings = get_settings()
    api_key = settings.nebius_api_key.get_secret_value()
    if not api_key:
        print("NEBIUS_API_KEY is not set (put it in .env)")
        return 1
    configured = {
        "nano": settings.model_nano,
        "super": settings.model_super,
        "ultra": settings.model_ultra,
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    with httpx.Client(base_url=settings.nebius_base_url, headers=headers, timeout=60) as client:
        return run(client, configured)


if __name__ == "__main__":
    sys.exit(main())
