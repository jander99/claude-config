# Web3 Integration and DApp Development

## Web3 Frontend Architecture

### Modern Web3 Tech Stack

**Next.js with TypeScript and Web3 Libraries**
```typescript
// pages/_app.tsx
import { WagmiConfig, createConfig, configureChains, mainnet } from 'wagmi'
import { publicProvider } from 'wagmi/providers/public'
import { ConnectKitProvider, getDefaultConfig } from 'connectkit'
import { MetaMaskConnector } from 'wagmi/connectors/metaMask'
import { WalletConnectConnector } from 'wagmi/connectors/walletConnect'

const { chains, publicClient } = configureChains(
  [mainnet],
  [publicProvider()]
)

const config = createConfig({
  autoConnect: true,
  connectors: [
    new MetaMaskConnector({ chains }),
    new WalletConnectConnector({
      chains,
      options: {
        projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID!,
      },
    }),
  ],
  publicClient,
})

export default function App({ Component, pageProps }: AppProps) {
  return (
    <WagmiConfig config={config}>
      <ConnectKitProvider theme="auto">
        <Component {...pageProps} />
      </ConnectKitProvider>
    </WagmiConfig>
  )
}
```

**React Hooks for Contract Interaction**
```typescript
// hooks/useContract.ts
import { useContract, useContractRead, useContractWrite, usePrepareContractWrite } from 'wagmi'
import { ERC20_ABI, LENDING_POOL_ABI } from '../constants/abis'

export function useTokenBalance(tokenAddress: string, userAddress: string) {
  const { data: balance, isLoading } = useContractRead({
    address: tokenAddress as `0x${string}`,
    abi: ERC20_ABI,
    functionName: 'balanceOf',
    args: [userAddress],
    watch: true,
  })

  return {
    balance: balance ? formatEther(balance) : '0',
    isLoading,
  }
}

export function useTokenApproval(tokenAddress: string, spenderAddress: string, amount: string) {
  const { config } = usePrepareContractWrite({
    address: tokenAddress as `0x${string}`,
    abi: ERC20_ABI,
    functionName: 'approve',
    args: [spenderAddress, parseEther(amount)],
  })

  const { write: approve, isLoading } = useContractWrite(config)

  return { approve, isLoading }
}

export function useLendingPool(poolAddress: string) {
  const { config: supplyConfig } = usePrepareContractWrite({
    address: poolAddress as `0x${string}`,
    abi: LENDING_POOL_ABI,
    functionName: 'supply',
  })

  const { write: supply, isLoading: isSupplying } = useContractWrite(supplyConfig)

  const { config: borrowConfig } = usePrepareContractWrite({
    address: poolAddress as `0x${string}`,
    abi: LENDING_POOL_ABI,
    functionName: 'borrow',
  })

  const { write: borrow, isLoading: isBorrowing } = useContractWrite(borrowConfig)

  return {
    supply,
    borrow,
    isSupplying,
    isBorrowing,
  }
}
```

### Wallet Integration Patterns

**Multi-Wallet Support Component**
```typescript
// components/WalletConnect.tsx
import { useAccount, useConnect, useDisconnect } from 'wagmi'
import { useState } from 'react'

interface WalletConnectProps {
  onConnect?: (address: string) => void
  onDisconnect?: () => void
}

export function WalletConnect({ onConnect, onDisconnect }: WalletConnectProps) {
  const { address, isConnected } = useAccount()
  const { connect, connectors, error, isLoading, pendingConnector } = useConnect()
  const { disconnect } = useDisconnect()
  const [showConnectors, setShowConnectors] = useState(false)

  const handleConnect = (connector: any) => {
    connect({ connector })
    onConnect?.(address || '')
    setShowConnectors(false)
  }

  const handleDisconnect = () => {
    disconnect()
    onDisconnect?.()
  }

  if (isConnected) {
    return (
      <div className="flex items-center gap-4">
        <div className="text-sm">
          {address?.slice(0, 6)}...{address?.slice(-4)}
        </div>
        <button
          onClick={handleDisconnect}
          className="px-4 py-2 bg-red-500 text-white rounded"
        >
          Disconnect
        </button>
      </div>
    )
  }

  return (
    <div className="relative">
      <button
        onClick={() => setShowConnectors(!showConnectors)}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Connect Wallet
      </button>

      {showConnectors && (
        <div className="absolute top-full mt-2 bg-white border rounded shadow-lg z-10">
          {connectors.map((connector) => (
            <button
              key={connector.id}
              onClick={() => handleConnect(connector)}
              disabled={!connector.ready}
              className="block w-full px-4 py-2 text-left hover:bg-gray-100"
            >
              {connector.name}
              {!connector.ready && ' (unsupported)'}
              {isLoading && connector.id === pendingConnector?.id && ' (connecting)'}
            </button>
          ))}
        </div>
      )}

      {error && <div className="text-red-500 mt-2">{error.message}</div>}
    </div>
  )
}
```

**Transaction Management Hook**
```typescript
// hooks/useTransaction.ts
import { useState } from 'react'
import { useWaitForTransaction } from 'wagmi'
import { toast } from 'react-hot-toast'

interface TransactionState {
  isLoading: boolean
  isSuccess: boolean
  isError: boolean
  error?: Error
  hash?: string
}

export function useTransaction() {
  const [txState, setTxState] = useState<TransactionState>({
    isLoading: false,
    isSuccess: false,
    isError: false,
  })

  const { isLoading: isWaiting } = useWaitForTransaction({
    hash: txState.hash as `0x${string}`,
    onSuccess: () => {
      setTxState(prev => ({ ...prev, isSuccess: true, isLoading: false }))
      toast.success('Transaction confirmed!')
    },
    onError: (error) => {
      setTxState(prev => ({ ...prev, isError: true, isLoading: false, error }))
      toast.error('Transaction failed')
    },
  })

  const executeTransaction = async (txFunction: () => Promise<any>) => {
    try {
      setTxState({ isLoading: true, isSuccess: false, isError: false })
      
      const tx = await txFunction()
      setTxState(prev => ({ ...prev, hash: tx.hash }))
      
      toast.success('Transaction submitted!')
    } catch (error) {
      setTxState({ 
        isLoading: false, 
        isSuccess: false, 
        isError: true, 
        error: error as Error 
      })
      toast.error('Transaction rejected')
    }
  }

  return {
    ...txState,
    isWaiting,
    executeTransaction,
  }
}
```

## Smart Contract Integration Patterns

### Contract Factory Integration

**Dynamic Contract Deployment**
```typescript
// services/contractFactory.ts
import { ethers } from 'ethers'
import { FACTORY_ABI, TOKEN_BYTECODE } from '../constants'

export class ContractFactory {
  private factory: ethers.Contract
  private signer: ethers.Signer

  constructor(factoryAddress: string, signer: ethers.Signer) {
    this.factory = new ethers.Contract(factoryAddress, FACTORY_ABI, signer)
    this.signer = signer
  }

  async deployToken(
    name: string,
    symbol: string,
    totalSupply: string
  ): Promise<{ address: string; tx: string }> {
    const tx = await this.factory.createToken(
      name,
      symbol,
      ethers.utils.parseEther(totalSupply)
    )

    const receipt = await tx.wait()
    const event = receipt.events?.find(e => e.event === 'TokenCreated')
    const tokenAddress = event?.args?.token

    return {
      address: tokenAddress,
      tx: tx.hash,
    }
  }

  async getDeployedTokens(creator: string): Promise<string[]> {
    const tokens = await this.factory.getCreatorTokens(creator)
    return tokens
  }

  async getTokenInfo(tokenAddress: string) {
    const tokenContract = new ethers.Contract(
      tokenAddress,
      ['function name() view returns (string)', 'function symbol() view returns (string)', 'function totalSupply() view returns (uint256)'],
      this.signer
    )

    const [name, symbol, totalSupply] = await Promise.all([
      tokenContract.name(),
      tokenContract.symbol(),
      tokenContract.totalSupply(),
    ])

    return { name, symbol, totalSupply: ethers.utils.formatEther(totalSupply) }
  }
}
```

**Multi-Network Contract Manager**
```typescript
// services/contractManager.ts
interface NetworkConfig {
  chainId: number
  name: string
  rpcUrl: string
  contracts: {
    [key: string]: string
  }
}

const NETWORK_CONFIGS: { [key: number]: NetworkConfig } = {
  1: {
    chainId: 1,
    name: 'Ethereum Mainnet',
    rpcUrl: 'https://eth-mainnet.alchemyapi.io/v2/YOUR-API-KEY',
    contracts: {
      lendingPool: '0x...',
      tokenFactory: '0x...',
      governance: '0x...',
    },
  },
  5: {
    chainId: 5,
    name: 'Goerli Testnet',
    rpcUrl: 'https://eth-goerli.alchemyapi.io/v2/YOUR-API-KEY',
    contracts: {
      lendingPool: '0x...',
      tokenFactory: '0x...',
      governance: '0x...',
    },
  },
}

export class ContractManager {
  private providers: { [chainId: number]: ethers.providers.JsonRpcProvider } = {}
  private contracts: { [key: string]: ethers.Contract } = {}

  constructor(private chainId: number) {
    this.initializeProvider()
  }

  private initializeProvider() {
    const config = NETWORK_CONFIGS[this.chainId]
    if (!config) throw new Error(`Unsupported chain ID: ${this.chainId}`)

    this.providers[this.chainId] = new ethers.providers.JsonRpcProvider(config.rpcUrl)
  }

  async getContract(contractName: string, signer?: ethers.Signer): Promise<ethers.Contract> {
    const key = `${this.chainId}-${contractName}`
    
    if (!this.contracts[key]) {
      const config = NETWORK_CONFIGS[this.chainId]
      const address = config.contracts[contractName]
      
      if (!address) throw new Error(`Contract ${contractName} not found for chain ${this.chainId}`)

      const provider = signer || this.providers[this.chainId]
      const abi = await this.getContractABI(contractName)
      
      this.contracts[key] = new ethers.Contract(address, abi, provider)
    }

    return this.contracts[key]
  }

  async switchNetwork(newChainId: number) {
    this.chainId = newChainId
    this.initializeProvider()
    
    // Clear cached contracts for different network
    this.contracts = {}
  }

  private async getContractABI(contractName: string): Promise<any[]> {
    // Load ABI from constants or fetch from API
    const abis = {
      lendingPool: LENDING_POOL_ABI,
      tokenFactory: TOKEN_FACTORY_ABI,
      governance: GOVERNANCE_ABI,
    }
    
    return abis[contractName] || []
  }
}
```

### Event Listening and Real-Time Updates

**Event Subscription Service**
```typescript
// services/eventService.ts
import { ethers } from 'ethers'
import EventEmitter from 'events'

export class EventService extends EventEmitter {
  private provider: ethers.providers.Provider
  private contracts: Map<string, ethers.Contract> = new Map()
  private listeners: Map<string, ethers.providers.Listener> = new Map()

  constructor(provider: ethers.providers.Provider) {
    super()
    this.provider = provider
  }

  async subscribeToContract(
    contractAddress: string,
    abi: any[],
    eventName: string,
    filter?: any
  ) {
    const contract = new ethers.Contract(contractAddress, abi, this.provider)
    const filterKey = `${contractAddress}-${eventName}`

    // Remove existing listener if any
    this.unsubscribe(filterKey)

    // Create event filter
    const eventFilter = filter ? contract.filters[eventName](...filter) : contract.filters[eventName]()

    // Set up listener
    const listener = (...args: any[]) => {
      const event = args[args.length - 1] // Last arg is the event object
      this.emit(`${filterKey}`, {
        ...event,
        parsedArgs: args.slice(0, -1),
      })
    }

    contract.on(eventFilter, listener)
    this.listeners.set(filterKey, listener)
    this.contracts.set(contractAddress, contract)

    return filterKey
  }

  async getHistoricalEvents(
    contractAddress: string,
    abi: any[],
    eventName: string,
    fromBlock: number = 0,
    toBlock: number | string = 'latest'
  ) {
    const contract = new ethers.Contract(contractAddress, abi, this.provider)
    const filter = contract.filters[eventName]()

    const events = await contract.queryFilter(filter, fromBlock, toBlock)
    return events.map(event => ({
      ...event,
      parsedArgs: contract.interface.parseLog(event).args,
    }))
  }

  unsubscribe(filterKey: string) {
    const listener = this.listeners.get(filterKey)
    if (listener) {
      // Find contract and remove listener
      for (const [address, contract] of this.contracts.entries()) {
        contract.removeAllListeners()
      }
      this.listeners.delete(filterKey)
    }
  }

  unsubscribeAll() {
    for (const contract of this.contracts.values()) {
      contract.removeAllListeners()
    }
    this.listeners.clear()
    this.contracts.clear()
  }
}

// Usage in React component
export function useContractEvents(
  contractAddress: string,
  abi: any[],
  eventName: string,
  filter?: any[]
) {
  const [events, setEvents] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const eventService = useRef<EventService>()

  useEffect(() => {
    if (!window.ethereum) return

    const provider = new ethers.providers.Web3Provider(window.ethereum)
    eventService.current = new EventService(provider)

    const setupSubscription = async () => {
      try {
        // Get historical events first
        const historicalEvents = await eventService.current!.getHistoricalEvents(
          contractAddress,
          abi,
          eventName
        )
        setEvents(historicalEvents)
        setIsLoading(false)

        // Subscribe to new events
        const subscription = await eventService.current!.subscribeToContract(
          contractAddress,
          abi,
          eventName,
          filter
        )

        eventService.current!.on(subscription, (event) => {
          setEvents(prev => [event, ...prev])
        })
      } catch (error) {
        console.error('Error setting up event subscription:', error)
        setIsLoading(false)
      }
    }

    setupSubscription()

    return () => {
      eventService.current?.unsubscribeAll()
    }
  }, [contractAddress, eventName])

  return { events, isLoading }
}
```

## DApp Architecture Patterns

### State Management for Web3 Applications

**Redux Store for DApp State**
```typescript
// store/web3Slice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'

interface TokenInfo {
  address: string
  name: string
  symbol: string
  decimals: number
  balance: string
  price: number
}

interface DAppState {
  isConnected: boolean
  address: string | null
  chainId: number | null
  tokens: TokenInfo[]
  transactions: Transaction[]
  loading: {
    tokens: boolean
    transactions: boolean
  }
  error: string | null
}

const initialState: DAppState = {
  isConnected: false,
  address: null,
  chainId: null,
  tokens: [],
  transactions: [],
  loading: {
    tokens: false,
    transactions: false,
  },
  error: null,
}

export const fetchTokenBalances = createAsyncThunk(
  'web3/fetchTokenBalances',
  async ({ address, tokenAddresses }: { address: string; tokenAddresses: string[] }) => {
    const provider = new ethers.providers.Web3Provider(window.ethereum)
    const balances = await Promise.all(
      tokenAddresses.map(async (tokenAddress) => {
        const contract = new ethers.Contract(tokenAddress, ERC20_ABI, provider)
        const [name, symbol, decimals, balance] = await Promise.all([
          contract.name(),
          contract.symbol(),
          contract.decimals(),
          contract.balanceOf(address),
        ])
        
        return {
          address: tokenAddress,
          name,
          symbol,
          decimals,
          balance: ethers.utils.formatUnits(balance, decimals),
          price: 0, // Fetch from price API
        }
      })
    )
    
    return balances
  }
)

const web3Slice = createSlice({
  name: 'web3',
  initialState,
  reducers: {
    connectWallet: (state, action: PayloadAction<{ address: string; chainId: number }>) => {
      state.isConnected = true
      state.address = action.payload.address
      state.chainId = action.payload.chainId
      state.error = null
    },
    disconnectWallet: (state) => {
      state.isConnected = false
      state.address = null
      state.chainId = null
      state.tokens = []
      state.transactions = []
    },
    addTransaction: (state, action: PayloadAction<Transaction>) => {
      state.transactions.unshift(action.payload)
    },
    updateTransaction: (state, action: PayloadAction<{ hash: string; status: string }>) => {
      const tx = state.transactions.find(tx => tx.hash === action.payload.hash)
      if (tx) {
        tx.status = action.payload.status
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTokenBalances.pending, (state) => {
        state.loading.tokens = true
      })
      .addCase(fetchTokenBalances.fulfilled, (state, action) => {
        state.loading.tokens = false
        state.tokens = action.payload
      })
      .addCase(fetchTokenBalances.rejected, (state, action) => {
        state.loading.tokens = false
        state.error = action.error.message || 'Failed to fetch token balances'
      })
  },
})

export const { connectWallet, disconnectWallet, addTransaction, updateTransaction } = web3Slice.actions
export default web3Slice.reducer
```

**Context Provider for DApp Data**
```typescript
// contexts/DAppContext.tsx
interface DAppContextType {
  account: string | null
  chainId: number | null
  provider: ethers.providers.Web3Provider | null
  signer: ethers.Signer | null
  contracts: { [key: string]: ethers.Contract }
  isLoading: boolean
  error: string | null
  connect: () => Promise<void>
  disconnect: () => void
  switchChain: (chainId: number) => Promise<void>
  getContract: (name: string) => ethers.Contract | null
}

const DAppContext = createContext<DAppContextType | null>(null)

export function DAppProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState({
    account: null,
    chainId: null,
    provider: null,
    signer: null,
    contracts: {},
    isLoading: false,
    error: null,
  })

  const connect = async () => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }))

      if (!window.ethereum) {
        throw new Error('No wallet found')
      }

      const provider = new ethers.providers.Web3Provider(window.ethereum)
      await provider.send('eth_requestAccounts', [])
      
      const signer = provider.getSigner()
      const account = await signer.getAddress()
      const network = await provider.getNetwork()

      // Initialize contracts
      const contracts = await initializeContracts(signer, network.chainId)

      setState(prev => ({
        ...prev,
        account,
        chainId: network.chainId,
        provider,
        signer,
        contracts,
        isLoading: false,
      }))

      // Set up event listeners
      window.ethereum.on('accountsChanged', handleAccountsChanged)
      window.ethereum.on('chainChanged', handleChainChanged)
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: (error as Error).message,
      }))
    }
  }

  const disconnect = () => {
    setState({
      account: null,
      chainId: null,
      provider: null,
      signer: null,
      contracts: {},
      isLoading: false,
      error: null,
    })

    // Remove event listeners
    if (window.ethereum) {
      window.ethereum.removeAllListeners()
    }
  }

  const switchChain = async (chainId: number) => {
    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: `0x${chainId.toString(16)}` }],
      })
    } catch (error) {
      console.error('Failed to switch chain:', error)
    }
  }

  const getContract = (name: string) => {
    return state.contracts[name] || null
  }

  const value: DAppContextType = {
    ...state,
    connect,
    disconnect,
    switchChain,
    getContract,
  }

  return <DAppContext.Provider value={value}>{children}</DAppContext.Provider>
}

export const useDApp = () => {
  const context = useContext(DAppContext)
  if (!context) {
    throw new Error('useDApp must be used within a DAppProvider')
  }
  return context
}
```

### Error Handling and User Experience

**Transaction Error Handler**
```typescript
// utils/errorHandler.ts
export interface TransactionError {
  code: number
  message: string
  userMessage: string
  action?: string
}

export function parseTransactionError(error: any): TransactionError {
  // User rejected transaction
  if (error.code === 4001) {
    return {
      code: 4001,
      message: error.message,
      userMessage: 'Transaction was rejected by user',
      action: 'retry',
    }
  }

  // Insufficient funds
  if (error.code === -32000 && error.message.includes('insufficient funds')) {
    return {
      code: -32000,
      message: error.message,
      userMessage: 'Insufficient funds for transaction',
      action: 'fund_wallet',
    }
  }

  // Gas estimation failed
  if (error.message.includes('gas required exceeds allowance')) {
    return {
      code: -32000,
      message: error.message,
      userMessage: 'Transaction would fail. Please check parameters and try again.',
      action: 'adjust_params',
    }
  }

  // Contract revert with reason
  if (error.reason) {
    return {
      code: error.code || -1,
      message: error.message,
      userMessage: `Transaction failed: ${error.reason}`,
      action: 'check_conditions',
    }
  }

  // Network error
  if (error.code === 'NETWORK_ERROR') {
    return {
      code: error.code,
      message: error.message,
      userMessage: 'Network connection error. Please try again.',
      action: 'retry',
    }
  }

  // Generic error
  return {
    code: error.code || -1,
    message: error.message || 'Unknown error',
    userMessage: 'An unexpected error occurred. Please try again.',
    action: 'retry',
  }
}

export function useTransactionErrorHandler() {
  const [error, setError] = useState<TransactionError | null>(null)

  const handleError = useCallback((error: any) => {
    const parsedError = parseTransactionError(error)
    setError(parsedError)
    
    // Auto-clear error after 10 seconds
    setTimeout(() => setError(null), 10000)
    
    return parsedError
  }, [])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  return { error, handleError, clearError }
}
```

**Loading States and Progressive Enhancement**
```typescript
// components/TransactionButton.tsx
interface TransactionButtonProps {
  onClick: () => Promise<void>
  disabled?: boolean
  children: React.ReactNode
  loadingText?: string
  successText?: string
}

export function TransactionButton({
  onClick,
  disabled,
  children,
  loadingText = 'Processing...',
  successText = 'Success!',
}: TransactionButtonProps) {
  const [state, setState] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [error, setError] = useState<string | null>(null)

  const handleClick = async () => {
    try {
      setState('loading')
      setError(null)
      
      await onClick()
      
      setState('success')
      setTimeout(() => setState('idle'), 2000)
    } catch (err) {
      setState('error')
      setError((err as Error).message)
      setTimeout(() => setState('idle'), 3000)
    }
  }

  const getButtonContent = () => {
    switch (state) {
      case 'loading':
        return (
          <div className="flex items-center gap-2">
            <Spinner className="w-4 h-4" />
            {loadingText}
          </div>
        )
      case 'success':
        return (
          <div className="flex items-center gap-2">
            <CheckIcon className="w-4 h-4" />
            {successText}
          </div>
        )
      case 'error':
        return (
          <div className="flex items-center gap-2">
            <XIcon className="w-4 h-4" />
            Error
          </div>
        )
      default:
        return children
    }
  }

  const getButtonClass = () => {
    const base = 'px-4 py-2 rounded font-medium transition-colors'
    
    switch (state) {
      case 'loading':
        return `${base} bg-yellow-500 text-white cursor-wait`
      case 'success':
        return `${base} bg-green-500 text-white`
      case 'error':
        return `${base} bg-red-500 text-white`
      default:
        return `${base} bg-blue-500 text-white hover:bg-blue-600 disabled:bg-gray-400`
    }
  }

  return (
    <div>
      <button
        onClick={handleClick}
        disabled={disabled || state === 'loading'}
        className={getButtonClass()}
      >
        {getButtonContent()}
      </button>
      
      {error && (
        <div className="mt-2 text-sm text-red-600">
          {error}
        </div>
      )}
    </div>
  )
}
```

## Testing and Deployment

### E2E Testing for DApps

**Playwright with MetaMask Integration**
```typescript
// tests/e2e/dapp.spec.ts
import { test, expect } from '@playwright/test'
import { MetaMask } from '@playwright/test-metamask'

test.describe('DApp E2E Tests', () => {
  let metamask: MetaMask

  test.beforeEach(async ({ page }) => {
    // Initialize MetaMask
    metamask = new MetaMask(page)
    await metamask.setup({
      secretPhrase: process.env.TEST_WALLET_SEED!,
      network: 'localhost',
      password: 'testPassword123',
    })

    // Navigate to DApp
    await page.goto('http://localhost:3000')
  })

  test('should connect wallet and display balance', async ({ page }) => {
    // Click connect wallet button
    await page.click('[data-testid="connect-wallet"]')
    
    // Confirm connection in MetaMask
    await metamask.approveConnection()
    
    // Verify wallet is connected
    await expect(page.locator('[data-testid="wallet-address"]')).toBeVisible()
    await expect(page.locator('[data-testid="token-balance"]')).toBeVisible()
  })

  test('should perform token swap', async ({ page }) => {
    // Connect wallet first
    await page.click('[data-testid="connect-wallet"]')
    await metamask.approveConnection()
    
    // Navigate to swap interface
    await page.click('[data-testid="swap-link"]')
    
    // Enter swap amounts
    await page.fill('[data-testid="token-input"]', '1')
    await page.selectOption('[data-testid="token-select"]', 'USDC')
    
    // Approve token spending
    await page.click('[data-testid="approve-button"]')
    await metamask.confirmTransaction()
    
    // Execute swap
    await page.click('[data-testid="swap-button"]')
    await metamask.confirmTransaction()
    
    // Verify success
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible()
  })

  test('should handle transaction errors gracefully', async ({ page }) => {
    // Connect wallet
    await page.click('[data-testid="connect-wallet"]')
    await metamask.approveConnection()
    
    // Try to perform action without sufficient balance
    await page.click('[data-testid="borrow-link"]')
    await page.fill('[data-testid="borrow-amount"]', '1000000')
    await page.click('[data-testid="borrow-button"]')
    
    // Reject transaction in MetaMask
    await metamask.rejectTransaction()
    
    // Verify error handling
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible()
    await expect(page.locator('[data-testid="error-message"]')).toContainText('rejected')
  })
})
```

### Production Deployment Pipeline

**Docker Configuration for DApp**
```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/out /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Infrastructure as Code with Terraform**
```hcl
# infrastructure/main.tf
resource "aws_s3_bucket" "dapp_frontend" {
  bucket = "${var.project_name}-frontend-${var.environment}"
}

resource "aws_s3_bucket_website_configuration" "dapp_frontend" {
  bucket = aws_s3_bucket.dapp_frontend.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_cloudfront_distribution" "dapp_cdn" {
  origin {
    domain_name = aws_s3_bucket.dapp_frontend.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.dapp_frontend.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-${aws_s3_bucket.dapp_frontend.id}"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }
}
```