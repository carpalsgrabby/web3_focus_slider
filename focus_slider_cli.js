#!/usr/bin/env node


const { ethers } = require("ethers");
const RED = "\x1b[31m";
const RESET = "\x1b[0m";

function err(msg) {
  console.error(RED + msg + RESET);
}
// --- config from env ---
const RPC_URL = process.env.RPC_URL?.trim();
const PRIVATE_KEY = process.env.PRIVATE_KEY?.trim();
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS?.trim();

// Minimal ABI for a simple focus slider contract:
// - getFocus(): view-only getter
// - setFocus(uint256): updates the stored focus value
const ABI = [

  "function getFocus() view returns (uint256)",
  "function setFocus(uint256 newFocus)",
];

async function main() {
  const [cmd, arg] = process.argv.slice(2);
async function main() {
  console.error("focus-slider-cli starting...");
  const [cmd, arg] = process.argv.slice(2);

  if (cmd === "--help" || cmd === "-h") {
    console.log(
      "Focus slider CLI\n\n" +
        "Usage:\n" +
        "  node focus_slider_cli.js get\n" +
        "  node focus_slider_cli.js set <value>\n\n" +
        "Env:\n" +
        "  RPC_URL           JSON-RPC endpoint\n" +
        "  PRIVATE_KEY       Signer key (required for 'set')\n" +
        "  CONTRACT_ADDRESS  Deployed focus slider contract address"
    );
    process.exit(0);
  }


  if (!RPC_URL || !CONTRACT_ADDRESS) {
    err(
      "ERROR: RPC_URL and CONTRACT_ADDRESS must be set in the environment."
    );

    process.exit(1);
  }
  if (RPC_URL.includes("your") && RPC_URL.includes("infura.io")) {
    console.error(
      "WARNING: RPC_URL looks like it still contains a placeholder Infura project key."
    );
  }

  if (!RPC_URL.startsWith("http")) {
    console.error("ERROR: RPC_URL does not look like a valid HTTP(s) URL.");
    process.exit(1);
  }


  const provider = new ethers.JsonRpcProvider(RPC_URL);
    const network = await provider.getNetwork();
  console.error(
    `Connected to chainId=${network.chainId.toString()} (${network.name || "unknown"})`
  );
  const contract = (() => {
    if (cmd === "get") {
      // read-only: no signer needed
      
      return new ethers.Contract(CONTRACT_ADDRESS, ABI, provider);
    }

       if (!PRIVATE_KEY) {
      console.error(
        "ERROR: PRIVATE_KEY must be set in the environment to call 'set'."
      );
      console.error(
        "Hint: never commit PRIVATE_KEY to git; use a .env file or secret manager."
      );
      process.exit(1);
    }

    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
    return new ethers.Contract(CONTRACT_ADDRESS, ABI, wallet);
  })();
  console.error(`Target contract: ${CONTRACT_ADDRESS}`);

  if (cmd === "get" || cmd === "get-raw") {
    const focus = await contract.getFocus();
    if (cmd === "get-raw") {
      console.log(focus.toString());
    } else {
      console.log(`Current focus: ${focus.toString()}`);
    }
    return;
  }


  if (cmd === "set") {
    if (arg === undefined) {
           const script = process.argv[1] || "focus_slider_cli.js";
      console.error(`Usage: node ${script} set <value>`);
      process.exit(1);
    }

    let parsedArg = arg;
    if (/^0x[0-9a-fA-F]+$/.test(arg)) {
      // allow hex input
      parsedArg = BigInt(arg).toString();
    } else if (!/^-?\d+$/.test(arg)) {
      console.error("ERROR: <value> must be an integer or 0x-prefixed hex.");
      process.exit(1);
    }

    const value = BigInt(parsedArg);

    console.log(`Setting focus to: ${value.toString()} ...`);

    const tx = await contract.setFocus(value);
    console.log(`Tx sent: ${tx.hash}`);
       const receipt = await tx.wait();
    console.log(`Tx mined in block ${receipt.blockNumber}`);
    if (receipt.gasUsed && receipt.gasPrice) {
      const gasUsed = receipt.gasUsed.toString();
      const gasPriceGwei = ethers.formatUnits(receipt.gasPrice, "gwei");
      console.log(`Gas used: ${gasUsed} @ ${gasPriceGwei} gwei`);
    }
    return;

  }

  const script = process.argv[1] || "focus_slider_cli.js";
  console.error(
    "Usage:\n" +
      `  node ${script} get\n` +
      `  node ${script} set <value>`
  );

}

async function runMain() {
  try {
    await main();
  } catch (err) {
    console.error("Unexpected error:", err);
    process.exit(1);
  }
}

runMain();
