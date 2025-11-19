import argparse
import json
from typing import Dict, List

from app import STYLES, Web3Style  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="list_styles",
        description="List raw Web3 style profiles used by web3_focus_slider.",
    )
        parser.add_argument(
        "--sort-desc",
        action="store_true",
        help="Sort in descending order (default) for numeric fields; ignored for key.",
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


def sort_styles(sort_by: str, sort_desc: bool = True) -> List[Web3Style]:

    """Return the style profiles sorted according to the requested field."""
    styles: List[Web3Style] = list(STYLES.values())

      if sort_by == "privacy":
        styles.sort(key=lambda s: s.privacy, reverse=sort_desc)
    elif sort_by == "soundness":
        styles.sort(key=lambda s: s.soundness, reverse=sort_desc)
    elif sort_by == "speed":
        styles.sort(key=lambda s: s.ux_speed, reverse=sort_desc)
    else:
        # sort_by == "key"
        styles.sort(key=lambda s: s.key, reverse=False)


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

    for s in styles:
        print(
            f"{s.key:10s} "
            f"{s.name[:26]:26s} "
            f"{s.privacy:0.2f}    "
            f"{s.soundness:0.2f}      "
            f"{s.ux_speed:0.2f}"
        )


def main() -> int:
    args = parse_args()

        styles = sort_styles(args.sort_by, sort_desc=True)

    if args.limit > 0:
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
