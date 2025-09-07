# Quant Analyst Technical Analysis

## Quantitative Technical Analysis Framework

### Systematic Technical Analysis Approach
**CRITICAL: Quantitative analyst implements rigorous, data-driven technical analysis that combines traditional chart patterns with statistical validation and systematic testing:**

1. **Statistical Technical Indicators**
   - Moving averages and trend-following systems
   - Momentum oscillators and mean reversion indicators
   - Volatility measures and regime detection
   - Volume analysis and market microstructure indicators
   - Pattern recognition and chart formation analysis

2. **Systematic Strategy Development**
   - Signal generation and filtering mechanisms
   - Entry and exit rule optimization
   - Risk management and position sizing
   - Portfolio-level technical analysis and sector rotation
   - Multi-timeframe analysis and confirmation systems

3. **Backtesting and Validation Framework**
   - Historical performance analysis and statistical significance
   - Out-of-sample testing and walk-forward validation
   - Transaction cost integration and realistic implementation
   - Risk-adjusted performance measurement and comparison
   - Robustness testing and parameter sensitivity analysis

## Core Technical Indicators and Implementation

### 1. Trend Analysis and Moving Averages

**Advanced Moving Average Systems:**
```python
import pandas as pd
import numpy as np
from scipy import stats
import talib

class TechnicalIndicators:
    def __init__(self, price_data):
        self.data = price_data.copy()
        self.indicators = {}
        
    def calculate_moving_averages(self, periods=[10, 20, 50, 200]):
        """Calculate multiple moving average types"""
        
        for period in periods:
            # Simple Moving Average
            self.data[f'SMA_{period}'] = self.data['close'].rolling(period).mean()
            
            # Exponential Moving Average
            self.data[f'EMA_{period}'] = self.data['close'].ewm(span=period).mean()
            
            # Weighted Moving Average
            weights = np.arange(1, period + 1)
            self.data[f'WMA_{period}'] = self.data['close'].rolling(period).apply(
                lambda x: np.dot(x, weights) / weights.sum(), raw=True
            )
            
            # Hull Moving Average (HMA)
            half_period = int(period / 2)
            sqrt_period = int(np.sqrt(period))
            
            wma_half = self.data['close'].rolling(half_period).apply(
                lambda x: np.dot(x, np.arange(1, len(x) + 1)) / np.sum(np.arange(1, len(x) + 1)), raw=True
            )
            wma_full = self.data['close'].rolling(period).apply(
                lambda x: np.dot(x, np.arange(1, len(x) + 1)) / np.sum(np.arange(1, len(x) + 1)), raw=True
            )
            hma_raw = (2 * wma_half - wma_full)
            self.data[f'HMA_{period}'] = hma_raw.rolling(sqrt_period).apply(
                lambda x: np.dot(x, np.arange(1, len(x) + 1)) / np.sum(np.arange(1, len(x) + 1)), raw=True
            )
        
        return self.data
    
    def calculate_trend_strength(self, ma_period=20):
        """Calculate trend strength and direction"""
        
        # ADX (Average Directional Index)
        self.data['ADX'] = talib.ADX(
            self.data['high'].values,
            self.data['low'].values, 
            self.data['close'].values,
            timeperiod=14
        )
        
        # Custom trend strength indicator
        price_changes = self.data['close'].pct_change()
        ma = self.data['close'].rolling(ma_period).mean()
        ma_slope = ma.pct_change(5)  # 5-day slope
        
        # Trend consistency (percentage of positive/negative moves)
        rolling_consistency = price_changes.rolling(ma_period).apply(
            lambda x: (x > 0).sum() / len(x) if len(x) > 0 else 0.5
        )
        
        self.data['trend_strength'] = (
            (abs(ma_slope) * 100) *  # Slope magnitude
            (2 * abs(rolling_consistency - 0.5))  # Consistency factor
        )
        
        self.data['trend_direction'] = np.where(ma_slope > 0, 1, -1)
        
        return self.data
```

**Adaptive Moving Averages:**
```python
def calculate_adaptive_ma(price_data, fast_period=2, slow_period=30):
    """
    Calculate Kaufman's Adaptive Moving Average (KAMA)
    """
    
    # Efficiency Ratio calculation
    change = abs(price_data - price_data.shift(10))
    volatility = abs(price_data - price_data.shift(1)).rolling(10).sum()
    efficiency_ratio = change / volatility
    
    # Smoothing constants
    fast_sc = 2 / (fast_period + 1)
    slow_sc = 2 / (slow_period + 1)
    
    # Adaptive smoothing constant
    smoothing_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2
    
    # Calculate KAMA
    kama = price_data.copy()
    for i in range(1, len(price_data)):
        if not pd.isna(smoothing_constant.iloc[i]):
            kama.iloc[i] = (
                kama.iloc[i-1] + 
                smoothing_constant.iloc[i] * (price_data.iloc[i] - kama.iloc[i-1])
            )
    
    return kama

def variable_ma(price_data, volatility_period=20):
    """
    Variable Moving Average based on volatility
    """
    # Calculate volatility
    returns = price_data.pct_change()
    volatility = returns.rolling(volatility_period).std()
    
    # Adaptive period based on volatility
    # Higher volatility = shorter period (faster adaptation)
    max_period = 50
    min_period = 5
    volatility_normalized = (volatility - volatility.min()) / (volatility.max() - volatility.min())
    adaptive_period = max_period - (volatility_normalized * (max_period - min_period))
    
    # Calculate variable MA
    vma = pd.Series(index=price_data.index, dtype=float)
    for i in range(len(price_data)):
        if i >= min_period and not pd.isna(adaptive_period.iloc[i]):
            period = int(adaptive_period.iloc[i])
            start_idx = max(0, i - period + 1)
            vma.iloc[i] = price_data.iloc[start_idx:i+1].mean()
    
    return vma
```

### 2. Momentum and Oscillator Analysis

**Comprehensive Momentum Framework:**
```python
class MomentumIndicators:
    def __init__(self, price_data):
        self.data = price_data.copy()
        
    def calculate_rsi_family(self, periods=[14, 21]):
        """Calculate RSI and related momentum oscillators"""
        
        for period in periods:
            # Standard RSI
            self.data[f'RSI_{period}'] = talib.RSI(
                self.data['close'].values, timeperiod=period
            )
            
            # Stochastic RSI
            rsi = self.data[f'RSI_{period}']
            rsi_min = rsi.rolling(period).min()
            rsi_max = rsi.rolling(period).max()
            self.data[f'StochRSI_{period}'] = (
                (rsi - rsi_min) / (rsi_max - rsi_min) * 100
            )
            
            # Connors RSI (combines RSI, streak, and rank components)
            # Streak component
            price_changes = self.data['close'].pct_change()
            streaks = self._calculate_streaks(price_changes > 0)
            streak_rsi = self._rsi_calculation(streaks, period)
            
            # Rank component  
            returns = self.data['close'].pct_change()
            rank_component = returns.rolling(period).apply(
                lambda x: stats.percentileofscore(x, x.iloc[-1])
            )
            
            # Combined Connors RSI
            connors_rsi = (rsi + streak_rsi + rank_component) / 3
            self.data[f'ConnorsRSI_{period}'] = connors_rsi
    
    def calculate_macd_family(self, fast=12, slow=26, signal=9):
        """Calculate MACD and variations"""
        
        # Standard MACD
        exp1 = self.data['close'].ewm(span=fast).mean()
        exp2 = self.data['close'].ewm(span=slow).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        self.data['MACD'] = macd
        self.data['MACD_signal'] = signal_line
        self.data['MACD_histogram'] = histogram
        
        # MACD-Histogram divergence
        price_peaks = self._find_peaks(self.data['close'])
        macd_peaks = self._find_peaks(histogram)
        self.data['MACD_divergence'] = self._calculate_divergence(
            price_peaks, macd_peaks
        )
        
        # Zero-lag MACD
        ema1 = self.data['close'].ewm(span=fast).mean()
        ema2 = self.data['close'].ewm(span=slow).mean()
        
        # Zero-lag calculation
        zl_ema1 = 2 * ema1 - ema1.ewm(span=fast).mean()
        zl_ema2 = 2 * ema2 - ema2.ewm(span=slow).mean()
        
        self.data['ZL_MACD'] = zl_ema1 - zl_ema2
        self.data['ZL_MACD_signal'] = self.data['ZL_MACD'].ewm(span=signal).mean()
    
    def calculate_stochastic_oscillators(self):
        """Calculate stochastic oscillators and variations"""
        
        # Standard Stochastic
        k_period = 14
        d_period = 3
        
        lowest_low = self.data['low'].rolling(k_period).min()
        highest_high = self.data['high'].rolling(k_period).max()
        
        k_percent = ((self.data['close'] - lowest_low) / 
                    (highest_high - lowest_low)) * 100
        
        self.data['Stoch_K'] = k_percent
        self.data['Stoch_D'] = k_percent.rolling(d_period).mean()
        
        # Slow Stochastic
        self.data['Slow_K'] = self.data['Stoch_D']
        self.data['Slow_D'] = self.data['Slow_K'].rolling(d_period).mean()
        
        # Williams %R
        self.data['Williams_R'] = (
            (highest_high - self.data['close']) / 
            (highest_high - lowest_low)
        ) * -100
    
    def _calculate_streaks(self, condition_series):
        """Calculate consecutive streak lengths"""
        streaks = []
        current_streak = 0
        
        for value in condition_series:
            if pd.isna(value):
                streaks.append(0)
                current_streak = 0
            elif value:
                current_streak += 1
                streaks.append(current_streak)
            else:
                current_streak = 0
                streaks.append(current_streak)
        
        return pd.Series(streaks, index=condition_series.index)
    
    def _rsi_calculation(self, series, period):
        """Custom RSI calculation for any series"""
        delta = series.diff()
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        avg_gains = gains.rolling(period).mean()
        avg_losses = losses.rolling(period).mean()
        
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
```

### 3. Volatility and Market Structure Analysis

**Advanced Volatility Indicators:**
```python
class VolatilityIndicators:
    def __init__(self, price_data):
        self.data = price_data.copy()
        
    def calculate_bollinger_bands(self, period=20, std_dev=2):
        """Calculate Bollinger Bands and related indicators"""
        
        # Standard Bollinger Bands
        sma = self.data['close'].rolling(period).mean()
        std = self.data['close'].rolling(period).std()
        
        self.data['BB_upper'] = sma + (std * std_dev)
        self.data['BB_lower'] = sma - (std * std_dev)
        self.data['BB_middle'] = sma
        
        # %B (Percent B)
        self.data['Percent_B'] = (
            (self.data['close'] - self.data['BB_lower']) / 
            (self.data['BB_upper'] - self.data['BB_lower'])
        )
        
        # Bandwidth
        self.data['BB_bandwidth'] = (
            (self.data['BB_upper'] - self.data['BB_lower']) / 
            self.data['BB_middle']
        ) * 100
        
        # Bollinger Band squeeze detection
        bb_squeeze_threshold = self.data['BB_bandwidth'].rolling(50).quantile(0.2)
        self.data['BB_squeeze'] = self.data['BB_bandwidth'] < bb_squeeze_threshold
        
        # Keltner Channels for squeeze confirmation
        tr = self._true_range()
        atr = tr.rolling(period).mean()
        ema = self.data['close'].ewm(span=period).mean()
        
        self.data['KC_upper'] = ema + (atr * 1.5)
        self.data['KC_lower'] = ema - (atr * 1.5)
        
        # Squeeze occurs when BB is inside KC
        self.data['Squeeze'] = (
            (self.data['BB_upper'] < self.data['KC_upper']) & 
            (self.data['BB_lower'] > self.data['KC_lower'])
        )
    
    def calculate_atr_indicators(self, period=14):
        """Calculate Average True Range and related indicators"""
        
        # True Range
        tr = self._true_range()
        
        # Average True Range
        self.data['ATR'] = tr.rolling(period).mean()
        
        # ATR Bands
        multiplier = 2
        self.data['ATR_upper'] = self.data['close'] + (self.data['ATR'] * multiplier)
        self.data['ATR_lower'] = self.data['close'] - (self.data['ATR'] * multiplier)
        
        # Volatility-adjusted position sizing
        self.data['Vol_Position_Size'] = 1 / (self.data['ATR'] / self.data['close'])
        
        # ATR trend
        self.data['ATR_trend'] = self.data['ATR'].pct_change(5)
        
        # Relative ATR (current ATR vs historical average)
        atr_ma = self.data['ATR'].rolling(50).mean()
        self.data['Relative_ATR'] = self.data['ATR'] / atr_ma
    
    def calculate_realized_volatility(self, window=20):
        """Calculate realized volatility measures"""
        
        # Log returns
        log_returns = np.log(self.data['close'] / self.data['close'].shift(1))
        
        # Realized volatility (annualized)
        self.data['Realized_Vol'] = (
            log_returns.rolling(window).std() * np.sqrt(252) * 100
        )
        
        # Parkinson volatility (high-low estimator)
        parkinson_vol = np.log(self.data['high'] / self.data['low']) ** 2
        self.data['Parkinson_Vol'] = (
            parkinson_vol.rolling(window).mean() * 
            (252 / (4 * np.log(2))) * 100
        ) ** 0.5
        
        # Garman-Klass volatility
        if all(col in self.data.columns for col in ['open', 'high', 'low', 'close']):
            ln_ho = np.log(self.data['high'] / self.data['open'])
            ln_hc = np.log(self.data['high'] / self.data['close'])
            ln_lo = np.log(self.data['low'] / self.data['open'])
            ln_lc = np.log(self.data['low'] / self.data['close'])
            
            gk_vol = ln_ho * ln_hc + ln_lo * ln_lc
            self.data['GK_Vol'] = (
                gk_vol.rolling(window).mean() * 252 * 100
            ) ** 0.5
    
    def _true_range(self):
        """Calculate True Range"""
        tr1 = self.data['high'] - self.data['low']
        tr2 = abs(self.data['high'] - self.data['close'].shift(1))
        tr3 = abs(self.data['low'] - self.data['close'].shift(1))
        
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return true_range
```

### 4. Pattern Recognition and Chart Analysis

**Automated Pattern Detection:**
```python
from scipy.signal import find_peaks, find_peaks_cwt
from scipy.stats import linregress

class PatternRecognition:
    def __init__(self, price_data):
        self.data = price_data.copy()
        self.patterns = {}
        
    def detect_support_resistance(self, window=20, min_touches=2):
        """Detect support and resistance levels"""
        
        # Find local minima and maxima
        highs = self.data['high'].rolling(window, center=True).max()
        lows = self.data['low'].rolling(window, center=True).min()
        
        # Identify peaks and troughs
        peaks = self.data['high'] == highs
        troughs = self.data['low'] == lows
        
        # Get peak and trough levels
        resistance_levels = self.data.loc[peaks, 'high'].values
        support_levels = self.data.loc[troughs, 'low'].values
        
        # Cluster similar levels
        def cluster_levels(levels, tolerance=0.01):
            if len(levels) == 0:
                return []
                
            clustered = []
            levels_sorted = np.sort(levels)
            
            current_cluster = [levels_sorted[0]]
            for level in levels_sorted[1:]:
                if (level - current_cluster[-1]) / current_cluster[-1] <= tolerance:
                    current_cluster.append(level)
                else:
                    if len(current_cluster) >= min_touches:
                        clustered.append(np.mean(current_cluster))
                    current_cluster = [level]
            
            if len(current_cluster) >= min_touches:
                clustered.append(np.mean(current_cluster))
            
            return clustered
        
        self.patterns['resistance_levels'] = cluster_levels(resistance_levels)
        self.patterns['support_levels'] = cluster_levels(support_levels)
        
        return self.patterns
    
    def detect_trend_lines(self, min_periods=10):
        """Detect trend lines and channels"""
        
        # Find significant peaks and troughs
        window = 10
        peaks_idx = find_peaks(self.data['high'], distance=window)[0]
        troughs_idx = find_peaks(-self.data['low'], distance=window)[0]
        
        # Get peak and trough data
        peaks_data = self.data.iloc[peaks_idx][['high']].reset_index()
        troughs_data = self.data.iloc[troughs_idx][['low']].reset_index()
        
        # Convert dates to numeric for regression
        peaks_data['date_num'] = pd.to_numeric(peaks_data.index)
        troughs_data['date_num'] = pd.to_numeric(troughs_data.index)
        
        # Fit trend lines
        if len(peaks_data) >= 2:
            # Resistance trend line
            slope, intercept, r_value, _, _ = linregress(
                peaks_data['date_num'], peaks_data['high']
            )
            self.patterns['resistance_trend'] = {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value**2,
                'points': len(peaks_data)
            }
        
        if len(troughs_data) >= 2:
            # Support trend line
            slope, intercept, r_value, _, _ = linregress(
                troughs_data['date_num'], troughs_data['low']
            )
            self.patterns['support_trend'] = {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value**2,
                'points': len(troughs_data)
            }
    
    def detect_chart_patterns(self):
        """Detect common chart patterns"""
        patterns_detected = []
        
        # Head and Shoulders pattern
        h_and_s = self._detect_head_and_shoulders()
        if h_and_s:
            patterns_detected.append(h_and_s)
        
        # Double Top/Bottom patterns
        double_patterns = self._detect_double_patterns()
        patterns_detected.extend(double_patterns)
        
        # Triangle patterns
        triangles = self._detect_triangles()
        patterns_detected.extend(triangles)
        
        self.patterns['chart_patterns'] = patterns_detected
        return patterns_detected
    
    def _detect_head_and_shoulders(self, window=5):
        """Detect Head and Shoulders pattern"""
        # Simplified implementation
        # Find three consecutive peaks where middle is highest
        
        peaks_idx = find_peaks(self.data['high'], distance=window)[0]
        
        for i in range(len(peaks_idx) - 2):
            left_peak = self.data['high'].iloc[peaks_idx[i]]
            head = self.data['high'].iloc[peaks_idx[i+1]]
            right_peak = self.data['high'].iloc[peaks_idx[i+2]]
            
            # Check if middle peak is highest
            if (head > left_peak and head > right_peak and 
                abs(left_peak - right_peak) / left_peak < 0.05):  # Shoulders similar height
                
                return {
                    'pattern': 'head_and_shoulders',
                    'head_date': self.data.index[peaks_idx[i+1]],
                    'head_price': head,
                    'left_shoulder': left_peak,
                    'right_shoulder': right_peak,
                    'confidence': min(head/left_peak, head/right_peak) - 1
                }
        
        return None
    
    def _detect_double_patterns(self):
        """Detect Double Top and Double Bottom patterns"""
        patterns = []
        
        # Double Top
        peaks_idx = find_peaks(self.data['high'], distance=10)[0]
        for i in range(len(peaks_idx) - 1):
            peak1 = self.data['high'].iloc[peaks_idx[i]]
            peak2 = self.data['high'].iloc[peaks_idx[i+1]]
            
            # Check if peaks are similar height
            if abs(peak1 - peak2) / peak1 < 0.02:
                patterns.append({
                    'pattern': 'double_top',
                    'peak1_date': self.data.index[peaks_idx[i]],
                    'peak2_date': self.data.index[peaks_idx[i+1]],
                    'peak1_price': peak1,
                    'peak2_price': peak2,
                    'confidence': 1 - abs(peak1 - peak2) / peak1
                })
        
        return patterns
    
    def _detect_triangles(self):
        """Detect triangle patterns (ascending, descending, symmetric)"""
        # Simplified triangle detection
        # Would require more sophisticated analysis of trend line convergence
        return []
```

## Strategy Development and Backtesting

### 1. Technical Strategy Framework

**Multi-Signal Strategy Development:**
```python
class TechnicalStrategy:
    def __init__(self, data):
        self.data = data.copy()
        self.signals = pd.DataFrame(index=data.index)
        self.positions = pd.DataFrame(index=data.index)
        self.performance = {}
        
    def generate_ma_crossover_signals(self, fast_period=10, slow_period=20):
        """Generate moving average crossover signals"""
        
        fast_ma = self.data['close'].rolling(fast_period).mean()
        slow_ma = self.data['close'].rolling(slow_period).mean()
        
        # Basic crossover signals
        self.signals['ma_signal'] = np.where(fast_ma > slow_ma, 1, -1)
        
        # Signal only on crossover (not continuous)
        ma_crossover = (fast_ma > slow_ma) != (fast_ma.shift(1) > slow_ma.shift(1))
        self.signals['ma_entry'] = np.where(
            ma_crossover & (fast_ma > slow_ma), 1,
            np.where(ma_crossover & (fast_ma < slow_ma), -1, 0)
        )
        
        return self.signals['ma_signal']
    
    def generate_mean_reversion_signals(self, lookback=20, threshold=2):
        """Generate mean reversion signals using z-score"""
        
        rolling_mean = self.data['close'].rolling(lookback).mean()
        rolling_std = self.data['close'].rolling(lookback).std()
        z_score = (self.data['close'] - rolling_mean) / rolling_std
        
        # Mean reversion signals
        self.signals['mr_signal'] = np.where(
            z_score > threshold, -1,  # Sell when overextended up
            np.where(z_score < -threshold, 1, 0)  # Buy when overextended down
        )
        
        return self.signals['mr_signal']
    
    def combine_signals(self, weights=None):
        """Combine multiple signals with optional weights"""
        
        if weights is None:
            weights = {col: 1.0 for col in self.signals.columns if '_signal' in col}
        
        # Weighted combination
        combined_signal = pd.Series(0, index=self.signals.index)
        total_weight = sum(weights.values())
        
        for signal_col, weight in weights.items():
            if signal_col in self.signals.columns:
                combined_signal += (self.signals[signal_col] * weight / total_weight)
        
        # Convert to discrete signals
        self.signals['combined'] = np.where(
            combined_signal > 0.5, 1,
            np.where(combined_signal < -0.5, -1, 0)
        )
        
        return self.signals['combined']
    
    def apply_filters(self, volume_filter=True, volatility_filter=True):
        """Apply filters to improve signal quality"""
        
        filtered_signals = self.signals.copy()
        
        if volume_filter:
            # Require above-average volume for signals
            avg_volume = self.data['volume'].rolling(50).mean()
            volume_condition = self.data['volume'] > avg_volume
            filtered_signals = filtered_signals.where(volume_condition, 0)
        
        if volatility_filter:
            # Avoid signals during very high volatility periods
            volatility = self.data['close'].pct_change().rolling(20).std()
            vol_threshold = volatility.quantile(0.8)
            vol_condition = volatility < vol_threshold
            filtered_signals = filtered_signals.where(vol_condition, 0)
        
        self.signals['filtered'] = filtered_signals.get('combined', 0)
        return self.signals['filtered']
```

This comprehensive technical analysis framework enables quantitative analysts to implement sophisticated, systematic approaches to technical analysis while maintaining rigorous statistical validation and robust backtesting procedures.