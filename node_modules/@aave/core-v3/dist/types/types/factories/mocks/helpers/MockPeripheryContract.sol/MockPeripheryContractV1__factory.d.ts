import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../../common";
import type { MockPeripheryContractV1, MockPeripheryContractV1Interface } from "../../../../mocks/helpers/MockPeripheryContract.sol/MockPeripheryContractV1";
type MockPeripheryContractV1ConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class MockPeripheryContractV1__factory extends ContractFactory {
    constructor(...args: MockPeripheryContractV1ConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<MockPeripheryContractV1>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): MockPeripheryContractV1;
    connect(signer: Signer): MockPeripheryContractV1__factory;
    static readonly bytecode = "0x608060405234801561001057600080fd5b506101cd806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c8063cd6dc68714610046578063d0ebdbe7146100a1578063d5009584146100f6575b600080fd5b61009f61005436600461014b565b600080547fffffffffffffffffffffffff00000000000000000000000000000000000000001673ffffffffffffffffffffffffffffffffffffffff9390931692909217909155600155565b005b61009f6100af366004610175565b600080547fffffffffffffffffffffffff00000000000000000000000000000000000000001673ffffffffffffffffffffffffffffffffffffffff92909216919091179055565b6000546040805173ffffffffffffffffffffffffffffffffffffffff9092168252519081900360200190f35b803573ffffffffffffffffffffffffffffffffffffffff8116811461014657600080fd5b919050565b6000806040838503121561015e57600080fd5b61016783610122565b946020939093013593505050565b60006020828403121561018757600080fd5b61019082610122565b939250505056fea2646970667358221220eca9b28a5e720f2c23a76466bcf567d4f865fd67b02882a6a2647eb86f0006b364736f6c634300080a0033";
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
    static createInterface(): MockPeripheryContractV1Interface;
    static connect(address: string, signerOrProvider: Signer | Provider): MockPeripheryContractV1;
}
export {};
//# sourceMappingURL=MockPeripheryContractV1__factory.d.ts.map