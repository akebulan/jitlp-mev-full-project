import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IReserveInterestRateStrategy, IReserveInterestRateStrategyInterface } from "../../interfaces/IReserveInterestRateStrategy";
export declare class IReserveInterestRateStrategy__factory {
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
    static createInterface(): IReserveInterestRateStrategyInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IReserveInterestRateStrategy;
}
//# sourceMappingURL=IReserveInterestRateStrategy__factory.d.ts.map