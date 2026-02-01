# Tutorial 04: C# Debugging in VS Code

**Duration:** 60 minutes (15 min reading + 45 min hands-on)
**Prerequisites:** Tutorial 02 completed, VS Code installed
**Goal:** Debug C# code in VS Code for LEAN development

---

## 📋 Table of Contents

1. [Overview](#1-overview-5-min)
2. [C# Dev Kit Configuration](#2-c-dev-kit-configuration-10-min)
3. [Launch Configurations for LEAN](#3-launch-configurations-for-lean-15-min)
4. [Debugging C# Algorithms](#4-debugging-c-algorithms-15-min)
5. [Debugging C# and Python Together](#5-debugging-c-and-python-together-10-min)
6. [VS Code vs Rider Comparison](#6-vs-code-vs-rider-comparison-5-min)
7. [Validation Checklist](#7-validation-checklist-5-min)

---

## 1. Overview (5 min)

### VS Code for C# Debugging

**Strengths:**
- ✅ Lightweight and fast
- ✅ Free and open source
- ✅ Excellent Python support (already configured)
- ✅ Good C# debugging via C# Dev Kit

**Limitations:**
- ⚠️ Slower IntelliSense than Rider/Visual Studio
- ⚠️ Less integrated profiling tools
- ⚠️ Manual launch configuration required

**Best For:**
- Quick edits and debugging
- Python-first development with occasional C#
- Teams wanting standardized tooling

---

### What You'll Configure

```
1. C# Dev Kit extension (Microsoft)
2. Launch configurations (.vscode/launch.json)
3. Breakpoints and debugging workflow
4. Simultaneous C# + Python debugging
```

---

## 2. C# Dev Kit Configuration (10 min)

### Step 1: Verify Extensions

**Open Extensions** (Ctrl+Shift+X)

**Required Extensions:**
```
✓ C# Dev Kit (ms-dotnettools.csdevkit)
✓ C# (ms-dotnettools.csharp) - auto-installed with Dev Kit
✓ Python (ms-python.python)
```

**If not installed:**
```
Search: "C# Dev Kit"
Click: Install
Wait for C# extension to install automatically
Reload VS Code if prompted
```

---

### Step 2: Open LEAN Project

```
File → Open Folder
Navigate to: C:\Projects\LEAN
Click "Select Folder"
```

**VS Code will:**
1. Detect `.sln` file
2. Load C# project structure
3. Show "Solution Explorer" in sidebar
4. Index C# code (~1-2 minutes)

**Check Bottom Bar:**
```
C# (Indexing...) → C# (Ready) ✓
```

---

### Step 3: Verify Solution Loaded

**Solution Explorer Panel:**
```
QUANTCONNECT.LEAN (solution)
├── QuantConnect.Configuration
├── QuantConnect.Lean.Engine
├── QuantConnect.Lean.Launcher
├── Algorithm.CSharp
└── ... (other projects)
```

**If not visible:**
```
View → Open View → Solution Explorer
OR
Click C# icon in left sidebar
```

---

## 3. Launch Configurations for LEAN (15 min)

### Understanding launch.json

**File:** `.vscode/launch.json`

Defines how to run and debug applications:
- What executable to run
- Working directory
- Environment variables
- Debugger settings

---

### Exercise 1: Create C# Debug Configuration (10 min)

**Step 1: Open Debug Panel**

```
View → Run (Ctrl+Shift+D)
OR
Click Debug icon in left sidebar (bug with play button)
```

**Step 2: Create launch.json**

If `.vscode/launch.json` doesn't exist:

```
Click "create a launch.json file"
Select: "C#"
Select template: ".NET Core Launch (console)"
```

**Step 3: Configure for LEAN**

Edit `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug LEAN C# Algorithm",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "build",
            "program": "${workspaceFolder}/Launcher/bin/Debug/QuantConnect.Lean.Launcher.dll",
            "args": [],
            "cwd": "${workspaceFolder}/Launcher/bin/Debug",
            "console": "internalConsole",
            "stopAtEntry": false,
            "justMyCode": false
        }
    ]
}
```

**Key Settings:**
- `program`: Path to LEAN launcher DLL
- `cwd`: Working directory (where config.json lives)
- `justMyCode: false`: Allows stepping into LEAN engine code

---

**Step 4: Create Build Task**

**File:** `.vscode/tasks.json`

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "command": "dotnet",
            "type": "process",
            "args": [
                "build",
                "${workspaceFolder}/QuantConnect.Lean.sln",
                "/property:GenerateFullPaths=true",
                "/consoleloggerparameters:NoSummary"
            ],
            "problemMatcher": "$msCompile"
        }
    ]
}
```

**Purpose:**
- `preLaunchTask: "build"` in launch.json runs this before debugging
- Ensures latest code is compiled

---

### Exercise 2: Verify Configuration (5 min)

**Step 1: Ensure config.json exists**

```powershell
# In VS Code terminal (Ctrl+`)
cp Launcher/config.json Launcher/bin/Debug/config.json
```

**Step 2: Update algorithm in config.json**

Edit `Launcher/bin/Debug/config.json`:

```json
{
  "algorithm-type-name": "BasicTemplateFrameworkAlgorithm",
  "algorithm-language": "CSharp",
  "data-folder": "../../../Data"
}
```

**Step 3: Test Build**

```
Terminal → Run Build Task (Ctrl+Shift+B)
Select: "build"
Check OUTPUT tab: "Build succeeded"
```

---

## 4. Debugging C# Algorithms (15 min)

### Exercise 3: First C# Debugging Session (10 min)

**Step 1: Open Algorithm File**

```
File Explorer (Ctrl+Shift+E)
Navigate: Algorithm.CSharp/BasicTemplateFrameworkAlgorithm.cs
```

**Step 2: Set Breakpoint**

Find `Initialize()` method:

```csharp
public override void Initialize()
{
    SetStartDate(2013, 10, 07);  // ← Click left gutter here
    SetEndDate(2013, 10, 11);
    SetCash(100000);

    AddEquity("SPY", Resolution.Minute);
}
```

**Red dot appears** = Breakpoint set

---

**Step 3: Start Debugging**

```
Run → Start Debugging (F5)
OR
Debug panel → Click green play button
```

**What Happens:**
1. VS Code runs build task
2. Compiles LEAN
3. Starts launcher
4. Execution pauses at breakpoint

---

**Step 4: Debug Controls**

**Toolbar appears at top:**

| Button | Action | Shortcut |
|--------|--------|----------|
| ▶️ Continue | Resume execution | F5 |
| ⤵️ Step Over | Execute line, move next | F10 |
| ⬇️ Step Into | Enter method call | F11 |
| ⬆️ Step Out | Exit current method | Shift+F11 |
| 🔄 Restart | Restart debugging | Ctrl+Shift+F5 |
| ⏹️ Stop | Stop debugging | Shift+F5 |

**Key Difference from Rider:**
- VS Code: F10 (Step Over), F11 (Step Into)
- Rider: F8 (Step Over), F7 (Step Into)

---

**Step 5: Inspect Variables**

**Variables Panel** (left sidebar):

```
Local
├── this (BasicTemplateFrameworkAlgorithm)
│   ├── StartDate: 2013-10-07
│   ├── EndDate: 2013-10-11
│   ├── Cash: 100000
│   └── Securities: {}
```

**Watch Panel:**
```
Click "+" to add watch
Enter: Time
Shows: 2013-10-07 00:00:00
```

---

**Step 6: Step Through Code**

```
Press F10 (Step Over) 4 times
Watch variables update:
  - SetStartDate executes
  - SetEndDate executes
  - SetCash executes
  - AddEquity executes
```

**Check Securities collection:**
```
Variables → this → Securities → Count: 1
Expand: Securities[0] → Symbol: "SPY"
```

---

### Exercise 4: Conditional Breakpoint (5 min)

**Right-click breakpoint** (red dot):

```
Select: "Edit Breakpoint"
Choose: "Expression"
Enter: Portfolio.TotalPortfolioValue > 100000
Press Enter
```

**Breakpoint changes:**
- Red dot with white center (conditional)

**Run debugger (F5):**
- Only stops when condition true
- Useful for tracking profitable trades

---

## 5. Debugging C# and Python Together (10 min)

### Simultaneous Debugging Setup

**Goal:** Debug C# engine AND Python algorithm together

---

**Step 1: Add Python Debug Configuration**

Edit `.vscode/launch.json`, add second configuration:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug LEAN C# Algorithm",
            "type": "coreclr",
            // ... existing config
        },
        {
            "name": "Attach to LEAN Python",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/Algorithm.Python",
                    "remoteRoot": "."
                }
            ]
        }
    ]
}
```

---

**Step 2: Update config.json for Python Debugging**

Edit `Launcher/bin/Debug/config.json`:

```json
{
  "algorithm-type-name": "BasicTemplateAlgorithm",
  "algorithm-language": "Python",
  "debugging": true,
  "debugging-method": "DebugPy"
}
```

---

**Step 3: Debugging Workflow**

**Method 1: Python Only**

```
1. Set breakpoint in Python algorithm
2. Select "Attach to LEAN Python" in dropdown
3. Press F5
4. Start LEAN from terminal:
   cd Launcher/bin/Debug
   dotnet QuantConnect.Lean.Launcher.dll
5. VS Code attaches when Python starts
```

**Method 2: C# and Python (Advanced)**

```
1. Set breakpoints in both C# and Python
2. Start "Debug LEAN C# Algorithm" (F5)
3. When Python code loads, switch to "Attach to LEAN Python"
4. Click attach
5. Both debuggers active simultaneously
```

---

**Step 4: Test Python Debugging**

File: `Algorithm.Python/BasicTemplateAlgorithm.py`

```python
def Initialize(self):
    self.SetStartDate(2013, 10, 7)  # ← Set breakpoint
    self.SetEndDate(2013, 10, 11)
    self.SetCash(100000)
    self.AddEquity("SPY", Resolution.Minute)
```

**Run:**
```
Select: "Attach to LEAN Python"
F5 → Waiting for connection
Terminal: dotnet QuantConnect.Lean.Launcher.dll
Breakpoint hits → Inspect variables
```

---

## 6. VS Code vs Rider Comparison (5 min)

### Feature Comparison

| Feature | VS Code | Rider |
|---------|---------|-------|
| **Setup Complexity** | Manual launch.json | Auto-detect |
| **Debugging Speed** | Fast | Faster |
| **IntelliSense** | Good | Excellent |
| **Stepping Into LEAN** | Requires `justMyCode: false` | Automatic |
| **Python + C# Together** | Possible (manual) | Seamless |
| **Memory Usage** | Low (~300 MB) | Medium (~800 MB) |
| **Cost** | Free | $149/year |

---

### When to Use Which

**Use VS Code When:**
- Quick debugging sessions
- Already using VS Code for Python
- Lightweight environment preferred
- Free tooling required

**Use Rider When:**
- Heavy C# development
- Need advanced profiling
- Want seamless Python+C# switching
- Budget allows commercial tool

**Hybrid Approach:**
- Primary: VS Code (daily work)
- Secondary: Rider (complex debugging)

---

## 7. Validation Checklist (5 min)

### Configuration
- [ ] C# Dev Kit extension installed and active
- [ ] LEAN solution loaded in Solution Explorer
- [ ] `.vscode/launch.json` configured for LEAN
- [ ] `.vscode/tasks.json` configured for build
- [ ] `config.json` copied to `Launcher/bin/Debug/`

### C# Debugging
- [ ] Can set breakpoints in C# algorithm code
- [ ] F5 starts debugging and hits breakpoints
- [ ] F10 steps over, F11 steps into methods
- [ ] Variables panel shows current state
- [ ] Can evaluate expressions in Debug Console
- [ ] Conditional breakpoints work

### Python Debugging (Optional)
- [ ] Python debug configuration added to launch.json
- [ ] Can attach to Python debugging (port 5678)
- [ ] Breakpoints in Python algorithm hit

### Understanding
- [ ] I know difference between F10 (step over) and F11 (step into)
- [ ] I understand launch.json structure
- [ ] I can switch between debug configurations
- [ ] I know how to build before debugging (Ctrl+Shift+B)

---

## 🔧 Troubleshooting

### Issue: "Cannot find task 'build'"

**Fix:**
1. Ensure `.vscode/tasks.json` exists
2. Verify `label: "build"` matches `preLaunchTask` in launch.json

---

### Issue: Breakpoints not hitting

**Check:**
```json
// In launch.json
"console": "internalConsole",  // NOT "externalTerminal"
"justMyCode": false,           // Allow stepping into LEAN
```

**Also verify:**
```
Algorithm in config.json matches file with breakpoint
```

---

### Issue: "The .NET Core SDK cannot be located"

**Fix:**
```powershell
# Restart VS Code
# OR
Ctrl+Shift+P → "Reload Window"
```

**Verify SDK:**
```powershell
dotnet --version
# Should show 9.0.xxx
```

---

## 📚 Further Reading

**Essential:**
- [VS Code C# Debugging](https://code.visualstudio.com/docs/csharp/debugging)
- [Launch Configuration](https://code.visualstudio.com/docs/editor/debugging#_launch-configurations)

**Setup Guide:**
- Refer to `docs/SETUP_WINDOWS_VSCODE.md` for comprehensive setup

---

## 🎯 Key Takeaways

1. **C# Dev Kit enables C# debugging** - Free, lightweight alternative to Rider
2. **launch.json is critical** - Defines how to run and debug
3. **F10 = Step Over, F11 = Step Into** - Different shortcuts than Rider
4. **Can debug C# and Python together** - Requires two configurations
5. **justMyCode: false** - Allows exploring LEAN engine code

---

## ⏭️ Next Tutorial

**Tutorial 05: Environment Management on Windows**
- .NET SDK versioning
- NuGet package management
- Solution file management
- Dependency resolution

**Time to Complete:** 45 minutes

---

**🎓 Congratulations!** You can now debug C# code in VS Code. You have a lightweight, free debugging environment for LEAN development.

*Mark this tutorial as complete in the main README.md*

---

*Last Updated: 2025-11-16*
