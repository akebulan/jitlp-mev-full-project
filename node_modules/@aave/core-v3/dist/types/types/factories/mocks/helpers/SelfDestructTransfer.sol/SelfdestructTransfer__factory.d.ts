import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../../common";
import type { SelfdestructTransfer, SelfdestructTransferInterface } from "../../../../mocks/helpers/SelfDestructTransfer.sol/SelfdestructTransfer";
type SelfdestructTransferConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class SelfdestructTransfer__factory extends ContractFactory {
    constructor(...args: SelfdestructTransferConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<SelfdestructTransfer>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): SelfdestructTransfer;
    connect(signer: Signer): SelfdestructTransfer__factory;
    static readonly bytecode = "0x608060405234801561001057600080fd5b5060bc8061001f6000396000f3fe608060405260043610601c5760003560e01c8063785e07b3146021575b600080fd5b6030602c366004604b565b6032565b005b8073ffffffffffffffffffffffffffffffffffffffff16ff5b600060208284031215605c57600080fd5b813573ffffffffffffffffffffffffffffffffffffffff81168114607f57600080fd5b939250505056fea2646970667358221220fea252da90a06bc70e97eaaf66c9b86a6b69d59e6b6880b4aee35184b56b6efb64736f6c634300080a0033";
    static readonly abi: {
        inputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        outputs: never[];
        stateMutability: string;
        type: string;
    }[];
    static createInterface(): SelfdestructTransferInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): SelfdestructTransfer;
}
export {};
//# sourceMappingURL=SelfdestructTransfer__factory.d.ts.map