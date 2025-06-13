require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: "0.8.20",
  networks: {
    base: {
      url: process.env.BASE_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
      chainId: 8453
    },
    sepolia: {
      url: "https://base-sepolia.infura.io/v3/205278e55e9e4a3fa8f6d8f348238a17",
      accounts: [process.env.PRIVATE_KEY]
    }

  }
};
