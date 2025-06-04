import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../common";
import type { MockIncentivesController, MockIncentivesControllerInterface } from "../../../mocks/helpers/MockIncentivesController";
type MockIncentivesControllerConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class MockIncentivesController__factory extends ContractFactory {
    constructor(...args: MockIncentivesControllerConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<MockIncentivesController>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): MockIncentivesController;
    connect(signer: Signer): MockIncentivesController__factory;
    static readonly bytecode = "0x608060405234801561001057600080fd5b5060c18061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c806331873e2e14602d575b600080fd5b603d6038366004603f565b505050565b005b600080600060608486031215605357600080fd5b833573ffffffffffffffffffffffffffffffffffffffff81168114607657600080fd5b9560208501359550604090940135939250505056fea2646970667358221220c8aea5b2f0f79d20c8d43eb83844f385685a0dd278834d37cd56f47a0c05b3e564736f6c634300080a0033";
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
    static createInterface(): MockIncentivesControllerInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): MockIncentivesController;
}
export {};
//# sourceMappingURL=MockIncentivesController__factory.d.ts.map