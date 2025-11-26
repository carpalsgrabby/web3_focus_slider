#!/usr/bin/env python3

import argparse
import json
import os
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Validate and inspect a JSON file.")
    p.add_argument("file", help="Path to JSON file.")
    return p.parse_args()


def main():
    args = parse_args()
    path = args.file

    if not os.path.isfile(path):
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    print(f"=== Checking JSON file: {path} ===")

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
        num_keys = len(data)
        print(f"Number of keys: {num_keys}")
        keys = list(data.keys())
        max_keys = 10
        shown_keys = keys[:max_keys]
        suffix = "…" if num_keys > max_keys else ""
        print("Keys:", ", ".join(shown_keys), suffix)

    # preview
    preview = json.dumps(data, indent=2)[:300]
    print("\nPreview:")
    print(preview)
    if len(preview) == 300:
        print("… (truncated)")


if __name__ == "__main__":
    main()
