"""Load the fictional "Riya" persona (emails, notes, quizzes). The real seeding lands on Oct 17."""

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed the Riya demo persona")
    parser.add_argument("--reset", action="store_true", help="wipe existing data before seeding")
    parser.parse_args(argv)
    print("demo seed: not implemented yet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
