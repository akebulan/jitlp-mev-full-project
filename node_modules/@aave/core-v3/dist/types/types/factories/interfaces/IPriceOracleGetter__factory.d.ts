import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IPriceOracleGetter, IPriceOracleGetterInterface } from "../../interfaces/IPriceOracleGetter";
export declare class IPriceOracleGetter__factory {
    static readonly abi: {
        inputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        outputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
    }[];
    static createInterface(): IPriceOracleGetterInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IPriceOracleGetter;
}
//# sourceMappingURL=IPriceOracleGetter__factory.d.ts.map