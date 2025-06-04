import { Signer, ContractFactory, BigNumberish, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../../common";
import type { MockAggregator, MockAggregatorInterface } from "../../../../mocks/oracle/CLAggregators/MockAggregator";
type MockAggregatorConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class MockAggregator__factory extends ContractFactory {
    constructor(...args: MockAggregatorConstructorParams);
    deploy(initialAnswer: PromiseOrValue<BigNumberish>, overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<MockAggregator>;
    getDeployTransaction(initialAnswer: PromiseOrValue<BigNumberish>, overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): MockAggregator;
    connect(signer: Signer): MockAggregator__factory;
    static readonly bytecode = "0x608060405234801561001057600080fd5b5060405161013838038061013883398101604081905261002f9161006f565b600081815560405142815282907f0559884fd3a460db3073b7fc896cc77986f16e378210ded43186175bf646fc5f9060200160405180910390a350610088565b60006020828403121561008157600080fd5b5051919050565b60a2806100966000396000f3fe6080604052348015600f57600080fd5b5060043610603c5760003560e01c8063313ce56714604157806350d25bcd146055578063fcab1819146066575b600080fd5b604051600881526020015b60405180910390f35b6000545b604051908152602001604c565b6001605956fea2646970667358221220f0cdec7e455e88df72a271e04f233a0a504843bda6ee29c9575ae83cd5f046cf64736f6c634300080a0033";
    static readonly abi: ({
        inputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
        anonymous?: undefined;
        name?: undefined;
        outputs?: undefined;
    } | {
        anonymous: boolean;
        inputs: {
            indexed: boolean;
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        type: string;
        stateMutability?: undefined;
        outputs?: undefined;
    } | {
        inputs: never[];
        name: string;
        outputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
        anonymous?: undefined;
    })[];
    static createInterface(): MockAggregatorInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): MockAggregator;
}
export {};
//# sourceMappingURL=MockAggregator__factory.d.ts.map