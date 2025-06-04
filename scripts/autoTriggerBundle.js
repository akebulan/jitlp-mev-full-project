const { exec } = require("child_process");

const estFees = 8;    // simulated swap fees earned
const estGasCost = 1; // in USD
const flashLoanFee = 0.1;

const netProfit = estFees - estGasCost - flashLoanFee;

if (netProfit > 1) {
  console.log("💰 Profitable, sending bundle...");
  exec("node sendFlashbotsBundle.js");
} else {
  console.log("❌ Not profitable, skipping.");
}
