"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.usingTenderly = void 0;
const usingTenderly = () => hre &&
    (hre.network.name.includes('tenderly') ||
        process.env.TENDERLY === 'true');
exports.usingTenderly = usingTenderly;
