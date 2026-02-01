# Tutorial: Algorithm Development and Debugging in LEAN

**Project:** LEAN Energy Trading - Learning Exercise
**Purpose:** Learn algorithm development by building a simple strategy with debugging in both PyCharm and VS Code
**Prerequisites:** Phase 1 (PyCharm) and Phase 2 (VS Code) setup complete
**Estimated Time:** 2-3 hours (hands-on learning)

---

## Table of Contents

1. [Overview](#overview)
2. [Learning Objectives](#learning-objectives)
3. [Exercise 1: Understanding the POC Algorithm](#exercise-1-understanding-the-poc-algorithm)
4. [Exercise 2: Building Your First Custom Algorithm](#exercise-2-building-your-first-custom-algorithm)
5. [Exercise 3: Adding Risk Controls](#exercise-3-adding-risk-controls)
6. [Exercise 4: Debugging in PyCharm](#exercise-4-debugging-in-pycharm)
7. [Exercise 5: Debugging in VS Code](#exercise-5-debugging-in-vs-code)
8. [Exercise 6: Advanced Algorithm Logic](#exercise-6-advanced-algorithm-logic)
9. [Key Concepts Reference](#key-concepts-reference)
10. [Common Patterns and Best Practices](#common-patterns-and-best-practices)

---

## Overview

### What You'll Learn

This tutorial teaches **algorithmic trading fundamentals** using LEAN's event-driven architecture through hands-on exercises:

- ✅ **LEAN Architecture** - Event-driven execution model (Initialize → OnData → OnOrderEvent)
- ✅ **Algorithm Structure** - How to organize trading logic, state management, signals
- ✅ **Indicators** - Using technical indicators (SMA, RSI, Bollinger Bands)
- ✅ **Order Management** - Placing, tracking, and managing orders
- ✅ **Risk Controls** - Position sizing, stop losses, maximum drawdown limits
- ✅ **Debugging Workflow** - Step-through debugging, variable inspection, breakpoints
- ✅ **IDE Comparison** - PyCharm vs VS Code debugging techniques

### Approach

**Progressive Learning:**
1. **Understand** existing POC algorithm by debugging it
2. **Build** your own simple algorithm from scratch
3. **Enhance** with risk controls and advanced logic
4. **Debug** using both IDEs to understand workflow differences

**Hands-On Focus:**
- Each exercise includes step-by-step instructions
- Debugging checkpoints throughout
- Expected outputs documented
- Common mistakes highlighted

---

## Learning Objectives

By the end of this tutorial, you will be able to:

### Core Skills
- [ ] **Explain** LEAN's event-driven architecture and execution flow
- [ ] **Write** a basic trading algorithm from scratch in Python
- [ ] **Implement** entry and exit signals using technical indicators
- [ ] **Add** risk management controls (position limits, stop losses)
- [ ] **Debug** algorithms step-by-step in both PyCharm and VS Code
- [ ] **Inspect** variables and algorithm state during execution
- [ ] **Modify** strategy logic and observe behavior changes

### LEAN Concepts
- [ ] **Understand** Initialize() vs OnData() vs OnOrderEvent() lifecycle
- [ ] **Use** built-in indicators (SMA, RSI, MACD, Bollinger Bands)
- [ ] **Manage** portfolio state (positions, cash, invested status)
- [ ] **Track** algorithm performance (P&L, trades, statistics)
- [ ] **Handle** data subscriptions and resolution (Daily, Hourly, Minute)

### Debugging Skills
- [ ] **Set** breakpoints in algorithm code
- [ ] **Step through** code execution (F10, F11, F5)
- [ ] **Inspect** variables during runtime
- [ ] **Compare** PyCharm vs VS Code debugging workflows
- [ ] **Troubleshoot** algorithm errors and unexpected behavior

---

## Exercise 1: Understanding the POC Algorithm

**Goal:** Learn LEAN's structure by debugging the existing SimpleMovingAveragePOC algorithm.

### Step 1.1: Review the Algorithm Code

**Open:** `strategies_basic/lean_poc_orderbook/SimpleMovingAveragePOC.py`

**Key Sections to Understand:**

```python
class SimpleMovingAveragePOC(QCAlgorithm):

    def initialize(self):
        """Called ONCE at backtest start"""
        # 1. Set time period
        # 2. Subscribe to data
        # 3. Create indicators
        # 4. Initialize state

    def on_data(self, data):
        """Called for EACH new bar of data"""
        # 1. Check if ready (indicators warmed up)
        # 2. Get current values
        # 3. Generate signals
        # 4. Execute trades

    def on_order_event(self, order_event):
        """Called when order status changes"""
        # 1. Log order fills
        # 2. Track execution

    def on_end_of_algorithm(self):
        """Called ONCE at backtest end"""
        # 1. Final statistics
        # 2. Summary logging
```

**Questions to Answer (write down your answers):**

1. What are the three main event handlers and when are they called?
2. How does the algorithm determine when to enter a long position?
3. Why does it check `if not self.sma_slow.is_ready`?
4. What does `self.set_holdings(self.symbol, 1.0)` do?
5. How does the algorithm exit positions?

---

### Step 1.2: Debug in PyCharm (Understanding Flow)

**Configure PyCharm Debugging:**

1. Edit `Launcher/config.json`:
   ```json
   {
     "algorithm-type-name": "SimpleMovingAveragePOC",
     "algorithm-language": "Python",
     "algorithm-location": "../../../strategies_basic/lean_poc_orderbook/SimpleMovingAveragePOC.py",
     "debugging": true,
     "debugging-method": "PyCharm"
   }
   ```

2. Copy to build directory:
   ```cmd
   copy Launcher\config.json Launcher\bin\Debug\config.json
   ```

**Set Breakpoints:**

Set breakpoints at these key lines:

- [ ] Line 44: `def initialize(self):` - Algorithm initialization
- [ ] Line 80: `def on_data(self, data):` - Every data event
- [ ] Line 90: `if not self.sma_slow.is_ready:` - Indicator warmup check
- [ ] Line 113: `if fast_value > slow_value * (1 + tolerance):` - Long entry signal
- [ ] Line 120: `if fast_value < slow_value:` - Exit signal
- [ ] Line 133: `if order_event.status == OrderStatus.FILLED:` - Order filled

**Debug Workflow:**

1. **Start PyCharm Debug Server** (Shift+F9)
2. **Run LEAN** in command prompt:
   ```cmd
   cd C:\Projects\LEAN\Launcher\bin\Debug
   dotnet QuantConnect.Lean.Launcher.dll
   ```
3. **Execution pauses at** `initialize()` breakpoint

**Inspection Checklist:**

At each breakpoint, inspect these variables:

**At `initialize()` breakpoint:**
- [ ] Inspect `self.start_date` and `self.end_date`
- [ ] Inspect `self.symbol` - should show SPY
- [ ] Inspect `self.sma_fast` and `self.sma_slow` objects
- [ ] Press **F10** (Step Over) through each line of initialize()
- [ ] Press **F5** (Continue) to next breakpoint

**At first `on_data()` call:**
- [ ] Inspect `data` object - what data is available?
- [ ] Inspect `self.sma_slow.is_ready` - should be `False` initially
- [ ] Press **F5** to continue (will hit this breakpoint many times)

**After ~30 iterations (SMA warmed up):**
- [ ] Inspect `self.sma_slow.is_ready` - now `True`
- [ ] Inspect `fast_value` and `slow_value` - compare values
- [ ] Inspect `self.portfolio[self.symbol].quantity` - check position
- [ ] Inspect `holdings` variable

**At long entry signal:**
- [ ] Inspect `fast_value` vs `slow_value` - fast should be greater
- [ ] Press **F10** to step into `self.set_holdings()` call
- [ ] After execution, inspect `self.portfolio.invested` - should be `True`

**At `on_order_event()` with FILLED status:**
- [ ] Inspect `order_event.fill_price`
- [ ] Inspect `order_event.order_id`
- [ ] Inspect `self.portfolio.total_portfolio_value`

**Key Learning:**
- Notice how many times `on_data()` is called vs `initialize()` (once)
- Observe indicator values gradually converging
- See portfolio state change after orders execute

---

### Step 1.3: Debug in VS Code (Same Algorithm)

**Configure VS Code Debugging:**

1. Edit `Launcher/config.json` (same as PyCharm but different debug method):
   ```json
   {
     "debugging": true,
     "debugging-method": "DebugPy"
   }
   ```

2. Copy to build directory:
   ```cmd
   copy Launcher\config.json Launcher\bin\Debug\config.json
   ```

**Set Breakpoints** (same locations as PyCharm):
- Line 44, 80, 90, 113, 120, 133

**Debug Workflow (different from PyCharm!):**

1. **Run LEAN FIRST** (order matters for VS Code!):
   ```cmd
   cd C:\Projects\LEAN\Launcher\bin\Debug
   dotnet QuantConnect.Lean.Launcher.dll
   ```
   - LEAN outputs: "waiting for debugger to attach at localhost:5678..."

2. **Attach VS Code Debugger** (within 10 seconds):
   - Open Debug panel (Ctrl+Shift+D)
   - Select "Attach to Python"
   - Press F5
   - VS Code connects to running LEAN process

3. **Execution resumes** and pauses at first breakpoint

**Inspection (same as PyCharm):**
- Use same inspection checklist as Step 1.2
- Note: VS Code uses F10 (Step Over), F11 (Step Into), F5 (Continue)
- Variables panel on left shows all local variables
- Watch panel allows adding custom expressions

**Comparison Notes:**

| Aspect | PyCharm | VS Code |
|--------|---------|---------|
| **Workflow** | Start server first, then run LEAN | Run LEAN first, then attach |
| **Port** | 6000 | 5678 |
| **Method** | `"PyCharm"` | `"DebugPy"` |
| **Step Over** | F8 | F10 |
| **Step Into** | F7 | F11 |
| **Continue** | F9 | F5 |

---

### Step 1.4: Document Your Observations

Create a file: `C:\Projects\LEAN\my_notes\exercise1_observations.md`

Answer these questions based on debugging:

```markdown
# Exercise 1 Observations

## Algorithm Flow
1. How many times did `on_data()` execute during the backtest?
   - Answer:

2. How many times did `on_order_event()` execute?
   - Answer:

3. What was the final portfolio value?
   - Answer:

## Indicator Behavior
4. How many bars did it take for `sma_slow` to become ready?
   - Answer: (should be 30)

5. What were the SMA values at the first long entry?
   - Fast SMA:
   - Slow SMA:

## PyCharm vs VS Code
6. Which IDE did you find easier for debugging? Why?
   - Answer:

7. Which keyboard shortcuts felt more natural?
   - Answer:

## Algorithm Logic
8. What would happen if you changed the tolerance from 0.00015 to 0.01?
   - Hypothesis:

9. What would happen if you used faster SMAs (5/15 instead of 10/30)?
   - Hypothesis:
```

---

## Exercise 2: Building Your First Custom Algorithm

**Goal:** Write a simple RSI-based mean reversion algorithm from scratch.

### Step 2.1: Create New Algorithm File

**Location:** `Algorithm.Python/MyRsiStrategy.py`

**Create the file with this template:**

```python
from AlgorithmImports import *

class MyRsiStrategy(QCAlgorithm):
    """
    My First Custom Algorithm: RSI Mean Reversion

    Strategy Logic:
    - Buy when RSI < 30 (oversold)
    - Sell when RSI > 70 (overbought)

    Learning Goals:
    - Understand algorithm structure
    - Use RSI indicator
    - Implement entry/exit logic
    """

    def initialize(self):
        """Setup algorithm parameters"""
        # TODO: Implement initialization
        pass

    def on_data(self, data):
        """Main trading logic"""
        # TODO: Implement trading logic
        pass
```

---

### Step 2.2: Implement Initialize Method

Fill in the `initialize()` method:

```python
def initialize(self):
    """Setup algorithm parameters"""
    # 1. Set backtest period
    self.set_start_date(2023, 1, 1)
    self.set_end_date(2023, 6, 30)  # 6 months

    # 2. Set starting capital
    self.set_cash(100000)

    # 3. Add equity data subscription
    self.symbol = self.add_equity("SPY", Resolution.DAILY).symbol

    # 4. Create RSI indicator (14-period standard)
    self.rsi = self.rsi(self.symbol, 14, Resolution.DAILY)

    # 5. Track state
    self.previous_date = None

    # 6. Log initialization
    self.log(f"MyRsiStrategy Initialized")
    self.log(f"Symbol: {self.symbol}")
    self.log(f"RSI Period: 14")
    self.log(f"Capital: ${self.portfolio.cash:,.0f}")
```

**Debug Checkpoint 1:**

- [ ] Set breakpoint at line 1 of `initialize()`
- [ ] Run algorithm and verify all variables initialize correctly
- [ ] Inspect `self.rsi` object - should show RSI indicator
- [ ] Inspect `self.symbol` - should show SPY symbol

---

### Step 2.3: Implement Trading Logic

Fill in the `on_data()` method:

```python
def on_data(self, data):
    """Main trading logic"""
    # 1. Wait for RSI to be ready (needs 14 bars)
    if not self.rsi.is_ready:
        return

    # 2. Trade once per day
    if self.previous_date is not None and self.previous_date == self.time.date():
        return
    self.previous_date = self.time.date()

    # 3. Get current RSI value
    rsi_value = self.rsi.current.value

    # 4. Check current position
    holdings = self.portfolio[self.symbol].quantity

    # 5. Entry logic: Buy when oversold (RSI < 30)
    if holdings == 0 and rsi_value < 30:
        self.set_holdings(self.symbol, 1.0)  # Go 100% long
        self.log(f"BUY: RSI = {rsi_value:.2f} (oversold)")

    # 6. Exit logic: Sell when overbought (RSI > 70)
    elif holdings > 0 and rsi_value > 70:
        self.liquidate(self.symbol)
        self.log(f"SELL: RSI = {rsi_value:.2f} (overbought)")
```

**Debug Checkpoint 2:**

- [ ] Set breakpoint at line 1 of `on_data()`
- [ ] Run and observe RSI values over time
- [ ] Inspect `rsi_value` when it drops below 30
- [ ] Step through the buy logic line by line (F10)
- [ ] Verify `holdings` changes after `set_holdings()` call

---

### Step 2.4: Run and Test

**Update config.json:**

```json
{
  "algorithm-type-name": "MyRsiStrategy",
  "algorithm-language": "Python",
  "algorithm-location": "../../../Algorithm.Python/MyRsiStrategy.py",
  "debugging": false
}
```

**Run without debugging first:**

```cmd
cd C:\Projects\LEAN\Launcher\bin\Debug
dotnet QuantConnect.Lean.Launcher.dll
```

**Expected Output:**
- Algorithm should execute successfully
- Should see BUY and SELL log messages
- Results panel shows statistics

**Questions to Answer:**

1. How many trades did your algorithm make?
2. What was the final return percentage?
3. What was the maximum drawdown?
4. On what dates did trades occur?

---

### Step 2.5: Experiment with Parameters

Try these modifications and observe results:

**Experiment 1: Change RSI Thresholds**

```python
# Original: Buy < 30, Sell > 70
# Try: Buy < 40, Sell > 60 (wider range)

if holdings == 0 and rsi_value < 40:  # Changed
    self.set_holdings(self.symbol, 1.0)

elif holdings > 0 and rsi_value > 60:  # Changed
    self.liquidate(self.symbol)
```

**Result:** More trades? Better/worse performance?

**Experiment 2: Change RSI Period**

```python
# Original: 14-period RSI
# Try: 7-period RSI (more sensitive)

self.rsi = self.rsi(self.symbol, 7, Resolution.DAILY)
```

**Result:** How does faster RSI affect signals?

**Experiment 3: Partial Position Sizing**

```python
# Original: 100% position
# Try: 50% position for better risk management

if holdings == 0 and rsi_value < 30:
    self.set_holdings(self.symbol, 0.5)  # Only 50% of capital
```

**Result:** Lower returns but safer?

---

## Exercise 3: Adding Risk Controls

**Goal:** Add professional risk management to your algorithm.

### Step 3.1: Add Position Size Limit

Modify `initialize()` to add maximum position size:

```python
def initialize(self):
    # ... existing code ...

    # Risk management parameters
    self.max_position_size = 0.5  # Max 50% of portfolio in single position
    self.max_total_invested = 0.8  # Max 80% of portfolio invested
```

Modify `on_data()` to use position limit:

```python
def on_data(self, data):
    # ... existing code ...

    # Entry logic with position limit
    if holdings == 0 and rsi_value < 30:
        # Calculate available capital
        available_buying_power = self.portfolio.cash * self.max_position_size
        target_quantity = int(available_buying_power / self.securities[self.symbol].price)

        # Place market order instead of set_holdings
        if target_quantity > 0:
            self.market_order(self.symbol, target_quantity)
            self.log(f"BUY {target_quantity} shares: RSI = {rsi_value:.2f}")
```

**Debug Checkpoint 3:**

- [ ] Set breakpoint at position size calculation
- [ ] Inspect `available_buying_power`
- [ ] Inspect `target_quantity`
- [ ] Verify quantity doesn't exceed limits

---

### Step 3.2: Add Stop Loss

Add stop loss tracking to `initialize()`:

```python
def initialize(self):
    # ... existing code ...

    # Stop loss parameters
    self.stop_loss_percentage = 0.05  # 5% stop loss
    self.entry_price = None  # Track entry price
```

Add stop loss check to `on_data()`:

```python
def on_data(self, data):
    # ... existing code ...

    # Stop loss check (BEFORE entry/exit logic)
    if holdings > 0 and self.entry_price is not None:
        current_price = self.securities[self.symbol].price
        loss_pct = (self.entry_price - current_price) / self.entry_price

        if loss_pct > self.stop_loss_percentage:
            self.liquidate(self.symbol)
            self.log(f"STOP LOSS: Entry ${self.entry_price:.2f}, Current ${current_price:.2f}, Loss {loss_pct*100:.1f}%")
            self.entry_price = None
            return  # Exit early, don't check other signals

    # Entry logic (track entry price when buying)
    if holdings == 0 and rsi_value < 30:
        # ... existing buy logic ...
        self.entry_price = self.securities[self.symbol].price  # Track entry
```

**Debug Checkpoint 4:**

- [ ] Set breakpoint at stop loss check
- [ ] Manually test by setting low `stop_loss_percentage` (e.g., 0.01)
- [ ] Verify stop loss triggers correctly
- [ ] Inspect `loss_pct` calculation

---

### Step 3.3: Add Maximum Drawdown Circuit Breaker

Add drawdown tracking to `initialize()`:

```python
def initialize(self):
    # ... existing code ...

    # Drawdown circuit breaker
    self.max_drawdown_limit = 0.10  # Quit if down 10%
    self.peak_portfolio_value = self.portfolio.total_portfolio_value
```

Add drawdown check to `on_data()`:

```python
def on_data(self, data):
    # Circuit breaker check (FIRST thing in on_data)
    current_value = self.portfolio.total_portfolio_value

    # Track peak
    if current_value > self.peak_portfolio_value:
        self.peak_portfolio_value = current_value

    # Calculate drawdown
    drawdown = (self.peak_portfolio_value - current_value) / self.peak_portfolio_value

    # Circuit breaker triggered
    if drawdown > self.max_drawdown_limit:
        self.liquidate()  # Close all positions
        self.quit(f"CIRCUIT BREAKER: Max drawdown {drawdown*100:.1f}% exceeded limit {self.max_drawdown_limit*100:.1f}%")
        return

    # ... rest of trading logic ...
```

**Debug Checkpoint 5:**

- [ ] Set breakpoint at circuit breaker check
- [ ] Inspect `drawdown` calculation each day
- [ ] Test by setting low limit (e.g., 0.02) to trigger artificially
- [ ] Verify algorithm quits when triggered

---

## Exercise 4: Debugging in PyCharm (Advanced)

**Goal:** Master advanced PyCharm debugging techniques.

### Step 4.1: Conditional Breakpoints

**Scenario:** You want to pause execution only when RSI drops below 25 (rare event).

**Setup:**

1. Set breakpoint at line with RSI check: `if rsi_value < 30:`
2. **Right-click breakpoint** → **Edit Breakpoint**
3. Add condition: `rsi_value < 25`
4. Check **"Condition"** checkbox
5. Click **Done**

**Result:** Debugger only pauses when condition is true.

**Exercise:**
- [ ] Set conditional breakpoint for `rsi_value < 25`
- [ ] Run algorithm and see it pause only at extreme oversold
- [ ] Inspect variables at this rare condition

---

### Step 4.2: Watch Expressions

**Scenario:** Track calculated values without adding print statements.

**Setup:**

1. Run algorithm in debug mode
2. Pause at any breakpoint
3. Right-click variable → **Add to Watches**
4. Or manually add expression in Watch panel:
   - `self.portfolio.total_portfolio_value`
   - `(self.portfolio.total_portfolio_value / 100000 - 1) * 100`  (return %)
   - `len(self.transactions.orders)`  (order count)

**Result:** Watched expressions update as you step through code.

**Exercise:**
- [ ] Add watch for portfolio value
- [ ] Add watch for custom return % calculation
- [ ] Step through 10 iterations and observe values change

---

### Step 4.3: Evaluate Expression (Live Calculations)

**Scenario:** Test a calculation without modifying code.

**Setup:**

1. Pause at breakpoint
2. Press **Alt+F8** (Evaluate Expression)
3. Enter Python expression:
   ```python
   self.rsi.current.value * 1.1  # What if RSI was 10% higher?
   ```
4. Press **Evaluate**

**Result:** See result without running algorithm again.

**Exercise:**
- [ ] Evaluate different RSI thresholds
- [ ] Calculate hypothetical position sizes
- [ ] Test indicator calculations

---

### Step 4.4: Drop to Frame (Re-run Code)

**Scenario:** You stepped past a line you wanted to inspect.

**Setup:**

1. Pause at breakpoint
2. Call stack panel shows function frames
3. **Right-click** previous frame → **Drop Frame**

**Result:** Execution rewinds to start of that function.

**Warning:** Only rewinds execution pointer, doesn't undo state changes!

---

## Exercise 5: Debugging in VS Code (Advanced)

**Goal:** Master VS Code debugging features.

### Step 5.1: Logpoints (Debug without Stopping)

**Scenario:** Log values without pausing execution.

**Setup:**

1. **Right-click** in left margin (where breakpoint would be)
2. Select **"Add Logpoint"**
3. Enter message: `RSI Value: {rsi_value}`
4. Press Enter

**Result:** Logs message to Debug Console without pausing.

**Exercise:**
- [ ] Add logpoint for RSI value in `on_data()`
- [ ] Run algorithm and watch Debug Console
- [ ] See RSI values stream without pausing

---

### Step 5.2: Debug Console REPL

**Scenario:** Execute Python code in current context.

**Setup:**

1. Pause at any breakpoint
2. Open **Debug Console** (Ctrl+Shift+Y)
3. Type Python expressions:
   ```python
   >>> self.rsi.current.value
   45.23
   >>> self.portfolio.invested
   True
   ```

**Result:** Interactive Python REPL in algorithm context.

**Exercise:**
- [ ] Query indicator values
- [ ] Check portfolio state
- [ ] Test calculations interactively

---

### Step 5.3: Data Breakpoints (Watch Variable Changes)

**Scenario:** Pause when a variable changes value.

**Setup:**

1. Pause at breakpoint
2. Variables panel → **Right-click variable** → **Break on Value Change**

**Result:** Debugger pauses whenever that variable changes.

**Exercise:**
- [ ] Set data breakpoint on `self.entry_price`
- [ ] Continue execution
- [ ] Pause automatically when entry_price changes

---

## Exercise 6: Advanced Algorithm Logic

**Goal:** Implement a multi-indicator strategy.

### Step 6.1: Combine RSI + Moving Average

Create new algorithm: `Algorithm.Python/MyComboStrategy.py`

```python
from AlgorithmImports import *

class MyComboStrategy(QCAlgorithm):
    """
    Advanced Strategy: RSI + SMA Combination

    Entry Rules:
    - RSI < 30 (oversold) AND
    - Price > 50-day SMA (uptrend)

    Exit Rules:
    - RSI > 70 (overbought) OR
    - Price < 50-day SMA (trend break)
    """

    def initialize(self):
        self.set_start_date(2023, 1, 1)
        self.set_end_date(2023, 12, 31)
        self.set_cash(100000)

        self.symbol = self.add_equity("SPY", Resolution.DAILY).symbol

        # Multiple indicators
        self.rsi = self.rsi(self.symbol, 14, Resolution.DAILY)
        self.sma = self.sma(self.symbol, 50, Resolution.DAILY)

        self.previous_date = None

    def on_data(self, data):
        # Wait for both indicators
        if not self.rsi.is_ready or not self.sma.is_ready:
            return

        if self.previous_date == self.time.date():
            return
        self.previous_date = self.time.date()

        rsi_value = self.rsi.current.value
        sma_value = self.sma.current.value
        price = self.securities[self.symbol].price
        holdings = self.portfolio[self.symbol].quantity

        # Entry: RSI oversold AND price above SMA (uptrend)
        if holdings == 0:
            if rsi_value < 30 and price > sma_value:
                self.set_holdings(self.symbol, 1.0)
                self.log(f"BUY: RSI={rsi_value:.1f}, Price=${price:.2f} > SMA=${sma_value:.2f}")

        # Exit: RSI overbought OR price below SMA (trend break)
        elif holdings > 0:
            if rsi_value > 70 or price < sma_value:
                self.liquidate(self.symbol)
                reason = "RSI overbought" if rsi_value > 70 else "SMA trend break"
                self.log(f"SELL ({reason}): RSI={rsi_value:.1f}, Price=${price:.2f} vs SMA=${sma_value:.2f}")
```

**Debug Challenge:**

- [ ] Set breakpoints at entry and exit conditions
- [ ] Inspect why certain signals trigger (RSI vs SMA)
- [ ] Compare performance to single-indicator strategy

---

### Step 6.2: Add Bollinger Bands

Enhance algorithm with Bollinger Bands:

```python
def initialize(self):
    # ... existing code ...

    # Add Bollinger Bands
    self.bb = self.bb(self.symbol, 20, 2, Resolution.DAILY)

def on_data(self, data):
    # ... existing code ...

    # Get Bollinger Band values
    bb_upper = self.bb.upper_band.current.value
    bb_middle = self.bb.middle_band.current.value
    bb_lower = self.bb.lower_band.current.value

    # Enhanced entry: Price near lower band (support)
    if holdings == 0:
        if rsi_value < 30 and price > sma_value and price < bb_lower * 1.02:
            # Price within 2% of lower Bollinger Band
            self.set_holdings(self.symbol, 1.0)
```

**Debug Exercise:**

- [ ] Inspect Bollinger Band values during entry signals
- [ ] Visualize how price relates to bands
- [ ] Test different standard deviations (1.5 vs 2.0)

---

## Key Concepts Reference

### LEAN Event Lifecycle

```
Algorithm Start
    ↓
Initialize() ← Called ONCE
    ↓
┌─────────────────────────┐
│  OnData(slice)          │ ← Called for EVERY bar
│    ├─ Check signals     │
│    ├─ Place orders      │
│    └─ Manage positions  │
└─────────────────────────┘
    ↓ (when order status changes)
OnOrderEvent(orderEvent)  ← Called on order updates
    ↓ (backtest end)
OnEndOfAlgorithm()        ← Called ONCE
```

### Indicator Ready State

```python
# Indicators need warmup period
self.sma = self.sma(self.symbol, 50, Resolution.DAILY)

# Not ready for first 49 bars (need 50 data points)
if not self.sma.is_ready:
    return  # Skip trading logic

# After 50 bars, indicator is ready
sma_value = self.sma.current.value
```

### Portfolio State

```python
# Check if invested
self.portfolio.invested  # True/False

# Check specific position
holdings = self.portfolio[self.symbol].quantity
holding_value = self.portfolio[self.symbol].holdings_value

# Portfolio totals
total_value = self.portfolio.total_portfolio_value
cash = self.portfolio.cash
```

### Order Methods

```python
# Method 1: Set target allocation (LEAN calculates quantity)
self.set_holdings(self.symbol, 0.5)  # 50% of portfolio

# Method 2: Market order (specific quantity)
self.market_order(self.symbol, 100)  # Buy 100 shares

# Method 3: Limit order (specify price)
self.limit_order(self.symbol, 100, limit_price)

# Method 4: Stop market order
self.stop_market_order(self.symbol, -100, stop_price)

# Exit all positions
self.liquidate(self.symbol)  # Specific symbol
self.liquidate()  # All positions
```

---

## Common Patterns and Best Practices

### Pattern 1: Once-Per-Day Trading

```python
def initialize(self):
    self.previous_date = None

def on_data(self, data):
    # Prevent multiple signals same day
    if self.previous_date == self.time.date():
        return
    self.previous_date = self.time.date()

    # ... trading logic ...
```

### Pattern 2: Indicator Warmup Check

```python
def on_data(self, data):
    # Always check indicator readiness
    if not self.indicator.is_ready:
        return

    # Safe to use indicator
    value = self.indicator.current.value
```

### Pattern 3: State-Based Trading

```python
def on_data(self, data):
    holdings = self.portfolio[self.symbol].quantity

    # Clear entry/exit separation
    if holdings == 0:
        # Entry logic
        if entry_signal:
            self.set_holdings(self.symbol, 1.0)

    elif holdings > 0:
        # Exit logic
        if exit_signal:
            self.liquidate(self.symbol)
```

### Pattern 4: Risk-First Checks

```python
def on_data(self, data):
    # Check risk controls BEFORE signals

    # 1. Circuit breaker
    if self.check_circuit_breaker():
        return

    # 2. Stop loss
    if self.check_stop_loss():
        return

    # 3. Position limits
    if self.at_position_limit():
        return

    # NOW check entry/exit signals
    # ... trading logic ...
```

### Pattern 5: Logging for Debugging

```python
def on_data(self, data):
    # Log key values for debugging
    self.debug(f"RSI: {rsi:.1f}, SMA: {sma:.2f}, Holdings: {holdings}")

    # Use appropriate log levels
    self.log("Important trade event")  # Normal
    self.debug("Detailed debugging info")  # Verbose
    self.error("Something went wrong")  # Errors
```

---

## Summary and Next Steps

### What You've Learned

✅ **LEAN Architecture**
- Event-driven model (Initialize, OnData, OnOrderEvent)
- Indicator lifecycle and warmup
- Portfolio management and state tracking

✅ **Algorithm Development**
- Built algorithms from scratch
- Implemented entry/exit signals
- Added risk management controls

✅ **Debugging Skills**
- Step-through debugging in both IDEs
- Breakpoints, watches, conditional breaks
- Variable inspection during runtime
- Compared PyCharm vs VS Code workflows

✅ **Best Practices**
- State-based trading logic
- Risk-first design
- Proper indicator handling
- Logging and debugging patterns

### Debugging Skills Summary

| Skill | PyCharm | VS Code |
|-------|---------|---------|
| **Basic Breakpoint** | Click margin | Click margin |
| **Conditional Break** | Right-click → Edit | Right-click → Edit |
| **Watch Variable** | Add to Watches | Variables panel |
| **Evaluate Expression** | Alt+F8 | Debug Console |
| **Logpoint** | - | Right-click → Add Logpoint |
| **Step Over** | F8 | F10 |
| **Step Into** | F7 | F11 |
| **Continue** | F9 | F5 |

### Your Algorithm Development Checklist

For future algorithms, use this checklist:

**Design Phase:**
- [ ] Define entry signals clearly
- [ ] Define exit signals clearly
- [ ] Plan risk controls (position size, stop loss, circuit breaker)
- [ ] Choose appropriate indicators
- [ ] Determine data resolution (Daily, Hourly, Minute)

**Implementation Phase:**
- [ ] Write `initialize()` with all parameters
- [ ] Implement indicator creation and warmup checks
- [ ] Code entry logic with position checks
- [ ] Code exit logic with position checks
- [ ] Add risk management (stops, limits, circuit breakers)
- [ ] Add logging for key events

**Testing Phase:**
- [ ] Run backtest without debugging first
- [ ] Review statistics and log output
- [ ] Debug with breakpoints to verify logic
- [ ] Test edge cases (first trade, last trade, max position)
- [ ] Experiment with parameter variations

**Debugging Checklist:**
- [ ] Set breakpoints at key decision points
- [ ] Inspect indicator values at signals
- [ ] Verify position state changes
- [ ] Check risk controls trigger correctly
- [ ] Use watch expressions for calculations

### Next Learning Path

**Option 1: Enhance Your Strategies**
- Add more sophisticated indicators (MACD, ADX, Stochastic)
- Implement multi-timeframe analysis
- Create portfolio strategies (multiple symbols)
- Add advanced risk controls (Kelly criterion, volatility sizing)

**Option 2: Move to Energy Markets (Tutorial 2)**
- Learn custom data integration
- Work with orderbook data (EPEX SPOT)
- Implement energy-specific strategies
- Handle continuous 24/7 markets

**Option 3: Optimize and Analyze**
- Parameter optimization
- Walk-forward analysis
- Monte Carlo simulation
- Statistical validation of strategy edge

---

## Appendix: Quick Command Reference

### PyCharm Debugging

```
Shift+F9        Start debug server (PyCharm method)
F8              Step Over
F7              Step Into
Shift+F8        Step Out
F9              Continue/Resume
Ctrl+F8         Toggle breakpoint
Alt+F8          Evaluate expression
Ctrl+Shift+F8   View breakpoints
```

### VS Code Debugging

```
F5              Start/Continue
F10             Step Over
F11             Step Into
Shift+F11       Step Out
F9              Toggle breakpoint
Ctrl+Shift+D    Open Debug panel
Ctrl+Shift+Y    Debug Console
```

### LEAN Configuration

```json
// PyCharm Debugging
{
  "debugging": true,
  "debugging-method": "PyCharm",
  "algorithm-location": "../../../Algorithm.Python/MyStrategy.py"
}

// VS Code Debugging
{
  "debugging": true,
  "debugging-method": "DebugPy",
  "algorithm-location": "../../../Algorithm.Python/MyStrategy.py"
}

// No Debugging (Fast Run)
{
  "debugging": false,
  "algorithm-location": "../../../Algorithm.Python/MyStrategy.py"
}
```

---

**Tutorial Complete!** You now have the skills to develop and debug algorithms in LEAN. Proceed to Tutorial 2 for energy market adaptation.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-16
**Author:** Claude (Systematic Trading Architect)
**Project:** LEAN Energy Trading Adaptation
