"use strict";
// ----------------
// MATH
// ----------------
Object.defineProperty(exports, "__esModule", { value: true });
exports.COVERAGE_CHAINID = exports.HARDHAT_CHAINID = exports.TEST_SNAPSHOT_ID = exports.AAVE_REFERRAL = exports.USD_ADDRESS = exports.MOCK_USD_PRICE_IN_WEI = exports.ONE_ADDRESS = exports.ZERO_ADDRESS = exports.ONE_YEAR = exports.MAX_UNBACKED_MINT_CAP = exports.MAX_SUPPLY_CAP = exports.MAX_BORROW_CAP = exports.MAX_UINT_AMOUNT = exports.oneRay = exports.oneEther = exports.WAD_RAY_RATIO = exports.HALF_RAY = exports.RAY = exports.HALF_WAD = exports.WAD = exports.HALF_PERCENTAGE = exports.PERCENTAGE_FACTOR = void 0;
const ethers_1 = require("ethers");
const utils_1 = require("ethers/lib/utils");
exports.PERCENTAGE_FACTOR = '10000';
exports.HALF_PERCENTAGE = ethers_1.BigNumber.from(exports.PERCENTAGE_FACTOR).div(2).toString();
exports.WAD = ethers_1.BigNumber.from(10).pow(18).toString();
exports.HALF_WAD = ethers_1.BigNumber.from(exports.WAD).div(2).toString();
exports.RAY = ethers_1.BigNumber.from(10).pow(27).toString();
exports.HALF_RAY = ethers_1.BigNumber.from(exports.RAY).div(2).toString();
exports.WAD_RAY_RATIO = (0, utils_1.parseUnits)('1', 9).toString();
exports.oneEther = (0, utils_1.parseUnits)('1', 18);
exports.oneRay = (0, utils_1.parseUnits)('1', 27);
exports.MAX_UINT_AMOUNT = '115792089237316195423570985008687907853269984665640564039457584007913129639935';
exports.MAX_BORROW_CAP = '68719476735';
exports.MAX_SUPPLY_CAP = '68719476735';
exports.MAX_UNBACKED_MINT_CAP = '68719476735';
exports.ONE_YEAR = '31536000';
exports.ZERO_ADDRESS = '0x0000000000000000000000000000000000000000';
exports.ONE_ADDRESS = '0x0000000000000000000000000000000000000001';
// ----------------
// PROTOCOL GLOBAL PARAMS
// ----------------
exports.MOCK_USD_PRICE_IN_WEI = '5848466240000000';
exports.USD_ADDRESS = '0x10F7Fc1F91Ba351f9C629c5947AD69bD03C05b96';
exports.AAVE_REFERRAL = '0';
exports.TEST_SNAPSHOT_ID = '0x1';
exports.HARDHAT_CHAINID = 31337;
exports.COVERAGE_CHAINID = 1337;
