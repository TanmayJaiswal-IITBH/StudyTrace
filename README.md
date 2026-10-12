# StudyTrace

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

StudyTrace reads your Google Classroom, college email and notes, remembers what you've learned and
what's due, and lets you trace every piece of advice back to the exact email, note or quiz it came
from.

Built for the Nebius x NVIDIA Global AI Hackathon, Personal AI track. See [GOAL.md](GOAL.md) for
what "done" means and [CLAUDE.md](CLAUDE.md) for the engineering rules.

## Quickstart

```bash
cp .env.example .env                          # then fill in keys
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" && pre-commit install
docker compose up -d --wait                   # Postgres + pgvector + memory service (localhost:8000)
curl localhost:8000/health                    # {"status":"ok"}
ruff check . && black --check . && pytest     # what CI runs
```

## How Nemotron and Token Factory are used

_To be written._

## Other Nebius services

_To be written._

## Architecture

_To be written._

## Feedback

_To be written._

## License

Apache-2.0. See [LICENSE](LICENSE).
