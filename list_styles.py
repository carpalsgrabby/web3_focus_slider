#!/usr/bin/env python3
"""
list_styles.py

Companion CLI for web3_focus_slider.

Lists the built-in Web3 style profiles and their privacy / soundness / UX speed
focus values.
"""

import argparse
import json
from typing import Dict, List

from app import STYLES, Web3Style  # type: ignore

__version__ = "0.1.0"
def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the list_styles CLI.
    """
    parser = argparse.ArgumentParser(

    parser = argparse.ArgumentParser(
        prog="list_styles",
        description="List raw Web3 style profiles used by web3_focus_slider.",
    )
        parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--sort-by",
        choices=("key", "privacy", "soundness", "speed"),
        default="key",
        help="Sort styles by key, privacy, soundness, or speed (default: key).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of a human-readable table.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Show only the top N rows after sorting (0 = show all).",
    )
    return parser.parse_args()


def sort_styles(sort_by: str) -> List[Web3Style]:
    """
    Return the style profiles sorted by the requested field.

    sort_by can be one of: 'key', 'privacy', 'soundness', 'speed'.
    """

    styles: List[Web3Style] = list(STYLES.values())

       # For privacy/soundness/speed, sort by highest value first; for key, use lexicographic order.
    if sort_by == "privacy":
        styles.sort(key=lambda s: s.privacy, reverse=True)
    elif sort_by == "soundness":
        styles.sort(key=lambda s: s.soundness, reverse=True)
    elif sort_by == "speed":
        styles.sort(key=lambda s: s.ux_speed, reverse=True)
    else:
        # sort_by == "key"
        styles.sort(key=lambda s: s.key)

    return styles


def print_table(styles: List[Web3Style]) -> None:
    """Print a simple table of style profiles."""
    if not styles:
        print("No styles defined.")
        return

    print("web3_focus_slider – style profiles")
    print("")
      header = f"{'Key':10s} {'Name':26s} {'Privacy':8s} {'Soundness':10s} {'Speed':8s}"
    print(header)
    print("-" * len(header))

        print(
            f"{s.key:10s} "
            f"{s.name[:26]:26s} "
            f"{s.privacy:>7.2f} "
            f"{s.soundness:>9.2f} "
            f"{s.ux_speed:>7.2f}"
        )


def main() -> int:
    args = parse_args()

    styles = sort_styles(args.sort_by)

     if args.limit < 0:
        print(f"WARNING: --limit {args.limit} is negative; ignoring.")
    elif args.limit > 0:
        styles = styles[: args.limit]


    if args.json:
        payload: List[Dict[str, object]] = []
        for s in styles:
            payload.append(
                {
                    "key": s.key,
                    "name": s.name,
                    "privacy": s.privacy,
                    "soundness": s.soundness,
                    "uxSpeed": s.ux_speed,
                    "note": s.note,
                }
            )
        print(json.dumps(payload, indent=2))
    else:
        print_table(styles)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
