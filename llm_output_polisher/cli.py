"""Command-line interface."""
import argparse
from pathlib import Path

from .core import Polisher


def main():
    parser = argparse.ArgumentParser(description="Polish raw LLM output into readable Markdown.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to polish")
    source.add_argument("--file", help="Path to a UTF-8 text file")
    parser.add_argument("--profile", choices=["general", "study", "technical", "concise"], default="general")
    parser.add_argument("--format-only", action="store_true", help="Clean Markdown without a model call")
    parser.add_argument("--instructions", help="Extra editing instructions")
    args = parser.parse_args()
    raw = args.text if args.text is not None else Path(args.file).read_text(encoding="utf-8")
    if args.format_only:
        print(Polisher.format_only(raw))
    else:
        print(Polisher().polish(raw, profile=args.profile, instructions=args.instructions))


if __name__ == "__main__":
    main()
