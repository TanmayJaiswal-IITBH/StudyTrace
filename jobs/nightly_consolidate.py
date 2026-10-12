"""Nightly consolidation entrypoint (Nebius Serverless Job). The real logic lands on Oct 25."""

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Nightly memory consolidation")
    parser.add_argument(
        "--local", action="store_true", help="run on this machine instead of as a Serverless Job"
    )
    parser.parse_args(argv)
    print("nightly consolidation: not implemented yet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
