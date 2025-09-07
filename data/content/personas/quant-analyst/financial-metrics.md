# Quant Analyst Financial Metrics

## Core Financial Metrics Framework

### Fundamental Financial Analysis
**CRITICAL: Quantitative analyst calculates and analyzes essential financial metrics that support investment decisions while maintaining strict accuracy and providing clear interpretation:**

1. **Risk-Return Metrics**
   - Sharpe ratio and risk-adjusted return analysis
   - Sortino ratio and downside risk measurement
   - Information ratio and active return assessment
   - Maximum drawdown and recovery period analysis
   - Value at Risk (VaR) and Expected Shortfall (ES) calculation

2. **Performance Attribution and Analysis**
   - Factor-based return decomposition and attribution
   - Asset allocation vs security selection effects
   - Benchmark comparison and tracking error analysis
   - Rolling performance and consistency measurement
   - Risk-adjusted performance evaluation frameworks

3. **Portfolio Analytics and Optimization**
   - Modern Portfolio Theory implementation and optimization
   - Risk budgeting and equal risk contribution analysis
   - Correlation analysis and diversification measurement
   - Rebalancing frequency and transaction cost analysis
   - Capacity analysis and scalability assessment

## Risk Metrics and Measurement

### 1. Volatility and Risk Assessment

**Statistical Risk Measures:**
```python
import numpy as np
import pandas as pd
from scipy import stats

def calculate_risk_metrics(returns):
    """Calculate comprehensive risk metrics for return series"""
    
    # Basic volatility measures
    daily_vol = returns.std()
    annual_vol = daily_vol * np.sqrt(252)
    
    # Downside risk measures
    downside_returns = returns[returns < 0]
    downside_deviation = downside_returns.std() * np.sqrt(252)
    
    # Value at Risk calculations
    var_95 = np.percentile(returns, 5)
    var_99 = np.percentile(returns, 1)
    
    # Expected Shortfall (Conditional VaR)
    es_95 = returns[returns <= var_95].mean()
    es_99 = returns[returns <= var_99].mean()
    
    # Maximum drawdown calculation
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        'annual_volatility': annual_vol,
        'downside_deviation': downside_deviation,
        'var_95': var_95,
        'var_99': var_99,
        'expected_shortfall_95': es_95,
        'expected_shortfall_99': es_99,
        'max_drawdown': max_drawdown
    }
```

**Advanced Risk Analytics:**
```yaml
Risk Decomposition:
  Factor Risk Analysis:
    - Beta calculation and market risk exposure
    - Factor loading estimation and attribution
    - Idiosyncratic risk and specific risk measurement
    - Active risk decomposition and tracking error sources
    - Risk budget allocation and optimization
  
  Tail Risk Assessment:
    - Extreme value theory and tail risk modeling
    - Stress testing and scenario analysis
    - Monte Carlo simulation for tail risk estimation
    - Copula modeling for dependency structure
    - Black swan event probability assessment
  
  Time-Varying Risk:
    - GARCH modeling for volatility clustering
    - Regime change detection and risk adjustment
    - Rolling window risk estimation
    - Forward-looking volatility forecasting
    - Risk regime identification and classification
```

### 2. Performance Attribution Framework

**Multi-Factor Attribution Analysis:**
```python
def brinson_attribution(portfolio_weights, benchmark_weights, 
                       portfolio_returns, benchmark_returns):
    """
    Calculate Brinson-Hood-Beebower attribution effects
    """
    
    # Asset allocation effect
    weight_diff = portfolio_weights - benchmark_weights
    allocation_effect = (weight_diff * benchmark_returns).sum()
    
    # Security selection effect  
    return_diff = portfolio_returns - benchmark_returns
    selection_effect = (benchmark_weights * return_diff).sum()
    
    # Interaction effect
    interaction_effect = (weight_diff * return_diff).sum()
    
    # Total active return
    total_active = allocation_effect + selection_effect + interaction_effect
    
    return {
        'allocation_effect': allocation_effect,
        'selection_effect': selection_effect,
        'interaction_effect': interaction_effect,
        'total_active_return': total_active
    }
```

**Performance Measurement Standards:**
```yaml
Return Calculation Methods:
  Time-Weighted Returns:
    - Daily valuation and geometric linking
    - Modified Dietz method for cash flow adjustment
    - GIPS compliance and standard methodology
    - Multi-period return calculation and annualization
    - Currency hedging and translation effects
  
  Risk-Adjusted Performance:
    - Sharpe ratio calculation and interpretation
    - Treynor ratio and systematic risk adjustment
    - Jensen's alpha and benchmark-relative performance
    - Information ratio and tracking error analysis
    - Appraisal ratio and specific return measurement
  
  Benchmark Analysis:
    - Appropriate benchmark selection and validation
    - Benchmark composition and rebalancing effects
    - Style analysis and benchmark fit assessment
    - Active share and portfolio differentiation
    - Benchmark timing and availability considerations
```

## Portfolio Analytics and Optimization

### 1. Modern Portfolio Theory Implementation

**Mean-Variance Optimization:**
```python
import numpy as np
from scipy.optimize import minimize
import cvxpy as cp

def mean_variance_optimization(expected_returns, covariance_matrix, risk_aversion):
    """
    Implement mean-variance optimization with risk aversion parameter
    """
    n_assets = len(expected_returns)
    
    # Decision variables
    weights = cp.Variable(n_assets)
    
    # Expected portfolio return
    portfolio_return = expected_returns.T @ weights
    
    # Portfolio variance
    portfolio_variance = cp.quad_form(weights, covariance_matrix)
    
    # Objective: maximize return minus risk penalty
    objective = cp.Maximize(portfolio_return - 0.5 * risk_aversion * portfolio_variance)
    
    # Constraints
    constraints = [
        cp.sum(weights) == 1,  # Weights sum to 1
        weights >= 0  # Long-only constraint
    ]
    
    # Solve optimization problem
    problem = cp.Problem(objective, constraints)
    problem.solve()
    
    return {
        'optimal_weights': weights.value,
        'expected_return': portfolio_return.value,
        'portfolio_volatility': np.sqrt(portfolio_variance.value),
        'sharpe_ratio': portfolio_return.value / np.sqrt(portfolio_variance.value)
    }
```

**Risk Budgeting Framework:**
```yaml
Equal Risk Contribution:
  Risk Parity Implementation:
    - Risk contribution calculation and decomposition
    - Equal risk contribution optimization
    - Volatility target and leverage determination
    - Rebalancing frequency and transaction costs
    - Performance evaluation and risk parity metrics
  
  Risk Budgeting Approaches:
    - Active risk budgeting and allocation
    - Factor risk budgeting and exposure limits
    - Tracking error budgeting and optimization
    - Downside risk budgeting and tail risk allocation
    - Custom risk budgeting and client-specific objectives
  
  Implementation Challenges:
    - Estimation error and parameter uncertainty
    - Transaction costs and rebalancing frequency
    - Concentration limits and diversification requirements
    - Liquidity constraints and capacity limitations
    - Tax implications and after-tax optimization
```

### 2. Factor Models and Analysis

**Multi-Factor Model Construction:**
```python
import statsmodels.api as sm
from sklearn.decomposition import PCA

def factor_model_analysis(returns, factor_returns):
    """
    Perform multi-factor model analysis and decomposition
    """
    results = {}
    
    for asset in returns.columns:
        # Regression analysis
        y = returns[asset].dropna()
        X = factor_returns.loc[y.index]
        X = sm.add_constant(X)  # Add intercept
        
        model = sm.OLS(y, X).fit()
        
        results[asset] = {
            'alpha': model.params[0],
            'factor_loadings': model.params[1:].to_dict(),
            'r_squared': model.rsquared,
            'residual_volatility': np.sqrt(model.mse_resid),
            't_statistics': model.tvalues.to_dict(),
            'p_values': model.pvalues.to_dict()
        }
    
    return results

def principal_component_analysis(returns, n_components=5):
    """
    Perform PCA for factor extraction
    """
    pca = PCA(n_components=n_components)
    factor_loadings = pca.fit_transform(returns.T)
    
    return {
        'explained_variance_ratio': pca.explained_variance_ratio_,
        'cumulative_variance': pca.explained_variance_ratio_.cumsum(),
        'factor_loadings': factor_loadings,
        'principal_components': pca.components_
    }
```

**Style Analysis and Factor Exposure:**
```yaml
Factor Identification:
  Fundamental Factors:
    - Value, growth, momentum, and quality factors
    - Size factor and market capitalization effects
    - Profitability and investment factors
    - Low volatility and defensive factors
    - Dividend yield and income factors
  
  Macroeconomic Factors:
    - Interest rate sensitivity and duration risk
    - Inflation expectations and real rate exposure
    - Currency exposure and foreign exchange risk
    - Commodity price exposure and inflation hedging
    - Credit spread sensitivity and default risk
  
  Statistical Factors:
    - Principal component analysis and factor extraction
    - Independent component analysis (ICA)
    - Dynamic factor models and time-varying loadings
    - Regime-switching factor models
    - Machine learning factor identification
```

## Trading Strategy Analytics

### 1. Strategy Development and Backtesting

**Systematic Strategy Framework:**
```python
def backtest_strategy(prices, signals, transaction_costs=0.001):
    """
    Comprehensive strategy backtesting framework
    """
    # Calculate returns
    returns = prices.pct_change().dropna()
    
    # Apply signals with lag to avoid look-ahead bias
    positions = signals.shift(1).dropna()
    
    # Calculate strategy returns
    strategy_returns = (positions * returns).sum(axis=1)
    
    # Apply transaction costs
    position_changes = positions.diff().abs().sum(axis=1)
    transaction_cost_drag = position_changes * transaction_costs
    net_returns = strategy_returns - transaction_cost_drag
    
    # Performance metrics
    cumulative_return = (1 + net_returns).cumprod()
    total_return = cumulative_return.iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(net_returns)) - 1
    volatility = net_returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / volatility if volatility > 0 else 0
    
    # Drawdown analysis
    running_max = cumulative_return.cummax()
    drawdown = (cumulative_return - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'cumulative_returns': cumulative_return,
        'drawdown_series': drawdown
    }
```

**Strategy Validation Framework:**
```yaml
Robustness Testing:
  Out-of-Sample Testing:
    - Walk-forward analysis and expanding window
    - Cross-validation and time series splits
    - Monte Carlo permutation testing
    - Bootstrap confidence intervals
    - Regime analysis and strategy stability
  
  Parameter Sensitivity:
    - Parameter sweep and sensitivity analysis
    - Optimization bias and overfitting detection
    - Statistical significance testing
    - Economic significance evaluation
    - Stability across time periods and markets
  
  Transaction Cost Analysis:
    - Market impact modeling and estimation
    - Bid-ask spread and execution costs
    - Timing costs and opportunity costs
    - Implementation shortfall analysis
    - Capacity constraints and scalability
```

### 2. Risk Management and Position Sizing

**Dynamic Risk Management:**
```python
def kelly_criterion_sizing(win_rate, avg_win, avg_loss):
    """
    Calculate Kelly criterion optimal position size
    """
    if avg_loss == 0:
        return 0
    
    win_loss_ratio = avg_win / abs(avg_loss)
    kelly_fraction = win_rate - (1 - win_rate) / win_loss_ratio
    
    # Apply fractional Kelly for risk management
    fractional_kelly = max(0, kelly_fraction * 0.25)  # Quarter Kelly
    
    return fractional_kelly

def volatility_target_sizing(returns, target_vol=0.10, lookback=252):
    """
    Implement volatility targeting for position sizing
    """
    rolling_vol = returns.rolling(lookback).std() * np.sqrt(252)
    vol_scalar = target_vol / rolling_vol
    
    # Cap leverage and apply smoothing
    vol_scalar = vol_scalar.clip(0.1, 2.0)  # Limit between 10% and 200%
    vol_scalar = vol_scalar.fillna(1.0)
    
    return vol_scalar
```

**Risk Monitoring Framework:**
```yaml
Real-Time Risk Management:
  Position Risk Monitoring:
    - Portfolio-level risk measurement and limits
    - Individual position size and concentration limits
    - Sector and geographic exposure limits
    - Factor exposure and risk budget utilization
    - Correlation and diversification monitoring
  
  Dynamic Hedging:
    - Delta hedging for option positions
    - Beta hedging for market exposure
    - Currency hedging for foreign investments
    - Interest rate hedging for duration risk
    - Volatility hedging for gamma risk
  
  Stop-Loss and Risk Controls:
    - Fixed percentage stop-loss rules
    - Trailing stop-loss and profit protection
    - Volatility-adjusted stop-loss levels
    - Time-based exit rules and holding periods
    - Drawdown-based risk controls
```

## Performance Reporting and Communication

### 1. Client Reporting Framework

**Institutional Performance Reports:**
```yaml
Monthly Performance Summary:
  Executive Summary:
    - Performance highlights and attribution
    - Market commentary and positioning
    - Risk metrics and compliance status
    - Outlook and strategic positioning
  
  Detailed Analytics:
    - Benchmark comparison and relative performance
    - Risk-adjusted return metrics
    - Factor exposure and attribution analysis
    - Sector and security-level contribution
    - Transaction summary and cost analysis
  
  Risk Analysis:
    - Portfolio risk metrics and trends
    - Stress testing and scenario analysis
    - Liquidity analysis and capacity assessment
    - Correlation and diversification analysis
    - Compliance and limit monitoring
```

**Regulatory and Compliance Reporting:**
```yaml
Standard Compliance:
  GIPS Compliance:
    - Composite construction and maintenance
    - Performance calculation standards
    - Disclosure requirements and documentation
    - Verification and quality assurance
    - Record keeping and audit trail
  
  Risk Reporting:
    - Value at Risk and stress testing
    - Concentration and exposure reporting
    - Liquidity and redemption analysis
    - Market risk and sensitivity analysis
    - Operational risk and control assessment
```

This comprehensive financial metrics framework provides quantitative analysts with robust tools for measuring, analyzing, and reporting investment performance while maintaining the highest standards of accuracy and professional presentation.