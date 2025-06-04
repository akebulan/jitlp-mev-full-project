const hre = require("hardhat");
require("dotenv").config();

async function main() {
  const JITLP = await hre.ethers.getContractFactory("JITLPWithAave");
  const contract = await JITLP.deploy(
    process.env.AAVE_POOL,
    process.env.WETH,
    process.env.USDC,
    process.env.UNISWAP_ROUTER,
    process.env.POSITION_MANAGER
  );
  await contract.deployed();

  console.log("✅ Contract deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
