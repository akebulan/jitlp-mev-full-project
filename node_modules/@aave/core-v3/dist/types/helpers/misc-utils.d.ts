import { BigNumber } from 'ethers';
export declare const createRandomAddress: () => string;
export declare const timeLatest: () => Promise<BigNumber>;
export declare const setBlocktime: (time: number) => Promise<void>;
export declare const setAutomine: (activate: boolean) => Promise<void>;
export declare const setAutomineEvm: (activate: boolean) => Promise<void>;
export declare const impersonateAccountsHardhat: (accounts: string[]) => Promise<void>;
//# sourceMappingURL=misc-utils.d.ts.map