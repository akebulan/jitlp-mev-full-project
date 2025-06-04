import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IDefaultInterestRateStrategy, IDefaultInterestRateStrategyInterface } from "../../interfaces/IDefaultInterestRateStrategy";
export declare class IDefaultInterestRateStrategy__factory {
    static readonly abi: {
        inputs: {
            components: {
                internalType: string;
                name: string;
                type: string;
            }[];
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
    static createInterface(): IDefaultInterestRateStrategyInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IDefaultInterestRateStrategy;
}
//# sourceMappingURL=IDefaultInterestRateStrategy__factory.d.ts.map