const { Alchemy, Network } = require("alchemy-sdk");
const { exec } = require("child_process");

const config = {
  apiKey: process.env.ALCHEMY_API_KEY,
  network: Network.BASE_MAINNET,
};

const alchemy = new Alchemy(config);

alchemy.ws.on("pending", async (txHash) => {
  try {
    const tx = await alchemy.core.getTransaction(txHash);
    if (!tx || !tx.to) return;

    const methodSig = tx.data.slice(0, 10);
    const UNISWAP_EXACT_INPUT_SINGLE = "0x04e45aaf";

    if (
      methodSig === UNISWAP_EXACT_INPUT_SINGLE &&
      tx.to.toLowerCase() === process.env.UNISWAP_ROUTER.toLowerCase()
    ) {
      console.log("Detected swap TX:", txHash);
      exec("node autoTriggerBundle.js");
    }
  } catch (err) {
    console.error("Mempool error:", err);
  }
});
