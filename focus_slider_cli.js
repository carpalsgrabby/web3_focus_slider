#!/usr/bin/env node


const { ethers } = require("ethers");

// --- config from env ---
const RPC_URL = process.env.RPC_URL?.trim();
const PRIVATE_KEY = process.env.PRIVATE_KEY?.trim();
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS?.trim();

// minimal ABI for a simple focus slider contract
const ABI = [
  "function getFocus() view returns (uint256)",
  "function setFocus(uint256 newFocus)",
];

async function main() {
  const [cmd, arg] = process.argv.slice(2);
async function main() {
  console.error("focus-slider-cli starting...");
  const [cmd, arg] = process.argv.slice(2);

  if (!RPC_URL || !CONTRACT_ADDRESS) {
    console.error(
      "ERROR: RPC_URL and CONTRACT_ADDRESS must be set in the environment."
    );
    process.exit(1);
  }
  if (RPC_URL.includes("your") && RPC_URL.includes("infura.io")) {
    console.error(
      "WARNING: RPC_URL looks like it still contains a placeholder Infura project key."
    );
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
      console.error(
        "Hint: never commit PRIVATE_KEY to git; use a .env file or secret manager."
      );
      process.exit(1);
    }

    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
    return new ethers.Contract(CONTRACT_ADDRESS, ABI, wallet);
  })();

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

    const value = BigInt(arg);
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
