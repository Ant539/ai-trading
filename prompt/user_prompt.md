It has been {minutes_elapsed} minutes since you started trading.

Below, we are providing you with a variety of state data, price data, and predictive signals so you can discover alpha. Below that is your current account information, value, performance, and holdings.

⚠️ CRITICAL: ALL OF THE PRICE OR SIGNAL DATA BELOW IS ORDERED: OLDEST → NEWEST

Timeframes note:
- Primary decision timeframe: 5-minute (5m)
- Micro-structure (entry refinement only, does NOT directly trigger buy/sell): 3-minute (3m)
- Filter timeframe: 15-minute (15m)
- Background context: 4-hour (4h)
- Unless otherwise stated in a section title, intraday series are provided at 5-minute intervals.

---

## CURRENT MARKET STATE FOR ALL COINS

### ALL BTC DATA

**Current Snapshot (5m primary):**
- current_price = {btc_price}
- 5m EMA20 (current) = {btc_ema20_5m_current}
- 5m EMA50 (current) = {btc_ema50_5m_current}
- 5m MACD(12,26,9) (current) = {btc_macd_5m_current}
- 5m MACD histogram (current) = {btc_macd_hist_5m_current}
- 5m RSI(14) (current) = {btc_rsi14_5m_current}
- 5m ATR(14) (current) = {btc_atr14_5m_current}
- 5m Volume (current) = {btc_volume_5m_current}
- 5m Volume average (N bars) = {btc_volume_5m_avg}
- 5m Volume ratio (current/avg) = {btc_volume_ratio_5m}

**Market Sentiment Indicators (from Futures Market):**
- Open Interest: Latest: {btc_oi_latest} | Average: {btc_oi_avg} | Deviation%: {btc_oi_deviation_pct}
- Funding Rate: {btc_funding_rate}
- Funding Rate persistence (consecutive 5m bars positive/negative): {btc_funding_rate_persist_5m_bars}

**Intraday Series (3-minute intervals, oldest → latest; micro-structure, entry refinement only):**
- Mid prices (3m): [{btc_prices_3m}]
- EMA20 (3m): [{btc_ema20_3m}]
- MACD(12,26,9) (3m): [{btc_macd_3m}]
- RSI(14) (3m): [{btc_rsi14_3m}]

**Filter timeframe (15m, current values only):**
- 15m EMA50 (current) = {btc_ema50_15m_current}
- 15m RSI(14) (current) = {btc_rsi14_15m_current}
- 15m ATR(14) (current) = {btc_atr14_15m_current}
- Optional 15m MACD histogram (current) = {btc_macd_hist_15m_current}

**Longer-term Context (4-hour timeframe):**
- 20-Period EMA (4h): {btc_ema20_4h} vs. 50-Period EMA (4h): {btc_ema50_4h}
- 3-Period ATR (4h): {btc_atr3_4h} vs. 14-Period ATR (4h): {btc_atr14_4h}
- Current Volume (4h): {btc_volume_current} vs. Average Volume (4h): {btc_volume_avg}
- MACD(12,26,9) indicators (4h, series): [{btc_macd_4h}]
- RSI(14) indicators (4h, series): [{btc_rsi14_4h}]

---

### ALL ETH DATA
(Same fields as BTC, replace btc_ with eth_)

---

### ALL SOL DATA
(Same fields as BTC, replace btc_ with sol_)

---

### ALL BNB DATA
(Same fields as BTC, replace btc_ with bnb_)

---

### ALL DOGE DATA
(Same fields as BTC, replace btc_ with doge_)
- Liquidity level tag (high/medium/low): {doge_liquidity_level}

---

### ALL XRP DATA
(Same fields as BTC, replace btc_ with xrp_)
- Liquidity level tag (high/medium/low): {xrp_liquidity_level}

---

## USAGE GUIDANCE FOR THE MODEL (for consistent decisions)

Triggering rules (use 5m as primary):
- Price must close above 5m EMA50 to consider long setups.
- 5m MACD histogram should be ≥ 0 and preferably expanding vs. previous bar.
- 5m RSI(14) should be within [40, 70] to avoid extreme overbought/oversold.
- 5m Volume ratio ≥ 1.2 indicates acceptable participation.
- Stop distance should be ≥ 0.8 × 5m ATR(14); ensure account risk ∈ [1%, 3%].
- Apply volatility override: if short-term volatility regime is elevated (e.g., 5m ATR(14) vs. its N-bar average rises ≥ 30%), cap high-conviction allocation to 35-40%.

Filter rules (15m & 4h):
- If 15m RSI(14) > 75 or 15m MACD histogram notably negative, lower confidence or skip trade.
- Use 4h EMA20/EMA50 alignment to gauge broader trend; reduce allocation when 4h shows downtrend or ATR is elevated.

Futures sentiment (OI & funding):
- Funding Rate absolute value > 0.02% and persistence ≥ 3 consecutive 5m bars may adjust confidence up/down.
- OI deviation beyond ±10% from average indicates crowding/deleveraging; use for confidence adjustment only, not direct triggers.

Micro-structure (3m):
- Use 3m data for entry refinement (e.g., optimize limit price or wait for minor pullback), but do NOT directly trigger buy/sell.

Minimum position size guidance (scaled for ~¥3000 account):
- Base threshold: ≥ ¥800 (≈ $110–130)
- Preferred threshold: ≥ ¥1500 (≈ $200)
- Rationale: Maintain fee/slippage efficiency and adequate stop distance; avoid positions below ¥800 unless necessary for diversification or strict risk control.
- Note: For significantly larger accounts, scale these thresholds proportionally to maintain similar cost efficiency.

---

## HERE IS YOUR ACCOUNT INFORMATION & PERFORMANCE

**Performance Metrics:**
- Current Total Return (percent): {return_pct}%
- Sharpe Ratio: {sharpe_ratio}

**Account Status:**
- Available Cash: ${cash_available}
- Current Account Value: ${account_value}
- Positions count (current): {positions_count_current}

**Current Asset Holdings & Performance:**

```python
[
  {
    'symbol': '{coin_symbol}',
    'quantity': {position_quantity},
    'entry_price': {entry_price},
    'average_entry_price_after_add_on': {avg_entry_after_add_on},
    'current_price': {current_price},
    'unrealized_pnl': {unrealized_pnl},
    'notional_usd': {notional_usd},
    'exit_plan': {
      'profit_target': {profit_target},
      'stop_loss': {stop_loss},
      'invalidation_condition': '{invalidation_condition}'
    },
    'original_trade_confidence': {confidence},
    'initial_risk_usd': {risk_usd},
    'add_on_used': {add_on_used},  # True/False
    'position_open_timestamp': '{position_open_ts}',
    'position_last_update_timestamp': '{position_last_update_ts}'
  },
  # ... additional holdings if any
]

If no open positions:
[]
```

---

Ensure that:
- Triggers are based on 5m data; 15m/4h act as filters; 3m only refines entries.
- Risk_usd is verified to be within 1-3% of account value.
- Volatility override is applied when short-term ATR regime is elevated.
- Respect positions cap (≤ 3 coins) and the minimum position size guidance above.
- Provide honest confidence scores and consistent exit plans.

Now, analyze the market data provided above and make your trading decision.

Return the decision as a valid JSON object (buy/sell/hold) according to the system specification.
