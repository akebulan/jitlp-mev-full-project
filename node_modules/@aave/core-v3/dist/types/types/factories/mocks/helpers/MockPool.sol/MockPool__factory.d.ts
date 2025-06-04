import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../../common";
import type { MockPool, MockPoolInterface } from "../../../../mocks/helpers/MockPool.sol/MockPool";
type MockPoolConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class MockPool__factory extends ContractFactory {
    constructor(...args: MockPoolConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<MockPool>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): MockPool;
    connect(signer: Signer): MockPool__factory;
    static readonly bytecode = "0x608060405234801561001057600080fd5b506103b2806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c8063c4d66de814610046578063d1946dbc1461009d578063e636a4f4146100bb575b600080fd5b61009b610054366004610227565b606480547fffffffffffffffffffffffff00000000000000000000000000000000000000001673ffffffffffffffffffffffffffffffffffffffff92909216919091179055565b005b6100a5610140565b6040516100b29190610264565b60405180910390f35b61009b6100c9366004610227565b606580546001810182556000919091527f8ff97419363ffd7000167f130ef7168fbea05faf9251824ca5043f113cc6a7c70180547fffffffffffffffffffffffff00000000000000000000000000000000000000001673ffffffffffffffffffffffffffffffffffffffff92909216919091179055565b60655460609060009067ffffffffffffffff811115610161576101616102be565b60405190808252806020026020018201604052801561018a578160200160208202803683370190505b50905060005b60655481101561022157606581815481106101ad576101ad6102ed565b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff168282815181106101ea576101ea6102ed565b73ffffffffffffffffffffffffffffffffffffffff90921660209283029190910190910152806102198161031c565b915050610190565b50919050565b60006020828403121561023957600080fd5b813573ffffffffffffffffffffffffffffffffffffffff8116811461025d57600080fd5b9392505050565b6020808252825182820181905260009190848201906040850190845b818110156102b257835173ffffffffffffffffffffffffffffffffffffffff1683529284019291840191600101610280565b50909695505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b60007fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff821415610375577f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b506001019056fea2646970667358221220c5452da3ab36cc11ed1a02a9c52cf35987001395534a3cd81e4bd00c1c95285364736f6c634300080a0033";
    static readonly abi: ({
        inputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        outputs: never[];
        stateMutability: string;
        type: string;
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
    })[];
    static createInterface(): MockPoolInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): MockPool;
}
export {};
//# sourceMappingURL=MockPool__factory.d.ts.map