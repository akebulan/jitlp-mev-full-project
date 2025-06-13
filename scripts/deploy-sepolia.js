// scripts/deploy-base.js
const hre = require("hardhat");

async function main() {
    const [deployer] = await hre.ethers.getSigners();
    console.log("Deploying as:", deployer.address);

    const AaveV3Liquidator = await hre.ethers.getContractFactory("AaveV3Liquidator");
    const liquidator = await AaveV3Liquidator.deploy(
        "0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D", // PoolAddressesProvider (Base Mainnet)
        "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"  // Aave Pool (Base Mainnet)
    );

    await liquidator.deployed();
    console.log("🟢 Deployed to:", liquidator.address);
}

main().catch((e) => {
    console.error(e);
    process.exitCode = 1;
});
