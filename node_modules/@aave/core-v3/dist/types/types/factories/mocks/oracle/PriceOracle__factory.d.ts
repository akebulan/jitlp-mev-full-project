import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../common";
import type { PriceOracle, PriceOracleInterface } from "../../../mocks/oracle/PriceOracle";
type PriceOracleConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class PriceOracle__factory extends ContractFactory {
    constructor(...args: PriceOracleConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<PriceOracle>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): PriceOracle;
    connect(signer: Signer): PriceOracle__factory;
    static readonly bytecode = "0x608060405234801561001057600080fd5b50610231806100206000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c806351323f7214610051578063a0a8045e14610066578063b3596f071461007c578063b951883a146100b2575b600080fd5b61006461005f366004610196565b6100c5565b005b6001545b60405190815260200160405180910390f35b61006a61008a3660046101c0565b73ffffffffffffffffffffffffffffffffffffffff1660009081526020819052604090205490565b6100646100c03660046101e2565b61012d565b73ffffffffffffffffffffffffffffffffffffffff821660008181526020818152604091829020849055815192835282018390524282820152517fce6e0b57367bae95ca7198e1172f653ea64a645c16ab586b4cefa9237bfc2d929181900360600190a15050565b6001819055604080518281524260208201527fb4f35977939fa8b5ffe552d517a8ff5223046b1fdd3ee0068ae38d1e2b8d0016910160405180910390a150565b803573ffffffffffffffffffffffffffffffffffffffff8116811461019157600080fd5b919050565b600080604083850312156101a957600080fd5b6101b28361016d565b946020939093013593505050565b6000602082840312156101d257600080fd5b6101db8261016d565b9392505050565b6000602082840312156101f457600080fd5b503591905056fea2646970667358221220dbb79c57db1d61f4d1b2cd2fcb4c35895ebc4dc003660d97adf5e6e2c51438d264736f6c634300080a0033";
    static readonly abi: ({
        anonymous: boolean;
        inputs: {
            indexed: boolean;
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        type: string;
        outputs?: undefined;
        stateMutability?: undefined;
    } | {
        inputs: {
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
        anonymous?: undefined;
    })[];
    static createInterface(): PriceOracleInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): PriceOracle;
}
export {};
//# sourceMappingURL=PriceOracle__factory.d.ts.map