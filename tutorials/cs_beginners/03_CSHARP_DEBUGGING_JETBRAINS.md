# Tutorial 03: C# Debugging in JetBrains IDEs

**Duration:** 90 minutes (20 min reading + 70 min hands-on)
**Prerequisites:** Tutorial 02 completed, Rider or PyCharm Professional installed
**Goal:** Master C# debugging in Rider/PyCharm for LEAN development

---

## 📋 Table of Contents

1. [Overview](#1-overview-5-min)
2. [Rider vs PyCharm Professional](#2-rider-vs-pycharm-professional-10-min)
3. [Setting Up C# Debugging in Rider](#3-setting-up-c-debugging-in-rider-15-min)
4. [Debugging C# Algorithms](#4-debugging-c-algorithms-20-min)
5. [Advanced Debugging Techniques](#5-advanced-debugging-techniques-20-min)
6. [Debugging LEAN Engine Code](#6-debugging-lean-engine-code-15-min)
7. [Common Pitfalls](#7-common-pitfalls-5-min)
8. [Validation Checklist](#8-validation-checklist-5-min)

---

## 1. Overview (5 min)

### Why JetBrains for LEAN?

**Rider Advantages:**
- Native C# debugging (faster than VS Code)
- Seamless Python + C# in one IDE
- Excellent performance profiling
- Familiar UI if using PyCharm

**PyCharm Professional:**
- Can debug C# via Rider plugin (limited)
- Better for Python-first development
- **Recommendation:** Use Rider for C# debugging

---

### What You'll Learn

```
✓ Set up Rider to debug LEAN C# code
✓ Place breakpoints in C# algorithms
✓ Step through C# engine code
✓ Inspect variables and call stacks
✓ Debug C# and Python simultaneously
✓ Profile performance bottlenecks
```

---

### Debugging Workflow Overview

```
1. Open LEAN solution in Rider
2. Set breakpoint in C# algorithm or engine code
3. Start debugger (F5 or Ctrl+F5)
4. LEAN runs until breakpoint hit
5. Step through code (F8, F7, F9)
6. Inspect variables, evaluate expressions
7. Continue or stop execution
```

---

## 2. Rider vs PyCharm Professional (10 min)

### Feature Comparison

| Feature | Rider | PyCharm Pro |
|---------|-------|-------------|
| **C# Debugging** | Native, excellent | Plugin-based, basic |
| **Python Debugging** | Excellent | Excellent (native) |
| **LEAN Solution Loading** | Fast, full support | Slow, limited |
| **C# IntelliSense** | Best-in-class | Basic |
| **Performance Profiling** | Built-in | Requires plugin |
| **Memory Analysis** | Built-in | Limited |
| **Price** | $149/year | $199/year |
| **Trial** | 30 days | 30 days |

**Recommendation:**
- **Primarily C# work:** Use Rider
- **Primarily Python work:** Use PyCharm + VS Code for C#
- **Equal C#/Python:** Use Rider (single IDE)

---

### Can PyCharm Debug C#?

**Short Answer:** Limited support

**PyCharm Approach:**
1. Install "Rider Plugin" in PyCharm
2. Opens Rider for C# files
3. Not seamless integration

**Better Approach:**
- Use Rider for LEAN C# development
- Keep PyCharm for pure Python projects
- OR use Rider for both (includes Python support)

---

## 3. Setting Up C# Debugging in Rider (15 min)

### Step 1: Install Rider (If Not Installed)

**Download:**
https://www.jetbrains.com/rider/download/

```powershell
# Download and install Rider
# Start 30-day trial or activate license
```

---

### Step 2: Open LEAN Solution

**Launch Rider:**
```
File → Open
Navigate to: C:\Projects\LEAN
Select: QuantConnect.Lean.sln
Click "Open"
```

**First-Time Setup (automatic):**
```
Rider will:
1. Index solution (~2-3 minutes)
2. Restore NuGet packages
3. Build solution
4. Ready when indexing complete
```

**Check Status Bar:**
```
Bottom of window: "Indexing completed" ✓
```

---

### Step 3: Configure Build Settings

**Open Settings:**
```
File → Settings (Ctrl+Alt+S)
```

**Navigate to:**
```
Build, Execution, Deployment
  → Toolset and Build
    → Use: .NET SDK (MSBuild)
    → MSBuild version: Auto-detect
```

**Apply changes:**
```
Click "OK"
```

---

### Step 4: Create Debug Configuration

**Method 1: Automatic (Recommended)**

Rider auto-detects LEAN's launcher project:

```
Top toolbar → Run Configurations dropdown
Should show: "Launcher" (auto-detected)
```

**Method 2: Manual Creation**

If not auto-detected:

```
Run → Edit Configurations
Click "+" → .NET Project
Name: LEAN Launcher
Project: QuantConnect.Lean.Launcher
Working directory: C:\Projects\LEAN\Launcher\bin\Debug
Click "OK"
```

---

### Step 5: Verify Configuration File

**Critical:** `config.json` must be in build output

```powershell
# From PowerShell or Terminal in Rider
cd C:\Projects\LEAN
copy Launcher\config.json Launcher\bin\Debug\config.json
```

**Rider Terminal:**
```
View → Tool Windows → Terminal (Alt+F12)
# Run copy command above
```

---

## 4. Debugging C# Algorithms (20 min)

### Exercise 1: Debug a Simple C# Algorithm (10 min)

**Step 1: Create Test Algorithm**

Create file: `Algorithm.CSharp\DebugTestAlgorithm.cs`

```csharp
namespace QuantConnect.Algorithm.CSharp
{
    public class DebugTestAlgorithm : QCAlgorithm
    {
        private Symbol _symbol;

        public override void Initialize()
        {
            SetStartDate(2023, 1, 1);
            SetEndDate(2023, 1, 10);
            SetCash(100000);

            // Add SPY equity
            _symbol = AddEquity("SPY", Resolution.Daily).Symbol;

            // Set breakpoint on next line
            Debug("Algorithm initialized");
        }

        public override void OnData(Slice data)
        {
            // Set breakpoint here
            if (!Portfolio.Invested)
            {
                // Set breakpoint here
                SetHoldings(_symbol, 1.0);
                Debug($"Purchased {_symbol} at {Securities[_symbol].Price}");
            }
        }
    }
}
```

**Step 2: Update config.json**

Edit: `Launcher\bin\Debug\config.json`

```json
{
  "algorithm-type-name": "DebugTestAlgorithm",
  "algorithm-language": "CSharp",
  // ... rest of config
}
```

**Step 3: Set Breakpoints**

In Rider, click in left gutter (next to line numbers):

```csharp
public override void Initialize()
{
    SetStartDate(2023, 1, 1);
    SetEndDate(2023, 1, 10);
    SetCash(100000);

    _symbol = AddEquity("SPY", Resolution.Daily).Symbol;

    // ◉ RED DOT = Breakpoint set here
    Debug("Algorithm initialized");
}
```

Set breakpoints at:
1. Line with `Debug("Algorithm initialized")`
2. Line with `if (!Portfolio.Invested)`
3. Line with `SetHoldings(_symbol, 1.0)`

---

**Step 4: Start Debugging**

**Click Debug icon** (bug icon) or press **F5**

```
Top toolbar: Debug button (shift+F9)
OR
Right-click "Launcher" → Debug 'Launcher'
```

**What Happens:**
1. Rider compiles solution
2. Starts LEAN launcher
3. Execution pauses at first breakpoint

---

**Step 5: Inspect State**

When paused at `Debug("Algorithm initialized")`:

**Variables Window** (Auto-opens):
```
this (DebugTestAlgorithm)
  ├─ _symbol: null (not set yet)
  ├─ Time: 2023-01-01 00:00:00
  ├─ Portfolio: { ... }
  └─ Securities: { ... }
```

**Evaluate Expression:**
```
Alt+F8 → Evaluate Expression
Type: Securities.Count
Result: 1 (SPY added)
```

---

**Step 6: Step Through Code**

**Debugger Controls:**

| Action | Shortcut | Description |
|--------|----------|-------------|
| **Step Over** | F8 | Execute current line, move to next |
| **Step Into** | F7 | Enter method call |
| **Step Out** | Shift+F8 | Exit current method |
| **Resume** | F9 | Continue until next breakpoint |
| **Stop** | Ctrl+F2 | Stop debugging |

**Practice:**
1. Press **F8** (Step Over) - moves to next line
2. Watch `_symbol` populate in Variables window
3. Press **F9** (Resume) - continues to next breakpoint
4. Should stop at `if (!Portfolio.Invested)`

---

**Step 7: Inspect Data Slice**

When paused in `OnData`:

**Check data parameter:**
```
Variables window:
data (Slice)
  ├─ Time: 2023-01-02 16:00:00
  ├─ Bars: { SPY: TradeBar {...} }
  ├─ Keys: [SPY]
  └─ ContainsKey("SPY"): true
```

**Evaluate:**
```
Alt+F8 → Evaluate
data.Bars[_symbol].Close
Result: 382.45 (SPY closing price)
```

---

### Exercise 2: Conditional Breakpoints (5 min)

**Scenario:** Only break when price > $400

**Right-click breakpoint** (red dot):
```
More → Condition
Enter: Securities[_symbol].Price > 400
Click "Done"
```

**Breakpoint Changes:**
- Red dot with **question mark (?)**
- Only triggers when condition true

**Test:**
```
F9 (Resume)
Debugger only stops when SPY price > $400
```

**Use Cases:**
- Debug specific market conditions
- Track down intermittent bugs
- Monitor rare events (e.g., price spike)

---

### Exercise 3: Logging Points (5 min)

**Log without stopping execution:**

**Right-click breakpoint:**
```
More → Evaluate and Log
Enter: $"Price: {Securities[_symbol].Price}"
Uncheck "Suspend"
Click "Done"
```

**Breakpoint Changes:**
- Red dot with **diamond (◇)**
- Logs to console without pausing

**Run Debugger (F5):**
```
Debug Output:
Price: 382.45
Price: 385.20
Price: 387.60
...
```

**Use Cases:**
- Monitor values during backtest
- Track execution flow
- Debug without interrupting

---

## 5. Advanced Debugging Techniques (20 min)

### Technique 1: Call Stack Navigation (5 min)

**When paused at breakpoint:**

**Frames Window** (shows call stack):
```
DebugTestAlgorithm.OnData(Slice data) ← Current
  QCAlgorithm.OnData(Slice data)
    Engine.Run()
      Launcher.Main()
```

**Click different frame:**
- Shows code at that level
- Inspect variables at each level
- Understand execution path

**Example:**
```
1. Paused in OnData
2. Click "Engine.Run()" frame
3. See LEAN engine code
4. Inspect engine state
```

---

### Technique 2: Watch Window (5 min)

**Add persistent watched expressions:**

**Watches Tab:**
```
Click "+" to add watch
Enter expressions:
  - Portfolio.TotalPortfolioValue
  - Securities[_symbol].Holdings.Quantity
  - Time.ToString("yyyy-MM-dd HH:mm:ss")
```

**Updates automatically:**
- Each step
- Each breakpoint
- Track multiple values simultaneously

---

### Technique 3: Immediate Window (5 min)

**Execute code during debugging:**

**Open Immediate Window:**
```
Run → Evaluate Expression (Alt+F8)
```

**Execute statements:**
```csharp
// Check portfolio value
Portfolio.TotalPortfolioValue

// Modify state (careful!)
SetHoldings(_symbol, 0.5)

// Call methods
Securities[_symbol].Price
```

**Use Cases:**
- Test expressions before adding to code
- Inspect complex object graphs
- Experiment with LEAN API calls

---

### Technique 4: Exception Breakpoints (5 min)

**Break on any exception thrown:**

**Run → View Breakpoints (Ctrl+Shift+F8)**

```
Click "+"
Select: "Exception Breakpoints"
Choose:
  ☑ System.Exception (catches all)
  ☑ Break when: Thrown
Click "Done"
```

**Now:**
- Debugger stops on ANY exception
- See exact line that threw
- Inspect state before exception

**Useful for:**
- Catching null reference exceptions
- Finding data errors
- Debugging LEAN data feeds

---

## 6. Debugging LEAN Engine Code (15 min)

### Exercise 4: Step Into LEAN Engine (10 min)

**Goal:** Understand how LEAN processes `SetHoldings`

**Step 1: Set Breakpoint in Algorithm**

```csharp
public override void OnData(Slice data)
{
    if (!Portfolio.Invested)
    {
        SetHoldings(_symbol, 1.0);  // ← Breakpoint here
    }
}
```

**Step 2: Start Debugging (F5)**

Execution pauses at breakpoint.

---

**Step 3: Step Into (F7)**

Press **F7** to enter `SetHoldings` method.

**Rider navigates to:**
```
File: Algorithm/QCAlgorithm.Trading.cs
Method: SetHoldings(Symbol symbol, decimal percentage)

public void SetHoldings(Symbol symbol, decimal percentage)
{
    // You're now in LEAN source code!
    SetHoldings(symbol, percentage, false);
}
```

---

**Step 4: Continue Stepping (F7)**

Keep pressing F7:

```
SetHoldings(symbol, percentage, liquidateExistingHoldings)
  ↓
CalculateOrderQuantity(symbol, target)
  ↓
MarketOrder(symbol, quantity)
  ↓
SubmitOrder(order)
```

**Watch Call Stack build up:**
```
Frames:
SubmitOrder          ← Current
MarketOrder
CalculateOrderQuantity
SetHoldings
OnData
```

---

**Step 5: Inspect LEAN Internals**

While in engine code:

```
Variables window shows LEAN internals:
_transactions: TransactionManager
_securities: SecurityManager
_portfolio: SecurityPortfolioManager
```

**Evaluate:**
```
Alt+F8
_portfolio.TotalPortfolioValue
_securities[symbol].Holdings.Quantity
```

---

### Exercise 5: Finding Code from Error (5 min)

**Simulate error:**

```csharp
public override void OnData(Slice data)
{
    // Intentional null reference
    Symbol badSymbol = null;
    SetHoldings(badSymbol, 1.0);  // Will throw!
}
```

**Run without debugger:**
```
Exception in OnData: NullReferenceException
at DebugTestAlgorithm.OnData(Slice data) in DebugTestAlgorithm.cs:line 25
```

**Find the issue:**
1. Click stack trace line in console
2. Rider jumps to exact line
3. Set breakpoint, debug again
4. Step through to understand

---

## 7. Common Pitfalls (5 min)

### Pitfall 1: Breakpoints Not Hitting

**Symptom:** Breakpoint ignored, code runs through

**Causes:**
1. **Code not executed** - Check algorithm logic
2. **Old build** - Clean and rebuild
3. **Wrong configuration** - config.json points to different algorithm

**Fix:**
```powershell
# Clean rebuild
dotnet clean
dotnet build

# Verify config.json
cat Launcher\bin\Debug\config.json | Select-String "algorithm-type-name"
```

---

### Pitfall 2: "Source Not Available"

**Symptom:** Stepped into method, shows "Source not available"

**Cause:** Trying to step into .NET framework code (no source)

**Fix:**
- Press **Shift+F8** (Step Out)
- Don't step into framework methods
- Use **F8** (Step Over) instead of F7

---

### Pitfall 3: Debugger Too Slow

**Symptom:** Each step takes seconds

**Cause:** Evaluating large collections in Variables window

**Fix:**
```
Settings → Build, Execution, Deployment
  → Debugger
    → Data Views
      ☐ Enable auto-evaluation
```

**OR:**
- Collapse large collections in Variables window
- Use specific watches instead of expanding all

---

### Pitfall 4: Modified Code Not Reflecting

**Symptom:** Changes not visible in debugger

**Cause:** Need to rebuild after code changes

**Fix:**
```
1. Stop debugger (Ctrl+F2)
2. Build solution (Ctrl+F9)
3. Start debugging again (Shift+F9)
```

**Note:** Rider supports "Hot Reload" for some changes (limited in C#)

---

## 8. Validation Checklist (5 min)

### Basic Debugging
- [ ] I can set breakpoints in C# algorithm code
- [ ] Breakpoints hit when debugging (F5)
- [ ] I can step over (F8), step into (F7), step out (Shift+F8)
- [ ] Variables window shows current state
- [ ] I can evaluate expressions (Alt+F8)

### Advanced Techniques
- [ ] I can set conditional breakpoints
- [ ] I can create logging points (tracepoints)
- [ ] Call stack window shows execution path
- [ ] Watch window tracks persistent expressions
- [ ] Exception breakpoints catch errors

### LEAN-Specific
- [ ] I can step into LEAN engine code (QCAlgorithm methods)
- [ ] I understand how SetHoldings flows through engine
- [ ] I can inspect LEAN internals (Portfolio, Securities)
- [ ] I can navigate call stack from algorithm → engine → launcher

### Troubleshooting
- [ ] I know how to verify config.json settings
- [ ] I can clean and rebuild if breakpoints don't hit
- [ ] I understand when to use Step Over vs Step Into

---

## 📚 Further Reading

**Rider Documentation:**
- [Debugger Basics](https://www.jetbrains.com/help/rider/Debugging_Code.html)
- [Advanced Debugging](https://www.jetbrains.com/help/rider/Advanced_Debugging.html)

**LEAN Code to Explore:**
- `Algorithm/QCAlgorithm.Trading.cs` - Order methods
- `Engine/Engine.cs` - Main engine loop
- `Common/Securities/SecurityPortfolioManager.cs` - Portfolio management

---

## 🎯 Key Takeaways

1. **Rider is excellent for C# debugging** - Native support, fast performance
2. **F7 = Step Into** - Explore LEAN engine internals
3. **Conditional breakpoints** - Debug specific scenarios
4. **Call stack navigation** - Understand execution flow
5. **Step through engine code** - Learn how LEAN works internally

---

## ⏭️ Next Tutorial

**Tutorial 04: C# Debugging in VS Code**
- Configure C# Dev Kit for debugging
- Create launch configurations
- Debug C# and Python simultaneously
- Compare VS Code vs Rider workflow

**Time to Complete:** 60 minutes

---

**🎓 Congratulations!** You can now debug C# code in Rider like a pro. You're ready to explore LEAN's engine and debug complex algorithms.

*Mark this tutorial as complete in the main README.md*

---

*Last Updated: 2025-11-16*
