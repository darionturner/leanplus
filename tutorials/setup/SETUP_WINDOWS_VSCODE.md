# Visual Studio Code Setup Guide for LEAN Energy Trading

**Project:** LEAN Algorithmic Trading Engine - Energy Market Adaptation
**Environment:** Windows 10/11
**Purpose:** Secondary IDE for LEAN development (learning, C# debugging, lightweight editing)
**Prerequisites:** Phase 1 Complete (Windows Native with PyCharm)
**Estimated Time:** 45-60 minutes

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites Verification](#prerequisites-verification)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Building LEAN](#building-lean)
6. [Debugging C# Algorithms](#debugging-c-algorithms)
7. [Debugging Python Algorithms](#debugging-python-algorithms)
8. [Comparison with PyCharm](#comparison-with-pycharm)
9. [Troubleshooting](#troubleshooting)
10. [Quick Reference](#quick-reference)

---

## Overview

### Why VS Code for LEAN?

Visual Studio Code provides a **lightweight, versatile environment** for LEAN development, complementing PyCharm Professional:

**VS Code Advantages:**
- ✅ **Free and open-source** (PyCharm Professional requires license)
- ✅ **Excellent C# debugging** via C# Dev Kit
- ✅ **Fast startup** (lighter than PyCharm)
- ✅ **Git integration** out of the box
- ✅ **Preconfigured** - LEAN repository includes `.vscode/` configs
- ✅ **Cross-platform** (Windows, macOS, Linux)

**VS Code Use Cases:**
- C# debugging and engine development
- Quick edits to configuration files
- Git operations and diff viewing
- Learning LEAN internals (C# codebase exploration)
- Team members without PyCharm licenses

**PyCharm Remains Primary for:**
- Python algorithm development (superior autocomplete)
- Remote debugging Python algorithms
- Complex refactoring

---

## Prerequisites Verification

Before starting, verify Phase 1 is complete:

### Required from Phase 1

```cmd
# Check .NET 9 SDK installed
dotnet --version
# Expected: 9.0.x

# Check Python environment
conda activate lean_py311
python --version
# Expected: Python 3.11.11

# Check LEAN builds
cd C:\Projects\LEAN
dotnet build QuantConnect.Lean.sln
# Expected: Build succeeded, 0 errors

# Check environment variable
echo %PYTHONNET_PYDLL%
# Expected: C:\Users\datu\.conda\envs\lean_py311\python311.dll
```

**If any checks fail:** Complete Phase 1 first (`docs/SETUP_WINDOWS_WSL_NATIVE.md`)

---

## Installation

### Step 1: Download and Install VS Code

**Download:** https://code.visualstudio.com/download

**Select:** Windows x64 User Installer (recommended)

**Installation Options:**

Select **all checkboxes** for convenience:

- ☑ Add "Open with Code" action to Windows Explorer file context menu
- ☑ Add "Open with Code" action to Windows Explorer directory context menu
- ☑ Register Code as an editor for supported file types
- ☑ Add to PATH (enables `code` command in terminal)

**Installation Time:** ~2 minutes

---

### Step 2: Install Required Extensions

Launch VS Code and install essential extensions:

#### Method 1: Via Extensions Panel (Recommended)

1. Click **Extensions** icon (Ctrl+Shift+X) or View → Extensions
2. Search and install the following:

**Essential Extensions:**

| Extension | ID | Purpose |
|-----------|-----|---------|
| **C# Dev Kit** | `ms-dotnettools.csdevkit` | C# debugging, IntelliSense, build tasks |
| **Python** | `ms-python.python` | Python language support, debugging |

**Recommended Extensions:**

| Extension | ID | Purpose |
|-----------|-----|---------|
| **GitLens** | `eamodio.gitlens` | Enhanced Git integration, blame annotations |
| **Markdown All in One** | `yzhang.markdown-all-in-one` | README and docs editing |
| **JSON** | `ZainChen.json` | JSON validation and formatting |
| **.gitignore Generator** | `piotrpalarz.vscode-gitignore-generator` | Generate .gitignore files |

#### Method 2: Via Command Line

Open Command Prompt or PowerShell:

```cmd
code --install-extension ms-dotnettools.csdevkit
code --install-extension ms-python.python
code --install-extension eamodio.gitlens
code --install-extension yzhang.markdown-all-in-one
```

**Verification:**
- Extensions panel (Ctrl+Shift+X) should show all installed extensions
- C# Dev Kit may prompt to install .NET SDK (select "I have .NET SDK" if prompted)

---

## Configuration

### Step 3: Open LEAN Project

**Open Folder:**
1. File → Open Folder (Ctrl+K Ctrl+O)
2. Navigate to `C:\Projects\LEAN`
3. Click **Select Folder**

**Trust Project:**
- VS Code will ask: "Do you trust the authors of the files in this folder?"
- Click **Yes, I trust the authors** (this is your own project)

**Initial Workspace Setup:**
- VS Code reads `.vscode/` configuration automatically
- Wait ~10 seconds for extensions to activate
- Bottom panel may show build/restore tasks running

---

### Step 4: Configure Python Interpreter

VS Code needs to know which Python environment to use:

1. Open any Python file: `Algorithm.Python/BasicTemplateAlgorithm.py`
2. Bottom-right corner shows Python version
3. Click on Python version indicator
4. Select: `Python 3.11.11 ('lean_py311': conda)`
   - If not listed, click "Enter interpreter path..." and navigate to:
     `C:\Users\datu\Miniconda3\envs\lean_py311\python.exe`

**Verify:**
- Bottom-right shows: `3.11.11 ('lean_py311': conda)`
- Open Command Palette (Ctrl+Shift+P)
- Type "Python: Show Interpreter Details"
- Should display full path to conda environment

---

### Step 5: Verify Preconfigured Files

LEAN repository includes VS Code configuration. Verify they exist:

**Check Files:**

```cmd
dir C:\Projects\LEAN\.vscode
```

**Expected Files:**
- `launch.json` - Debugging configurations (C# and Python)
- `tasks.json` - Build tasks (build, rebuild, clean)
- `settings.json` - Workspace settings
- `readme.md` - VS Code usage documentation

**If files are missing:** LEAN repository should have them. Check git status:
```cmd
cd C:\Projects\LEAN
git status
```

**Contents Overview:**

**launch.json** provides two debug configurations:
1. **Launch** - Builds and runs LEAN with C# debugging
2. **Attach to Python** - Connects to Python algorithm (DebugPy method)

**tasks.json** provides build tasks:
1. **build** - Standard build
2. **rebuild** - Clean and rebuild
3. **clean** - Delete build artifacts

---

### Step 6: Update Configuration for Windows Paths

The default `.vscode/launch.json` uses `${workspaceFolder}` which works cross-platform, but verify the build path:

**Check launch.json:**
```json
{
    "name": "Launch",
    "type": "coreclr",
    "request": "launch",
    "preLaunchTask": "build",
    "program": "${workspaceFolder}/Launcher/bin/Debug/QuantConnect.Lean.Launcher.dll",
    "args": [
        "--config",
        "${workspaceFolder}/Launcher/bin/Debug/config.json"
    ],
    "cwd": "${workspaceFolder}/Launcher/bin/Debug/",
    "stopAtEntry": false,
    "console": "integratedTerminal"
}
```

**✅ No changes needed** - paths are cross-platform compatible.

---

### Step 7: Copy Config to Build Directory

Like PyCharm, VS Code runs LEAN from the build directory:

**Copy Configuration:**
```cmd
copy C:\Projects\LEAN\Launcher\config.json C:\Projects\LEAN\Launcher\bin\Debug\config.json
```

**Important:** Always copy config after editing. Consider creating a batch script:

**Create `copy_config.bat` in `C:\Projects\LEAN\`:**
```batch
@echo off
echo Copying config.json to build directory...
copy Launcher\config.json Launcher\bin\Debug\config.json
echo Done!
pause
```

**Usage:** Double-click `copy_config.bat` after editing `Launcher/config.json`

---

## Building LEAN

### Step 8: Build LEAN in VS Code

VS Code provides multiple ways to build:

#### Method 1: Using Tasks (Recommended)

1. Open Command Palette (Ctrl+Shift+P)
2. Type: **Tasks: Run Build Task**
3. Select: **build** (or press Ctrl+Shift+B)
4. Terminal panel opens and shows build output

**Build Tasks Available:**

| Task | Purpose | When to Use |
|------|---------|-------------|
| **build** | Incremental build | Regular development |
| **rebuild** | Full rebuild (no-incremental) | Debugging symbol issues |
| **clean** | Delete build outputs | Clean slate before rebuild |

#### Method 2: Using Terminal

1. Terminal → New Terminal (Ctrl+Shift+`)
2. Run:
```cmd
dotnet build QuantConnect.Lean.sln
```

**Expected Output:**
```
Build succeeded.
    6858 Warning(s)
    0 Error(s)

Time Elapsed 00:01:30
```

**⚠️ Warnings are normal** - nullable reference type warnings (6000-7000 range) are expected and safe.

---

## Debugging C# Algorithms

### Step 9: Debug C# Algorithm

VS Code excels at C# debugging with the C# Dev Kit.

#### Configure for C# Algorithm

**Edit `Launcher/config.json`:**
```json
{
  "algorithm-type-name": "BasicTemplateFrameworkAlgorithm",
  "algorithm-language": "CSharp",
  "algorithm-location": "QuantConnect.Algorithm.CSharp.dll",
  "debugging": false,
  "debugging-method": "",
}
```

**Copy to build directory:**
```cmd
copy Launcher\config.json Launcher\bin\Debug\config.json
```

#### Set Breakpoints

1. Open: `Algorithm.CSharp/BasicTemplateFrameworkAlgorithm.cs`
2. Find `Initialize()` method (around line 40)
3. Click in the **left margin** next to line:
   ```csharp
   SetStartDate(2013, 10, 07);
   ```
4. **Red dot** appears indicating breakpoint

#### Launch Debugger

**Method 1: Debug Panel**
1. Click **Run and Debug** icon (Ctrl+Shift+D)
2. Select **Launch** from dropdown
3. Click **green play button** (F5)

**Method 2: Keyboard Shortcut**
- Press **F5** directly

**What Happens:**
1. VS Code runs `build` task automatically
2. Build output shows in terminal
3. LEAN launches with debugger attached
4. Execution **pauses** at your breakpoint
5. Current line highlighted in yellow
6. Variables panel shows local variables

#### Using the Debugger

**Debug Toolbar Appears:**

| Button | Shortcut | Action |
|--------|----------|--------|
| Continue | F5 | Resume execution |
| Step Over | F10 | Execute current line, move to next |
| Step Into | F11 | Enter function calls |
| Step Out | Shift+F11 | Exit current function |
| Restart | Ctrl+Shift+F5 | Restart debugging |
| Stop | Shift+F5 | Stop debugging |

**Panels Available:**

- **Variables** - Local variables, `this` object, algorithm state
- **Watch** - Add expressions to watch: right-click variable → Add to Watch
- **Call Stack** - Function call hierarchy
- **Breakpoints** - Manage all breakpoints

**Example Debugging Session:**

1. Execution pauses at `SetStartDate(2013, 10, 07);`
2. Variables panel shows `this` with algorithm properties
3. Press **F10** (Step Over) → moves to next line
4. Press **F10** again → moves to `SetEndDate`
5. Press **F5** (Continue) → algorithm runs to completion
6. Results appear in terminal

---

## Debugging Python Algorithms

### Step 10: Debug Python Algorithm (DebugPy Method)

Python debugging in VS Code uses the **DebugPy** method (different from PyCharm's method).

#### Configure for Python Algorithm

**Edit `Launcher/config.json`:**
```json
{
  "algorithm-type-name": "BasicTemplateAlgorithm",
  "algorithm-language": "Python",
  "algorithm-location": "../../../Algorithm.Python/BasicTemplateAlgorithm.py",
  "debugging": true,
  "debugging-method": "DebugPy",
}
```

**⚠️ Note:** `"DebugPy"` is correct for VS Code (PyCharm uses `"PyCharm"`)

**Copy to build directory:**
```cmd
copy Launcher\config.json Launcher\bin\Debug\config.json
```

#### Ensure DebugPy Installed

DebugPy should be included with the Python extension, but verify:

```cmd
conda activate lean_py311
pip show debugpy
```

If not installed:
```cmd
pip install debugpy
```

#### Two-Step Debugging Process

**Step 1: Launch LEAN (waits for debugger)**

1. Open VS Code integrated terminal (Ctrl+Shift+`)
2. Run LEAN:
   ```cmd
   cd C:\Projects\LEAN\Launcher\bin\Debug
   dotnet QuantConnect.Lean.Launcher.dll
   ```
3. LEAN outputs:
   ```
   DebuggerHelper.Initialize(): python initialization done
   DebuggerHelper.Initialize(): starting...
   DebuggerHelper.Initialize(): waiting for debugger to attach at localhost:5678...
   ```
4. LEAN **waits** for debugger connection (30 seconds timeout)

**Step 2: Attach VS Code Debugger**

1. Open: `Algorithm.Python/BasicTemplateAlgorithm.py`
2. Set breakpoint: Click left margin next to line 29:
   ```python
   self.set_start_date(2013, 10, 7)
   ```
3. Open **Run and Debug** panel (Ctrl+Shift+D)
4. Select **Attach to Python** from dropdown
5. Click **green play button** (F5)
6. VS Code connects to LEAN on port 5678
7. Execution continues and **pauses** at your breakpoint

#### Using Python Debugger

Same debug toolbar and panels as C# debugging:

- **F10** - Step over current line
- **F11** - Step into function
- **F5** - Continue execution
- **Variables panel** - Shows `self`, algorithm state, data

**Example:**
1. Execution pauses at `self.set_start_date(2013, 10, 7)`
2. Variables panel shows `self` object
3. Expand `self` → see algorithm properties
4. Press **F10** → moves to `self.set_end_date`
5. Press **F5** → continues to completion

#### Python Debugging Notes

**Differences from PyCharm:**
- **PyCharm:** Start debug server FIRST, then run LEAN (PyCharm listens)
- **VS Code:** Run LEAN FIRST, then attach VS Code (LEAN listens)

**Port Difference:**
- **PyCharm method:** Port 6000
- **DebugPy method:** Port 5678

**Path Mapping:**
The `.vscode/launch.json` includes path mappings:
```json
"pathMappings": [{
    "localRoot": "${workspaceFolder}",
    "remoteRoot": "${workspaceFolder}"
}]
```

This maps your source files to LEAN's runtime location. Works for `Algorithm.Python/` directory by default.

**If using custom algorithm location:** Update `localRoot` in `launch.json`:
```json
"pathMappings": [{
    "localRoot": "C:\\Projects\\LEAN\\CustomAlgorithms",
    "remoteRoot": "C:\\Projects\\LEAN\\CustomAlgorithms"
}]
```

---

## Comparison with PyCharm

### When to Use Each IDE

**Use PyCharm Professional for:**
- ✅ **Primary Python algorithm development** (superior autocomplete, refactoring)
- ✅ **Remote Python debugging** (simpler workflow - start server, run LEAN)
- ✅ **Complex Python refactoring** (rename, extract method, etc.)
- ✅ **Jupyter notebook integration** (Research notebooks)

**Use VS Code for:**
- ✅ **C# debugging and engine development** (excellent .NET support)
- ✅ **Quick configuration edits** (faster startup than PyCharm)
- ✅ **Git operations** (GitLens provides superior visualization)
- ✅ **Markdown documentation** (README, journals, design docs)
- ✅ **Team members without PyCharm licenses** (VS Code is free)

### Feature Comparison

| Feature | PyCharm Professional | VS Code |
|---------|---------------------|---------|
| **Python Autocomplete** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good |
| **C# Support** | ⭐⭐ Basic (view only) | ⭐⭐⭐⭐⭐ Excellent |
| **Python Debugging** | ⭐⭐⭐⭐⭐ Server mode, port 6000 | ⭐⭐⭐⭐ Attach mode, port 5678 |
| **C# Debugging** | ❌ Not supported | ⭐⭐⭐⭐⭐ Native .NET support |
| **Startup Speed** | ⭐⭐⭐ Slower | ⭐⭐⭐⭐⭐ Very fast |
| **Git Integration** | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ GitLens is superior |
| **Configuration** | ⭐⭐⭐ Manual setup | ⭐⭐⭐⭐⭐ Preconfigured in repo |
| **Cost** | 💰 Requires license | 🆓 Free |
| **LEAN Preconfiguration** | ❌ Manual setup | ✅ `.vscode/` included |

### Recommended Workflow

**Dual-IDE Setup (Recommended):**

1. **PyCharm:** Keep open for Python algorithm development
   - Main coding window
   - Debug Python algorithms with PyCharm method

2. **VS Code:** Use for secondary tasks
   - C# debugging and exploration
   - Quick config edits
   - Git commits and diffs
   - Documentation editing

**Example Day:**
- **Morning:** Develop Python strategy in PyCharm
- **Afternoon:** Debug C# engine issue in VS Code
- **Evening:** Git commit/review in VS Code, update docs

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Build Task Not Found

**Error:** "No build task found"

**Solution:**
1. Verify `.vscode/tasks.json` exists
2. Reload window: Ctrl+Shift+P → "Developer: Reload Window"
3. If still missing, check git status:
   ```cmd
   git status .vscode/tasks.json
   ```

---

#### Issue 2: C# Debugging Doesn't Start

**Error:** "Could not find QuantConnect.Lean.Launcher.dll"

**Cause:** LEAN not built yet

**Solution:**
1. Build LEAN first: Ctrl+Shift+B
2. Verify build succeeded (0 errors)
3. Check file exists:
   ```cmd
   dir C:\Projects\LEAN\Launcher\bin\Debug\QuantConnect.Lean.Launcher.dll
   ```
4. Try debugging again (F5)

---

#### Issue 3: Python Debugger Won't Attach

**Error:** "Connection refused" or timeout

**Possible Causes and Solutions:**

**Cause 1: LEAN not running yet**
- **Solution:** Launch LEAN first, THEN attach debugger
- **Order:** Terminal → run LEAN → wait for "waiting for debugger" message → F5 to attach

**Cause 2: Wrong port**
- **Solution:** Verify `launch.json` uses port 5678 (not 6000):
  ```json
  "port": 5678,
  ```

**Cause 3: Config not set to DebugPy**
- **Solution:** Verify `config.json`:
  ```json
  "debugging": true,
  "debugging-method": "DebugPy",
  ```

**Cause 4: Config not copied to build directory**
- **Solution:**
  ```cmd
  copy Launcher\config.json Launcher\bin\Debug\config.json
  ```

**Cause 5: Debugpy not installed**
- **Solution:**
  ```cmd
  conda activate lean_py311
  pip install debugpy
  ```

---

#### Issue 4: Breakpoints Not Hitting

**Symptom:** Execution doesn't pause at breakpoints

**Solutions:**

**For C# Breakpoints:**
1. Verify algorithm language in config.json: `"algorithm-language": "CSharp"`
2. Rebuild with debug symbols: Ctrl+Shift+P → "Tasks: Run Task" → "rebuild"
3. Check breakpoint is in correct file matching algorithm-type-name

**For Python Breakpoints:**
1. Verify algorithm-location in config.json points to correct file
2. Verify path mapping in launch.json includes algorithm directory
3. Set breakpoint BEFORE attaching debugger
4. Try breakpoint at start of Initialize() method first

---

#### Issue 5: Python Extension Not Detecting Conda Environment

**Symptom:** Bottom-right shows wrong Python version

**Solution:**
1. Open Command Palette (Ctrl+Shift+P)
2. Type: "Python: Select Interpreter"
3. If `lean_py311` not listed:
   - Select "Enter interpreter path..."
   - Navigate to: `C:\Users\datu\Miniconda3\envs\lean_py311\python.exe`
   - Click OK
4. Reload window: Ctrl+Shift+P → "Developer: Reload Window"

---

#### Issue 6: "Comments are not permitted in JSON" Errors

**Symptom:** Red squiggles in `config.json` or `.vscode/*.json`

**Explanation:** VS Code supports JSONC (JSON with Comments) for config files

**Solution (Choose one):**

**Option 1: Ignore warnings** (recommended - comments are valid for these files)

**Option 2: Disable for workspace:**
1. File → Preferences → Settings (Ctrl+,)
2. Search: "json.schemas"
3. Edit in settings.json:
   ```json
   "json.schemas": []
   ```

**Option 3: Change file association:**
1. Click on "JSON" in bottom-right corner
2. Select "Configure File Association for 'config.json'"
3. Select "JSON with Comments"

---

#### Issue 7: OmniSharp Errors in C# Files

**Symptom:** C# IntelliSense not working, OmniSharp errors in Output panel

**Solution:**
1. Ctrl+Shift+P → "OmniSharp: Restart OmniSharp"
2. Wait 10-30 seconds for OmniSharp to reload
3. If persists, rebuild: Ctrl+Shift+B
4. Check Output panel (View → Output) → select "OmniSharp Log" from dropdown
5. Look for errors about .NET SDK or project files

**Common Fix:**
```cmd
# Restore NuGet packages
dotnet restore QuantConnect.Lean.sln
```

---

## Quick Reference

### Keyboard Shortcuts

**General:**
- `Ctrl+Shift+P` - Command Palette (access all commands)
- `Ctrl+,` - Settings
- `Ctrl+K Ctrl+O` - Open Folder
- `` Ctrl+` `` - Toggle integrated terminal

**Editing:**
- `Ctrl+Shift+F` - Search across all files
- `Ctrl+P` - Quick file open
- `Ctrl+/` - Toggle line comment
- `Alt+Up/Down` - Move line up/down
- `Ctrl+D` - Select next occurrence of current word

**Building:**
- `Ctrl+Shift+B` - Run build task
- `Ctrl+Shift+P` → "Tasks: Run Task" - Show all tasks

**Debugging:**
- `F5` - Start debugging / Continue
- `Shift+F5` - Stop debugging
- `Ctrl+Shift+F5` - Restart debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into
- `Shift+F11` - Step out
- `Ctrl+Shift+D` - Open Debug panel

**Git:**
- `Ctrl+Shift+G` - Open Source Control panel
- `Ctrl+Shift+G G` - Commit (after staging)

### Build Tasks

```
Ctrl+Shift+P → Tasks: Run Build Task
```

- **build** - Incremental build (fast)
- **rebuild** - Full rebuild (clean slate)
- **clean** - Delete build outputs

### Debug Configurations

**Run and Debug Panel (Ctrl+Shift+D):**

- **Launch** - Build and run LEAN with C# debugging
- **Attach to Python** - Connect to running LEAN Python debugger

### Configuration Files

**Master Configuration:**
- `Launcher/config.json` - Edit this file

**Runtime Configuration:**
- `Launcher/bin/Debug/config.json` - Copy master here after editing

**VS Code Configuration:**
- `.vscode/launch.json` - Debug configurations
- `.vscode/tasks.json` - Build tasks
- `.vscode/settings.json` - Workspace settings

### Algorithm Configuration Snippets

**C# Algorithm:**
```json
{
  "algorithm-type-name": "BasicTemplateFrameworkAlgorithm",
  "algorithm-language": "CSharp",
  "algorithm-location": "QuantConnect.Algorithm.CSharp.dll",
  "debugging": false
}
```

**Python Algorithm (VS Code debugging):**
```json
{
  "algorithm-type-name": "BasicTemplateAlgorithm",
  "algorithm-language": "Python",
  "algorithm-location": "../../../Algorithm.Python/BasicTemplateAlgorithm.py",
  "debugging": true,
  "debugging-method": "DebugPy"
}
```

### Terminal Commands

**Build:**
```cmd
cd C:\Projects\LEAN
dotnet build QuantConnect.Lean.sln
```

**Run Algorithm:**
```cmd
cd C:\Projects\LEAN\Launcher\bin\Debug
dotnet QuantConnect.Lean.Launcher.dll
```

**Copy Config:**
```cmd
copy C:\Projects\LEAN\Launcher\config.json C:\Projects\LEAN\Launcher\bin\Debug\config.json
```

**Activate Python Environment:**
```cmd
conda activate lean_py311
```

---

## Validation Checklist

Complete this checklist to verify VS Code setup is fully functional:

### Installation Verification

- [ ] VS Code version 1.85 or later installed
- [ ] C# Dev Kit extension installed and activated
- [ ] Python extension installed and activated
- [ ] GitLens extension installed (optional but recommended)

### Configuration Verification

- [ ] Project opened at `C:\Projects\LEAN`
- [ ] Python interpreter set to `lean_py311` (bottom-right corner)
- [ ] `.vscode/launch.json` exists and contains "Launch" and "Attach to Python"
- [ ] `.vscode/tasks.json` exists and contains build tasks

### Build Verification

- [ ] Build task runs successfully (Ctrl+Shift+B)
- [ ] Build completes with 0 errors (warnings OK)
- [ ] `Launcher/bin/Debug/QuantConnect.Lean.Launcher.dll` exists after build

### C# Debugging Verification

- [ ] Config.json set to C# algorithm
- [ ] Config.json copied to `bin/Debug/` directory
- [ ] Breakpoint set in `BasicTemplateFrameworkAlgorithm.cs`
- [ ] F5 starts debugger and pauses at breakpoint
- [ ] Variables panel shows algorithm state
- [ ] F10 steps through code
- [ ] F5 continues to completion

### Python Debugging Verification

- [ ] Config.json set to Python algorithm with `"debugging-method": "DebugPy"`
- [ ] Config.json copied to `bin/Debug/` directory
- [ ] Debugpy package installed in `lean_py311` environment
- [ ] LEAN runs and shows "waiting for debugger" message
- [ ] "Attach to Python" configuration attaches successfully
- [ ] Breakpoint in `BasicTemplateAlgorithm.py` pauses execution
- [ ] Variables panel shows Python algorithm state

### Workflow Verification

- [ ] Can switch between C# and Python algorithms by editing config.json
- [ ] Can build from VS Code tasks
- [ ] Can debug both C# and Python algorithms
- [ ] Can use integrated terminal for git commands
- [ ] Can edit and save files without issues

---

## Next Steps

### Completed Phase 2 ✅

You now have a **fully functional VS Code environment** for LEAN development!

**What You Can Do:**
- ✅ Build LEAN solution
- ✅ Debug C# algorithms and engine code
- ✅ Debug Python algorithms
- ✅ Edit configurations and algorithms
- ✅ Use Git integration for version control

### Continue to Phase 3: WSL Native Setup

**Purpose:** Enable Claude Code automation and Linux-based development

**Location:** `docs/SETUP_WINDOWS_WSL_NATIVE.md` - Phase 3

**Estimated Time:** 1.5 hours

**What You'll Gain:**
- LEAN running natively in WSL environment
- Claude Code can build and test algorithms
- Cross-platform development validation
- Preparation for Docker-based deployment

### OR: Begin Energy Market Development

If you're eager to start development, you can proceed with energy market adaptation:

**Next Development Phase:**
- Design EPEX brokerage plugin architecture
- Create custom data types (PowerPrice, GasPrice)
- Define 24/7 market hours for energy markets
- Implement data loading for intraday power/gas prices

**Documentation:**
- Reference: `CLAUDE.md` - System Adaptation Areas section
- Journal: Update `JOURNAL.md` with development progress

---

## Summary

**Phase 2 Complete! 🎉**

You now have **two powerful IDEs** configured for LEAN development:

1. **PyCharm Professional** - Primary Python algorithm development
2. **Visual Studio Code** - C# debugging, quick edits, Git operations

**Your Development Toolkit:**

| Task | Recommended IDE | Alternative |
|------|----------------|-------------|
| Python algorithm coding | PyCharm | VS Code (basic) |
| Python algorithm debugging | PyCharm | VS Code (DebugPy) |
| C# engine debugging | VS Code | N/A |
| Configuration editing | VS Code | PyCharm |
| Git operations | VS Code | PyCharm |
| Documentation | VS Code | PyCharm |

**Key Takeaways:**

✅ VS Code provides **excellent C# support** for LEAN engine development
✅ VS Code is **preconfigured** in LEAN repository (`.vscode/` folder)
✅ Python debugging works but requires **two-step process** (run LEAN, then attach)
✅ PyCharm remains **primary for Python** algorithm development
✅ **Both IDEs can coexist** - use each for its strengths

**Ready for Phase 3?** Proceed to WSL Native Setup to enable Claude Code automation.

**Ready to develop?** Reference `CLAUDE.md` for energy market adaptation roadmap.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-15
**Author:** Claude (Systematic Trading Architect)
**Project:** LEAN Energy Trading Adaptation
