# Smart Contract Development and Security

## Smart Contract Architecture Patterns

### Contract Design Principles

**Modularity and Separation of Concerns**
- Single responsibility principle for contract functions
- Interface segregation for contract interactions
- Dependency inversion through abstract contracts
- Proxy patterns for upgradeable contracts

**Security-First Development**
- Fail-safe defaults and conservative state changes
- Input validation and boundary condition checks
- Access control and permission management
- Emergency stop mechanisms and circuit breakers

**Gas Optimization Strategies**
- Efficient data structure selection and storage patterns
- Function modifier optimization and call delegation
- Event emission for off-chain data storage
- Batch operations and transaction bundling

### Solidity Best Practices

**Variable and State Management**
```solidity
// Efficient storage packing
struct User {
    address wallet;      // 20 bytes
    uint96 balance;      // 12 bytes - fits in same slot
    bool isActive;       // 1 byte - fits in same slot
}

// Gas-efficient mappings
mapping(address => mapping(uint256 => bool)) private userTokenAccess;

// Use events for historical data
event UserBalanceUpdated(address indexed user, uint256 oldBalance, uint256 newBalance);
```

**Function Design and Access Control**
```solidity
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract SecureContract is AccessControl, ReentrancyGuard, Pausable {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant USER_ROLE = keccak256("USER_ROLE");
    
    modifier onlyValidAddress(address _addr) {
        require(_addr != address(0), "Invalid address");
        _;
    }
    
    function sensitiveOperation() 
        external 
        nonReentrant 
        whenNotPaused 
        onlyRole(USER_ROLE) 
    {
        // Implementation with security checks
    }
}
```

**Error Handling and Validation**
```solidity
// Custom errors for gas efficiency
error InsufficientBalance(uint256 requested, uint256 available);
error InvalidOperation(string reason);

contract ErrorHandling {
    function withdraw(uint256 amount) external {
        if (balances[msg.sender] < amount) {
            revert InsufficientBalance(amount, balances[msg.sender]);
        }
        // Safe withdrawal logic
    }
}
```

### Contract Testing Framework

**Unit Testing with Hardhat**
```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SecureContract", function () {
    let contract;
    let owner, user1, user2;
    
    beforeEach(async function () {
        [owner, user1, user2] = await ethers.getSigners();
        const Contract = await ethers.getContractFactory("SecureContract");
        contract = await Contract.deploy();
    });
    
    it("Should enforce access control", async function () {
        await expect(
            contract.connect(user1).adminFunction()
        ).to.be.revertedWith("AccessControl: account is missing role");
    });
    
    it("Should handle reentrancy attacks", async function () {
        // Reentrancy test implementation
    });
});
```

**Integration Testing Patterns**
```javascript
describe("Contract Integration", function () {
    it("Should handle multi-contract interactions", async function () {
        // Deploy dependent contracts
        // Test cross-contract calls
        // Verify state consistency
    });
    
    it("Should maintain invariants across operations", async function () {
        // Property-based testing
        // State invariant verification
    });
});
```

## Security Audit Framework

### Common Vulnerability Prevention

**Reentrancy Attack Prevention**
```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureWithdrawal is ReentrancyGuard {
    mapping(address => uint256) private balances;
    
    function withdraw() external nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance to withdraw");
        
        // Update state before external call
        balances[msg.sender] = 0;
        
        // External call after state update
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

**Integer Overflow Protection**
```solidity
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract SafeArithmetic {
    using SafeMath for uint256;
    
    function safeAdd(uint256 a, uint256 b) public pure returns (uint256) {
        return a.add(b); // Reverts on overflow
    }
    
    // For Solidity 0.8+, built-in overflow protection
    function checkedAdd(uint256 a, uint256 b) public pure returns (uint256) {
        unchecked {
            uint256 c = a + b;
            require(c >= a, "Addition overflow");
            return c;
        }
    }
}
```

**Access Control Implementation**
```solidity
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract RoleBasedAccess is AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant BURNER_ROLE = keccak256("BURNER_ROLE");
    
    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }
    
    function mint(address to, uint256 amount) 
        public 
        onlyRole(MINTER_ROLE) 
    {
        // Minting logic
    }
}
```

### Security Testing Procedures

**Automated Security Analysis**
```bash
# Slither static analysis
slither contracts/

# Mythril security analysis
myth analyze contracts/Contract.sol

# Echidna property-based testing
echidna-test contracts/ --contract Contract --config echidna.yaml
```

**Manual Security Review Checklist**
- [ ] Access control verification for all functions
- [ ] Reentrancy protection on external calls
- [ ] Integer overflow/underflow prevention
- [ ] Front-running attack mitigation
- [ ] Gas limit DoS prevention
- [ ] Oracle manipulation resistance
- [ ] Flash loan attack protection
- [ ] MEV (Maximal Extractable Value) considerations

## Advanced Smart Contract Patterns

### Proxy and Upgrade Patterns

**Transparent Proxy Implementation**
```solidity
import "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
import "@openzeppelin/contracts/proxy/transparent/ProxyAdmin.sol";

contract UpgradeableLogic is Initializable {
    uint256 public value;
    
    function initialize(uint256 _value) public initializer {
        value = _value;
    }
    
    function setValue(uint256 _value) public {
        value = _value;
    }
}
```

**Diamond Pattern for Complex Upgrades**
```solidity
import "./interfaces/IDiamondCut.sol";
import "./libraries/LibDiamond.sol";

contract Diamond {
    constructor(IDiamondCut.FacetCut[] memory _diamondCut, address _init, bytes memory _calldata) payable {
        LibDiamond.diamondCut(_diamondCut, _init, _calldata);
    }
    
    fallback() external payable {
        LibDiamond.DiamondStorage storage ds;
        bytes32 position = LibDiamond.DIAMOND_STORAGE_POSITION;
        assembly {
            ds.slot := position
        }
        
        address facet = ds.selectorToFacetAndPosition[msg.sig].facetAddress;
        require(facet != address(0), "Diamond: Function does not exist");
        
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), facet, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```

### Factory and Registry Patterns

**Contract Factory Implementation**
```solidity
contract TokenFactory {
    event TokenCreated(address indexed creator, address indexed token, string name);
    
    mapping(address => address[]) public creatorTokens;
    address[] public allTokens;
    
    function createToken(
        string memory name,
        string memory symbol,
        uint256 totalSupply
    ) external returns (address) {
        CustomToken token = new CustomToken(name, symbol, totalSupply, msg.sender);
        address tokenAddress = address(token);
        
        creatorTokens[msg.sender].push(tokenAddress);
        allTokens.push(tokenAddress);
        
        emit TokenCreated(msg.sender, tokenAddress, name);
        return tokenAddress;
    }
}
```

**Registry Pattern for Service Discovery**
```solidity
contract ServiceRegistry is AccessControl {
    bytes32 public constant REGISTRY_ADMIN = keccak256("REGISTRY_ADMIN");
    
    struct Service {
        address serviceAddress;
        string name;
        string version;
        bool active;
    }
    
    mapping(bytes32 => Service) private services;
    bytes32[] private serviceIds;
    
    function registerService(
        string memory name,
        string memory version,
        address serviceAddress
    ) external onlyRole(REGISTRY_ADMIN) {
        bytes32 serviceId = keccak256(abi.encodePacked(name, version));
        services[serviceId] = Service(serviceAddress, name, version, true);
        serviceIds.push(serviceId);
    }
    
    function getService(string memory name, string memory version) 
        external view returns (address) 
    {
        bytes32 serviceId = keccak256(abi.encodePacked(name, version));
        require(services[serviceId].active, "Service not active");
        return services[serviceId].serviceAddress;
    }
}
```

## Gas Optimization Techniques

### Storage Optimization Strategies

**Struct Packing Optimization**
```solidity
// Inefficient - uses 3 storage slots
struct BadStruct {
    bool active;      // 1 byte
    uint256 value;    // 32 bytes
    bool verified;    // 1 byte
}

// Efficient - uses 2 storage slots
struct GoodStruct {
    uint256 value;    // 32 bytes - slot 1
    bool active;      // 1 byte
    bool verified;    // 1 byte - both bools in slot 2
}
```

**Mapping vs Array Optimization**
```solidity
contract StorageOptimization {
    // For sparse data, mappings are more efficient
    mapping(uint256 => uint256) public sparseData;
    
    // For dense data, arrays can be more efficient
    uint256[] public denseData;
    
    // Packed array for small values
    uint8[] public smallValues;
    
    // Use events for historical data instead of storage
    event DataUpdated(uint256 indexed id, uint256 value, uint256 timestamp);
}
```

### Function Optimization Patterns

**Modifier Optimization**
```solidity
// Gas-efficient modifier
modifier validRange(uint256 value, uint256 min, uint256 max) {
    assembly {
        if or(lt(value, min), gt(value, max)) {
            mstore(0x00, 0x08c379a0) // Error selector
            mstore(0x20, 0x0000000000000000000000000000000000000000000000000000000000000020)
            mstore(0x4a, 0x0d496e76616c69642072616e6765) // "Invalid range"
            revert(0x00, 0x64)
        }
    }
    _;
}

// Batch operations for efficiency
function batchTransfer(address[] calldata recipients, uint256[] calldata amounts) 
    external 
{
    require(recipients.length == amounts.length, "Array length mismatch");
    
    for (uint256 i = 0; i < recipients.length; ) {
        _transfer(msg.sender, recipients[i], amounts[i]);
        unchecked { ++i; }
    }
}
```

### Assembly Optimization

**Low-Level Optimizations**
```solidity
contract AssemblyOptimized {
    function efficientHash(bytes calldata data) external pure returns (bytes32) {
        bytes32 result;
        assembly {
            result := keccak256(data.offset, data.length)
        }
        return result;
    }
    
    function efficientMemCopy(bytes memory dest, bytes memory src) internal pure {
        assembly {
            let destPtr := add(dest, 0x20)
            let srcPtr := add(src, 0x20)
            let length := mload(src)
            
            for { let i := 0 } lt(i, length) { i := add(i, 0x20) } {
                mstore(add(destPtr, i), mload(add(srcPtr, i)))
            }
        }
    }
}
```

## Testing and Deployment Framework

### Comprehensive Testing Strategy

**Property-Based Testing**
```javascript
const { expect } = require("chai");
const fc = require("fast-check");

describe("Property-Based Tests", function () {
    it("Should maintain invariants", async function () {
        await fc.assert(fc.asyncProperty(
            fc.array(fc.nat(), 1, 100),
            async (values) => {
                // Test invariants across random inputs
                for (const value of values) {
                    await contract.testFunction(value);
                }
                
                const totalSupply = await contract.totalSupply();
                expect(totalSupply).to.be.gte(0);
            }
        ));
    });
});
```

**Deployment and Verification Scripts**
```javascript
const { ethers } = require("hardhat");
const { verify } = require("../utils/verify");

async function main() {
    const constructorArgs = [
        "TokenName",
        "TKN",
        ethers.utils.parseEther("1000000")
    ];
    
    const Contract = await ethers.getContractFactory("CustomToken");
    const contract = await Contract.deploy(...constructorArgs);
    await contract.deployed();
    
    console.log(`Contract deployed to: ${contract.address}`);
    
    // Wait for block confirmations
    await contract.deployTransaction.wait(6);
    
    // Verify on Etherscan
    await verify(contract.address, constructorArgs);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
```