# Tutorial 07: Project Planning and CI/CD for C#

**Duration:** 120 minutes (40 min reading + 80 min hands-on)
**Prerequisites:** Tutorial 06 completed
**Goal:** Set up professional workflows for LEAN C# development

---

## 📋 Table of Contents

1. [Overview - Professional C# Development](#1-overview---professional-c-development-5-min)
2. [Architecture Planning for C# Components](#2-architecture-planning-for-c-components-20-min)
3. [Automated Testing with GitHub Actions](#3-automated-testing-with-github-actions-25-min)
4. [Performance Benchmarking Automation](#4-performance-benchmarking-automation-20-min)
5. [Deployment Strategies](#5-deployment-strategies-15-min)
6. [Documentation and Maintenance](#6-documentation-and-maintenance-10-min)
7. [Validation Checklist](#7-validation-checklist-5-min)

---

## 1. Overview - Professional C# Development (5 min)

### From Learner to Professional

**You've learned:**
- ✅ C# syntax and fundamentals
- ✅ Debugging in multiple IDEs
- ✅ Testing and code review
- ✅ Cross-platform development (Windows/WSL)

**Now add:**
- 🎯 Professional project planning
- 🎯 Automated CI/CD pipelines
- 🎯 Performance benchmarking
- 🎯 Deployment automation

---

## 2. Architecture Planning for C# Components (20 min)

### LEAN Extension Points

**Where to add your C# code:**

```
1. Custom Security Types
   → Common/Securities/[NewType]/

2. Custom Data Handlers
   → Common/Data/Custom/

3. Brokerage Integrations
   → Brokerages/[NewBrokerage]/

4. Algorithm Extensions
   → Algorithm/[Feature]/
```

---

### Exercise 1: Design PowerDelivery Security Type (15 min)

**Requirements:**
- Represent power contracts with delivery periods
- Support orderbook data
- Enable backtesting with intraday data

**Architecture Plan:**

```
Project: QuantConnect.Securities.Power
Location: Common/Securities/Power/

Files:
├── PowerDelivery.cs              # Main security class
├── PowerDeliveryHolding.cs       # Position tracking
├── PowerDeliveryCache.cs         # Data caching
├── PowerDeliveryMarginModel.cs   # Margin calculations
└── PowerDeliveryExchange.cs      # Market hours, fees

Dependencies:
- QuantConnect.Common (core types)
- QuantConnect.Data (BaseData)

Performance Target:
- Process 10K contracts in < 50ms
- Memory: < 100 MB for 100K orderbooks
```

**Design Document Template:**

```markdown
# PowerDelivery Security Type

## Overview
Custom security type for European power intraday markets.

## Architecture

### Class Hierarchy
```
Security (LEAN base)
  └── PowerDelivery (new)
        ├── Properties: ContractId, DeliveryStart, Duration
        ├── Methods: UpdateOrderBook(), CalculateMargin()
        └── Events: OnOrderBookUpdate
```

### Data Flow
1. Parquet files → PowerOrderBookReader
2. Reader → PowerDelivery.UpdateOrderBook()
3. PowerDelivery → Algorithm.OnData()

### Performance Considerations
- Struct-based orderbook (28 bytes)
- Object pooling for repeated allocations
- Memory-mapped file reading

### Testing Strategy
- Unit tests: Each class independently
- Integration tests: Full backtest with sample data
- Performance tests: 10K contracts benchmark

### Risks & Mitigations
- Risk: High cardinality (10K+ contracts)
- Mitigation: Efficient data structures, lazy loading

### Implementation Phases
1. Week 1: Core PowerDelivery class
2. Week 2: Orderbook integration
3. Week 3: Margin and risk models
4. Week 4: Testing and optimization
```

---

## 3. Automated Testing with GitHub Actions (25 min)

### Setting Up CI/CD

**Goal:** Auto-test every commit

---

### Exercise 2: Create GitHub Actions Workflow (20 min)

**Step 1: Create workflow file**

`.github/workflows/dotnet-ci.yml`

```yaml
name: .NET CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: '9.0.x'

    - name: Restore dependencies
      run: dotnet restore QuantConnect.Lean.sln

    - name: Build
      run: dotnet build QuantConnect.Lean.sln --no-restore --configuration Release

    - name: Run tests
      run: dotnet test --no-build --configuration Release --verbosity normal

    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: '**/TestResults/*.trx'
```

---

**Step 2: Add test coverage**

Update workflow to include coverage:

```yaml
    - name: Run tests with coverage
      run: dotnet test --no-build --configuration Release --collect:"XPlat Code Coverage"

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: '**/coverage.cobertura.xml'
```

---

**Step 3: Add matrix testing**

Test across multiple .NET versions:

```yaml
jobs:
  build-and-test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        dotnet-version: ['8.0.x', '9.0.x']

    steps:
    - name: Setup .NET ${{ matrix.dotnet-version }}
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: ${{ matrix.dotnet-version }}
    # ... rest of workflow
```

---

**Step 4: Commit and push**

```bash
git add .github/workflows/dotnet-ci.yml
git commit -m "Add CI/CD pipeline for automated testing"
git push origin main
```

**Verify on GitHub:**
- Navigate to repository → Actions tab
- See workflow running
- Green checkmark = all tests passed

---

## 4. Performance Benchmarking Automation (20 min)

### BenchmarkDotNet Integration

**Install BenchmarkDotNet:**

```powershell
cd Tests/Performance
dotnet add package BenchmarkDotNet
```

---

### Exercise 3: Create Performance Benchmark (15 min)

**File:** `Tests/Performance/PowerOrderBookBenchmarks.cs`

```csharp
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

namespace QuantConnect.Tests.Performance
{
    [MemoryDiagnoser]
    [SimpleJob(iterationCount: 100)]
    public class PowerOrderBookBenchmarks
    {
        private List<PowerOrderBook> _orderBooks;

        [GlobalSetup]
        public void Setup()
        {
            // Prepare test data
            _orderBooks = Enumerable.Range(0, 10000)
                .Select(i => new PowerOrderBook
                {
                    Symbol = $"EPEX-GB-HH-{i}",
                    BidPrice = 65.50m + i * 0.01m,
                    AskPrice = 65.75m + i * 0.01m
                })
                .ToList();
        }

        [Benchmark]
        public void ProcessOrderBooks_Old()
        {
            // Old implementation
            foreach (var ob in _orderBooks)
            {
                var spread = ob.AskPrice - ob.BidPrice;
                // Process...
            }
        }

        [Benchmark]
        public void ProcessOrderBooks_New()
        {
            // Claude's optimized version
            foreach (var ob in _orderBooks)
            {
                var spread = ob.Spread;  // Cached property
                // Process...
            }
        }

        [Benchmark]
        public decimal CalculateAverageSpread()
        {
            return _orderBooks.Average(ob => ob.Spread);
        }
    }

    public class Program
    {
        public static void Main(string[] args)
        {
            var summary = BenchmarkRunner.Run<PowerOrderBookBenchmarks>();
        }
    }
}
```

---

**Run benchmark:**

```powershell
cd Tests/Performance
dotnet run -c Release

# Output:
|                    Method |     Mean |   Gen0 | Allocated |
|-------------------------- |---------:|-------:|----------:|
|  ProcessOrderBooks_Old    | 125.2 μs |      - |       0 B |
|  ProcessOrderBooks_New    |  85.3 μs |      - |       0 B |
| CalculateAverageSpread    |  45.6 μs |      - |       0 B |

# Speedup: 125.2 / 85.3 = 1.47x (47% faster)
```

---

### Automate Benchmarks in CI

**Add to GitHub Actions:**

``yaml
    - name: Run performance benchmarks
      run: dotnet run --project Tests/Performance/QuantConnect.Tests.Performance.csproj -c Release

    - name: Upload benchmark results
      uses: actions/upload-artifact@v3
      with:
        name: benchmarks
        path: '**/BenchmarkDotNet.Artifacts/**'
```

---

## 5. Deployment Strategies (15 min)

### Packaging LEAN Extensions

**Create NuGet Package:**

Edit `Common/Securities/Power/QuantConnect.Securities.Power.csproj`:

```xml
<PropertyGroup>
  <PackageId>QuantConnect.Securities.Power</PackageId>
  <Version>1.0.0</Version>
  <Authors>Your Team</Authors>
  <Description>Power delivery security type for LEAN</Description>
  <PackageLicenseExpression>Apache-2.0</PackageLicenseExpression>
</PropertyGroup>
```

**Build package:**

```powershell
dotnet pack Common/Securities/Power/QuantConnect.Securities.Power.csproj -c Release

# Output: bin/Release/QuantConnect.Securities.Power.1.0.0.nupkg
```

**Publish to private NuGet feed:**

```powershell
dotnet nuget push bin/Release/QuantConnect.Securities.Power.1.0.0.nupkg \
  --source https://your-nuget-server.com/v3/index.json \
  --api-key YOUR_API_KEY
```

---

### Docker Containerization

**Create:** `Dockerfile`

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy solution
COPY QuantConnect.Lean.sln .
COPY Common/ Common/
COPY Engine/ Engine/
COPY Launcher/ Launcher/

# Restore and build
RUN dotnet restore
RUN dotnet build -c Release --no-restore

# Runtime image
FROM mcr.microsoft.com/dotnet/runtime:9.0
WORKDIR /app
COPY --from=build /src/Launcher/bin/Release/ .

ENTRYPOINT ["dotnet", "QuantConnect.Lean.Launcher.dll"]
```

**Build and run:**

```bash
docker build -t lean-power:latest .
docker run -v $(pwd)/config.json:/app/config.json lean-power:latest
```

---

## 6. Documentation and Maintenance (10 min)

### XML Documentation Comments

**Document public APIs:**

```csharp
/// <summary>
/// Represents a power delivery contract for intraday trading
/// </summary>
/// <remarks>
/// Supports hourly and half-hourly delivery periods.
/// Compatible with EPEX SPOT market data.
/// </remarks>
public class PowerDelivery : Security
{
    /// <summary>
    /// Gets the contract delivery start time (UTC)
    /// </summary>
    public DateTime DeliveryStart { get; }

    /// <summary>
    /// Gets the contract duration in hours
    /// </summary>
    public decimal DurationHours { get; }

    /// <summary>
    /// Updates the orderbook with new bid/ask levels
    /// </summary>
    /// <param name="bidPrice">New bid price in EUR/MWh</param>
    /// <param name="askPrice">New ask price in EUR/MWh</param>
    /// <exception cref="ArgumentException">
    /// Thrown when askPrice is less than bidPrice
    /// </exception>
    public void UpdateOrderBook(decimal bidPrice, decimal askPrice)
    {
        if (askPrice < bidPrice)
            throw new ArgumentException("Ask must be >= Bid");

        // Implementation...
    }
}
```

**Generate documentation:**

```powershell
dotnet build /p:GenerateDocumentationFile=true
# Produces XML file: bin/Release/QuantConnect.Securities.Power.xml
```

---

### README for Custom Component

**Create:** `Common/Securities/Power/README.md`

```markdown
# PowerDelivery Security Type

Custom LEAN security type for European power intraday markets.

## Features
- Hourly and half-hourly contract support
- Orderbook data integration
- Margin and risk models
- Backtesting with historical data

## Usage

```csharp
public class PowerAlgorithm : QCAlgorithm
{
    public override void Initialize()
    {
        var symbol = AddSecurity(
            SecurityType.Power,
            "EPEX-GB-HH-14",
            Resolution.Minute
        ).Symbol;
    }
}
```

## Performance
- Processes 10K contracts in 45ms
- Memory: 80 MB for 100K orderbooks

## Testing
```bash
dotnet test Tests/Common/PowerDeliveryTests.cs
```

## License
Apache 2.0
```

---

## 7. Validation Checklist (5 min)

### Architecture Planning
- [ ] I can design C# components for LEAN
- [ ] I create design documents before coding
- [ ] I identify dependencies and risks
- [ ] I plan implementation in phases

### CI/CD
- [ ] I've set up GitHub Actions workflow
- [ ] Automated tests run on every commit
- [ ] I understand matrix testing (multiple OS/versions)
- [ ] Code coverage is tracked

### Benchmarking
- [ ] I can write BenchmarkDotNet tests
- [ ] I measure performance objectively
- [ ] I track performance over time
- [ ] Benchmarks run in CI pipeline

### Deployment
- [ ] I can create NuGet packages
- [ ] I understand versioning (SemVer)
- [ ] I can build Docker containers
- [ ] Documentation is up-to-date

---

## 🎯 Key Takeaways

1. **Plan before coding** - Design documents prevent rework
2. **Automate everything** - CI/CD catches bugs early
3. **Measure performance** - Benchmarks prove optimizations
4. **Document thoroughly** - XML comments + READMEs
5. **Package properly** - NuGet for distribution, Docker for deployment

---

## 🏆 Series Complete!

**Congratulations!** You've completed all 10 tutorials in the C# for Beginners series.

### What You've Learned

**Foundations:**
- ✅ C# syntax, types, and patterns
- ✅ LINQ, async/await, modern C# features

**Development:**
- ✅ Setup on Windows and WSL
- ✅ Debugging in Rider, VS Code, Visual Studio
- ✅ Environment and package management

**Professional Skills:**
- ✅ Testing (unit, integration, performance)
- ✅ Code review for AI-generated code
- ✅ CI/CD automation
- ✅ Architecture planning and deployment

### You're Now Ready To:

1. **Implement PowerDelivery security type** (LEAN engine extension)
2. **Build EPEX brokerage integration** (API connection)
3. **Create high-performance data handlers** (Parquet reading)
4. **Contribute to LEAN project** (open source)
5. **Collaborate with Claude on C# development** (safely!)

---

## 📚 Further Learning

**Advanced Topics:**
- Performance optimization (profiling, memory management)
- Parallel programming (TPL, async patterns)
- Design patterns (Gang of Four, SOLID principles)
- Financial mathematics (options pricing, risk models)

**LEAN Mastery:**
- Study existing brokerages (InteractiveBrokers, Coinbase)
- Explore LEAN engine internals (Engine/Engine.cs)
- Build custom indicators
- Optimize algorithm performance

**Energy Markets:**
- Understand power market mechanics
- Study orderbook dynamics
- Learn bid/ask spread strategies
- Research market microstructure

---

## 🎓 Final Checklist

- [ ] All 7 tutorials marked complete in README.md
- [ ] Practice exercises completed
- [ ] GitHub Actions workflow set up
- [ ] First benchmark written and run
- [ ] Ready to begin PowerDelivery implementation

---

**Thank you for completing this series! You're now equipped to develop production-quality C# code for LEAN energy trading systems.**

*Update your progress in the main README.md*

---

*Last Updated: 2025-11-16*
*Series Version: 1.0*
