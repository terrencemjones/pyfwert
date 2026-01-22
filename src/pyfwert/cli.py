#!/usr/bin/env python3
"""Command-line interface for Pyfwert password generator."""

import argparse
import sys

from pyfwert import PasswordGenerator, __version__


def main():
    """Main entry point for the pyfwert CLI."""
    parser = argparse.ArgumentParser(
        prog="pyfwert",
        description="Generate strong, memorable passwords using patterns.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pyfwert                        Generate 12 random passwords
  pyfwert -n 5                   Generate 5 passwords
  pyfwert -p "{word}.{word}"     Use a specific pattern
  pyfwert --show-pattern         Show the pattern used for each password

Pattern syntax:
  {word}           Random word from default wordlist
  {word(animal)}   Random word from specific wordlist
  {number}         Random digit (0-9)
  {number(99)}     Random number (0-99)
  {symbol}         Random symbol
  {letter}         Random letter
  {pronounceable}  Fake pronounceable word
  {sequence(5)}    Keyboard sequence

Modifiers:
  {word+uppercase}   Convert to uppercase
  {word+obscure}     Leet-speak substitutions
  {word+reverse}     Reverse the text
  {word+piglatin}    Convert to pig latin
        """
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=12,
        help="Number of passwords to generate (default: 12)"
    )
    parser.add_argument(
        "-p", "--pattern",
        type=str,
        default=None,
        help="Use a specific pattern instead of random"
    )
    parser.add_argument(
        "--show-pattern",
        action="store_true",
        help="Show the pattern used for each password"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode - just output passwords, one per line"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"pyfwert {__version__}"
    )

    args = parser.parse_args()

    gen = PasswordGenerator()

    if not args.quiet:
        print()
        print("=" * 60)
        print("  Pyfwert - Pattern-based Password Generator")
        print("=" * 60)
        print()

    for i in range(args.count):
        try:
            password = gen.generate(args.pattern)

            if args.quiet:
                print(password)
            elif args.show_pattern:
                # Truncate long patterns
                pattern = gen.last_pattern
                if len(pattern) > 40:
                    pattern = pattern[:37] + "..."
                print(f"  {i+1:2}. {password:<40}  [{pattern}]")
            else:
                print(f"  {i+1:2}. {password}")
        except Exception as e:
            if args.quiet:
                print(f"ERROR: {e}", file=sys.stderr)
            else:
                print(f"  {i+1:2}. (error: {e})")

    if not args.quiet:
        print()
        print("-" * 60)
        if args.pattern:
            print(f"  Pattern: {args.pattern}")
        else:
            print("  Tip: Use -p to specify a custom pattern")
            print("       Use --show-pattern to see patterns used")
        print()


if __name__ == "__main__":
    main()
