#!/usr/bin/env python3

import argparse
import json
import os
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Validate and inspect a JSON file.")
    p.add_argument("file", help="Path to JSON file.")
        p.add_argument(
        "--top-level-only",
        action="store_true",
        help="Skip printing the JSON preview and only show summary.",
    )

    return p.parse_args()


def main():
    args = parse_args()
    path = args.file

    if not os.path.isfile(path):
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    print(f"=== Checking JSON file: {path} ===")
    if not args.top_level_only:
        print("\nPreview:")
        if args.raw:
            print(json.dumps(data, indent=args.indent))
        else:
            preview = json.dumps(data, indent=args.indent)[:args.max_preview]
            print(preview)
            if len(preview) == args.max_preview:
                print("… (truncated)")

    # size
    size = os.path.getsize(path)
    print(f"File size: {size} bytes")

    # load JSON
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[!!] Invalid JSON: {e}")
        sys.exit(2)

    print("[OK] JSON is valid.")

    # summarize
    if isinstance(data, dict):
        print(f"Top-level type: object")
        print(f"Number of keys: {len(data)}")
        print("Keys:", ", ".join(list(data.keys())[:10]), "…")
    elif isinstance(data, list):
        print("Top-level type: array")
        print(f"Number of items: {len(data)}")
    else:
        print(f"Top-level type: {type(data).__name__}")

    # preview
    preview = json.dumps(data, indent=2)[:300]
    print("\nPreview:")
    print(preview)
    if len(preview) == 300:
        print("… (truncated)")


if __name__ == "__main__":
    main()
