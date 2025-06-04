import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../../common";
import type { ValidationLogic, ValidationLogicInterface } from "../../../../protocol/libraries/logic/ValidationLogic";
type ValidationLogicConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class ValidationLogic__factory extends ContractFactory {
    constructor(...args: ValidationLogicConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<ValidationLogic>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): ValidationLogic;
    connect(signer: Signer): ValidationLogic__factory;
    static readonly bytecode = "0x60e8610039600b82828239805160001a60731461002c57634e487b7160e01b600052600060045260246000fd5b30600052607381538281f3fe730000000000000000000000000000000000000000301460806040526004361060515760003560e01c80632b0139fa146056578063561cbec914608e578063abfcc86a14609c578063c3525c281460a4575b600080fd5b607c7fd1d2cf869016112a9af1107bcf43c3759daf22cf734aad47d0c9c726e33bc78281565b60405190815260200160405180910390f35b607c670d2f13f7789f000081565b607c61232881565b607c670de0b6b3a76400008156fea2646970667358221220013f70ccbd1294c7b972320f19ca52acb1df48273a65f89f3a3373f16569176a64736f6c634300080a0033";
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
    static createInterface(): ValidationLogicInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): ValidationLogic;
}
export {};
//# sourceMappingURL=ValidationLogic__factory.d.ts.map