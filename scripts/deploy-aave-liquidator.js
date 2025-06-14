const hre = require("hardhat");

async function main() {
  console.log("Deploying AaveV3Liquidator...");
  
  const AaveV3Liquidator = await hre.ethers.getContractFactory("AaveV3Liquidator");
  
  // Deploy with only the required Aave protocol addresses
  const liquidator = await AaveV3Liquidator.deploy(
    "0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D", // PoolAddressesProvider (Base Mainnet)
    "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"  // Aave Pool (Base Mainnet)
  );

  await liquidator.waitForDeployment();
  
  console.log(`AaveV3Liquidator deployed to: ${await liquidator.getAddress()}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });