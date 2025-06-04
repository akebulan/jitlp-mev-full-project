import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { ISequencerOracle, ISequencerOracleInterface } from "../../interfaces/ISequencerOracle";
export declare class ISequencerOracle__factory {
    static readonly abi: {
        inputs: never[];
        name: string;
        outputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
    }[];
    static createInterface(): ISequencerOracleInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): ISequencerOracle;
}
//# sourceMappingURL=ISequencerOracle__factory.d.ts.map