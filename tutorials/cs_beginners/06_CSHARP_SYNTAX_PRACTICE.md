# Tutorial 06: C# Syntax and Practice

**Duration:** 120 minutes (40 min reading + 80 min hands-on)
**Prerequisites:** Tutorial 05 completed
**Goal:** Master essential C# syntax through LEAN-focused practice

---

## 📋 Table of Contents

1. [LINQ Deep Dive](#1-linq-deep-dive-30-min)
2. [Async/Await in LEAN](#2-asyncawait-in-lean-20-min)
3. [Properties and Expression Bodies](#3-properties-and-expression-bodies-15-min)
4. [Pattern Matching](#4-pattern-matching-15-min)
5. [Extension Methods](#5-extension-methods-15-min)
6. [Practice Exercises](#6-practice-exercises-20-min)
7. [Validation Checklist](#7-validation-checklist-5-min)

---

## 1. LINQ Deep Dive (30 min)

### Essential LINQ Operators

**Filtering (`Where`):**
```csharp
// Get all power contracts for GB
var gbContracts = securities
    .Where(s => s.Symbol.ID.MarketArea == "GB")
    .Where(s => s.Symbol.SecurityType == SecurityType.Power)
    .ToList();

// Pythonic equivalent:
// [s for s in securities if s.symbol.market_area == "GB" and s.symbol.security_type == "Power"]
```

**Projection (`Select`):**
```csharp
// Get just the prices
var prices = orderbooks
    .Select(ob => ob.BidPrice)
    .ToList();

// Transform objects
var snapshots = orderbooks
    .Select(ob => new {
        Symbol = ob.Symbol,
        Spread = ob.AskPrice - ob.BidPrice,
        Time = ob.Time
    })
    .ToList();
```

**Aggregation:**
```csharp
// Statistics
decimal avgPrice = prices.Average();
decimal maxPrice = prices.Max();
decimal minPrice = prices.Min();
int count = prices.Count();
decimal sum = prices.Sum();

// Conditional aggregation
decimal avgHighPrice = prices
    .Where(p => p > 65)
    .Average();
```

---

### Exercise 1: LEAN Contract Analysis (10 min)

```csharp
// Sample data structure
public class PowerContract
{
    public string Symbol { get; set; }
    public string MarketArea { get; set; }
    public decimal Price { get; set; }
    public int Volume { get; set; }
    public DateTime DeliveryTime { get; set; }
}

// Get contracts for specific hour
var hour14Contracts = contracts
    .Where(c => c.DeliveryTime.Hour == 14)
    .Where(c => c.MarketArea == "GB")
    .OrderByDescending(c => c.Volume)
    .Take(10)
    .ToList();

// Group by market area
var byMarket = contracts
    .GroupBy(c => c.MarketArea)
    .Select(g => new {
        Market = g.Key,
        AvgPrice = g.Average(c => c.Price),
        TotalVolume = g.Sum(c => c.Volume),
        ContractCount = g.Count()
    })
    .ToList();
```

---

### Method Syntax vs Query Syntax

**Method Syntax (Preferred):**
```csharp
var highValue = contracts
    .Where(c => c.Price > 100)
    .OrderBy(c => c.DeliveryTime)
    .Select(c => c.Symbol)
    .ToList();
```

**Query Syntax:**
```csharp
var highValue = (from c in contracts
                 where c.Price > 100
                 orderby c.DeliveryTime
                 select c.Symbol).ToList();
```

**Recommendation:** Use method syntax (more common in LEAN codebase)

---

## 2. Async/Await in LEAN (20 min)

### Understanding Asynchronous Code

**Synchronous (blocking):**
```csharp
public OrderBook FetchOrderBook(string symbol)
{
    var response = _httpClient.GetAsync($"/orderbooks/{symbol}").Result;  // ❌ Blocks thread
    var content = response.Content.ReadAsStringAsync().Result;
    return JsonConvert.DeserializeObject<OrderBook>(content);
}
```

**Asynchronous (non-blocking):**
```csharp
public async Task<OrderBook> FetchOrderBookAsync(string symbol)
{
    var response = await _httpClient.GetAsync($"/orderbooks/{symbol}");  // ✅ Non-blocking
    var content = await response.Content.ReadAsStringAsync();
    return JsonConvert.DeserializeObject<OrderBook>(content);
}
```

---

### Exercise 2: Async Data Fetching (10 min)

```csharp
// Brokerage implementation pattern
public class EpexBrokerage : IBrokerage
{
    private readonly HttpClient _httpClient;

    public async Task<List<OrderBook>> GetOrderBooksAsync(List<string> symbols)
    {
        // Fetch all simultaneously (parallel)
        var tasks = symbols
            .Select(symbol => FetchOrderBookAsync(symbol))
            .ToArray();

        // Wait for all to complete
        var orderBooks = await Task.WhenAll(tasks);

        return orderBooks.ToList();
    }

    private async Task<OrderBook> FetchOrderBookAsync(string symbol)
    {
        var url = $"https://api.epex.com/orderbooks/{symbol}";
        var response = await _httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync();
        return JsonConvert.DeserializeObject<OrderBook>(json);
    }
}
```

**Python equivalent:**
```python
import asyncio
import aiohttp

async def fetch_orderbook(symbol):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.epex.com/orderbooks/{symbol}') as response:
            return await response.json()

async def get_orderbooks(symbols):
    tasks = [fetch_orderbook(s) for s in symbols]
    return await asyncio.gather(*tasks)
```

---

### Async Best Practices

**✅ Do:**
```csharp
public async Task ProcessDataAsync()
{
    var data = await FetchDataAsync();
    await SaveDataAsync(data);
}
```

**❌ Don't:**
```csharp
// Blocking async code (deadlock risk!)
public void ProcessData()
{
    var data = FetchDataAsync().Result;  // ❌ Blocks
    SaveDataAsync(data).Wait();          // ❌ Blocks
}
```

---

## 3. Properties and Expression Bodies (15 min)

### Auto-Properties

**Classic:**
```csharp
private decimal _bidPrice;
public decimal BidPrice
{
    get { return _bidPrice; }
    set { _bidPrice = value; }
}
```

**Auto-property (preferred):**
```csharp
public decimal BidPrice { get; set; }
```

**With default value:**
```csharp
public decimal BidPrice { get; set; } = 0m;
```

**Read-only:**
```csharp
public string Symbol { get; }  // Set only in constructor

public OrderBook(string symbol)
{
    Symbol = symbol;  // Can set in constructor
}
```

---

### Expression-Bodied Members

**Computed property:**
```csharp
// Old way
public decimal Spread
{
    get { return AskPrice - BidPrice; }
}

// Expression-bodied (C# 6+)
public decimal Spread => AskPrice - BidPrice;

// Methods
public decimal CalculateMidPrice() => (BidPrice + AskPrice) / 2;

// Property with logic
public bool IsActive => Price > 0 && Volume > 0;
```

---

### Exercise 3: Create OrderBook Class (10 min)

```csharp
public class OrderBook
{
    // Auto-properties
    public string Symbol { get; set; }
    public decimal BidPrice { get; set; }
    public decimal BidQuantity { get; set; }
    public decimal AskPrice { get; set; }
    public decimal AskQuantity { get; set; }
    public DateTime Timestamp { get; set; }

    // Computed properties
    public decimal Spread => AskPrice - BidPrice;
    public decimal MidPrice => (BidPrice + AskPrice) / 2;
    public decimal Imbalance =>
        (BidQuantity - AskQuantity) / (BidQuantity + AskQuantity);

    // Expression-bodied method
    public bool IsValid() => BidPrice > 0 && AskPrice > BidPrice;

    // Override ToString
    public override string ToString() =>
        $"{Symbol}: Bid={BidPrice:F2} Ask={AskPrice:F2} Spread={Spread:F2}";
}
```

---

## 4. Pattern Matching (15 min)

### Switch Expressions (C# 8+)

**Old switch:**
```csharp
string GetSecurityDescription(SecurityType type)
{
    switch (type)
    {
        case SecurityType.Equity:
            return "Stock";
        case SecurityType.Option:
            return "Option Contract";
        case SecurityType.Future:
            return "Futures Contract";
        default:
            return "Unknown";
    }
}
```

**Switch expression (modern):**
```csharp
string GetSecurityDescription(SecurityType type) => type switch
{
    SecurityType.Equity => "Stock",
    SecurityType.Option => "Option Contract",
    SecurityType.Future => "Futures Contract",
    _ => "Unknown"  // _ = default
};
```

---

### Pattern Matching with `is`

```csharp
// Type checking and casting
if (data is TradeBar bar)
{
    // 'bar' is automatically cast
    Console.WriteLine(bar.Close);
}

// Property pattern
if (orderBook is { Spread: > 1.0m })
{
    // Spread property is greater than 1.0
    Debug("Wide spread detected");
}

// Null checking
if (price is not null and > 0)
{
    ProcessPrice(price.Value);
}
```

---

## 5. Extension Methods (15 min)

### Creating Extension Methods

**Extend existing types without modifying them:**

```csharp
public static class ListExtensions
{
    // Extend List<T>
    public static decimal Median(this List<decimal> values)
    {
        if (values.Count == 0) return 0;

        var sorted = values.OrderBy(v => v).ToList();
        int mid = sorted.Count / 2;

        if (sorted.Count % 2 == 0)
            return (sorted[mid - 1] + sorted[mid]) / 2;
        else
            return sorted[mid];
    }
}

// Usage
var prices = new List<decimal> { 65.5m, 66.0m, 65.25m, 67.0m };
decimal median = prices.Median();  // Called like instance method!
```

---

### LEAN-Specific Extensions

```csharp
public static class SecurityExtensions
{
    public static bool IsPowerContract(this Security security)
    {
        return security.Symbol.SecurityType == SecurityType.Power;
    }

    public static bool IsDeliveryToday(this Security security)
    {
        // Assumes custom Symbol implementation
        return security.Symbol.ID.DeliveryDate.Date == DateTime.Today;
    }
}

// Usage in algorithm
public override void OnData(Slice data)
{
    foreach (var security in Securities.Values)
    {
        if (security.IsPowerContract() && security.IsDeliveryToday())
        {
            // Process today's power contracts
        }
    }
}
```

---

## 6. Practice Exercises (20 min)

### Exercise 4: LINQ Challenge (10 min)

**Goal:** Analyze mock orderbook data

```csharp
public class OrderBookSnapshot
{
    public string Symbol { get; set; }
    public DateTime Time { get; set; }
    public decimal BidPrice { get; set; }
    public decimal AskPrice { get; set; }
    public int Volume { get; set; }
}

// Sample data
var snapshots = new List<OrderBookSnapshot>
{
    new() { Symbol = "EPEX-GB-HH-14", Time = DateTime.Parse("2025-01-16 14:00"), BidPrice = 65.5m, AskPrice = 65.75m, Volume = 1000 },
    new() { Symbol = "EPEX-GB-HH-15", Time = DateTime.Parse("2025-01-16 15:00"), BidPrice = 66.0m, AskPrice = 66.30m, Volume = 1200 },
    // ... more data
};

// Task 1: Find average spread
var avgSpread = snapshots
    .Select(s => s.AskPrice - s.BidPrice)
    .Average();

// Task 2: Group by hour, get max volume
var maxVolumeByHour = snapshots
    .GroupBy(s => s.Time.Hour)
    .Select(g => new {
        Hour = g.Key,
        MaxVolume = g.Max(s => s.Volume),
        AvgPrice = g.Average(s => (s.BidPrice + s.AskPrice) / 2)
    })
    .OrderBy(x => x.Hour)
    .ToList();

// Task 3: Find snapshots with tight spread (< 0.20)
var tightSpreads = snapshots
    .Where(s => (s.AskPrice - s.BidPrice) < 0.20m)
    .OrderByDescending(s => s.Volume)
    .ToList();
```

---

### Exercise 5: Build a Simple Data Handler (10 min)

```csharp
public class PowerPriceDataHandler
{
    private readonly List<OrderBookSnapshot> _snapshots = new();

    public void AddSnapshot(OrderBookSnapshot snapshot)
    {
        _snapshots.Add(snapshot);
    }

    // Get snapshots for specific hour
    public List<OrderBookSnapshot> GetSnapshotsForHour(int hour) =>
        _snapshots
            .Where(s => s.Time.Hour == hour)
            .OrderBy(s => s.Time)
            .ToList();

    // Get current market summary
    public MarketSummary GetSummary() => new()
    {
        TotalSnapshots = _snapshots.Count,
        AverageSpread = _snapshots.Average(s => s.AskPrice - s.BidPrice),
        HighestBid = _snapshots.Max(s => s.BidPrice),
        LowestAsk = _snapshots.Min(s => s.AskPrice),
        TotalVolume = _snapshots.Sum(s => s.Volume)
    };
}

public class MarketSummary
{
    public int TotalSnapshots { get; set; }
    public decimal AverageSpread { get; set; }
    public decimal HighestBid { get; set; }
    public decimal LowestAsk { get; set; }
    public int TotalVolume { get; set; }
}
```

---

## 7. Validation Checklist (5 min)

### LINQ
- [ ] I can filter collections with `Where`
- [ ] I can transform collections with `Select`
- [ ] I can aggregate data (`Sum`, `Average`, `Max`, `Min`)
- [ ] I can group data with `GroupBy`
- [ ] I can sort with `OrderBy` and `OrderByDescending`
- [ ] I can chain LINQ operations

### Async/Await
- [ ] I understand `async` and `await` keywords
- [ ] I know difference between `Task` and `Task<T>`
- [ ] I can use `Task.WhenAll` for parallel operations
- [ ] I avoid blocking with `.Result` or `.Wait()`

### Modern C# Features
- [ ] I can use auto-properties
- [ ] I can write expression-bodied members (`=>`)
- [ ] I can use switch expressions
- [ ] I can create extension methods

### Practice
- [ ] I completed LINQ challenge exercise
- [ ] I built PowerPriceDataHandler class
- [ ] I tested with sample data

---

## 🎯 Key Takeaways

1. **LINQ is powerful** - Master it for data manipulation in backtests
2. **Async/await for I/O** - Non-blocking API calls and file operations
3. **Modern C# is concise** - Use expression bodies and pattern matching
4. **Extension methods extend** - Add functionality without modifying types
5. **Practice with LEAN context** - Apply syntax to actual trading scenarios

---

## Next Tutorial

**Tutorial 07: Project Planning and CI/CD for C#**
- Architecture planning for C# components
- Automated testing with xUnit
- GitHub Actions for LEAN
- Deployment strategies

**Time to Complete:** 2 hours

---

**🎓 Congratulations!** You now have solid C# syntax knowledge applied to LEAN development. You're ready to write and review production C# code.

*Mark this tutorial as complete in the main README.md*

---

*Last Updated: 2025-11-16*
