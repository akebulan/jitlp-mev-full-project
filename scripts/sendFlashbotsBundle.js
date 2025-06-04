const { FlashbotsBundleProvider } = require("@flashbots/ethers-provider-bundle");
const { ethers } = require("ethers");

require("dotenv").config();

async function main() {
  const provider = new ethers.providers.JsonRpcProvider(process.env.BASE_RPC_URL);
  const signer = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
  const flashbots = await FlashbotsBundleProvider.create(provider, signer);

  const contract = new ethers.Contract(process.env.JIT_CONTRACT, [
    "function initiateFlashLoan(uint256 amount) external"
  ], signer);

  const txData = await contract.populateTransaction.initiateFlashLoan(ethers.utils.parseUnits("10", 18));

  const bundle = [
    {
      signer: signer,
      transaction: {
        ...txData,
        chainId: 8453,
        type: 2,
        gasLimit: 1000000,
        maxFeePerGas: ethers.utils.parseUnits("40", "gwei"),
        maxPriorityFeePerGas: ethers.utils.parseUnits("2", "gwei")
      }
    }
  ];

  const block = await provider.getBlockNumber();
  const res = await flashbots.sendBundle(bundle, block + 1);
  console.log("Bundle sent:", res);
}

main();
