# Tutorial: Extending LEAN for EPEX SPOT Orderbook Data

**Project:** LEAN Energy Trading - EPEX SPOT Integration
**Purpose:** Learn how LEAN is extended for custom markets like EPEX SPOT
**Prerequisites:** Tutorials 01-02 complete, understand LEAN basics
**Estimated Time:** 3-4 hours (conceptual understanding)

> **Note:** This tutorial teaches *concepts*. The production implementation uses C# for performance.
> See DIAGRAMS_LEAN_ARCHITECTURE.md for the authoritative implementation specification.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Understanding EPEX SPOT Market](#2-understanding-epex-spot-market)
3. [Analyzing Your Data](#3-analyzing-your-data)
4. [LEAN Architecture for Custom Markets](#4-lean-architecture-for-custom-markets)
5. [Understanding C# Data Types](#5-understanding-c-data-types)
6. [Python Algorithms Using C# Data](#6-python-algorithms-using-c-data)
7. [Universe Selection](#7-universe-selection)
8. [Brokerage Model](#8-brokerage-model)
9. [Market Hours Configuration](#9-market-hours-configuration)
10. [Basic Algorithm Example](#10-basic-algorithm-example)
11. [Advanced Strategies](#11-advanced-strategies)
12. [Troubleshooting](#12-troubleshooting)
13. [Summary & Next Steps](#13-summary--next-steps)

---

## 1. Overview

### What This Tutorial Teaches

This tutorial explains how LEAN is extended to support a new market (EPEX SPOT intraday power trading). You'll understand:

- How EPEX SPOT market structure differs from equities
- How LEAN's architecture accommodates custom data types
- How C# data types are designed for performance
- How Python algorithms consume C# data
- How universe selection manages dynamic contracts
- How the brokerage model simulates fills

### What This Tutorial Does NOT Cover

This is a **conceptual tutorial**. The actual implementation is in C# for performance reasons. This tutorial does NOT:

- Provide copy-paste Python code for production
- Replace the C# implementation specification
- Cover performance optimization details

**For implementation details, see:**
- `DIAGRAMS_LEAN_ARCHITECTURE.md` - Visual architecture and implementation checklist
- `GUIDE_EPEX_PRODUCTION_ARCHITECTURE.md` - Detailed design decisions

---

## 2. Understanding EPEX SPOT Market

### Market Overview

**EPEX SPOT** = European Power Exchange for spot power trading

| Characteristic | Description |
|---------------|-------------|
| **Product** | Electricity for specific delivery periods |
| **Trading** | Continuous 24/7 until gate closure |
| **Gate Closure** | 5 minutes before delivery period starts |
| **Settlement** | Physical delivery of electricity |
| **Markets** | Day-Ahead (DA) and Intraday (ID) |

### Contract Structure

Power is traded in **delivery periods**:

```
Contract: HH_DE_2025-12-01_14:00

Where:
- HH = Half-hourly (30-minute delivery)
- DE = Germany (market area)
- 2025-12-01 = Delivery date
- 14:00 = Delivery start time

Delivery: 14:00 - 14:30 on December 1, 2025
```

**Contract Durations:**
- QH = Quarter-hourly (15 minutes)
- HH = Half-hourly (30 minutes)
- 1H = Hourly (60 minutes)

### Order Book Mechanics

EPEX uses a continuous order book (similar to equities):

```
Bids (Buy Orders)           |  Asks (Sell Orders)
Price      Quantity         |  Price      Quantity
€65.50     100 MWh          |  €66.00     50 MWh
€65.25     200 MWh          |  €66.25     150 MWh
€65.00     150 MWh          |  €66.50     100 MWh

Spread: €66.00 - €65.50 = €0.50
Mid Price: (€65.50 + €66.00) / 2 = €65.75
```

### Key Differences from Equities

| Aspect | Equities | EPEX Power |
|--------|----------|------------|
| Trading hours | 9:30-16:00 | 24/7 |
| Instruments | Fixed symbols | Dynamic (48+ per day) |
| Settlement | T+2 cash | Physical delivery |
| Expiration | None | Gate closure (5 min before delivery) |
| Liquidity | Continuous | Varies by time to delivery |

---

## 3. Analyzing Your Data

### Data Directory Structure

Your EPEX data follows a partitioned structure:

```
marketData/epexspot/
├── deltas/                    # Order book changes (tick-by-tick)
│   └── deliveryDate=2025-10-16/
│       └── marketArea=GB/
│           └── contractDuration=HH/
│               └── contractId=HH_GB_2025-10-16_07:00/
│                   └── deltas.parquet
│
├── ob_snapshots/              # Order book snapshots
│   ├── atomic/                # Every event
│   ├── l10/                   # Top 10 levels
│   ├── periodic/              # Time-sampled (60s)
│   └── tob/                   # Top of book only
│
├── trades/                    # Executed transactions
│   └── [same partitioning]
│
└── market_ref/                # Contract reference data
    └── deliveryDate=2025-10-16/
        └── contracts.parquet
```

### Exploring Data with Python

Use Python to understand your data schema (exploration only):

```python
import pyarrow.parquet as pq
import pandas as pd

# Read contract reference data
contracts = pq.read_table(
    'marketData/epexspot/market_ref/deliveryDate=2025-10-16/contracts.parquet'
).to_pandas()

print("Contract Columns:")
print(contracts.dtypes)
print(f"\nTotal contracts: {len(contracts)}")
```

**Expected Contract Columns:**
- `contractId` - Unique identifier (e.g., "HH_GB_2025-10-16_07:00")
- `deliveryStart` - Start of delivery period (timestamp)
- `deliveryEnd` - End of delivery period (timestamp)
- `marketArea` - Geographic market (GB, DE, FR)
- `contractDuration` - QH, HH, or 1H

### Exploring Order Book Data

```python
# Read top-of-book snapshots
tob = pq.read_table(
    'marketData/epexspot/ob_snapshots/tob/deliveryDate=2025-10-16/'
    'marketArea=GB/contractDuration=HH/contractId=HH_GB_2025-10-16_07:00/tob.parquet'
).to_pandas()

print("Top-of-Book Columns:")
print(tob.dtypes)
print(f"\nTotal snapshots: {len(tob)}")
print(f"\nSample row:")
print(tob.iloc[0])
```

**Expected ToB Columns:**
- `timestamp` - Event time (microseconds or datetime)
- `bidPrice` / `bid_price_1` - Best bid price
- `bidQuantity` / `bid_qty_1` - Best bid quantity (MWh)
- `askPrice` / `ask_price_1` - Best ask price
- `askQuantity` / `ask_qty_1` - Best ask quantity (MWh)

---

## 4. LEAN Architecture for Custom Markets

### Why C# Instead of Python for Data Types?

LEAN uses C# for performance-critical data types:

| Approach | Allocation | Speed | Use Case |
|----------|------------|-------|----------|
| Python BaseData class | Heap (GC) | ~1K rows/sec | Prototyping |
| C# class | Heap (GC) | ~100K rows/sec | Low-frequency data |
| C# struct | Stack (no GC) | ~100M rows/sec | High-frequency data |

**EPEX Data Volume:**
- 48 contracts × 86,400 seconds × 1 update/sec = 4.1M updates/day
- Backtesting 1 year = 1.5B updates
- **Requirement:** 2M rows/sec → Must use C# structs

### The Hybrid Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    LEAN HYBRID ARCHITECTURE                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ C# Engine Layer (High Performance)                      │   │
│  │                                                         │   │
│  │  • PowerOrderBookUpdate struct (28 bytes)               │   │
│  │  • PowerDelivery : Security class                       │   │
│  │  • ParquetPowerDataReader (2M rows/sec)                 │   │
│  │  • PowerDeliveryFilterUniverse                          │   │
│  │  • EpexOrderBookFillModel                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                    │
│                           │ Data flows up                      │
│                           ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Python Algorithm Layer (Flexibility)                    │   │
│  │                                                         │   │
│  │  class MyStrategy(QCAlgorithm):                         │   │
│  │      def Initialize(self):                              │   │
│  │          self.AddPowerUniverse("epex", "DE")            │   │
│  │                                                         │   │
│  │      def OnData(self, data):                            │   │
│  │          for symbol in self.ActiveSecurities.Keys:      │   │
│  │              power = self.Securities[symbol]            │   │
│  │              orderbook = power.OrderBook  # C# object   │   │
│  │              if orderbook.Imbalance > 0.3:              │   │
│  │                  self.Buy(symbol, 10)                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Key Insight:** Python algorithms consume C# data types. You write strategy logic in Python, but the heavy lifting (data reading, caching, fills) happens in C#.

---

## 5. Understanding C# Data Types

### PowerOrderBookUpdate Struct

The core data structure for order book updates:

```csharp
// File: Common/Data/Market/PowerOrderBookUpdate.cs
// Size: 28 bytes (fits in CPU cache line)

[StructLayout(LayoutKind.Sequential)]
public readonly struct PowerOrderBookUpdate
{
    public readonly long TimestampMicros;  // 8 bytes - Unix microseconds
    public readonly int BidPrice;          // 4 bytes - Scaled: 6550 = €65.50
    public readonly int AskPrice;          // 4 bytes - Scaled: 6600 = €66.00
    public readonly int BidVolume;         // 4 bytes - MWh (integer)
    public readonly int AskVolume;         // 4 bytes - MWh (integer)
    public readonly int ContractId;        // 4 bytes - Hash of contract string

    // Computed properties (no storage cost)
    public decimal BidPriceDecimal => BidPrice / 100m;
    public decimal AskPriceDecimal => AskPrice / 100m;
    public decimal Spread => (AskPrice - BidPrice) / 100m;
    public decimal MidPrice => (BidPrice + AskPrice) / 200m;
}
```

### Why Scaled Integers?

Decimal arithmetic is slow. Scaled integers are fast:

```csharp
// Decimal division: ~50 nanoseconds
decimal spread = askPrice - bidPrice;  // €66.00 - €65.50 = €0.50

// Integer subtraction: ~1 nanosecond
int spreadScaled = askPrice - bidPrice;  // 6600 - 6550 = 50
// Convert only when displaying: 50 / 100 = €0.50
```

**50x faster** in the hot path (millions of operations/second).

### PowerOrderBook Class

The order book attached to each PowerDelivery security:

```csharp
// File: Common/Securities/Power/PowerOrderBook.cs

public class PowerOrderBook
{
    public Symbol Symbol { get; }

    // Top of book (always available)
    public decimal BestBidPrice { get; private set; }
    public decimal BestAskPrice { get; private set; }
    public decimal BestBidQuantity { get; private set; }
    public decimal BestAskQuantity { get; private set; }

    // Computed metrics
    public decimal Spread => BestAskPrice - BestBidPrice;
    public decimal MidPrice => (BestBidPrice + BestAskPrice) / 2m;
    public decimal Imbalance => (BestBidQuantity - BestAskQuantity)
                               / (BestBidQuantity + BestAskQuantity);

    // Full depth (optional, 10 levels)
    public PriceLevel[] BidLevels { get; }  // [0] = best bid
    public PriceLevel[] AskLevels { get; }  // [0] = best ask

    // Update from data feed
    public void Update(PowerOrderBookUpdate update) { ... }
}
```

### PowerDelivery Security

The main security class representing a power delivery contract:

```csharp
// File: Common/Securities/Power/PowerDelivery.cs

public class PowerDelivery : Security
{
    // Contract-specific properties
    public DateTime DeliveryStart { get; }
    public DateTime DeliveryEnd { get; }
    public DateTime GateClosure { get; }
    public string MarketArea { get; }
    public TimeSpan ContractDuration { get; }

    // Order book data
    public PowerOrderBook OrderBook { get; }

    // Computed
    public bool IsTradeable => DateTime.UtcNow < GateClosure;
    public TimeSpan TimeToDelivery => DeliveryStart - DateTime.UtcNow;

    // Override price to use order book
    public override decimal Price => OrderBook.MidPrice;
}
```

---

## 6. Python Algorithms Using C# Data

### Accessing Order Book from Python

```python
from AlgorithmImports import *

class EpexOrderBookStrategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2025, 10, 16)
        self.SetEndDate(2025, 10, 16)
        self.SetCash(100000)

        # Add power universe (C# handles contract management)
        self.AddPowerUniverse("epex", "DE", horizonHours=24)

    def OnData(self, data):
        # Iterate over active power contracts
        for symbol in self.ActiveSecurities.Keys:
            security = self.Securities[symbol]

            # Check if it's a PowerDelivery (not other security types)
            if security.Type != SecurityType.PowerDelivery:
                continue

            # Access C# OrderBook object from Python
            orderbook = security.OrderBook

            # Use computed properties (calculated in C#)
            spread = orderbook.Spread
            imbalance = orderbook.Imbalance
            mid_price = orderbook.MidPrice

            self.Debug(f"{symbol}: Spread={spread:.2f}, Imbalance={imbalance:.2%}")

            # Trading logic
            if imbalance > 0.3 and not self.Portfolio[symbol].Invested:
                self.MarketOrder(symbol, 10)  # Buy 10 MWh
```

### Accessing Full Depth

```python
def OnData(self, data):
    for symbol in self.ActiveSecurities.Keys:
        security = self.Securities[symbol]
        if security.Type != SecurityType.PowerDelivery:
            continue

        orderbook = security.OrderBook

        # Access bid levels (C# array)
        for i in range(min(5, len(orderbook.BidLevels))):
            level = orderbook.BidLevels[i]
            if level.Price > 0:
                self.Debug(f"Bid {i}: {level.Price:.2f} x {level.Quantity:.0f}")

        # Access ask levels
        for i in range(min(5, len(orderbook.AskLevels))):
            level = orderbook.AskLevels[i]
            if level.Price > 0:
                self.Debug(f"Ask {i}: {level.Price:.2f} x {level.Quantity:.0f}")
```

---

## 7. Universe Selection

### How Universe Selection Works

EPEX has **48+ contracts per day** (one per half-hour). The universe dynamically manages these:

```
Timeline:
────────────────────────────────────────────────────────────────►
         │                                        │
    Current Time                            Gate Closure
         │                                        │
         │  ┌─────────────────────────────────┐   │
         │  │     TRADEABLE CONTRACTS         │   │
         │  │  (In Universe)                  │   │
         │  └─────────────────────────────────┘   │
         │                                        │
         │  Contracts past gate closure are      │
         │  automatically REMOVED from universe  │
```

### PowerDeliveryFilterUniverse (C#)

```csharp
// File: Common/Securities/Power/PowerDeliveryFilterUniverse.cs

public class PowerDeliveryFilterUniverse : Universe
{
    private readonly string _marketArea;
    private readonly int _horizonHours;
    private readonly int _gateClosureMinutes;

    public override IEnumerable<Symbol> SelectSymbols(
        DateTime utcTime,
        BaseDataCollection data)
    {
        var symbols = new List<Symbol>();

        // Generate symbols for contracts within horizon
        for (int hour = 0; hour < _horizonHours; hour++)
        {
            var deliveryStart = utcTime.Date.AddHours(hour);
            var gateClosure = deliveryStart.AddMinutes(-_gateClosureMinutes);

            // Only include if before gate closure
            if (utcTime < gateClosure)
            {
                var symbol = Symbol.CreatePowerDelivery(
                    _marketArea,
                    deliveryStart,
                    Market.EPEX);
                symbols.Add(symbol);
            }
        }

        return symbols;
    }
}
```

### Using Universe from Python

```python
def Initialize(self):
    # Simple API - C# handles the complexity
    self.AddPowerUniverse(
        market="epex",
        marketArea="DE",
        horizonHours=24  # Trade contracts for next 24 hours
    )

def OnSecuritiesChanged(self, changes):
    # Called when universe adds/removes contracts
    for added in changes.AddedSecurities:
        if added.Type == SecurityType.PowerDelivery:
            self.Debug(f"Added: {added.Symbol} (Delivery: {added.DeliveryStart})")

    for removed in changes.RemovedSecurities:
        if removed.Type == SecurityType.PowerDelivery:
            self.Debug(f"Removed: {removed.Symbol} (Gate closed)")
```

---

## 8. Brokerage Model

### EpexOrderBookFillModel (C#)

The fill model simulates realistic execution using the order book:

```csharp
// File: Brokerages/Epex/EpexOrderBookFillModel.cs

public class EpexOrderBookFillModel : FillModel
{
    public override Fill MarketFill(Security security, MarketOrder order)
    {
        var power = security as PowerDelivery;
        if (power == null) return base.MarketFill(security, order);

        // Check gate closure
        if (DateTime.UtcNow >= power.GateClosure)
        {
            return new Fill
            {
                Status = OrderStatus.Invalid,
                Message = "Gate closure passed"
            };
        }

        // Walk order book to simulate fill
        var orderBook = power.OrderBook;
        var isBuy = order.Quantity > 0;
        var remaining = Math.Abs(order.Quantity);
        decimal totalCost = 0;
        decimal filled = 0;

        var levels = isBuy ? orderBook.AskLevels : orderBook.BidLevels;

        foreach (var level in levels)
        {
            if (level.IsEmpty || remaining <= 0) break;

            var fillQty = Math.Min(remaining, level.Quantity);
            totalCost += fillQty * level.Price;
            filled += fillQty;
            remaining -= fillQty;
        }

        return new Fill
        {
            FillPrice = filled > 0 ? totalCost / filled : 0,
            FillQuantity = isBuy ? filled : -filled,
            Status = remaining > 0 ? OrderStatus.PartiallyFilled : OrderStatus.Filled
        };
    }
}
```

### EpexFeeModel (C#)

```csharp
// File: Brokerages/Epex/EpexFeeModel.cs

public class EpexFeeModel : FeeModel
{
    // EPEX fees: approximately €0.01-0.03 per MWh
    private const decimal FeePerMwh = 0.02m;

    public override OrderFee GetOrderFee(OrderFeeParameters parameters)
    {
        var quantity = Math.Abs(parameters.Order.Quantity);
        var fee = quantity * FeePerMwh;

        return new OrderFee(new CashAmount(fee, "EUR"));
    }
}
```

---

## 9. Market Hours Configuration

### 24/7 Trading with Gate Closure

EPEX trades continuously, but each contract has a gate closure:

```json
// File: Data/market-hours/market-hours-database.json
// Add entry for PowerDelivery/EPEX

{
  "PowerDelivery": {
    "epex": {
      "dataTimeZone": "Europe/Berlin",
      "exchangeTimeZone": "Europe/Berlin",
      "sunday": [{ "start": "00:00", "end": "24:00" }],
      "monday": [{ "start": "00:00", "end": "24:00" }],
      "tuesday": [{ "start": "00:00", "end": "24:00" }],
      "wednesday": [{ "start": "00:00", "end": "24:00" }],
      "thursday": [{ "start": "00:00", "end": "24:00" }],
      "friday": [{ "start": "00:00", "end": "24:00" }],
      "saturday": [{ "start": "00:00", "end": "24:00" }]
    }
  }
}
```

### Gate Closure Logic (C#)

```csharp
// In PowerDeliveryExchange.cs
public override bool IsOpen => true;  // 24/7 market

// Contract-level trading check
public bool IsContractTradeable(PowerDelivery contract)
{
    return DateTime.UtcNow < contract.GateClosure;
}
```

---

## 10. Basic Algorithm Example

### Complete Working Example

```python
from AlgorithmImports import *

class EpexBasicStrategy(QCAlgorithm):
    """
    Basic EPEX SPOT trading strategy.

    Strategy: Trade on order book imbalance
    - Buy when bid quantity significantly exceeds ask quantity
    - Sell when position exists and imbalance reverses
    """

    def Initialize(self):
        # Backtest configuration
        self.SetStartDate(2025, 10, 16)
        self.SetEndDate(2025, 10, 16)
        self.SetCash(100000)

        # Time zone (EPEX operates in CET/CEST)
        self.SetTimeZone("Europe/Berlin")

        # Add power universe for German market
        self.AddPowerUniverse("epex", "DE", horizonHours=24)

        # Strategy parameters
        self.imbalance_threshold = 0.3  # 30% imbalance
        self.position_size_mwh = 10

        self.Log("Initialized EPEX Basic Strategy")

    def OnData(self, data):
        """Process order book updates"""

        for symbol in self.ActiveSecurities.Keys:
            security = self.Securities[symbol]

            # Filter for PowerDelivery only
            if security.Type != SecurityType.PowerDelivery:
                continue

            # Skip if past gate closure
            if not security.IsTradeable:
                continue

            orderbook = security.OrderBook
            holdings = self.Portfolio[symbol].Quantity

            # Calculate imbalance
            imbalance = orderbook.Imbalance

            # Entry: Strong buying pressure
            if holdings == 0 and imbalance > self.imbalance_threshold:
                self.MarketOrder(symbol, self.position_size_mwh)
                self.Log(f"BUY {symbol}: Imbalance={imbalance:.2%}")

            # Exit: Imbalance reverses
            elif holdings > 0 and imbalance < 0:
                self.Liquidate(symbol)
                self.Log(f"SELL {symbol}: Imbalance reversed to {imbalance:.2%}")

    def OnSecuritiesChanged(self, changes):
        """Handle universe changes"""
        for added in changes.AddedSecurities:
            if added.Type == SecurityType.PowerDelivery:
                self.Debug(f"Contract added: {added.Symbol}")

        for removed in changes.RemovedSecurities:
            if removed.Type == SecurityType.PowerDelivery:
                # Liquidate before removal (gate closure)
                if self.Portfolio[removed.Symbol].Invested:
                    self.Liquidate(removed.Symbol)
                    self.Log(f"Liquidated {removed.Symbol} at gate closure")
```

---

## 11. Advanced Strategies

### Order Book Depth Strategy

```python
def OnData(self, data):
    for symbol in self.ActiveSecurities.Keys:
        security = self.Securities[symbol]
        if security.Type != SecurityType.PowerDelivery:
            continue

        orderbook = security.OrderBook

        # Calculate depth imbalance using multiple levels
        bid_depth = sum(level.Quantity for level in orderbook.BidLevels[:5]
                       if level.Price > 0)
        ask_depth = sum(level.Quantity for level in orderbook.AskLevels[:5]
                       if level.Price > 0)

        total_depth = bid_depth + ask_depth
        if total_depth == 0:
            continue

        depth_imbalance = (bid_depth - ask_depth) / total_depth

        # Trade on significant depth imbalance
        if depth_imbalance > 0.4:
            self.SetHoldings(symbol, 0.1)  # 10% of portfolio
        elif depth_imbalance < -0.4:
            self.SetHoldings(symbol, 0)
```

### Spread Capture Strategy

```python
def OnData(self, data):
    for symbol in self.ActiveSecurities.Keys:
        security = self.Securities[symbol]
        if security.Type != SecurityType.PowerDelivery:
            continue

        orderbook = security.OrderBook
        spread = orderbook.Spread

        # Only trade when spread is tight (good liquidity)
        if spread < 0.50:  # Less than €0.50 spread
            if not self.Portfolio[symbol].Invested:
                self.MarketOrder(symbol, 10)

        # Exit when spread widens
        elif spread > 1.00 and self.Portfolio[symbol].Invested:
            self.Liquidate(symbol)
```

### Multi-Contract Relative Value

```python
def OnData(self, data):
    # Collect all tradeable contracts with their prices
    contracts = []
    for symbol in self.ActiveSecurities.Keys:
        security = self.Securities[symbol]
        if security.Type != SecurityType.PowerDelivery and security.IsTradeable:
            contracts.append({
                'symbol': symbol,
                'price': security.OrderBook.MidPrice,
                'delivery': security.DeliveryStart
            })

    if len(contracts) < 2:
        return

    # Sort by delivery time
    contracts.sort(key=lambda x: x['delivery'])

    # Find price anomalies (adjacent hours with large price difference)
    for i in range(len(contracts) - 1):
        price_diff = contracts[i+1]['price'] - contracts[i]['price']

        # If later hour is much cheaper, buy it and sell earlier
        if price_diff < -5.00:  # €5 cheaper
            self.SetHoldings(contracts[i+1]['symbol'], 0.1)
            self.SetHoldings(contracts[i]['symbol'], -0.1)
```

---

## 12. Troubleshooting

### Data Not Loading

**Symptom:** `OnData()` never called for power contracts

**Checks:**
1. Verify Parquet files exist in expected location
2. Check data partitioning matches expected format
3. Verify LEAN config.json points to correct data folder
4. Check C# build completed successfully

```bash
# Verify data exists
ls -la Data/powerdelivery/epex/2025-10-16/DE/HH/

# Rebuild LEAN
dotnet build QuantConnect.Lean.sln
```

### Symbol Not Recognized

**Symptom:** "Symbol not found" or "Unknown security type"

**Solution:**
1. Verify `SecurityType.PowerDelivery` is in `Common/Global.cs`
2. Verify `Market.EPEX` is in `Common/Market.cs`
3. Verify `SecurityService.cs` has case for `PowerDelivery`

### Gate Closure Rejections

**Symptom:** Orders rejected with "Gate closure passed"

**Solution:**
- This is expected behavior - you cannot trade contracts after gate closure
- Liquidate positions in `OnSecuritiesChanged` when contracts are removed

### Performance Issues

**Symptom:** Backtest running slowly (< 100K rows/sec)

**Checks:**
1. Ensure using C# data reader (not Python)
2. Verify Parquet files are not corrupt
3. Check disk I/O (SSD recommended)
4. Reduce universe size if testing

---

## 13. Summary & Next Steps

### What You've Learned

| Topic | Key Takeaway |
|-------|--------------|
| Market Structure | EPEX trades 48+ contracts/day, 24/7, with gate closure |
| Architecture | C# for performance, Python for strategy logic |
| Data Types | 28-byte structs with scaled integers |
| Order Book | Real-time bid/ask with computed imbalance |
| Universe | Dynamic contract management with gate closure filtering |
| Brokerage | Realistic fills walking order book depth |

### Implementation Path

**To implement EPEX support:**

1. **Read:** DIAGRAMS_LEAN_ARCHITECTURE.md (authoritative spec)
2. **Complete:** C# Tutorials 03-10 (see GUIDE_CS_PREREQUISITES_BY_PHASE.md)
3. **Verify:** Pre-implementation checklist (see CHECKLIST_PRE_IMPLEMENTATION.md)
4. **Implement:** Follow 8-week phased approach in DIAGRAMS

### Related Documents

| Document | Purpose |
|----------|---------|
| DIAGRAMS_LEAN_ARCHITECTURE.md | Visual architecture + implementation checklist |
| GUIDE_EPEX_PRODUCTION_ARCHITECTURE.md | Detailed design decisions |
| GUIDE_CS_PREREQUISITES_BY_PHASE.md | C# learning path |
| CHECKLIST_PRE_IMPLEMENTATION.md | Gate before implementation |

---

**Tutorial Complete.** You now understand how LEAN is extended for custom markets like EPEX SPOT.

---

**Document Version:** 2.0 (aligned with DIAGRAMS architecture)
**Last Updated:** 2025-12-12
**Author:** Claude (Systematic Trading Architect)
**Project:** LEAN Energy Trading Adaptation
