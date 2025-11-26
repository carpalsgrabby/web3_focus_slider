#!/usr/bin/env python3
import os
import sys
from web3 import Web3


REQUIRED_VARS = [
    "RPC_URL",
    "PRIVATE_KEY",
    "CONTRACT_ADDRESS",
]


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


def main() -> None:
    """Run environment and RPC checks and exit with a status code."""
    ok_env = check_env_vars()
    ok_rpc = check_rpc()

    print("\n=== RESULT ===")
    if ok_env and ok_rpc:
        print("Environment looks good ✔️")
        sys.exit(0)
    else:
        print("Some checks FAILED ❌")
        sys.exit(1)


if __name__ == "__main__":
    main()
