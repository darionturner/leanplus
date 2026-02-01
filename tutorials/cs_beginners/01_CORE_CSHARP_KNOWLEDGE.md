# Tutorial 01: Core C# Knowledge for LEAN

**Duration:** 90 minutes (30 min reading + 60 min hands-on)
**Prerequisites:** Python proficiency, basic programming concepts
**Goal:** Understand C# fundamentals through the lens of LEAN development

---

## 📋 Table of Contents

1. [Overview](#1-overview-5-min)
2. [C# vs Python: Key Differences](#2-c-vs-python-key-differences-15-min)
3. [Type System & Memory Management](#3-type-system--memory-management-20-min)
4. [Key Concepts for LEAN Development](#4-key-concepts-for-lean-development-25-min)
5. [Reading LEAN Source Code](#5-reading-lean-source-code-20-min)
6. [Common Pitfalls for Python Developers](#6-common-pitfalls-for-python-developers-5-min)
7. [Validation Checklist](#7-validation-checklist-5-min)

---

## 1. Overview (5 min)

### Why C# for LEAN?

**Performance:** C# compiles to native code, crucial for backtesting millions of market events
- Python algorithm: ~1,000 orderbook updates/sec
- C# engine: ~100,000+ orderbook updates/sec
- **100x performance difference** for data-intensive operations

**Type Safety:** Catches errors at compile-time, not runtime
- Python: `price = "65.50"` (string) causes runtime error in calculations
- C#: `decimal price = "65.50";` → **compile error**, caught immediately

**LEAN's Architecture:**
- **Engine Core:** C# (performance-critical path)
- **Algorithms:** C# or Python (your trading logic)
- **Extensions:** C# required (brokerages, data handlers, security types)

### Your C# Learning Journey

```
Week 1: Read & understand C# code (this tutorial)
Week 2: Debug existing C# components
Week 3: Modify C# classes (data structures)
Week 4: Implement new C# features (PowerDelivery security type)
```

---

## 2. C# vs Python: Key Differences (15 min)

### Philosophy Comparison

| Aspect | Python | C# |
|--------|--------|-----|
| **Paradigm** | "Duck typing" - if it quacks, it's a duck | "Strict typing" - must declare it's a duck |
| **Compilation** | Interpreted (runtime) | Compiled (build-time) |
| **Error Detection** | Runtime | Compile-time + Runtime |
| **Performance** | Slower (dynamic) | Faster (static, optimized) |
| **Verbosity** | Concise | More explicit |
| **Memory** | Garbage collected | Garbage collected + manual control |

### Syntax Comparison: Common Patterns

#### Variables & Types

**Python:**
```python
# Dynamic typing - type inferred
price = 65.50
quantity = 100
contract_id = "14229494-14"
is_active = True

# Type hints (optional, not enforced)
def calculate_value(price: float, qty: int) -> float:
    return price * qty
```

**C#:**
```csharp
// Static typing - type must be declared
decimal price = 65.50m;        // 'm' suffix for decimal
int quantity = 100;
string contractId = "14229494-14";
bool isActive = true;

// Type inference with 'var' (still statically typed!)
var price = 65.50m;           // Compiler infers: decimal
var quantity = 100;           // Compiler infers: int

// Method signature (types enforced)
public decimal CalculateValue(decimal price, int qty)
{
    return price * qty;
}
```

**Key Difference:**
- Python: Types are optional hints, not enforced
- C#: Types are required, checked at compile-time (even with `var`)

#### Collections

**Python:**
```python
# List (dynamic, any type)
prices = [65.50, 66.00, 65.25]
prices.append(67.00)
first_price = prices[0]

# Dictionary
orderbook = {
    "bid": 65.50,
    "ask": 65.75,
    "volume": 1000
}

# List comprehension
high_prices = [p for p in prices if p > 66]
```

**C#:**
```csharp
// List<T> (strongly typed, generic)
List<decimal> prices = new List<decimal> { 65.50m, 66.00m, 65.25m };
prices.Add(67.00m);
decimal firstPrice = prices[0];

// Dictionary<TKey, TValue>
Dictionary<string, decimal> orderbook = new Dictionary<string, decimal>
{
    { "bid", 65.50m },
    { "ask", 65.75m },
    { "volume", 1000m }
};

// LINQ (Language Integrated Query) - like list comprehensions
var highPrices = prices.Where(p => p > 66).ToList();
```

**Key Difference:**
- Python: One list type holds anything
- C#: `List<decimal>` can ONLY hold decimals (compile-time enforced)

#### Classes & Objects

**Python:**
```python
class OrderBook:
    def __init__(self, symbol):
        self.symbol = symbol
        self.bid_price = 0.0
        self.ask_price = 0.0

    def update(self, bid, ask):
        self.bid_price = bid
        self.ask_price = ask

    @property
    def spread(self):
        return self.ask_price - self.bid_price

# Usage
book = OrderBook("EPEX-GB-HH-14")
book.update(65.50, 65.75)
print(book.spread)  # 0.25
```

**C#:**
```csharp
public class OrderBook
{
    // Properties (auto-implemented)
    public string Symbol { get; set; }
    public decimal BidPrice { get; set; }
    public decimal AskPrice { get; set; }

    // Constructor
    public OrderBook(string symbol)
    {
        Symbol = symbol;
        BidPrice = 0m;
        AskPrice = 0m;
    }

    // Method
    public void Update(decimal bid, decimal ask)
    {
        BidPrice = bid;
        AskPrice = ask;
    }

    // Computed property
    public decimal Spread => AskPrice - BidPrice;
}

// Usage
var book = new OrderBook("EPEX-GB-HH-14");
book.Update(65.50m, 65.75m);
Console.WriteLine(book.Spread);  // 0.25
```

**Key Differences:**
- Python: Properties defined in `__init__`, accessed directly
- C#: Properties declared with types, accessed via `{ get; set; }`
- C#: Computed properties use `=>` (expression-bodied member)

#### Null Handling

**Python:**
```python
price = None
if price is not None:
    value = price * 100
else:
    value = 0
```

**C#:**
```csharp
// Nullable types (C# 8.0+)
decimal? price = null;              // '?' makes it nullable
decimal value = price ?? 0;         // Null-coalescing operator

// Null-conditional operator
decimal? spread = orderBook?.Spread;  // Returns null if orderBook is null

// Pattern matching (C# 9.0+)
if (price is not null)
{
    value = price.Value * 100;      // .Value extracts the decimal
}
```

**Key Difference:**
- Python: Everything can be `None` by default
- C#: Types are non-nullable by default, use `?` for nullable

---

## 3. Type System & Memory Management (20 min)

### C#'s Type System

#### Value Types vs Reference Types

**Value Types** (stored on stack, copied by value)
```csharp
// Primitive types
int quantity = 100;
decimal price = 65.50m;
bool isActive = true;
DateTime timestamp = DateTime.UtcNow;

// Structs (user-defined value types)
public struct PriceLevel
{
    public decimal Price;
    public int Quantity;
}

PriceLevel level1 = new PriceLevel { Price = 65.50m, Quantity = 1000 };
PriceLevel level2 = level1;     // COPY created
level2.Price = 66.00m;          // Does NOT affect level1

Console.WriteLine(level1.Price);  // 65.50
Console.WriteLine(level2.Price);  // 66.00
```

**Reference Types** (stored on heap, copied by reference)
```csharp
// Classes (reference types)
public class OrderBook
{
    public decimal BidPrice { get; set; }
    public decimal AskPrice { get; set; }
}

OrderBook book1 = new OrderBook { BidPrice = 65.50m };
OrderBook book2 = book1;        // REFERENCE copied (both point to same object)
book2.BidPrice = 66.00m;        // DOES affect book1

Console.WriteLine(book1.BidPrice);  // 66.00 (changed!)
Console.WriteLine(book2.BidPrice);  // 66.00
```

**Python Comparison:**
```python
# Python: Everything is a reference (like C# classes)
book1 = {"bid": 65.50}
book2 = book1           # Reference copy
book2["bid"] = 66.00    # Affects book1

print(book1["bid"])     # 66.00
```

#### When to Use Struct vs Class in LEAN

**Use `struct`** for:
- Small, immutable data (< 16 bytes recommended)
- High-frequency, performance-critical code
- Example: `PriceLevel`, `TopOfBookSnapshot` (Tutorial design analysis)

**Use `class`** for:
- Complex objects with behavior
- Objects that need inheritance
- Example: `Security`, `OrderBook`, `Algorithm`

**LEAN Example from Design Analysis:**
```csharp
// Struct for performance (28 bytes, zero allocations)
[StructLayout(LayoutKind.Sequential, Pack = 1)]
public readonly struct TopOfBookSnapshot
{
    public readonly long TimestampTicks;
    public readonly int BidPriceScaled;
    public readonly int AskPriceScaled;
    public readonly int BidQuantityScaled;
    public readonly int AskQuantityScaled;

    // Computed properties (no storage overhead)
    public decimal BidPrice => BidPriceScaled / 100m;
    public decimal AskPrice => AskPriceScaled / 100m;
}

// Why struct? Processing 1M snapshots:
// - Class: 40 MB heap allocation + GC pauses
// - Struct: 28 MB stack allocation + zero GC
```

### Memory Management

#### Garbage Collection Basics

**Python:** Automatic, reference counting + cycle detection
```python
# Object created, GC handles cleanup
book = OrderBook("EPEX")
book = None  # GC will clean up when ready
```

**C#:** Automatic, generational GC
```csharp
// Object created on heap
var book = new OrderBook("EPEX");
book = null;  // Object eligible for GC

// GC runs automatically, reclaims memory
// Generations: 0 (short-lived), 1, 2 (long-lived)
```

#### Avoiding GC Pressure in LEAN

**Bad (causes GC pressure):**
```csharp
// Creating objects in hot loop (1M iterations)
for (int i = 0; i < 1_000_000; i++)
{
    var snapshot = new OrderBookSnapshot();  // 1M allocations!
    ProcessSnapshot(snapshot);
}
// Result: GC pauses, slow performance
```

**Good (using value types):**
```csharp
// Using struct (stack allocation, no GC)
for (int i = 0; i < 1_000_000; i++)
{
    TopOfBookSnapshot snapshot = GetSnapshot();  // Stack allocation
    ProcessSnapshot(snapshot);
}
// Result: No GC pressure, 10x faster
```

**Best (object pooling for classes):**
```csharp
// Reuse objects from pool
var pool = new ObjectPool<OrderBook>();
for (int i = 0; i < 1_000_000; i++)
{
    var book = pool.Get();      // Reuse existing object
    ProcessBook(book);
    pool.Return(book);          // Return to pool
}
// Result: Minimal allocations, consistent performance
```

---

## 4. Key Concepts for LEAN Development (25 min)

### Interfaces & Abstraction

**Python (Duck Typing):**
```python
# No formal interface, just implement methods
class EpexBrokerage:
    def connect(self):
        pass

    def place_order(self, order):
        pass

# Python accepts anything with these methods
```

**C# (Interface Contracts):**
```csharp
// LEAN's IBrokerage interface (simplified)
public interface IBrokerage
{
    bool IsConnected { get; }
    void Connect();
    void Disconnect();
    bool PlaceOrder(Order order);
}

// Must implement ALL interface members
public class EpexBrokerage : IBrokerage
{
    public bool IsConnected { get; private set; }

    public void Connect()
    {
        // Implementation
        IsConnected = true;
    }

    public void Disconnect()
    {
        IsConnected = false;
    }

    public bool PlaceOrder(Order order)
    {
        // Implementation
        return true;
    }
}
```

**Why Interfaces Matter in LEAN:**
- LEAN engine expects specific interfaces (`IBrokerage`, `IDataQueueHandler`, etc.)
- Compile-time check ensures you implement all required methods
- Enables polymorphism (LEAN doesn't care if it's EPEX, IB, or Coinbase)

### Generics

**Python (no generics, uses `Any` or type hints):**
```python
from typing import List, TypeVar

T = TypeVar('T')

def get_first(items: List[T]) -> T:
    return items[0]

prices = [65.50, 66.00]
first = get_first(prices)  # Type checker infers float
```

**C# (strong generics):**
```csharp
// Generic method (works with any type)
public T GetFirst<T>(List<T> items)
{
    return items[0];
}

// Usage
List<decimal> prices = new List<decimal> { 65.50m, 66.00m };
decimal first = GetFirst(prices);  // Type-safe, no casting

// LEAN example: Security<T>
public class Security<T> where T : ITimeKeeper
{
    // Only types implementing ITimeKeeper allowed
}
```

**LEAN's Generics Usage:**
```csharp
// Generic list of securities
List<Security> securities = new List<Security>();

// Generic dictionary for orderbooks
Dictionary<Symbol, OrderBook> orderBooks =
    new Dictionary<Symbol, OrderBook>();

// Generic event handler
EventHandler<OrderEvent> OnOrderEvent;
```

### LINQ (Language Integrated Query)

**Python List Comprehensions:**
```python
# Filter, map, reduce patterns
prices = [65.50, 66.00, 65.25, 67.00]

high_prices = [p for p in prices if p > 66]
doubled = [p * 2 for p in prices]
total = sum(prices)
max_price = max(prices)
```

**C# LINQ (More Powerful):**
```csharp
// Same operations, more readable
List<decimal> prices = new List<decimal> { 65.50m, 66.00m, 65.25m, 67.00m };

// Filter
var highPrices = prices.Where(p => p > 66).ToList();

// Map (transform)
var doubled = prices.Select(p => p * 2).ToList();

// Aggregate
decimal total = prices.Sum();
decimal maxPrice = prices.Max();

// Chaining operations
var result = prices
    .Where(p => p > 66)          // Filter
    .Select(p => p * 2)          // Transform
    .OrderByDescending(p => p)   // Sort
    .Take(5)                     // Limit
    .ToList();                   // Execute & materialize

// LEAN example: Get active contracts
var activeContracts = securities
    .Where(s => s.Symbol.SecurityType == SecurityType.Power)
    .Where(s => s.Price > 0)
    .OrderBy(s => s.Symbol.Value)
    .ToList();
```

**LINQ Deferred Execution:**
```csharp
// Query defined, NOT executed yet
var query = prices.Where(p => p > 66);  // IEnumerable<decimal>

// Executed when you iterate or materialize
foreach (var p in query)  // Executes now
{
    Console.WriteLine(p);
}

var list = query.ToList();  // Executes and creates List<decimal>
```

### Async/Await

**Python asyncio:**
```python
import asyncio

async def fetch_orderbook(symbol):
    await asyncio.sleep(1)  # Simulate API call
    return {"bid": 65.50, "ask": 65.75}

async def main():
    book = await fetch_orderbook("EPEX-GB-HH-14")
    print(book)

asyncio.run(main())
```

**C# async/await (similar pattern):**
```csharp
public async Task<OrderBook> FetchOrderBookAsync(string symbol)
{
    await Task.Delay(1000);  // Simulate API call
    return new OrderBook { BidPrice = 65.50m, AskPrice = 65.75m };
}

public async Task Main()
{
    OrderBook book = await FetchOrderBookAsync("EPEX-GB-HH-14");
    Console.WriteLine(book.BidPrice);
}
```

**LEAN Usage:**
```csharp
// Brokerage API calls are often async
public class EpexBrokerage : IBrokerage
{
    public async Task<bool> PlaceOrderAsync(Order order)
    {
        // Non-blocking HTTP request
        var response = await _httpClient.PostAsync(
            "/orders",
            CreateOrderPayload(order));

        return response.IsSuccessStatusCode;
    }
}
```

---

## 5. Reading LEAN Source Code (20 min)

### Navigating LEAN's Codebase

**Project Structure:**
```
LEAN/
├── Algorithm/              # QCAlgorithm base classes
├── Algorithm.Python/       # Python algorithm wrappers
├── Brokerages/            # Brokerage implementations
│   ├── InteractiveBrokers/
│   ├── Coinbase/
│   └── Paper/             # ← Good starting point!
├── Common/                # Core types and utilities
│   ├── Data/              # ← BaseData, subscriptions
│   ├── Orders/            # ← Order types
│   ├── Securities/        # ← Security, Symbol
│   └── Util/              # ← Extensions, helpers
├── Engine/                # Trading engine core
│   ├── DataFeeds/         # ← Data pipeline
│   ├── Results/           # ← Result handlers
│   └── TransactionHandlers/
├── Launcher/              # Entry point
└── Tests/                 # Unit & integration tests
```

### Exercise 1: Reading a Simple Class (15 min)

**File:** `Common/Data/BaseData.cs` (simplified excerpt)

```csharp
namespace QuantConnect.Data
{
    /// <summary>
    /// Base class for all data types in LEAN
    /// </summary>
    public abstract class BaseData
    {
        /// <summary>
        /// Time of this data point
        /// </summary>
        public DateTime Time { get; set; }

        /// <summary>
        /// Trading symbol for this data
        /// </summary>
        public Symbol Symbol { get; set; }

        /// <summary>
        /// Price of this data point
        /// </summary>
        public virtual decimal Value { get; set; }

        /// <summary>
        /// Reader method to parse custom data
        /// </summary>
        public abstract BaseData Reader(
            SubscriptionDataConfig config,
            string line,
            DateTime date,
            bool isLiveMode);

        /// <summary>
        /// Source location for this data
        /// </summary>
        public abstract SubscriptionDataSource GetSource(
            SubscriptionDataConfig config,
            DateTime date,
            bool isLiveMode);
    }
}
```

**Reading Guide:**

1. **Namespace:** `QuantConnect.Data` (organize code by domain)
2. **XML Comments:** `///` - documentation shown in IntelliSense
3. **Abstract Class:** Cannot instantiate directly, must inherit
4. **Properties:** `{ get; set; }` - auto-implemented properties
5. **Virtual:** `virtual decimal Value` - can be overridden by subclasses
6. **Abstract Methods:** Must be implemented by subclasses

**Your Custom Implementation:**
```csharp
public class PowerPrice : BaseData
{
    // Additional properties
    public decimal Volume { get; set; }
    public string DeliveryHour { get; set; }

    // Must implement abstract method
    public override BaseData Reader(
        SubscriptionDataConfig config,
        string line,
        DateTime date,
        bool isLiveMode)
    {
        // Parse CSV line
        string[] parts = line.Split(',');
        return new PowerPrice
        {
            Time = DateTime.Parse(parts[0]),
            Symbol = config.Symbol,
            Value = decimal.Parse(parts[1]),
            Volume = decimal.Parse(parts[2]),
            DeliveryHour = parts[3]
        };
    }

    // Must implement abstract method
    public override SubscriptionDataSource GetSource(
        SubscriptionDataConfig config,
        DateTime date,
        bool isLiveMode)
    {
        // Return data file location
        string source = $"Data/power/{date:yyyyMMdd}.csv";
        return new SubscriptionDataSource(source, SubscriptionTransportMedium.LocalFile);
    }
}
```

### Exercise 2: Understanding a LEAN Interface (5 min)

**File:** `Common/Brokerages/IBrokerage.cs` (simplified)

```csharp
public interface IBrokerage : IDisposable
{
    /// <summary>
    /// True if currently connected to brokerage
    /// </summary>
    bool IsConnected { get; }

    /// <summary>
    /// Connect to brokerage API
    /// </summary>
    void Connect();

    /// <summary>
    /// Disconnect from brokerage
    /// </summary>
    void Disconnect();

    /// <summary>
    /// Submit new order
    /// </summary>
    bool PlaceOrder(Order order);

    /// <summary>
    /// Cancel pending order
    /// </summary>
    bool CancelOrder(Order order);

    /// <summary>
    /// Get current account holdings
    /// </summary>
    List<Holding> GetAccountHoldings();

    /// <summary>
    /// Event fired when order is filled
    /// </summary>
    event EventHandler<OrderEvent> OrderStatusChanged;
}
```

**Key Observations:**
- Interface defines contract (what must be implemented)
- No implementation code (only signatures)
- Events: `event EventHandler<OrderEvent>` - pub/sub pattern
- `IDisposable`: Must implement `Dispose()` for cleanup

---

## 6. Common Pitfalls for Python Developers (5 min)

### Pitfall 1: Forgetting Semicolons
```csharp
// ❌ Python habit
decimal price = 65.50m
var book = new OrderBook()

// ✅ C# requires semicolons
decimal price = 65.50m;
var book = new OrderBook();
```

### Pitfall 2: Case Sensitivity
```csharp
// ❌ C# is case-sensitive (Python too, but different conventions)
OrderBook orderbook = new OrderBook();  // ❌ Compiler error: 'orderbook' != 'OrderBook'

// ✅ Match the type name exactly
OrderBook orderBook = new OrderBook();
```

### Pitfall 3: Null Reference Exceptions
```python
# Python: None is handled gracefully often
price = None
if price:  # Falsy check
    value = price * 100
```

```csharp
// ❌ C#: Will throw NullReferenceException
decimal? price = null;
decimal value = price * 100;  // ❌ Runtime exception!

// ✅ Always check for null
decimal value = price ?? 0;   // Null-coalescing
// OR
if (price != null)
{
    value = price.Value * 100;
}
```

### Pitfall 4: Integer Division
```python
# Python 3: Division always returns float
result = 7 / 2  # 3.5
```

```csharp
// ❌ C#: Integer division returns integer
int result = 7 / 2;      // 2 (not 3.5!)

// ✅ Use decimal for precision
decimal result = 7m / 2m;  // 3.5
// OR cast to double
double result = 7.0 / 2.0;  // 3.5
```

### Pitfall 5: List Modification During Iteration
```csharp
// ❌ Throws exception: Collection was modified
var prices = new List<decimal> { 65.50m, 66.00m, 67.00m };
foreach (var price in prices)
{
    if (price > 66)
        prices.Remove(price);  // ❌ Exception!
}

// ✅ Use ToList() or for loop
var pricesToRemove = prices.Where(p => p > 66).ToList();
foreach (var price in pricesToRemove)
{
    prices.Remove(price);
}

// OR
for (int i = prices.Count - 1; i >= 0; i--)
{
    if (prices[i] > 66)
        prices.RemoveAt(i);
}
```

---

## 7. Validation Checklist (5 min)

Mark each item as you complete it:

### Conceptual Understanding
- [X] I understand the difference between value types and reference types
- [X] I know when to use `struct` vs `class`
- [X] I can explain why C# uses compile-time type checking
- [X] I understand how LINQ compares to Python list comprehensions
- [X] I know what interfaces are and why LEAN uses them

### Code Reading
- [X] I can read a C# class definition and identify:
  - [X] Properties vs fields vs methods
  - [X] Public vs private members
  - [X] Abstract vs virtual vs sealed
- [X] I understand LEAN's `BaseData` class purpose
- [X] I can navigate LEAN's project structure

### Practical Skills
- [X] I've opened `Common/Data/BaseData.cs` in an editor
- [X] I've read through `Brokerages/Paper/PaperBrokerage.cs` (simple example)
- [X] I can identify where custom code would go (Brokerages/ or Common/)

### Next Steps Ready
- [ ] I'm comfortable reading C# syntax (even if not writing yet)
- [ ] I'm ready to set up a C# development environment
- [ ] I have questions noted for further exploration

---

## 📚 Further Reading

**Essential:**
- [C# Programming Guide](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/)
- [LEAN Documentation - Custom Data](https://www.quantconnect.com/docs/v2/writing-algorithms/importing-data)

**Deep Dives:**
- [Value Types vs Reference Types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)
- [LINQ Tutorial](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)
- [Async/Await Best Practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)

**LEAN-Specific:**
- Review `Common/Securities/Security.cs` for complex class example
- Review `Brokerages/Paper/PaperBrokerage.cs` for interface implementation
- Review `Algorithm/QCAlgorithm.cs` for LEAN's main algorithm base class

---

## 🎯 Key Takeaways

1. **C# = Performance + Safety**: Compile-time checks catch errors early, crucial for financial systems
2. **Types Matter**: Understanding value vs reference types is critical for LEAN performance
3. **LINQ is Powerful**: Master it for data manipulation in backtests
4. **Interfaces Define Contracts**: LEAN uses them extensively (IBrokerage, IDataQueueHandler)
5. **Read Before Writing**: Spend time reading LEAN code before modifying it

---

## ⏭️ Next Tutorial

**Tutorial 02: C# Setup on Windows**
- Install .NET SDK and verify installation
- Choose your IDE (Visual Studio, VS Code, or Rider)
- Build LEAN from source
- Run your first C# algorithm

**Time to Complete:** 45 minutes

---

**🎓 Congratulations!** You've completed the foundational C# knowledge tutorial. You're now ready to set up your C# development environment.

*Mark this tutorial as complete in the main README.md*

---

*Last Updated: 2025-11-16*
