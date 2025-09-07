# Blockchain Security and Audit Practices

## Smart Contract Security Framework

### Security-First Development Lifecycle

**Pre-Development Security Planning**
```solidity
// Security requirements definition
contract SecurityRequirements {
    // Define security roles and access patterns
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    bytes32 public constant EMERGENCY_ROLE = keccak256("EMERGENCY_ROLE");
    
    // Security constraints
    uint256 public constant MAX_SUPPLY = 1000000 * 10**18;
    uint256 public constant MIN_LOCK_PERIOD = 86400; // 24 hours
    uint256 public constant MAX_SLIPPAGE = 500; // 5%
    
    // Emergency controls
    bool public emergencyPaused;
    mapping(address => bool) public blacklisted;
    
    modifier whenNotEmergencyPaused() {
        require(!emergencyPaused, "Emergency paused");
        _;
    }
    
    modifier notBlacklisted(address account) {
        require(!blacklisted[account], "Address blacklisted");
        _;
    }
}
```

**Secure Coding Patterns**
```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureVault is ReentrancyGuard, Pausable, AccessControl {
    using SafeMath for uint256;
    using Address for address payable;
    
    // State variables for security
    mapping(address => uint256) private balances;
    mapping(address => uint256) private lastWithdrawal;
    uint256 private constant WITHDRAWAL_COOLDOWN = 3600; // 1 hour
    uint256 private constant MAX_WITHDRAWAL_RATE = 1000; // 10% per day
    
    event Deposit(address indexed user, uint256 amount, uint256 timestamp);
    event Withdrawal(address indexed user, uint256 amount, uint256 timestamp);
    event SecurityEvent(string eventType, address indexed user, uint256 timestamp);
    
    modifier withdrawalCooldown() {
        require(
            block.timestamp >= lastWithdrawal[msg.sender].add(WITHDRAWAL_COOLDOWN),
            "Withdrawal cooldown active"
        );
        _;
    }
    
    modifier rateLimited(uint256 amount) {
        uint256 dailyLimit = balances[msg.sender].mul(MAX_WITHDRAWAL_RATE).div(10000);
        require(amount <= dailyLimit, "Exceeds daily withdrawal limit");
        _;
    }
    
    function deposit() external payable whenNotPaused nonReentrant {
        require(msg.value > 0, "Deposit amount must be positive");
        require(msg.value <= 100 ether, "Deposit too large");
        
        balances[msg.sender] = balances[msg.sender].add(msg.value);
        emit Deposit(msg.sender, msg.value, block.timestamp);
    }
    
    function withdraw(uint256 amount) 
        external 
        whenNotPaused 
        nonReentrant 
        withdrawalCooldown 
        rateLimited(amount) 
    {
        require(amount > 0, "Withdrawal amount must be positive");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        balances[msg.sender] = balances[msg.sender].sub(amount);
        lastWithdrawal[msg.sender] = block.timestamp;
        
        // Use Address.sendValue for secure transfer
        payable(msg.sender).sendValue(amount);
        
        emit Withdrawal(msg.sender, amount, block.timestamp);
    }
    
    function emergencyWithdraw() external onlyRole(EMERGENCY_ROLE) {
        uint256 contractBalance = address(this).balance;
        payable(msg.sender).sendValue(contractBalance);
        
        emit SecurityEvent("Emergency withdrawal", msg.sender, block.timestamp);
    }
}
```

### Vulnerability Prevention Patterns

**Reentrancy Attack Prevention**
```solidity
contract ReentrancySecure {
    using ReentrancyGuard for uint256;
    
    mapping(address => uint256) private balances;
    uint256 private constant REENTRANCY_GUARD = 1;
    uint256 private constant REENTRANCY_GUARD_ENTERED = 2;
    uint256 private status;
    
    constructor() {
        status = REENTRANCY_GUARD;
    }
    
    modifier nonReentrant() {
        require(status != REENTRANCY_GUARD_ENTERED, "ReentrancyGuard: reentrant call");
        status = REENTRANCY_GUARD_ENTERED;
        _;
        status = REENTRANCY_GUARD;
    }
    
    // Checks-Effects-Interactions pattern
    function withdraw() external nonReentrant {
        uint256 balance = balances[msg.sender];
        
        // Checks
        require(balance > 0, "No balance to withdraw");
        
        // Effects (state changes before external calls)
        balances[msg.sender] = 0;
        
        // Interactions (external calls last)
        (bool success, ) = msg.sender.call{value: balance}("");
        if (!success) {
            // Revert state if call failed
            balances[msg.sender] = balance;
            revert("Transfer failed");
        }
    }
}
```

**Flash Loan Attack Prevention**
```solidity
contract FlashLoanSecure {
    mapping(address => uint256) private lastBlockInteraction;
    uint256 private priceSnapshot;
    uint256 private constant PRICE_UPDATE_DELAY = 1; // 1 block
    
    modifier noSameBlockInteraction() {
        require(
            lastBlockInteraction[msg.sender] != block.number,
            "Same block interaction not allowed"
        );
        lastBlockInteraction[msg.sender] = block.number;
        _;
    }
    
    modifier priceStabilityCheck() {
        uint256 currentPrice = getPrice();
        
        if (priceSnapshot > 0) {
            uint256 priceChange = currentPrice > priceSnapshot 
                ? currentPrice.sub(priceSnapshot).mul(10000).div(priceSnapshot)
                : priceSnapshot.sub(currentPrice).mul(10000).div(priceSnapshot);
                
            require(priceChange <= 500, "Price manipulation detected"); // 5% max change
        }
        
        priceSnapshot = currentPrice;
        _;
    }
    
    function sensitiveOperation() 
        external 
        noSameBlockInteraction 
        priceStabilityCheck 
    {
        // Implementation with flash loan protection
    }
    
    function getPrice() public view returns (uint256) {
        // Implement TWAP or multiple oracle price aggregation
        return oraclePrice;
    }
}
```

**Front-Running Protection**
```solidity
contract FrontRunningSecure {
    struct CommitReveal {
        bytes32 commitment;
        uint256 commitBlock;
        bool revealed;
    }
    
    mapping(address => CommitReveal) private commitments;
    uint256 private constant COMMIT_DURATION = 1;
    uint256 private constant REVEAL_DURATION = 10;
    
    function commitAction(bytes32 commitment) external {
        commitments[msg.sender] = CommitReveal({
            commitment: commitment,
            commitBlock: block.number,
            revealed: false
        });
    }
    
    function revealAndExecute(
        uint256 amount,
        uint256 price,
        uint256 nonce
    ) external {
        CommitReveal storage commit = commitments[msg.sender];
        
        require(commit.commitment != bytes32(0), "No commitment found");
        require(!commit.revealed, "Already revealed");
        require(
            block.number > commit.commitBlock + COMMIT_DURATION &&
            block.number <= commit.commitBlock + COMMIT_DURATION + REVEAL_DURATION,
            "Not in reveal window"
        );
        
        bytes32 hash = keccak256(abi.encodePacked(amount, price, nonce));
        require(hash == commit.commitment, "Invalid reveal");
        
        commit.revealed = true;
        
        // Execute the action with revealed parameters
        _executeAction(amount, price);
    }
    
    function _executeAction(uint256 amount, uint256 price) internal {
        // Protected action implementation
    }
}
```

## Security Auditing Framework

### Automated Security Analysis

**Comprehensive Security Test Suite**
```javascript
// test/security/SecurityAudit.test.js
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Security Audit Tests", function () {
    let contract;
    let owner, attacker, user1, user2;
    
    beforeEach(async function () {
        [owner, attacker, user1, user2] = await ethers.getSigners();
        
        const Contract = await ethers.getContractFactory("SecureContract");
        contract = await Contract.deploy();
    });
    
    describe("Reentrancy Tests", function () {
        it("Should prevent reentrancy attacks", async function () {
            // Deploy malicious contract
            const Attacker = await ethers.getContractFactory("ReentrancyAttacker");
            const attackerContract = await Attacker.deploy(contract.address);
            
            // Fund the target contract
            await contract.deposit({ value: ethers.utils.parseEther("10") });
            
            // Attempt reentrancy attack
            await attackerContract.attack({ value: ethers.utils.parseEther("1") });
            
            // Verify attack failed
            expect(await ethers.provider.getBalance(attackerContract.address))
                .to.be.lt(ethers.utils.parseEther("2"));
        });
    });
    
    describe("Access Control Tests", function () {
        it("Should enforce role-based access control", async function () {
            await expect(
                contract.connect(attacker).adminFunction()
            ).to.be.revertedWith("AccessControl: account is missing role");
        });
        
        it("Should allow role granting by admin only", async function () {
            await contract.grantRole(await contract.OPERATOR_ROLE(), user1.address);
            
            await expect(
                contract.connect(attacker).grantRole(await contract.ADMIN_ROLE(), attacker.address)
            ).to.be.revertedWith("AccessControl: account is missing role");
        });
    });
    
    describe("Integer Overflow/Underflow Tests", function () {
        it("Should prevent overflow attacks", async function () {
            const maxUint256 = ethers.constants.MaxUint256;
            
            await expect(
                contract.unsafeAdd(maxUint256, 1)
            ).to.be.revertedWith("SafeMath: addition overflow");
        });
        
        it("Should prevent underflow attacks", async function () {
            await expect(
                contract.unsafeSubtract(0, 1)
            ).to.be.revertedWith("SafeMath: subtraction overflow");
        });
    });
    
    describe("Flash Loan Attack Tests", function () {
        it("Should detect and prevent flash loan price manipulation", async function () {
            // Simulate flash loan attack
            const FlashLoanAttacker = await ethers.getContractFactory("FlashLoanAttacker");
            const flashAttacker = await FlashLoanAttacker.deploy();
            
            await expect(
                flashAttacker.executeFlashLoanAttack(contract.address)
            ).to.be.revertedWith("Price manipulation detected");
        });
    });
    
    describe("Front-Running Tests", function () {
        it("Should prevent front-running through commit-reveal", async function () {
            const commitment = ethers.utils.keccak256(
                ethers.utils.defaultAbiCoder.encode(
                    ["uint256", "uint256", "uint256"],
                    [1000, 100, 123456]
                )
            );
            
            // Commit phase
            await contract.commitAction(commitment);
            
            // Try to front-run before reveal window
            await expect(
                contract.revealAndExecute(1000, 100, 123456)
            ).to.be.revertedWith("Not in reveal window");
        });
    });
    
    describe("Gas Griefing Tests", function () {
        it("Should handle gas griefing in batch operations", async function () {
            const gasGriefer = await ethers.getContractFactory("GasGriefer");
            const griefer = await gasGriefer.deploy();
            
            // Test batch operation with gas griefing contract
            const recipients = [user1.address, griefer.address, user2.address];
            const amounts = [100, 100, 100];
            
            // Should complete partial execution without reverting entire batch
            await expect(
                contract.batchTransfer(recipients, amounts)
            ).to.not.be.reverted;
            
            // Verify legitimate transfers succeeded
            expect(await contract.balanceOf(user1.address)).to.equal(100);
            expect(await contract.balanceOf(user2.address)).to.equal(100);
        });
    });
});
```

**Property-Based Security Testing**
```javascript
// test/security/PropertyBasedTests.test.js
const fc = require("fast-check");

describe("Property-Based Security Tests", function () {
    let contract;
    
    beforeEach(async function () {
        const Contract = await ethers.getContractFactory("SecureVault");
        contract = await Contract.deploy();
    });
    
    it("Invariant: Total supply should never exceed max supply", async function () {
        await fc.assert(fc.asyncProperty(
            fc.array(fc.nat(1000), 1, 100),
            async (mintAmounts) => {
                let totalMinted = 0;
                
                for (const amount of mintAmounts) {
                    try {
                        await contract.mint(amount);
                        totalMinted += amount;
                    } catch (error) {
                        // Mint failed, which is acceptable
                    }
                }
                
                const totalSupply = await contract.totalSupply();
                const maxSupply = await contract.MAX_SUPPLY();
                
                expect(totalSupply.lte(maxSupply)).to.be.true;
            }
        ));
    });
    
    it("Invariant: User balance should never exceed their deposits", async function () {
        await fc.assert(fc.asyncProperty(
            fc.array(fc.record({
                action: fc.constantFrom("deposit", "withdraw"),
                amount: fc.nat(1000)
            }), 1, 50),
            async (actions) => {
                let totalDeposited = 0;
                let totalWithdrawn = 0;
                
                for (const action of actions) {
                    try {
                        if (action.action === "deposit") {
                            await contract.deposit({ value: action.amount });
                            totalDeposited += action.amount;
                        } else {
                            await contract.withdraw(action.amount);
                            totalWithdrawn += action.amount;
                        }
                    } catch (error) {
                        // Action failed, which is acceptable
                    }
                }
                
                const balance = await contract.balanceOf(owner.address);
                expect(totalWithdrawn).to.be.lte(totalDeposited);
            }
        ));
    });
});
```

### Manual Security Review Checklist

**Smart Contract Security Audit Checklist**
```markdown
# Smart Contract Security Audit Checklist

## Access Control
- [ ] Role-based access control implemented correctly
- [ ] Admin functions protected with appropriate modifiers
- [ ] Owner privileges are not excessive
- [ ] Multi-signature requirements for critical functions
- [ ] Time-lock mechanisms for sensitive operations

## Reentrancy Protection
- [ ] ReentrancyGuard modifier used on external functions
- [ ] Checks-Effects-Interactions pattern followed
- [ ] State changes occur before external calls
- [ ] Proper use of transfer() vs call() for ETH transfers

## Integer Overflow/Underflow
- [ ] SafeMath library used for arithmetic operations
- [ ] Solidity 0.8+ overflow protection utilized
- [ ] Edge cases tested (max/min values)
- [ ] Casting operations validated

## Input Validation
- [ ] All function parameters validated
- [ ] Array bounds checking implemented
- [ ] Zero address checks in place
- [ ] Reasonable limits on user inputs

## Front-Running Protection
- [ ] Commit-reveal schemes for sensitive operations
- [ ] Transaction ordering dependency minimized
- [ ] MEV protection mechanisms implemented
- [ ] Price manipulation resistance verified

## Oracle Security
- [ ] Multiple oracle sources for price feeds
- [ ] Price feed freshness checks implemented
- [ ] Circuit breakers for abnormal price movements
- [ ] Fallback mechanisms for oracle failures

## Flash Loan Protection
- [ ] Same-block interaction restrictions
- [ ] Price manipulation detection
- [ ] Liquidity threshold requirements
- [ ] Time-weighted average price (TWAP) usage

## Gas Optimization & DoS Protection
- [ ] Gas usage optimized and reasonable
- [ ] Unbounded loops avoided
- [ ] Gas griefing protection implemented
- [ ] Block gas limit considerations

## Upgrade Security
- [ ] Proxy patterns implemented securely
- [ ] Storage collision prevention
- [ ] Upgrade authorization controls
- [ ] Migration testing procedures

## Economic Security
- [ ] Token economics reviewed for exploits
- [ ] Incentive mechanisms aligned properly
- [ ] Economic attacks (governance, inflation) considered
- [ ] Slashing and penalty mechanisms validated
```

## Advanced Security Patterns

### Multi-Signature and Time-Lock Implementation

**Secure Multi-Signature Wallet**
```solidity
contract SecureMultiSig {
    struct Transaction {
        address to;
        uint256 value;
        bytes data;
        bool executed;
        uint256 confirmations;
        mapping(address => bool) confirmed;
    }
    
    mapping(uint256 => Transaction) public transactions;
    mapping(address => bool) public owners;
    uint256 public required;
    uint256 public transactionCount;
    uint256 public constant EXECUTION_DELAY = 86400; // 24 hours
    
    event TransactionSubmitted(uint256 indexed txId, address indexed owner);
    event TransactionConfirmed(uint256 indexed txId, address indexed owner);
    event TransactionExecuted(uint256 indexed txId);
    
    modifier onlyOwner() {
        require(owners[msg.sender], "Not an owner");
        _;
    }
    
    modifier transactionExists(uint256 txId) {
        require(txId < transactionCount, "Transaction does not exist");
        _;
    }
    
    modifier notConfirmed(uint256 txId) {
        require(!transactions[txId].confirmed[msg.sender], "Already confirmed");
        _;
    }
    
    modifier notExecuted(uint256 txId) {
        require(!transactions[txId].executed, "Already executed");
        _;
    }
    
    function submitTransaction(
        address to,
        uint256 value,
        bytes calldata data
    ) external onlyOwner returns (uint256 txId) {
        txId = transactionCount;
        transactions[txId].to = to;
        transactions[txId].value = value;
        transactions[txId].data = data;
        transactionCount++;
        
        emit TransactionSubmitted(txId, msg.sender);
        
        // Auto-confirm by submitter
        confirmTransaction(txId);
    }
    
    function confirmTransaction(uint256 txId)
        public
        onlyOwner
        transactionExists(txId)
        notConfirmed(txId)
        notExecuted(txId)
    {
        transactions[txId].confirmed[msg.sender] = true;
        transactions[txId].confirmations++;
        
        emit TransactionConfirmed(txId, msg.sender);
        
        if (transactions[txId].confirmations >= required) {
            executeTransaction(txId);
        }
    }
    
    function executeTransaction(uint256 txId)
        public
        transactionExists(txId)
        notExecuted(txId)
    {
        Transaction storage txn = transactions[txId];
        require(txn.confirmations >= required, "Not enough confirmations");
        
        txn.executed = true;
        
        (bool success, ) = txn.to.call{value: txn.value}(txn.data);
        require(success, "Transaction execution failed");
        
        emit TransactionExecuted(txId);
    }
}
```

**Time-Lock Contract for Critical Operations**
```solidity
contract TimeLock {
    mapping(bytes32 => uint256) public queuedTransactions;
    
    uint256 public constant GRACE_PERIOD = 14 days;
    uint256 public delay;
    address public admin;
    
    event QueueTransaction(
        bytes32 indexed txHash,
        address indexed target,
        uint256 value,
        string signature,
        bytes data,
        uint256 eta
    );
    
    event ExecuteTransaction(
        bytes32 indexed txHash,
        address indexed target,
        uint256 value,
        string signature,
        bytes data,
        uint256 eta
    );
    
    event CancelTransaction(bytes32 indexed txHash);
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }
    
    function queueTransaction(
        address target,
        uint256 value,
        string memory signature,
        bytes memory data,
        uint256 eta
    ) public onlyAdmin returns (bytes32) {
        require(
            eta >= getBlockTimestamp() + delay,
            "Transaction hasn't surpassed time lock"
        );
        
        bytes32 txHash = keccak256(abi.encode(target, value, signature, data, eta));
        queuedTransactions[txHash] = eta;
        
        emit QueueTransaction(txHash, target, value, signature, data, eta);
        return txHash;
    }
    
    function executeTransaction(
        address target,
        uint256 value,
        string memory signature,
        bytes memory data,
        uint256 eta
    ) public onlyAdmin returns (bytes memory) {
        bytes32 txHash = keccak256(abi.encode(target, value, signature, data, eta));
        
        require(queuedTransactions[txHash] != 0, "Transaction hasn't been queued");
        require(
            getBlockTimestamp() >= eta,
            "Transaction hasn't surpassed time lock"
        );
        require(
            getBlockTimestamp() <= eta + GRACE_PERIOD,
            "Transaction is stale"
        );
        
        queuedTransactions[txHash] = 0;
        
        bytes memory callData;
        if (bytes(signature).length == 0) {
            callData = data;
        } else {
            callData = abi.encodePacked(bytes4(keccak256(bytes(signature))), data);
        }
        
        (bool success, bytes memory returnData) = target.call{value: value}(callData);
        require(success, "Transaction execution reverted");
        
        emit ExecuteTransaction(txHash, target, value, signature, data, eta);
        
        return returnData;
    }
    
    function cancelTransaction(
        address target,
        uint256 value,
        string memory signature,
        bytes memory data,
        uint256 eta
    ) public onlyAdmin {
        bytes32 txHash = keccak256(abi.encode(target, value, signature, data, eta));
        queuedTransactions[txHash] = 0;
        
        emit CancelTransaction(txHash);
    }
}
```

### Emergency Response and Circuit Breakers

**Emergency Stop Mechanism**
```solidity
contract EmergencyStop {
    bool public emergencyStop;
    mapping(address => bool) public guardians;
    uint256 public guardianCount;
    uint256 public constant REQUIRED_GUARDIANS = 3;
    
    mapping(bytes32 => uint256) public emergencyVotes;
    mapping(bytes32 => mapping(address => bool)) public hasVoted;
    
    event EmergencyStopActivated(address indexed guardian, string reason);
    event EmergencyStopDeactivated(address indexed admin);
    event GuardianAdded(address indexed guardian);
    event GuardianRemoved(address indexed guardian);
    
    modifier notInEmergency() {
        require(!emergencyStop, "Emergency stop is active");
        _;
    }
    
    modifier onlyGuardian() {
        require(guardians[msg.sender], "Not a guardian");
        _;
    }
    
    modifier emergencyOnly() {
        require(emergencyStop, "Not in emergency");
        _;
    }
    
    function activateEmergencyStop(string calldata reason) 
        external 
        onlyGuardian 
    {
        bytes32 actionHash = keccak256(abi.encodePacked("EMERGENCY_STOP", reason));
        
        require(!hasVoted[actionHash][msg.sender], "Already voted");
        hasVoted[actionHash][msg.sender] = true;
        emergencyVotes[actionHash]++;
        
        if (emergencyVotes[actionHash] >= REQUIRED_GUARDIANS) {
            emergencyStop = true;
            emit EmergencyStopActivated(msg.sender, reason);
        }
    }
    
    function deactivateEmergencyStop() external onlyOwner emergencyOnly {
        emergencyStop = false;
        emit EmergencyStopDeactivated(msg.sender);
    }
    
    function emergencyWithdraw(address token, address to) 
        external 
        onlyOwner 
        emergencyOnly 
    {
        if (token == address(0)) {
            payable(to).transfer(address(this).balance);
        } else {
            IERC20(token).transfer(to, IERC20(token).balanceOf(address(this)));
        }
    }
}
```

**Circuit Breaker for Price Feeds**
```solidity
contract PriceCircuitBreaker {
    struct PriceData {
        uint256 price;
        uint256 timestamp;
        bool circuitBreakerActive;
    }
    
    mapping(address => PriceData) public assetPrices;
    mapping(address => uint256[]) public priceHistory;
    
    uint256 public constant MAX_PRICE_DEVIATION = 2000; // 20%
    uint256 public constant PRICE_HISTORY_WINDOW = 24 hours;
    uint256 public constant CIRCUIT_BREAKER_COOLDOWN = 1 hours;
    
    event CircuitBreakerTriggered(address indexed asset, uint256 oldPrice, uint256 newPrice);
    event CircuitBreakerReset(address indexed asset);
    
    function updatePrice(address asset, uint256 newPrice) external onlyOracle {
        PriceData storage priceData = assetPrices[asset];
        
        if (priceData.price > 0 && !priceData.circuitBreakerActive) {
            uint256 priceChange = newPrice > priceData.price 
                ? (newPrice - priceData.price) * 10000 / priceData.price
                : (priceData.price - newPrice) * 10000 / priceData.price;
            
            if (priceChange > MAX_PRICE_DEVIATION) {
                priceData.circuitBreakerActive = true;
                emit CircuitBreakerTriggered(asset, priceData.price, newPrice);
                return;
            }
        }
        
        // Update price if circuit breaker not active
        priceData.price = newPrice;
        priceData.timestamp = block.timestamp;
        
        // Add to price history
        priceHistory[asset].push(newPrice);
        
        // Clean old price history
        _cleanPriceHistory(asset);
    }
    
    function resetCircuitBreaker(address asset) external onlyAdmin {
        PriceData storage priceData = assetPrices[asset];
        
        require(priceData.circuitBreakerActive, "Circuit breaker not active");
        require(
            block.timestamp >= priceData.timestamp + CIRCUIT_BREAKER_COOLDOWN,
            "Cooldown period not finished"
        );
        
        priceData.circuitBreakerActive = false;
        emit CircuitBreakerReset(asset);
    }
    
    function getPrice(address asset) external view returns (uint256, bool) {
        PriceData memory priceData = assetPrices[asset];
        return (priceData.price, priceData.circuitBreakerActive);
    }
    
    function _cleanPriceHistory(address asset) internal {
        uint256[] storage history = priceHistory[asset];
        uint256 cutoff = block.timestamp - PRICE_HISTORY_WINDOW;
        
        // Remove old entries (simplified - in production, use more efficient data structure)
        while (history.length > 100) {
            for (uint i = 0; i < history.length - 1; i++) {
                history[i] = history[i + 1];
            }
            history.pop();
        }
    }
}
```

## Incident Response and Recovery

### Security Monitoring and Alerting

**On-Chain Security Monitoring**
```solidity
contract SecurityMonitor {
    struct SecurityEvent {
        string eventType;
        address actor;
        uint256 value;
        bytes data;
        uint256 timestamp;
        uint256 blockNumber;
    }
    
    SecurityEvent[] public securityEvents;
    mapping(string => uint256) public eventCounts;
    mapping(address => uint256) public suspiciousActivityCount;
    
    uint256 public constant SUSPICIOUS_THRESHOLD = 5;
    uint256 public constant TIME_WINDOW = 1 hours;
    
    event SecurityAlert(
        string indexed eventType,
        address indexed actor,
        uint256 severity,
        string description
    );
    
    function logSecurityEvent(
        string memory eventType,
        address actor,
        uint256 value,
        bytes memory data
    ) external {
        securityEvents.push(SecurityEvent({
            eventType: eventType,
            actor: actor,
            value: value,
            data: data,
            timestamp: block.timestamp,
            blockNumber: block.number
        }));
        
        eventCounts[eventType]++;
        suspiciousActivityCount[actor]++;
        
        _checkForSuspiciousActivity(eventType, actor);
    }
    
    function _checkForSuspiciousActivity(string memory eventType, address actor) internal {
        uint256 recentEvents = _countRecentEvents(actor);
        
        if (recentEvents >= SUSPICIOUS_THRESHOLD) {
            emit SecurityAlert(
                "SUSPICIOUS_ACTIVITY",
                actor,
                3, // High severity
                "Multiple suspicious events detected"
            );
        }
        
        // Check for specific event patterns
        if (keccak256(bytes(eventType)) == keccak256(bytes("LARGE_WITHDRAWAL"))) {
            emit SecurityAlert(
                "LARGE_WITHDRAWAL",
                actor,
                2, // Medium severity
                "Large withdrawal detected"
            );
        }
    }
    
    function _countRecentEvents(address actor) internal view returns (uint256) {
        uint256 count = 0;
        uint256 cutoff = block.timestamp - TIME_WINDOW;
        
        for (uint i = securityEvents.length; i > 0; i--) {
            SecurityEvent memory event = securityEvents[i - 1];
            if (event.timestamp < cutoff) break;
            if (event.actor == actor) count++;
        }
        
        return count;
    }
    
    function getRecentSecurityEvents(uint256 hours) 
        external 
        view 
        returns (SecurityEvent[] memory) 
    {
        uint256 cutoff = block.timestamp - (hours * 1 hours);
        uint256 count = 0;
        
        // Count recent events
        for (uint i = securityEvents.length; i > 0; i--) {
            if (securityEvents[i - 1].timestamp < cutoff) break;
            count++;
        }
        
        // Return recent events
        SecurityEvent[] memory recentEvents = new SecurityEvent[](count);
        uint256 index = 0;
        
        for (uint i = securityEvents.length; i > 0 && index < count; i--) {
            if (securityEvents[i - 1].timestamp >= cutoff) {
                recentEvents[index] = securityEvents[i - 1];
                index++;
            }
        }
        
        return recentEvents;
    }
}
```

### Post-Incident Recovery Procedures

**Contract Recovery and Migration**
```solidity
contract RecoveryMechanism {
    address public recoveryManager;
    bool public recoveryMode;
    uint256 public recoveryStartTime;
    
    mapping(address => uint256) public userBalances;
    mapping(address => bool) public recoveryCompleted;
    
    event RecoveryActivated(address indexed manager, string reason);
    event UserRecovered(address indexed user, uint256 amount);
    event RecoveryCompleted(uint256 totalRecovered);
    
    modifier onlyRecoveryManager() {
        require(msg.sender == recoveryManager, "Only recovery manager");
        _;
    }
    
    modifier inRecoveryMode() {
        require(recoveryMode, "Not in recovery mode");
        _;
    }
    
    function activateRecovery(string calldata reason) 
        external 
        onlyRecoveryManager 
    {
        recoveryMode = true;
        recoveryStartTime = block.timestamp;
        
        emit RecoveryActivated(msg.sender, reason);
    }
    
    function setUserBalance(address user, uint256 balance) 
        external 
        onlyRecoveryManager 
        inRecoveryMode 
    {
        require(!recoveryCompleted[user], "User already recovered");
        userBalances[user] = balance;
    }
    
    function claimRecovery() external inRecoveryMode {
        require(userBalances[msg.sender] > 0, "No balance to recover");
        require(!recoveryCompleted[msg.sender], "Already recovered");
        
        uint256 amount = userBalances[msg.sender];
        recoveryCompleted[msg.sender] = true;
        
        // Transfer recovered funds
        payable(msg.sender).transfer(amount);
        
        emit UserRecovered(msg.sender, amount);
    }
    
    function batchSetBalances(
        address[] calldata users,
        uint256[] calldata balances
    ) external onlyRecoveryManager inRecoveryMode {
        require(users.length == balances.length, "Array length mismatch");
        
        for (uint256 i = 0; i < users.length; i++) {
            if (!recoveryCompleted[users[i]]) {
                userBalances[users[i]] = balances[i];
            }
        }
    }
}
```