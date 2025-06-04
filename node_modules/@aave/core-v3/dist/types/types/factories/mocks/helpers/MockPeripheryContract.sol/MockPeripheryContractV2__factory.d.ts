import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../../common";
import type { MockPeripheryContractV2, MockPeripheryContractV2Interface } from "../../../../mocks/helpers/MockPeripheryContract.sol/MockPeripheryContractV2";
type MockPeripheryContractV2ConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class MockPeripheryContractV2__factory extends ContractFactory {
    constructor(...args: MockPeripheryContractV2ConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<MockPeripheryContractV2>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): MockPeripheryContractV2;
    connect(signer: Signer): MockPeripheryContractV2__factory;
    static readonly bytecode = "0x608060405234801561001057600080fd5b506101d1806100206000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c8063c4d66de814610051578063d0ebdbe7146100a8578063d5009584146100fd578063fe65acfe14610140575b600080fd5b6100a661005f36600461015e565b600280547fffffffffffffffffffffffff00000000000000000000000000000000000000001673ffffffffffffffffffffffffffffffffffffffff92909216919091179055565b005b6100a66100b636600461015e565b600080547fffffffffffffffffffffffff00000000000000000000000000000000000000001673ffffffffffffffffffffffffffffffffffffffff92909216919091179055565b60005473ffffffffffffffffffffffffffffffffffffffff165b60405173ffffffffffffffffffffffffffffffffffffffff909116815260200160405180910390f35b60025473ffffffffffffffffffffffffffffffffffffffff16610117565b60006020828403121561017057600080fd5b813573ffffffffffffffffffffffffffffffffffffffff8116811461019457600080fd5b939250505056fea2646970667358221220f1063d23fa5f3b700d275675cad2c521fb67e6b3fa4835e7c332bd2ff882d69564736f6c634300080a0033";
    static readonly abi: ({
        inputs: never[];
        name: string;
        outputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
    } | {
        inputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        outputs: never[];
        stateMutability: string;
        type: string;
    })[];
    static createInterface(): MockPeripheryContractV2Interface;
    static connect(address: string, signerOrProvider: Signer | Provider): MockPeripheryContractV2;
}
export {};
//# sourceMappingURL=MockPeripheryContractV2__factory.d.ts.map