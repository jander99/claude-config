# DeFi Protocol Development and Implementation

## DeFi Protocol Architecture

### Automated Market Maker (AMM) Implementation

**Constant Product AMM (Uniswap V2 Style)**
```solidity
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract ConstantProductAMM is ReentrancyGuard {
    IERC20 public immutable token0;
    IERC20 public immutable token1;
    
    uint256 public reserve0;
    uint256 public reserve1;
    uint256 public totalSupply;
    
    mapping(address => uint256) public balanceOf;
    
    event Mint(address indexed to, uint256 amount0, uint256 amount1);
    event Burn(address indexed to, uint256 amount0, uint256 amount1);
    event Swap(address indexed to, uint256 amount0In, uint256 amount1In, uint256 amount0Out, uint256 amount1Out);
    
    constructor(address _token0, address _token1) {
        token0 = IERC20(_token0);
        token1 = IERC20(_token1);
    }
    
    function addLiquidity(uint256 amount0, uint256 amount1) 
        external 
        nonReentrant 
        returns (uint256 liquidity) 
    {
        token0.transferFrom(msg.sender, address(this), amount0);
        token1.transferFrom(msg.sender, address(this), amount1);
        
        if (totalSupply == 0) {
            liquidity = sqrt(amount0 * amount1);
        } else {
            liquidity = min(
                (amount0 * totalSupply) / reserve0,
                (amount1 * totalSupply) / reserve1
            );
        }
        
        require(liquidity > 0, "Insufficient liquidity minted");
        balanceOf[msg.sender] += liquidity;
        totalSupply += liquidity;
        
        _update();
        emit Mint(msg.sender, amount0, amount1);
    }
    
    function swap(uint256 amount0Out, uint256 amount1Out, address to) 
        external 
        nonReentrant 
    {
        require(amount0Out > 0 || amount1Out > 0, "Insufficient output amount");
        require(amount0Out < reserve0 && amount1Out < reserve1, "Insufficient liquidity");
        
        if (amount0Out > 0) token0.transfer(to, amount0Out);
        if (amount1Out > 0) token1.transfer(to, amount1Out);
        
        uint256 balance0 = token0.balanceOf(address(this));
        uint256 balance1 = token1.balanceOf(address(this));
        
        uint256 amount0In = balance0 > reserve0 - amount0Out ? balance0 - (reserve0 - amount0Out) : 0;
        uint256 amount1In = balance1 > reserve1 - amount1Out ? balance1 - (reserve1 - amount1Out) : 0;
        
        require(amount0In > 0 || amount1In > 0, "Insufficient input amount");
        
        // Apply 0.3% fee
        uint256 balance0Adjusted = balance0 * 1000 - amount0In * 3;
        uint256 balance1Adjusted = balance1 * 1000 - amount1In * 3;
        
        require(
            balance0Adjusted * balance1Adjusted >= uint256(reserve0) * reserve1 * (1000**2),
            "K"
        );
        
        _update();
        emit Swap(to, amount0In, amount1In, amount0Out, amount1Out);
    }
}
```

**Concentrated Liquidity AMM (Uniswap V3 Style)**
```solidity
contract ConcentratedLiquidityAMM {
    struct Position {
        uint128 liquidity;
        uint256 feeGrowthInside0LastX128;
        uint256 feeGrowthInside1LastX128;
        uint128 tokensOwed0;
        uint128 tokensOwed1;
    }
    
    struct Tick {
        uint128 liquidityGross;
        int128 liquidityNet;
        uint256 feeGrowthOutside0X128;
        uint256 feeGrowthOutside1X128;
        bool initialized;
    }
    
    mapping(bytes32 => Position) public positions;
    mapping(int24 => Tick) public ticks;
    
    int24 public currentTick;
    uint160 public sqrtPriceX96;
    uint128 public liquidity;
    
    function mint(
        address recipient,
        int24 tickLower,
        int24 tickUpper,
        uint128 amount
    ) external returns (uint256 amount0, uint256 amount1) {
        require(tickLower < tickUpper, "Invalid tick range");
        require(tickLower >= MIN_TICK && tickUpper <= MAX_TICK, "Tick out of bounds");
        
        bytes32 positionKey = keccak256(abi.encodePacked(recipient, tickLower, tickUpper));
        Position storage position = positions[positionKey];
        
        // Calculate token amounts based on current price and range
        (amount0, amount1) = LiquidityAmounts.getAmountsForLiquidity(
            sqrtPriceX96,
            TickMath.getSqrtRatioAtTick(tickLower),
            TickMath.getSqrtRatioAtTick(tickUpper),
            amount
        );
        
        // Update position
        position.liquidity += amount;
        
        // Update ticks
        _updateTick(tickLower, amount, false);
        _updateTick(tickUpper, amount, true);
        
        // Update global liquidity if price is in range
        if (currentTick >= tickLower && currentTick < tickUpper) {
            liquidity += amount;
        }
    }
}
```

### Lending and Borrowing Protocols

**Compound-Style Lending Pool**
```solidity
import "./interfaces/IERC20.sol";
import "./libraries/SafeMath.sol";
import "./PriceOracle.sol";

contract LendingPool {
    using SafeMath for uint256;
    
    struct Market {
        IERC20 underlying;
        uint256 totalBorrows;
        uint256 totalReserves;
        uint256 reserveFactor;
        uint256 collateralFactor;
        uint256 liquidationIncentive;
        InterestRateModel interestRateModel;
        mapping(address => uint256) accountBorrows;
        mapping(address => BorrowSnapshot) accountBorrowSnapshots;
    }
    
    struct BorrowSnapshot {
        uint256 principal;
        uint256 interestIndex;
    }
    
    mapping(address => Market) public markets;
    mapping(address => mapping(address => uint256)) public accountTokens;
    
    PriceOracle public oracle;
    
    function supply(address asset, uint256 amount) external {
        Market storage market = markets[asset];
        require(address(market.underlying) != address(0), "Market not listed");
        
        market.underlying.transferFrom(msg.sender, address(this), amount);
        
        uint256 exchangeRate = getExchangeRate(asset);
        uint256 mintTokens = amount.mul(1e18).div(exchangeRate);
        
        accountTokens[msg.sender][asset] = accountTokens[msg.sender][asset].add(mintTokens);
        
        emit Supply(msg.sender, asset, amount, mintTokens);
    }
    
    function borrow(address asset, uint256 amount) external {
        Market storage market = markets[asset];
        require(address(market.underlying) != address(0), "Market not listed");
        
        // Check borrowing capacity
        uint256 accountLiquidity = getAccountLiquidity(msg.sender);
        uint256 borrowValue = oracle.getUnderlyingPrice(asset).mul(amount);
        require(accountLiquidity >= borrowValue, "Insufficient liquidity");
        
        // Update borrow balance
        uint256 borrowIndex = getBorrowIndex(asset);
        BorrowSnapshot storage snapshot = market.accountBorrowSnapshots[msg.sender];
        
        if (snapshot.interestIndex == 0) {
            snapshot.interestIndex = borrowIndex;
        }
        
        uint256 principalTimesIndex = snapshot.principal.mul(borrowIndex);
        uint256 newPrincipal = principalTimesIndex.div(snapshot.interestIndex).add(amount);
        
        snapshot.principal = newPrincipal;
        snapshot.interestIndex = borrowIndex;
        market.accountBorrows[msg.sender] = newPrincipal;
        market.totalBorrows = market.totalBorrows.add(amount);
        
        market.underlying.transfer(msg.sender, amount);
        
        emit Borrow(msg.sender, asset, amount);
    }
    
    function liquidate(
        address borrower,
        address assetBorrowed,
        uint256 repayAmount,
        address assetCollateral
    ) external {
        // Check if account is underwater
        uint256 accountLiquidity = getAccountLiquidity(borrower);
        require(accountLiquidity == 0, "Account not underwater");
        
        // Calculate liquidation amounts
        uint256 maxRepay = getMaxLiquidation(borrower, assetBorrowed);
        require(repayAmount <= maxRepay, "Excessive repay amount");
        
        uint256 collateralValue = oracle.getUnderlyingPrice(assetCollateral)
            .mul(accountTokens[borrower][assetCollateral])
            .mul(markets[assetCollateral].liquidationIncentive)
            .div(1e18);
            
        uint256 repayValue = oracle.getUnderlyingPrice(assetBorrowed).mul(repayAmount);
        uint256 seizeTokens = repayValue.mul(1e18).div(collateralValue);
        
        // Perform liquidation
        markets[assetBorrowed].underlying.transferFrom(msg.sender, address(this), repayAmount);
        
        // Reduce borrower's debt
        _repayBorrow(borrower, assetBorrowed, repayAmount);
        
        // Transfer collateral to liquidator
        accountTokens[borrower][assetCollateral] = accountTokens[borrower][assetCollateral].sub(seizeTokens);
        accountTokens[msg.sender][assetCollateral] = accountTokens[msg.sender][assetCollateral].add(seizeTokens);
        
        emit Liquidation(msg.sender, borrower, assetBorrowed, repayAmount, assetCollateral, seizeTokens);
    }
}
```

### Yield Farming and Staking Protocols

**Multi-Token Yield Farm**
```solidity
contract YieldFarm {
    struct UserInfo {
        uint256 amount;
        uint256 rewardDebt;
        uint256 pendingRewards;
    }
    
    struct PoolInfo {
        IERC20 lpToken;
        uint256 allocPoint;
        uint256 lastRewardBlock;
        uint256 accRewardPerShare;
        uint256 totalStaked;
    }
    
    IERC20 public rewardToken;
    uint256 public rewardPerBlock;
    uint256 public totalAllocPoint;
    uint256 public startBlock;
    
    PoolInfo[] public poolInfo;
    mapping(uint256 => mapping(address => UserInfo)) public userInfo;
    
    event Deposit(address indexed user, uint256 indexed pid, uint256 amount);
    event Withdraw(address indexed user, uint256 indexed pid, uint256 amount);
    event Harvest(address indexed user, uint256 indexed pid, uint256 amount);
    
    function addPool(
        uint256 _allocPoint,
        IERC20 _lpToken,
        bool _withUpdate
    ) external onlyOwner {
        if (_withUpdate) {
            massUpdatePools();
        }
        
        uint256 lastRewardBlock = block.number > startBlock ? block.number : startBlock;
        totalAllocPoint = totalAllocPoint.add(_allocPoint);
        
        poolInfo.push(PoolInfo({
            lpToken: _lpToken,
            allocPoint: _allocPoint,
            lastRewardBlock: lastRewardBlock,
            accRewardPerShare: 0,
            totalStaked: 0
        }));
    }
    
    function deposit(uint256 _pid, uint256 _amount) external {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        
        updatePool(_pid);
        
        if (user.amount > 0) {
            uint256 pending = user.amount.mul(pool.accRewardPerShare).div(1e12).sub(user.rewardDebt);
            if (pending > 0) {
                user.pendingRewards = user.pendingRewards.add(pending);
            }
        }
        
        if (_amount > 0) {
            pool.lpToken.transferFrom(msg.sender, address(this), _amount);
            user.amount = user.amount.add(_amount);
            pool.totalStaked = pool.totalStaked.add(_amount);
        }
        
        user.rewardDebt = user.amount.mul(pool.accRewardPerShare).div(1e12);
        emit Deposit(msg.sender, _pid, _amount);
    }
    
    function compound(uint256 _pid) external {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        
        updatePool(_pid);
        
        uint256 pending = user.amount.mul(pool.accRewardPerShare).div(1e12).sub(user.rewardDebt);
        uint256 totalPending = pending.add(user.pendingRewards);
        
        if (totalPending > 0) {
            // Convert rewards to LP tokens through DEX
            uint256 lpTokens = _swapRewardForLP(totalPending);
            
            user.amount = user.amount.add(lpTokens);
            pool.totalStaked = pool.totalStaked.add(lpTokens);
            user.pendingRewards = 0;
        }
        
        user.rewardDebt = user.amount.mul(pool.accRewardPerShare).div(1e12);
    }
}
```

## Advanced DeFi Mechanisms

### Flash Loan Implementation

**Flash Loan Provider**
```solidity
import "./interfaces/IFlashLoanReceiver.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract FlashLoanProvider is ReentrancyGuard {
    mapping(address => uint256) public poolBalance;
    uint256 public constant FLASH_LOAN_FEE = 9; // 0.09% fee
    uint256 public constant FEE_DENOMINATOR = 10000;
    
    event FlashLoan(address indexed receiver, address indexed asset, uint256 amount, uint256 fee);
    
    function flashLoan(
        address receiverAddress,
        address asset,
        uint256 amount,
        bytes calldata params
    ) external nonReentrant {
        uint256 availableBalance = IERC20(asset).balanceOf(address(this));
        require(amount <= availableBalance, "Insufficient pool balance");
        
        uint256 fee = amount.mul(FLASH_LOAN_FEE).div(FEE_DENOMINATOR);
        uint256 amountPlusFee = amount.add(fee);
        
        // Transfer flash loan amount to receiver
        IERC20(asset).transfer(receiverAddress, amount);
        
        // Execute receiver logic
        IFlashLoanReceiver(receiverAddress).executeOperation(
            asset,
            amount,
            fee,
            msg.sender,
            params
        );
        
        // Check repayment
        uint256 currentBalance = IERC20(asset).balanceOf(address(this));
        require(currentBalance >= availableBalance.add(fee), "Flash loan not repaid");
        
        emit FlashLoan(receiverAddress, asset, amount, fee);
    }
}

interface IFlashLoanReceiver {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 fee,
        address initiator,
        bytes calldata params
    ) external;
}
```

**Flash Loan Arbitrage Bot**
```solidity
contract ArbitrageBot is IFlashLoanReceiver {
    address public flashLoanProvider;
    
    struct ArbitrageParams {
        address tokenA;
        address tokenB;
        address dexA;
        address dexB;
        uint256 minProfit;
    }
    
    function executeArbitrage(
        address asset,
        uint256 amount,
        ArbitrageParams memory params
    ) external {
        bytes memory data = abi.encode(params);
        
        IFlashLoanProvider(flashLoanProvider).flashLoan(
            address(this),
            asset,
            amount,
            data
        );
    }
    
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 fee,
        address initiator,
        bytes calldata params
    ) external override {
        require(msg.sender == flashLoanProvider, "Invalid caller");
        
        ArbitrageParams memory arbParams = abi.decode(params, (ArbitrageParams));
        
        // Step 1: Swap on DEX A
        uint256 receivedTokenB = _swapOnDEX(
            arbParams.dexA,
            asset,
            arbParams.tokenB,
            amount
        );
        
        // Step 2: Swap back on DEX B
        uint256 receivedTokenA = _swapOnDEX(
            arbParams.dexB,
            arbParams.tokenB,
            asset,
            receivedTokenB
        );
        
        // Step 3: Calculate profit
        uint256 repayAmount = amount.add(fee);
        require(receivedTokenA >= repayAmount.add(arbParams.minProfit), "Insufficient profit");
        
        // Repay flash loan
        IERC20(asset).transfer(flashLoanProvider, repayAmount);
        
        // Keep profit
        uint256 profit = receivedTokenA.sub(repayAmount);
        IERC20(asset).transfer(initiator, profit);
    }
}
```

### Governance and DAO Implementation

**Token-Based Governance**
```solidity
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";

contract DAOGovernor is Governor, GovernorVotes, GovernorTimelockControl {
    constructor(
        ERC20Votes _token,
        TimelockController _timelock
    )
        Governor("DAO Governor")
        GovernorVotes(_token)
        GovernorTimelockControl(_timelock)
    {}
    
    function votingDelay() public pure override returns (uint256) {
        return 1; // 1 block
    }
    
    function votingPeriod() public pure override returns (uint256) {
        return 45818; // 1 week
    }
    
    function quorum(uint256 blockNumber) public pure override returns (uint256) {
        return 1000000e18; // 1M tokens
    }
    
    function proposalThreshold() public pure override returns (uint256) {
        return 100000e18; // 100K tokens to propose
    }
    
    // Custom proposal logic
    function propose(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        string memory description
    ) public override returns (uint256) {
        require(
            getVotes(msg.sender, block.number - 1) >= proposalThreshold(),
            "Governor: proposer votes below threshold"
        );
        
        return super.propose(targets, values, calldatas, description);
    }
    
    // Emergency actions for time-sensitive decisions
    function emergencyExecute(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) external onlyRole(EMERGENCY_ROLE) {
        _execute(0, targets, values, calldatas, descriptionHash);
    }
}
```

## Protocol Integration Patterns

### Cross-Protocol Composability

**DeFi Aggregator Pattern**
```solidity
contract DeFiAggregator {
    struct SwapParams {
        address tokenIn;
        address tokenOut;
        uint256 amountIn;
        uint256 minAmountOut;
        address[] exchanges;
        bytes[] swapData;
    }
    
    mapping(address => bool) public authorizedExchanges;
    
    function multiDexSwap(SwapParams calldata params) 
        external 
        returns (uint256 totalOut) 
    {
        IERC20(params.tokenIn).transferFrom(msg.sender, address(this), params.amountIn);
        
        uint256 remainingAmount = params.amountIn;
        
        for (uint256 i = 0; i < params.exchanges.length; i++) {
            require(authorizedExchanges[params.exchanges[i]], "Unauthorized exchange");
            
            uint256 swapAmount = remainingAmount / (params.exchanges.length - i);
            
            // Prepare swap data
            IERC20(params.tokenIn).approve(params.exchanges[i], swapAmount);
            
            // Execute swap
            (bool success, bytes memory result) = params.exchanges[i].call(params.swapData[i]);
            require(success, "Swap failed");
            
            remainingAmount -= swapAmount;
        }
        
        totalOut = IERC20(params.tokenOut).balanceOf(address(this));
        require(totalOut >= params.minAmountOut, "Insufficient output");
        
        IERC20(params.tokenOut).transfer(msg.sender, totalOut);
    }
}
```

**Yield Strategy Vault**
```solidity
contract YieldVault is ERC4626 {
    using SafeERC20 for IERC20;
    
    struct Strategy {
        address strategyContract;
        uint256 allocation; // Percentage of funds allocated (basis points)
        uint256 lastHarvest;
        bool active;
    }
    
    Strategy[] public strategies;
    uint256 public totalAllocation;
    uint256 public performanceFee = 1000; // 10%
    address public feeRecipient;
    
    function addStrategy(
        address strategyContract,
        uint256 allocation
    ) external onlyOwner {
        require(totalAllocation + allocation <= 10000, "Allocation exceeds 100%");
        
        strategies.push(Strategy({
            strategyContract: strategyContract,
            allocation: allocation,
            lastHarvest: block.timestamp,
            active: true
        }));
        
        totalAllocation += allocation;
    }
    
    function harvest() external {
        uint256 totalYield = 0;
        
        for (uint256 i = 0; i < strategies.length; i++) {
            if (strategies[i].active) {
                uint256 yield = IStrategy(strategies[i].strategyContract).harvest();
                totalYield += yield;
                strategies[i].lastHarvest = block.timestamp;
            }
        }
        
        // Take performance fee
        uint256 fee = totalYield * performanceFee / 10000;
        IERC20(asset()).safeTransfer(feeRecipient, fee);
        
        // Compound remaining yield
        _compound(totalYield - fee);
    }
    
    function rebalance() external onlyOwner {
        uint256 totalAssets = totalAssets();
        
        for (uint256 i = 0; i < strategies.length; i++) {
            if (strategies[i].active) {
                uint256 targetAmount = totalAssets * strategies[i].allocation / 10000;
                uint256 currentAmount = IStrategy(strategies[i].strategyContract).totalAssets();
                
                if (currentAmount > targetAmount) {
                    // Withdraw excess
                    IStrategy(strategies[i].strategyContract).withdraw(currentAmount - targetAmount);
                } else if (currentAmount < targetAmount) {
                    // Deposit more
                    uint256 available = IERC20(asset()).balanceOf(address(this));
                    uint256 toDeposit = Math.min(targetAmount - currentAmount, available);
                    
                    if (toDeposit > 0) {
                        IERC20(asset()).safeApprove(strategies[i].strategyContract, toDeposit);
                        IStrategy(strategies[i].strategyContract).deposit(toDeposit);
                    }
                }
            }
        }
    }
}
```

## Risk Management and Security

### Price Oracle Integration

**Chainlink Price Oracle with Fallbacks**
```solidity
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract PriceOracle {
    struct PriceFeed {
        AggregatorV3Interface chainlinkFeed;
        address backupOracle;
        uint256 heartbeat;
        uint256 maxPriceDeviation; // In basis points
    }
    
    mapping(address => PriceFeed) public priceFeeds;
    mapping(address => uint256) public assetPrices;
    
    function getPrice(address asset) external view returns (uint256) {
        PriceFeed memory feed = priceFeeds[asset];
        
        // Try Chainlink first
        try feed.chainlinkFeed.latestRoundData() returns (
            uint80 roundId,
            int256 price,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) {
            require(price > 0, "Invalid price");
            require(updatedAt > 0, "Price not updated");
            require(block.timestamp - updatedAt <= feed.heartbeat, "Price stale");
            
            // Check for price manipulation
            uint256 currentPrice = uint256(price);
            if (_isPriceValid(asset, currentPrice)) {
                return currentPrice;
            }
        } catch {
            // Chainlink failed, try backup
        }
        
        // Fallback to backup oracle
        if (feed.backupOracle != address(0)) {
            return IBackupOracle(feed.backupOracle).getPrice(asset);
        }
        
        revert("No valid price available");
    }
    
    function _isPriceValid(address asset, uint256 newPrice) internal view returns (bool) {
        uint256 oldPrice = assetPrices[asset];
        if (oldPrice == 0) return true; // First price update
        
        uint256 deviation = newPrice > oldPrice 
            ? (newPrice - oldPrice) * 10000 / oldPrice
            : (oldPrice - newPrice) * 10000 / oldPrice;
            
        return deviation <= priceFeeds[asset].maxPriceDeviation;
    }
}
```

### MEV Protection and Fair Ordering

**Commit-Reveal Scheme for Fair Ordering**
```solidity
contract FairOrderingDEX {
    struct Order {
        address trader;
        uint256 amount;
        uint256 price;
        bool isBuy;
        uint256 commitBlock;
        bytes32 commitment;
        bool revealed;
    }
    
    mapping(bytes32 => Order) public orders;
    mapping(uint256 => bytes32[]) public blockOrders;
    
    uint256 public constant COMMIT_DURATION = 1; // blocks
    uint256 public constant REVEAL_DURATION = 5; // blocks
    
    function commitOrder(bytes32 commitment) external payable {
        bytes32 orderId = keccak256(abi.encodePacked(msg.sender, block.timestamp));
        
        orders[orderId] = Order({
            trader: msg.sender,
            amount: 0,
            price: 0,
            isBuy: false,
            commitBlock: block.number,
            commitment: commitment,
            revealed: false
        });
        
        blockOrders[block.number].push(orderId);
    }
    
    function revealOrder(
        bytes32 orderId,
        uint256 amount,
        uint256 price,
        bool isBuy,
        uint256 nonce
    ) external {
        Order storage order = orders[orderId];
        require(order.trader == msg.sender, "Not order owner");
        require(!order.revealed, "Already revealed");
        require(
            block.number > order.commitBlock + COMMIT_DURATION &&
            block.number <= order.commitBlock + COMMIT_DURATION + REVEAL_DURATION,
            "Not in reveal window"
        );
        
        bytes32 hash = keccak256(abi.encodePacked(amount, price, isBuy, nonce));
        require(hash == order.commitment, "Invalid reveal");
        
        order.amount = amount;
        order.price = price;
        order.isBuy = isBuy;
        order.revealed = true;
    }
    
    function executeOrdersForBlock(uint256 blockNumber) external {
        require(
            block.number > blockNumber + COMMIT_DURATION + REVEAL_DURATION,
            "Reveal period not ended"
        );
        
        bytes32[] memory orderIds = blockOrders[blockNumber];
        
        // Sort orders by price for fair execution
        _sortOrdersByPrice(orderIds);
        
        // Execute orders in price-time priority
        for (uint256 i = 0; i < orderIds.length; i++) {
            Order storage order = orders[orderIds[i]];
            if (order.revealed) {
                _executeOrder(orderIds[i]);
            }
        }
    }
}
```