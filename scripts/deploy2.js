const hre = require("hardhat");
const { getAddress } = require("ethers");
require("dotenv").config();

async function main() {
  const JITLP = await hre.ethers.getContractFactory("JITLPWithAave");

  // ✅ Normalize all addresses with Ethers v6 getAddress
  const AAVE_POOL = getAddress(process.env.AAVE_POOL);
  const WETH = getAddress(process.env.WETH);
  const USDC = getAddress(process.env.USDC);
  const UNISWAP_ROUTER = getAddress(process.env.UNISWAP_ROUTER);
  const POSITION_MANAGER = getAddress(process.env.POSITION_MANAGER);

  const contract = await JITLP.deploy(
      AAVE_POOL,
      WETH,
      USDC,
      UNISWAP_ROUTER,
      POSITION_MANAGER
  );

  await contract.deployed();
  console.log("✅ Contract deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
