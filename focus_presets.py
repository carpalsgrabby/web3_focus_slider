#!/usr/bin/env python3
import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class FocusPreset:
    name: str
    value: int      # 0–100
    label: str
    description: str


PRESETS: Dict[str, FocusPreset] = {
    "chill": FocusPreset(
        name="chill",
        value=20,
        label="Chill",
        description="Low focus / low risk — conservative interactions."
    ),
    "balanced": FocusPreset(
        name="balanced",
        value=50,
        label="Balanced",
        description="Middle of the road — default for most users."
    ),
    "max": FocusPreset(
        name="max",
        value=90,
        label="Max Focus",
        description="High focus / aggressive behavior — use with care."
    ),
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Preset manager for web3_focus_slider."
    )
    sub = p.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="List all focus presets.")
    p_list.add_argument(
        "--json",
        action="store_true",
        help="Output presets as JSON.",
    )

    # show
    p_show = sub.add_parser("show", help="Show a single preset by name.")
    p_show.add_argument("name", help="Preset name (chill / balanced / max).")
    p_show.add_argument(
        "--json",
        action="store_true",
        help="Output the preset as JSON.",
    )

    return p


def cmd_list(as_json: bool) -> None:
    if as_json:
        data = [asdict(p) for p in PRESETS.values()]
        json.dump(data, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return

    print("Available focus presets:")
    for p in PRESETS.values():
        print(f" - {p.name:8} ({p.value:3}): {p.label}")
        print(f"     {p.description}")


def cmd_show(name: str, as_json: bool) -> None:
    """Show a single focus preset by name, optionally as JSON."""
    preset = PRESETS.get(name)
    if preset is None:
        print(f"ERROR: unknown preset '{name}'. Choices: {', '.join(PRESETS.keys())}", file=sys.stderr)
        sys.exit(1)

    if as_json:
        json.dump(asdict(preset), sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return

    print(f"Preset: {preset.name}")
    print(f"  Label      : {preset.label}")
    print(f"  Focus value: {preset.value}")
    print(f"  Description: {preset.description}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        cmd_list(as_json=getattr(args, "json", False))
    elif args.command == "show":
        cmd_show(name=args.name, as_json=getattr(args, "json", False))
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
