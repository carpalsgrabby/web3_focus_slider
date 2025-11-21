#!/usr/bin/env node


const { ethers } = require("ethers");
const RED = "\x1b[31m";
const RESET = "\x1b[0m";

function err(msg) {
  console.error(RED + msg + RESET);
}
// --- config from env ---
const RPC_URL = process.env.RPC_URL;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;

// minimal ABI for a simple focus slider contract
const ABI = [
  "function getFocus() view returns (uint256)",
  "function setFocus(uint256 newFocus)",
];

async function main() {
  const [cmd, arg] = process.argv.slice(2);

  if (!RPC_URL || !CONTRACT_ADDRESS) {
    err(
      "ERROR: RPC_URL and CONTRACT_ADDRESS must be set in the environment."
    );

    process.exit(1);
  }

  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const contract = (() => {
    if (cmd === "get") {
      // read-only: no signer needed
      return new ethers.Contract(CONTRACT_ADDRESS, ABI, provider);
    }

    if (!PRIVATE_KEY) {
      console.error(
        "ERROR: PRIVATE_KEY must be set in the environment to call 'set'."
      );
      process.exit(1);
    }
    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
    return new ethers.Contract(CONTRACT_ADDRESS, ABI, wallet);
  })();

  if (cmd === "get") {
    const focus = await contract.getFocus();
    console.log(`Current focus: ${focus.toString()}`);
    return;
  }

  if (cmd === "set") {
    if (arg === undefined) {
      console.error("Usage: node focus_slider_cli.js set <value>");
      process.exit(1);
    }

    const value = BigInt(arg);
    console.log(`Setting focus to: ${value.toString()} ...`);

    const tx = await contract.setFocus(value);
    console.log(`Tx sent: ${tx.hash}`);
    const receipt = await tx.wait();
    console.log(`Tx mined in block ${receipt.blockNumber}`);
    return;
  }

  console.error(
    "Usage:\n" +
      "  node focus_slider_cli.js get\n" +
      "  node focus_slider_cli.js set <value>"
  );
  process.exit(1);
}

main().catch((err) => {
  console.error("Unexpected error:", err);
  process.exit(1);
});
