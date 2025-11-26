#!/usr/bin/env python3
import os
import sys
from web3 import Web3


REQUIRED_VARS = [
    "RPC_URL",
    "PRIVATE_KEY",
    "CONTRACT_ADDRESS",
]
QUIET = False

def check_env_vars():
    print("=== Checking environment variables ===")
    missing = False
    for var in REQUIRED_VARS:
        val = os.getenv(var)
        if val:
            print(f"[OK] {var} is set")
        else:
            print(f"[!!] {var} is NOT set")
            missing = True
    return not missing


def check_rpc():
    rpc = os.getenv("RPC_URL")
    if not rpc:
        print("\nSkipping RPC check — RPC_URL missing.")
        return False

    print("\n=== Checking RPC endpoint ===")
    try:
        w3 = Web3(Web3.HTTPProvider(rpc))
        if not w3.is_connected():
            print("[!!] Cannot connect to RPC endpoint.")
            return False
        print("[OK] RPC is reachable.")
        print(f"Chain ID: {w3.eth.chain_id}")
        return True
    except Exception as e:
        print(f"[!!] RPC error: {e}")
        return False

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check required env vars and a Web3 RPC endpoint."
    )
    parser.add_argument(
        "--rpc-url",
        help="Override RPC_URL environment variable for this run.",
    )
        parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print the final result line.",
    )

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.rpc_url:
        os.environ["RPC_URL"] = args.rpc_url

    ok_env = check_env_vars()
    ok_rpc = check_rpc()


    print("\n=== RESULT ===")
    if ok_env and ok_rpc:
        print("Environment looks good ✔️")
        sys.exit(0)
    else:
        print("Some checks FAILED ❌")
        sys.exit(1)
def log(msg: str) -> None:
    if not QUIET:
        print(msg)


if __name__ == "__main__":
    main()
