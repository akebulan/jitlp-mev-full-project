import { BigNumber } from '@ethersproject/bignumber';
export interface SymbolMap<T> {
    [symbol: string]: T;
}
export type eNetwork = eEthereumNetwork;
export declare enum eEthereumNetwork {
    kovan = "kovan",
    ropsten = "ropsten",
    main = "main",
    coverage = "coverage",
    hardhat = "hardhat",
    tenderlyMain = "tenderlyMain"
}
export declare enum eContractid {
    Example = "Example",
    PoolAddressesProvider = "PoolAddressesProvider",
    MintableERC20 = "MintableERC20",
    MintableDelegationERC20 = "MintableDelegationERC20",
    PoolAddressesProviderRegistry = "PoolAddressesProviderRegistry",
    ACLManager = "ACLManager",
    PoolParametersProvider = "PoolParametersProvider",
    PoolConfigurator = "PoolConfigurator",
    ValidationLogic = "ValidationLogic",
    ReserveLogic = "ReserveLogic",
    GenericLogic = "GenericLogic",
    SupplyLogic = "SupplyLogic",
    BorrowLogic = "BorrowLogic",
    FlashLoanLogic = "FlashLoanLogic",
    LiquidationLogic = "LiquidationLogic",
    BridgeLogic = "BridgeLogic",
    EModeLogic = "EModeLogic",
    ConfiguratorLogic = "ConfiguratorLogic",
    Pool = "Pool",
    PriceOracle = "PriceOracle",
    Proxy = "Proxy",
    MockAggregator = "MockAggregator",
    AaveOracle = "AaveOracle",
    DefaultReserveInterestRateStrategy = "DefaultReserveInterestRateStrategy",
    InitializableImmutableAdminUpgradeabilityProxy = "InitializableImmutableAdminUpgradeabilityProxy",
    MockFlashLoanReceiver = "MockFlashLoanReceiver",
    AToken = "AToken",
    MockAToken = "MockAToken",
    DelegationAwareAToken = "DelegationAwareAToken",
    MockStableDebtToken = "MockStableDebtToken",
    MockVariableDebtToken = "MockVariableDebtToken",
    AaveProtocolDataProvider = "AaveProtocolDataProvider",
    IERC20Detailed = "IERC20Detailed",
    StableDebtToken = "StableDebtToken",
    VariableDebtToken = "VariableDebtToken",
    FeeProvider = "FeeProvider",
    TokenDistributor = "TokenDistributor",
    ReservesSetupHelper = "ReservesSetupHelper",
    WETH = "WETH",
    WETHMocked = "WETHMocked",
    PoolImpl = "PoolImpl",
    PoolConfiguratorImpl = "PoolConfiguratorImpl",
    MockIncentivesController = "MockIncentivesController",
    MockReserveConfiguration = "MockReserveConfiguration",
    MockPool = "MockPool",
    MockInitializableImple = "MockInitializableImple",
    MockInitializableImpleV2 = "MockInitializableImpleV2",
    MockInitializableFromConstructorImple = "MockInitializableFromConstructorImple",
    MockReentrantInitializableImple = "MockReentrantInitializableImple"
}
export declare enum ProtocolErrors {
    CALLER_NOT_POOL_ADMIN = "1",
    CALLER_NOT_EMERGENCY_ADMIN = "2",
    CALLER_NOT_POOL_OR_EMERGENCY_ADMIN = "3",
    CALLER_NOT_RISK_OR_POOL_ADMIN = "4",
    CALLER_NOT_ASSET_LISTING_OR_POOL_ADMIN = "5",
    CALLER_NOT_BRIDGE = "6",
    ADDRESSES_PROVIDER_NOT_REGISTERED = "7",
    INVALID_ADDRESSES_PROVIDER_ID = "8",
    NOT_CONTRACT = "9",
    CALLER_NOT_POOL_CONFIGURATOR = "10",
    CALLER_NOT_ATOKEN = "11",
    INVALID_ADDRESSES_PROVIDER = "12",
    INVALID_FLASHLOAN_EXECUTOR_RETURN = "13",
    RESERVE_ALREADY_ADDED = "14",
    NO_MORE_RESERVES_ALLOWED = "15",
    EMODE_CATEGORY_RESERVED = "16",
    INVALID_EMODE_CATEGORY_ASSIGNMENT = "17",
    RESERVE_LIQUIDITY_NOT_ZERO = "18",
    FLASHLOAN_PREMIUM_INVALID = "19",
    INVALID_RESERVE_PARAMS = "20",
    INVALID_EMODE_CATEGORY_PARAMS = "21",
    BRIDGE_PROTOCOL_FEE_INVALID = "22",
    CALLER_MUST_BE_POOL = "23",
    INVALID_MINT_AMOUNT = "24",
    INVALID_BURN_AMOUNT = "25",
    INVALID_AMOUNT = "26",
    RESERVE_INACTIVE = "27",
    RESERVE_FROZEN = "28",
    RESERVE_PAUSED = "29",
    BORROWING_NOT_ENABLED = "30",
    STABLE_BORROWING_NOT_ENABLED = "31",
    NOT_ENOUGH_AVAILABLE_USER_BALANCE = "32",
    INVALID_INTEREST_RATE_MODE_SELECTED = "33",
    COLLATERAL_BALANCE_IS_ZERO = "34",
    HEALTH_FACTOR_LOWER_THAN_LIQUIDATION_THRESHOLD = "35",
    COLLATERAL_CANNOT_COVER_NEW_BORROW = "36",
    COLLATERAL_SAME_AS_BORROWING_CURRENCY = "37",
    AMOUNT_BIGGER_THAN_MAX_LOAN_SIZE_STABLE = "38",
    NO_DEBT_OF_SELECTED_TYPE = "39",
    NO_EXPLICIT_AMOUNT_TO_REPAY_ON_BEHALF = "40",
    NO_OUTSTANDING_STABLE_DEBT = "41",
    NO_OUTSTANDING_VARIABLE_DEBT = "42",
    UNDERLYING_BALANCE_ZERO = "43",
    INTEREST_RATE_REBALANCE_CONDITIONS_NOT_MET = "44",
    HEALTH_FACTOR_NOT_BELOW_THRESHOLD = "45",
    COLLATERAL_CANNOT_BE_LIQUIDATED = "46",
    SPECIFIED_CURRENCY_NOT_BORROWED_BY_USER = "47",
    INCONSISTENT_FLASHLOAN_PARAMS = "49",
    BORROW_CAP_EXCEEDED = "50",
    SUPPLY_CAP_EXCEEDED = "51",
    UNBACKED_MINT_CAP_EXCEEDED = "52",
    DEBT_CEILING_EXCEEDED = "53",
    UNDERLYING_CLAIMABLE_RIGHTS_NOT_ZERO = "54",
    STABLE_DEBT_NOT_ZERO = "55",
    VARIABLE_DEBT_SUPPLY_NOT_ZERO = "56",
    LTV_VALIDATION_FAILED = "57",
    INCONSISTENT_EMODE_CATEGORY = "58",
    PRICE_ORACLE_SENTINEL_CHECK_FAILED = "59",
    ASSET_NOT_BORROWABLE_IN_ISOLATION = "60",
    RESERVE_ALREADY_INITIALIZED = "61",
    USER_IN_ISOLATION_MODE_OR_LTV_ZERO = "62",
    INVALID_LTV = "63",
    INVALID_LIQ_THRESHOLD = "64",
    INVALID_LIQ_BONUS = "65",
    INVALID_DECIMALS = "66",
    INVALID_RESERVE_FACTOR = "67",
    INVALID_BORROW_CAP = "68",
    INVALID_SUPPLY_CAP = "69",
    INVALID_LIQUIDATION_PROTOCOL_FEE = "70",
    INVALID_EMODE_CATEGORY = "71",
    INVALID_UNBACKED_MINT_CAP = "72",
    INVALID_DEBT_CEILING = "73",
    INVALID_RESERVE_INDEX = "74",
    ACL_ADMIN_CANNOT_BE_ZERO = "75",
    INCONSISTENT_PARAMS_LENGTH = "76",
    ZERO_ADDRESS_NOT_VALID = "77",
    INVALID_EXPIRATION = "78",
    INVALID_SIGNATURE = "79",
    OPERATION_NOT_SUPPORTED = "80",
    DEBT_CEILING_NOT_ZERO = "81",
    ASSET_NOT_LISTED = "82",
    INVALID_OPTIMAL_USAGE_RATIO = "83",
    INVALID_OPTIMAL_STABLE_TO_TOTAL_DEBT_RATIO = "84",
    UNDERLYING_CANNOT_BE_RESCUED = "85",
    ADDRESSES_PROVIDER_ALREADY_ADDED = "86",
    POOL_ADDRESSES_DO_NOT_MATCH = "87",
    STABLE_BORROWING_ENABLED = "88",
    SILOED_BORROWING_VIOLATION = "89",
    RESERVE_DEBT_NOT_ZERO = "90",
    FLASHLOAN_DISABLED = "91",
    SAFECAST_UINT128_OVERFLOW = "SafeCast: value doesn't fit in 128 bits",
    OWNABLE_ONLY_OWNER = "Ownable: caller is not the owner",
    ERC20_TRANSFER_AMOUNT_EXCEEDS_BALANCE = "ERC20: transfer amount exceeds balance",
    INVALID_FROM_BALANCE_AFTER_TRANSFER = "Invalid from balance after transfer",
    INVALID_TO_BALANCE_AFTER_TRANSFER = "Invalid from balance after transfer",
    INVALID_HF = "Invalid health factor"
}
export type tEthereumAddress = string;
export type tStringTokenBigUnits = string;
export type tBigNumberTokenBigUnits = BigNumber;
export type tStringTokenSmallUnits = string;
export type tBigNumberTokenSmallUnits = BigNumber;
export interface iAssetCommon<T> {
    [key: string]: T;
}
export interface iAssetBase<T> {
    WETH: T;
    DAI: T;
    TUSD: T;
    USDC: T;
    USDT: T;
    SUSD: T;
    AAVE: T;
    BAT: T;
    MKR: T;
    LINK: T;
    KNC: T;
    WBTC: T;
    MANA: T;
    ZRX: T;
    SNX: T;
    BUSD: T;
    YFI: T;
    UNI: T;
    USD: T;
    REN: T;
    ENJ: T;
    UniDAIWETH: T;
    UniWBTCWETH: T;
    UniAAVEWETH: T;
    UniBATWETH: T;
    UniDAIUSDC: T;
    UniCRVWETH: T;
    UniLINKWETH: T;
    UniMKRWETH: T;
    UniRENWETH: T;
    UniSNXWETH: T;
    UniUNIWETH: T;
    UniUSDCWETH: T;
    UniWBTCUSDC: T;
    UniYFIWETH: T;
    BptWBTCWETH: T;
    BptBALWETH: T;
    WMATIC: T;
    STAKE: T;
    xSUSHI: T;
}
export type iAssetsWithoutETH<T> = Omit<iAssetBase<T>, 'ETH'>;
export type iAssetsWithoutUSD<T> = Omit<iAssetBase<T>, 'USD'>;
export type iAavePoolAssets<T> = Pick<iAssetsWithoutUSD<T>, 'DAI' | 'TUSD' | 'USDC' | 'USDT' | 'SUSD' | 'AAVE' | 'BAT' | 'MKR' | 'LINK' | 'KNC' | 'WBTC' | 'MANA' | 'ZRX' | 'SNX' | 'BUSD' | 'WETH' | 'YFI' | 'UNI' | 'REN' | 'ENJ' | 'xSUSHI'>;
export type iMultiPoolsAssets<T> = iAssetCommon<T> | iAavePoolAssets<T>;
export type iAssetAggregatorBase<T> = iAssetsWithoutETH<T>;
export declare enum TokenContractId {
    DAI = "DAI",
    AAVE = "AAVE",
    TUSD = "TUSD",
    BAT = "BAT",
    WETH = "WETH",
    USDC = "USDC",
    USDT = "USDT",
    SUSD = "SUSD",
    ZRX = "ZRX",
    MKR = "MKR",
    WBTC = "WBTC",
    LINK = "LINK",
    KNC = "KNC",
    MANA = "MANA",
    REN = "REN",
    SNX = "SNX",
    BUSD = "BUSD",
    USD = "USD",
    YFI = "YFI",
    UNI = "UNI",
    ENJ = "ENJ",
    UniDAIWETH = "UniDAIWETH",
    UniWBTCWETH = "UniWBTCWETH",
    UniAAVEWETH = "UniAAVEWETH",
    UniBATWETH = "UniBATWETH",
    UniDAIUSDC = "UniDAIUSDC",
    UniCRVWETH = "UniCRVWETH",
    UniLINKWETH = "UniLINKWETH",
    UniMKRWETH = "UniMKRWETH",
    UniRENWETH = "UniRENWETH",
    UniSNXWETH = "UniSNXWETH",
    UniUNIWETH = "UniUNIWETH",
    UniUSDCWETH = "UniUSDCWETH",
    UniWBTCUSDC = "UniWBTCUSDC",
    UniYFIWETH = "UniYFIWETH",
    BptWBTCWETH = "BptWBTCWETH",
    BptBALWETH = "BptBALWETH",
    WMATIC = "WMATIC",
    STAKE = "STAKE",
    xSUSHI = "xSUSHI"
}
export interface IReserveParams extends IReserveBorrowParams, IReserveCollateralParams {
    aTokenImpl: eContractid;
    reserveFactor: string;
    supplyCap: string;
    strategy: IInterestRateStrategyParams;
}
export interface IInterestRateStrategyParams {
    name: string;
    optimalUsageRatio: string;
    baseVariableBorrowRate: string;
    variableRateSlope1: string;
    variableRateSlope2: string;
    stableRateSlope1: string;
    stableRateSlope2: string;
    baseStableRateOffset: string;
    stableRateExcessOffset: string;
    optimalStableToTotalDebtRatio: string;
}
export interface IReserveBorrowParams {
    borrowingEnabled: boolean;
    stableBorrowRateEnabled: boolean;
    reserveDecimals: string;
    borrowCap: string;
}
export interface IReserveCollateralParams {
    baseLTVAsCollateral: string;
    liquidationThreshold: string;
    liquidationBonus: string;
}
export interface IMarketRates {
    borrowRate: string;
}
export type iParamsPerNetwork<T> = iEthereumParamsPerNetwork<T>;
export interface iParamsPerNetworkAll<T> extends iEthereumParamsPerNetwork<T> {
}
export interface iEthereumParamsPerNetwork<T> {
    [eEthereumNetwork.coverage]: T;
    [eEthereumNetwork.kovan]: T;
    [eEthereumNetwork.ropsten]: T;
    [eEthereumNetwork.main]: T;
    [eEthereumNetwork.hardhat]: T;
    [eEthereumNetwork.tenderlyMain]: T;
}
export declare enum RateMode {
    None = "0",
    Stable = "1",
    Variable = "2"
}
export interface IProtocolGlobalConfig {
    TokenDistributorPercentageBase: string;
    MockUsdPriceInWei: string;
    UsdAddress: tEthereumAddress;
    NilAddress: tEthereumAddress;
    OneAddress: tEthereumAddress;
    AaveReferral: string;
}
export interface IMocksConfig {
    AllAssetsInitialPrices: iAssetBase<string>;
}
export interface IRate {
    borrowRate: string;
}
export interface ICommonConfiguration {
    MarketId: string;
    ATokenNamePrefix: string;
    StableDebtTokenNamePrefix: string;
    VariableDebtTokenNamePrefix: string;
    SymbolPrefix: string;
    ProviderId: number;
    ProtocolGlobalParams: IProtocolGlobalConfig;
    Mocks: IMocksConfig;
    ProviderRegistry: tEthereumAddress | undefined;
    ProviderRegistryOwner: tEthereumAddress | undefined;
    PoolConfigurator: tEthereumAddress | undefined;
    Pool: tEthereumAddress | undefined;
    TokenDistributor: tEthereumAddress | undefined;
    AaveOracle: tEthereumAddress | undefined;
    FallbackOracle: tEthereumAddress | undefined;
    ChainlinkAggregator: tEthereumAddress | undefined;
    PoolAdmin: tEthereumAddress | undefined;
    PoolAdminIndex: number;
    EmergencyAdmin: tEthereumAddress | undefined;
    EmergencyAdminIndex: number;
    ReserveAssets: SymbolMap<tEthereumAddress> | SymbolMap<undefined>;
    ReservesConfig: iMultiPoolsAssets<IReserveParams>;
    ATokenDomainSeparator: string;
    WETH: tEthereumAddress | undefined;
    WrappedNativeToken: tEthereumAddress | undefined;
    ReserveFactorTreasuryAddress: tEthereumAddress;
    IncentivesController: tEthereumAddress | undefined;
}
export interface IAaveConfiguration extends ICommonConfiguration {
    ReservesConfig: iMultiPoolsAssets<IReserveParams>;
}
export type PoolConfiguration = ICommonConfiguration | IAaveConfiguration;
//# sourceMappingURL=types.d.ts.map