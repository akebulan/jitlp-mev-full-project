import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../common";
import type { ZeroReserveInterestRateStrategy, ZeroReserveInterestRateStrategyInterface } from "../../misc/ZeroReserveInterestRateStrategy";
type ZeroReserveInterestRateStrategyConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class ZeroReserveInterestRateStrategy__factory extends ContractFactory {
    constructor(...args: ZeroReserveInterestRateStrategyConstructorParams);
    deploy(provider: PromiseOrValue<string>, overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<ZeroReserveInterestRateStrategy>;
    getDeployTransaction(provider: PromiseOrValue<string>, overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): ZeroReserveInterestRateStrategy;
    connect(signer: Signer): ZeroReserveInterestRateStrategy__factory;
    static readonly bytecode = "0x60a060405234801561001057600080fd5b506040516103c23803806103c283398101604081905261002f91610040565b6001600160a01b0316608052610070565b60006020828403121561005257600080fd5b81516001600160a01b038116811461006957600080fd5b9392505050565b60805161033861008a600039600060f401526103386000f3fe608060405234801561001057600080fd5b50600436106100ea5760003560e01c8063a58987091161008c578063bc62690811610066578063bc62690814610140578063d5cd739114610140578063f420240914610140578063fe5fd6981461015157600080fd5b8063a589870914610161578063a9c622f814610151578063acd786861461019457600080fd5b806334762ca5116100c857806334762ca51461014057806354c365c6146101515780636fb925891461015157806380031e371461015957600080fd5b80630542975c146100ef5780630b3429a21461014057806314e32da414610140575b600080fd5b6101167f000000000000000000000000000000000000000000000000000000000000000081565b60405173ffffffffffffffffffffffffffffffffffffffff90911681526020015b60405180910390f35b60005b604051908152602001610137565b610143600081565b61014361019c565b61017961016f36600461023e565b5060009081908190565b60408051938452602084019290925290820152606001610137565b6101436101b8565b6000806101a981806102c3565b6101b391906102c3565b905090565b60006101b381806102c3565b604051610120810167ffffffffffffffff8111828210171561020f577f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b60405290565b803573ffffffffffffffffffffffffffffffffffffffff8116811461023957600080fd5b919050565b6000610120828403121561025157600080fd5b6102596101c4565b823581526020830135602082015260408301356040820152606083013560608201526080830135608082015260a083013560a082015260c083013560c08201526102a560e08401610215565b60e08201526101006102b8818501610215565b908201529392505050565b600082198211156102fd577f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b50019056fea26469706673582212200a33995c44b95df6678fe8cc060c29647cfda7b6403d3df3ccbbe0922ad8df0464736f6c634300080a0033";
    static readonly abi: ({
        inputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
        name?: undefined;
        outputs?: undefined;
    } | {
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
    })[];
    static createInterface(): ZeroReserveInterestRateStrategyInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): ZeroReserveInterestRateStrategy;
}
export {};
//# sourceMappingURL=ZeroReserveInterestRateStrategy__factory.d.ts.map