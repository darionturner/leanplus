# LEAN Development Environment Setup Guide
## Windows 10 + WSL2 Dual Native Installation

**Target Configuration:**
- **Primary Development:** Windows 10 Enterprise + PyCharm Professional
- **Secondary Learning:** Windows + VS Code
- **Automation Environment:** WSL2 Ubuntu for Claude Code

**Repository Strategy:** Windows-hosted, WSL-mounted for automation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Critical Decisions & Strategy](#critical-decisions--strategy)
3. [Phase 1: Windows Native Setup](#phase-1-windows-native-setup-primary-development)
4. [Phase 2: VS Code Setup](#phase-2-vs-code-setup-secondarylearning)
5. [Phase 3: WSL Native Setup](#phase-3-wsl-native-setup-claude-code-automation)
6. [Cross-Platform Considerations](#cross-platform-considerations)
7. [Validation & Testing](#validation--testing)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Best Practices](#best-practices)
10. [Quick Reference](#quick-reference-commands)

---

## Executive Summary

This guide provides step-by-step instructions for setting up a complete LEAN development environment across Windows and WSL2. The setup supports:

- **Windows Native Development** (PyCharm) - Primary workflow for algorithm and engine development
- **VS Code on Windows** - Secondary IDE for learning and flexibility
- **WSL Native Environment** - Independent build for Claude Code automation and testing

**Current System Status:**
- WSL2 kernel: 6.6.87.2-microsoft-standard-WSL2
- Ubuntu: 24.04.3 LTS
- Existing: Conda 25.7.0, Python 3.12.3
- Missing: .NET SDK, Python 3.11.11 environment

**Estimated Total Setup Time:** 5-8 hours (includes downloads, installation, configuration, testing)

---

## Critical Decisions & Strategy

### 1. Repository Location

**DECISION: Host on Windows, Access from WSL via Mount**

**Recommended Location:**
```
Windows: C:\Projects\LEAN  (or D:\Projects\LEAN if separate drive)
WSL Access: /mnt/c/Projects/LEAN  (or /mnt/d/Projects/LEAN)
```

**Rationale:**
- Primary development in PyCharm (Windows) → Native Windows performance
- WSL access via mount is acceptable for Claude Code (not file-intensive)
- Single source of truth, no synchronization needed
- Simpler Git workflow

**Alternative NOT Recommended:**
- Repository in WSL, Windows accesses via `\\wsl$\...` → Slow, permission issues with PyCharm

---

### 2. Git Line Endings

**DECISION: Use LF (Linux-style) Everywhere**

**Configuration:**
```ini
# Both Windows and WSL .gitconfig
[core]
    autocrlf = false
    eol = lf
```

**`.gitattributes` in repository root:**
```
* text=auto eol=lf
*.{cmd,[cC][mM][dD]} text eol=crlf
*.{bat,[bB][aA][tT]} text eol=crlf
```

**Rationale:**
- LEAN is cross-platform, LF is standard
- Prevents "everything is modified" when switching platforms
- Modern Windows tools handle LF fine
- Ensures consistency

---

### 3. .NET Version

**CRITICAL: LEAN Requires .NET 9**

- LEAN v2.5.16913+ requires .NET 9.0
- Do NOT install .NET 6 unless using older LEAN versions
- Install on both Windows AND WSL

---

### 4. Python Version & Environment

**REQUIRED: Python 3.11.11 (NOT 3.12)**

**Strategy: SEPARATE Installations**
- **Windows:** Miniconda + conda environment `lean_py311`
- **WSL:** Separate conda environment `lean_py311` (you already have conda installed)
- **Cannot Share:** .exe/.dll vs .so libraries

**Packages:** pandas=2.2.3, wrapt=1.16.0, quantconnect-stubs

---

### 5. Build Strategy

**DECISION: Separate Builds**

- Windows builds on Windows filesystem
- WSL builds independently (even though accessing mounted drive)
- .NET artifacts are platform-specific with Python.NET

**Do NOT share `bin/` outputs between platforms**

---

## Phase 1: Windows Native Setup (Primary Development)

**Estimated Time:** 2-3 hours

### Step 1.1: Prepare Repository Location

```cmd
:: Create projects directory (choose one based on your drive setup)
mkdir C:\Projects

:: If LEAN is currently at C:\Users\datu\ReposWSL\LEAN, move it:
move C:\Users\datu\ReposWSL\LEAN C:\Projects\LEAN

:: Verify
dir C:\Projects\LEAN\QuantConnect.Lean.sln
```

**Expected:** `QuantConnect.Lean.sln` file exists at new location

---

### Step 1.2: Install Git for Windows

**Download:** https://git-scm.com/download/win

**Installation:**
- Accept defaults EXCEPT:
- **Line Ending Conversion:** Select "Checkout as-is, commit as-is" (we configure via .gitconfig)
- Ensure "Git from command line and also from 3rd-party software" is selected

**Post-Installation Configuration:**

```cmd
git config --global core.autocrlf false
git config --global core.eol lf
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Create `.gitattributes` in repository:**

```cmd
cd C:\Projects\LEAN
echo * text=auto eol=lf > .gitattributes
echo *.{cmd,[cC][mM][dD]} text eol=crlf >> .gitattributes
echo *.{bat,[bB][aA][tT]} text eol=crlf >> .gitattributes
```

**Verify:**
```cmd
git config --get core.autocrlf
:: Output: false
git config --get core.eol
:: Output: lf
```

---

### Step 1.3: Install .NET 9 SDK

**Download:** https://dotnet.microsoft.com/en-us/download/dotnet/9.0

- Select ".NET 9.0 SDK (v9.x.x) - Windows x64 Installer"
- Run installer with default settings

**Verify Installation:**
```cmd
dotnet --version
:: Expected: 9.x.x

dotnet --list-sdks
:: Expected: 9.0.xxx listed
```

**If Installation Fails:**
- Ensure Windows 10 is up-to-date
- Check system requirements: https://github.com/dotnet/core/blob/main/release-notes/9.0/supported-os.md

---

### Step 1.4: Install Miniconda (Windows)

**Download:** https://docs.conda.io/en/latest/miniconda.html
- Select "Miniconda3 Windows 64-bit"

**Installation:**
1. Run installer
2. **Install for:** Just Me (recommended)
3. **Destination:** `C:\Users\datu\Miniconda3` (default)
4. **Advanced Options:**
   - ☑ Add Miniconda3 to PATH (easier for command line, though installer warns against it)
   - ☐ Register as system Python (leave unchecked)

**Create LEAN Python Environment:**

Open **Anaconda Prompt** (or Command Prompt if added to PATH):

```cmd
:: Create environment with Python and pandas (wrapt not available via conda)
conda create -n lean_py311 python=3.11.11 pandas=2.2.3 -y

:: Activate environment
conda activate lean_py311

:: Install wrapt and autocomplete support via pip
pip install wrapt==1.16.0 quantconnect-stubs

:: Verify
python --version
:: Expected: Python 3.11.11

python -c "import pandas; print(pandas.__version__)"
:: Expected: 2.2.3

python -c "import wrapt; print(wrapt.__version__)"
:: Expected: 1.16.0
```

---

### Step 1.5: Set PYTHONNET_PYDLL Environment Variable

**Critical:** LEAN uses Python.NET which needs to know Python DLL location

**Set Environment Variable:**

1. Press Windows Key, search "Environment Variables"
2. Click "Edit the system environment variables"
3. Click "Environment Variables..." button
4. Under "User variables for datu" (or "System variables"), click "New..."
5. Variable name: `PYTHONNET_PYDLL`
6. Variable value: `C:\Users\datu\Miniconda3\envs\lean_py311\python311.dll`
7. Click OK on all dialogs

**Verify:**

**IMPORTANT:** Open a NEW Command Prompt (environment variables load at session start)

```cmd
echo %PYTHONNET_PYDLL%
:: Expected: C:\Users\datu\Miniconda3\envs\lean_py311\python311.dll

dir %PYTHONNET_PYDLL%
:: Expected: File information displayed (proves file exists)
```

---

### Step 1.6: Build LEAN (Windows)

```cmd
cd C:\Projects\LEAN

:: First-time NuGet restore (may take a few minutes)
dotnet restore QuantConnect.Lean.sln

:: Build solution
dotnet build QuantConnect.Lean.sln
```

**Expected Output:**
```
Build succeeded.
    XXXX Warning(s)  (6000-7000 warnings is normal - mostly nullable reference warnings)
    0 Error(s)

Time Elapsed 00:01:30.00
```

**Verify Build Artifacts:**
```cmd
:: Check where DLL was actually built (path may vary)
dir /s /b Launcher\bin\QuantConnect.Lean.Launcher.dll

:: Common location (no net9.0 subdirectory in some configurations):
dir Launcher\bin\Debug\QuantConnect.Lean.Launcher.dll
:: Expected: File exists
```

**Common Build Issues:**

**Issue:** NuGet package restore errors
**Solution:**
```cmd
dotnet clean QuantConnect.Lean.sln
dotnet restore QuantConnect.Lean.sln
dotnet build QuantConnect.Lean.sln
```

**Issue:** Python.NET build errors
**Solution:** Verify `PYTHONNET_PYDLL` is set correctly, restart terminal

---

### Step 1.7: Run LEAN (Validate Setup)

**Run C# Algorithm:**

```cmd
:: Navigate to wherever the DLL was built (check from Step 1.6)
cd C:\Projects\LEAN\Launcher\bin\Debug
dotnet QuantConnect.Lean.Launcher.dll
```

**Expected Output:**
```
LEAN ALGORITHMIC TRADING ENGINE v2.x.x.x Launcher
...
20xx-xx-xx 00:00:00 Launching analysis for BasicTemplateFrameworkAlgorithm...
...
Algorithm Id:(BasicTemplateFrameworkAlgorithm) completed in X.XX seconds
```

**Run Python Algorithm:**

⚠️ **IMPORTANT:** LEAN reads config.json from the **bin/Debug directory** (where the DLL runs), not from Launcher root.

1. Edit `Launcher\config.json` (main config):
```json
{
  "algorithm-type-name": "BasicTemplateAlgorithm",
  "algorithm-language": "Python",
  "algorithm-location": "../../../Algorithm.Python/BasicTemplateAlgorithm.py",
  ...
}
```

**CRITICAL: Note the comma after "Python" - JSON syntax must be correct!**

2. Copy updated config to bin/Debug:
```cmd
copy C:\Projects\LEAN\Launcher\config.json C:\Projects\LEAN\Launcher\bin\Debug\config.json
:: Type Y to overwrite when prompted
```

3. Activate conda environment and run LEAN:
```cmd
conda activate lean_py311
cd C:\Projects\LEAN\Launcher\bin\Debug
dotnet QuantConnect.Lean.Launcher.dll
```

**Expected:** You should see:
- `PythonInitializer.Initialize(): start...`
- `Python version 3.11.11`
- `Importing python module BasicTemplateAlgorithm`
- `numpy test >>> print numpy.pi: 3.141592653589793`
- Algorithm completes successfully with statistics

**Common Python Runtime Issues:**

**Issue:** `BadPythonDllException`
**Solution:**
1. Verify `PYTHONNET_PYDLL` environment variable is set
2. Ensure you opened NEW command prompt after setting variable
3. Verify DLL file exists at specified path

**Issue:** `ModuleNotFoundError: No module named 'pandas'`
**Solution:**
```cmd
conda activate lean_py311
pip install pandas==2.2.3 wrapt==1.16.0
```

**Issue:** `ModuleNotFoundError: No module named 'clr'` when testing quantconnect-stubs
**Solution:** This is expected and normal! The stubs are for IDE autocomplete only. The actual QuantConnect modules are loaded by LEAN at runtime via Python.NET. You can ignore this error.

**Issue:** `JsonReaderException: After parsing a value an unexpected character was encountered`
**Solution:** JSON syntax error in config.json. Common causes:
- Missing comma after `"Python"` in `"algorithm-language": "Python"`
- Ensure all JSON lines (except the last in each block) end with commas
- Validate JSON syntax at https://jsonlint.com if unsure

---

### Step 1.8: Install PyCharm Professional

**Edition Required:** PyCharm Professional (Community lacks remote debugging)

**Download:** https://www.jetbrains.com/pycharm/download/?section=windows

**Installation:**
- Select all checkboxes for convenience:
  - ☑ Create Desktop Shortcut
  - ☑ Add "bin" folder to PATH
  - ☑ Add "Open Folder as Project"
  - ☑ .py file associations

**Initial Launch:**
1. Launch PyCharm
2. Skip importing settings (first install)
3. Choose UI theme (Darcula recommended for dark mode)
4. Skip plugin installation screen (we'll add as needed)

---

### Step 1.9: Configure PyCharm for LEAN

**Open Project:**
1. File → Open
2. Navigate to `C:\Projects\LEAN`
3. Click "Open"
4. Click "Trust Project" when prompted

**Configure Python Interpreter:**
1. File → Settings (Ctrl+Alt+S)
2. Project: LEAN → Python Interpreter
3. Click gear icon ⚙ → Add Interpreter → Add Local Interpreter...
4. Select "Conda Environment" tab
5. Choose "Existing environment"
6. Interpreter: `C:\Users\datu\Miniconda3\envs\lean_py311\python.exe`
7. Click "OK"

**Verify Configuration:**
- Bottom right of PyCharm window should show: `Python 3.11 (lean_py311)`
- Open `Algorithm.Python/BasicTemplateAlgorithm.py`
- Type `from AlgorithmImports import *` - autocomplete should work
- Hover over `QCAlgorithm` - should show type hints

**Install Recommended Plugins:**
1. File → Settings → Plugins
2. Search and install:
   - **.ignore** - .gitignore syntax highlighting
   - **Markdown** - README viewing
   - **CSV** - CSV file viewing (useful for data files)

---

### Step 1.10: PyCharm External Tools (Build LEAN)

Since PyCharm doesn't natively support C#, set up external tool for building:

1. File → Settings → Tools → External Tools
2. Click "+" to add new tool
3. Configure:
   - **Name:** `Build LEAN`
   - **Program:** `C:\Program Files\dotnet\dotnet.exe`
   - **Arguments:** `build QuantConnect.Lean.sln`
   - **Working directory:** `$ProjectFileDir$`
   - Click "OK"

**Usage:** Tools → External Tools → Build LEAN (builds C# components when needed)

---

### Step 1.11: PyCharm Remote Debugging Setup

**Install PyCharm Debugger Package:**

Activate conda environment and install the debugger:
```cmd
conda activate lean_py311
pip install pydevd-pycharm~=231.9225
```

**⚠️ Version Note:** Use version `231.9225` specifically. LEAN expects the older pydevd API (camelCase methods). Newer versions (252.x+) use snake_case and are incompatible. PyCharm may show a version warning - ignore it.

**Enable Debugging in LEAN:**

Edit `Launcher\config.json`:
```json
{
  "debugging": true,
  "debugging-method": "PyCharm",
  ...
}
```

**⚠️ Critical:** The method must be `"PyCharm"` (case-sensitive), not `"DebugPy"`

**Copy Config to Build Directory:**
```cmd
copy C:\Projects\LEAN\Launcher\config.json C:\Projects\LEAN\Launcher\bin\Debug\config.json
```

**⚠️ Important:** LEAN reads config from the execution directory (`bin\Debug\`), not the project root. Always copy after editing.

**Create PyCharm Debug Configuration:**

1. Run → Edit Configurations...
2. Click "+" → Python Debug Server
3. Configure:
   - **Name:** `PyCharm Debug for LEAN`
   - **IDE host name:** `localhost`
   - **Port:** `6000` ⚠️ **NOT 5678!** PyCharm method uses port 6000, VS Code uses port 5678
   - **Uncheck:** "Suspend after connect"
   - **Check:** "Store as project file" (optional, for team sharing)
   - Click "OK"

**Debugging Workflow:**

1. Open algorithm file: `Algorithm.Python/BasicTemplateAlgorithm.py`
2. Set breakpoint: Click left margin next to line 29: `self.set_start_date(2013,10, 7)`
   - Red dot appears indicating breakpoint
3. Start PyCharm debug server: Press `Shift+F9` or Run → Debug 'PyCharm Debug for LEAN'
   - Console shows: "Starting debug server at port 6,000"
   - Shows: "Waiting for process connection..."
4. Within 10 seconds, run LEAN in Command Prompt:
   ```cmd
   cd C:\Projects\LEAN\Launcher\bin\Debug
   dotnet QuantConnect.Lean.Launcher.dll
   ```
5. PyCharm console shows: "Connected to pydev debugger" and "SUCCESS: Connected to local program"
6. PyCharm switches to Debugger tab automatically
7. Execution **PAUSES** at your breakpoint (line highlighted in blue)

**Using the Debugger:**
- **F8:** Step Over (execute current line, move to next)
- **F7:** Step Into (enter function calls)
- **F9:** Resume (continue to next breakpoint or end)
- **Variables Panel:** Inspect `self`, algorithm state, data objects
- **Watches:** Right-click variable → Add to Watches
- **Evaluate Expression:** Alt+F8 to run code in current context

**Verify Debugging:**
- Execution should pause at line 29 in `initialize()` method
- Variables panel shows `self` object with algorithm properties
- You can step through each line of initialization
- Algorithm completes successfully after resuming

**Common Issues:**

1. **"Connection refused" error:**
   - PyCharm debug server not running - start it first (Shift+F9)
   - Wrong port - must be 6000 for PyCharm method

2. **"Wrong debugger version" warning:**
   - Normal and safe to ignore
   - PyCharm wants 252.x but LEAN requires 231.x
   - Connection works despite warning

3. **Execution doesn't pause:**
   - Breakpoint may be in wrong file (check config.json algorithm-location)
   - Debug server must start before LEAN (within 10 seconds)
   - Verify config.json copied to bin\Debug directory

4. **"settrace() got unexpected keyword argument" error:**
   - Wrong pydevd-pycharm version installed
   - Run: `pip install pydevd-pycharm~=231.9225`

---

## Phase 2: VS Code Setup (Secondary/Learning)

**Estimated Time:** 45 minutes

### Step 2.1: Install VS Code

**Download:** https://code.visualstudio.com/download

**Installation:**
- Accept all default options
- Select all "Additional Tasks" for convenience:
  - ☑ Add "Open with Code" to context menu
  - ☑ Add to PATH
  - ☑ Register Code as editor for supported file types

---

### Step 2.2: Install Required Extensions

Open VS Code:

1. Click Extensions icon (Ctrl+Shift+X)
2. Search and install:
   - **C# Dev Kit** (ms-dotnettools.csdevkit) - Full C# support including debugging
   - **Python** (ms-python.python) - Python language support
   - **GitLens** (eamodio.gitlens) - Enhanced Git integration (optional)

**Restart VS Code after installing extensions**

---

### Step 2.3: Open LEAN Project

1. File → Open Folder...
2. Select `C:\Projects\LEAN`
3. Click "Select Folder"
4. Click "Yes, I trust the authors" when prompted

**VS Code Auto-Discovery:**
- C# extension finds `QuantConnect.Lean.sln`
- Python extension detects Python files
- If prompted to install additional tools, accept

---

### Step 2.4: Configure Python Interpreter

1. Open any `.py` file (e.g., `Algorithm.Python/BasicTemplateAlgorithm.py`)
2. Bottom right: Click Python version indicator (or "Select Interpreter")
3. Select `Python 3.11.11 ('lean_py311': conda)`
   - If not listed: "Enter interpreter path..." → Find → `C:\Users\datu\Miniconda3\envs\lean_py311\python.exe`

**Verify:** Bottom status bar shows `Python 3.11.11 64-bit ('lean_py311': conda)`

---

### Step 2.5: Configure Build and Debug

**Create `.vscode/tasks.json`:**

Create file at `C:\Projects\LEAN\.vscode\tasks.json`:

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
            "problemMatcher": "$msCompile",
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "clean",
            "command": "dotnet",
            "type": "process",
            "args": [
                "clean",
                "${workspaceFolder}/QuantConnect.Lean.sln"
            ],
            "problemMatcher": "$msCompile"
        }
    ]
}
```

**Create `.vscode/launch.json`:**

Create file at `C:\Projects\LEAN\.vscode\launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch LEAN (C#)",
            "type": "dotnet",
            "request": "launch",
            "preLaunchTask": "build",
            "program": "${workspaceFolder}/Launcher/bin/Debug/net9.0/QuantConnect.Lean.Launcher.dll",
            "args": [],
            "cwd": "${workspaceFolder}/Launcher/bin/Debug/net9.0",
            "console": "integratedTerminal",
            "stopAtEntry": false
        },
        {
            "name": "Attach to Python Algorithm",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/Algorithm.Python",
                    "remoteRoot": "${workspaceFolder}/Algorithm.Python"
                }
            ]
        }
    ]
}
```

---

### Step 2.6: Test VS Code Build and Debug

**Test Build:**
1. Terminal → Run Build Task... (Ctrl+Shift+B)
2. Select "build"
3. **Expected:** Build succeeds, no errors

**Test C# Debugging:**
1. Open `Launcher/Program.cs`
2. Set breakpoint (click left margin, line ~50 or inside `Main()`)
3. Run and Debug view (Ctrl+Shift+D)
4. Select "Launch LEAN (C#)"
5. Press F5
6. **Expected:** Execution pauses at breakpoint

**Test Python Debugging:**
1. Edit `Launcher/config.json`: Set `"debugging": true, "debugging-method": "DebugPy"`
2. Set breakpoint in `Algorithm.Python/BasicTemplateAlgorithm.py`
3. Start "Attach to Python Algorithm" debug configuration
4. In terminal, run LEAN separately:
   ```cmd
   cd Launcher\bin\Debug\net9.0
   dotnet QuantConnect.Lean.Launcher.dll
   ```
5. **Expected:** VS Code attaches, pauses at breakpoint

---

## Phase 3: WSL Native Setup (Claude Code Automation)

**Estimated Time:** 1.5 hours

### Step 3.1: Verify WSL and Repository Access

**Open WSL Terminal** (Windows Terminal or `wsl` command):

```bash
# Check WSL version and distribution
wsl --list --verbose
# Expected: Ubuntu-24.04, WSL version 2

# Navigate to repository (adjust drive letter if using D:\)
cd /mnt/c/Projects/LEAN

# Verify access
ls -la QuantConnect.Lean.sln
# Expected: File listed

# Check current git config
git config --get core.autocrlf
# If not "false", configure it (next step)
```

---

### Step 3.2: Configure Git in WSL

```bash
# Set line ending configuration (critical for cross-platform)
git config --global core.autocrlf false
git config --global core.eol lf
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
git config --get core.autocrlf  # Should output: false
git config --get core.eol        # Should output: lf

# Check git status (should show no unexpected modifications)
cd /mnt/c/Projects/LEAN
git status
```

**If git shows many modified files:**
```bash
# Reset working directory to match repository (discards uncommitted changes)
git rm --cached -r .
git reset --hard
git status  # Should now be clean
```

---

### Step 3.3: Install .NET 9 SDK (WSL/Ubuntu)

```bash
# Add Microsoft package repository
wget https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

# Update package list
sudo apt update

# Install .NET 9 SDK
sudo apt install -y dotnet-sdk-9.0

# Verify installation
dotnet --version
# Expected: 9.x.x

dotnet --list-sdks
# Expected: 9.0.xxx listed
```

**Alternative Installation (if apt fails):**
```bash
# Using snap
sudo snap install dotnet-sdk --classic --channel=9.0
```

---

### Step 3.4: Create Python 3.11.11 Environment (WSL)

**You already have Miniconda installed at `/home/datu/miniconda`**

```bash
# Initialize conda for bash (if not already done)
~/miniconda/bin/conda init bash
source ~/.bashrc

# Create LEAN Python environment (wrapt not available via conda)
conda create -n lean_py311 python=3.11.11 pandas=2.2.3 -y

# Activate environment
conda activate lean_py311

# Install wrapt and autocomplete stubs via pip
pip install wrapt==1.16.0 quantconnect-stubs

# Verify
python --version
# Expected: Python 3.11.11

python -c "import pandas; print(pandas.__version__)"
# Expected: 2.2.3

python -c "import wrapt; print(wrapt.__version__)"
# Expected: 1.16.0
```

---

### Step 3.5: Set PYTHONNET_PYDLL (WSL)

**Find Python shared library location:**

```bash
conda activate lean_py311
PYTHON_SO=$(python -c "import sys; print(f'{sys.prefix}/lib/libpython3.11.so')")
echo $PYTHON_SO
# Expected: /home/datu/miniconda/envs/lean_py311/lib/libpython3.11.so

# Verify file exists
ls -l $PYTHON_SO
# Expected: File information displayed
```

**Configure Environment Variable (Conda-Specific Approach):**

```bash
# Create activation script for conda environment
mkdir -p ~/miniconda/envs/lean_py311/etc/conda/activate.d

cat > ~/miniconda/envs/lean_py311/etc/conda/activate.d/env_vars.sh << 'EOF'
#!/bin/sh
export PYTHONNET_PYDLL="$CONDA_PREFIX/lib/libpython3.11.so"
EOF

# Create deactivation script
mkdir -p ~/miniconda/envs/lean_py311/etc/conda/deactivate.d

cat > ~/miniconda/envs/lean_py311/etc/conda/deactivate.d/env_vars.sh << 'EOF'
#!/bin/sh
unset PYTHONNET_PYDLL
EOF

# Make scripts executable
chmod +x ~/miniconda/envs/lean_py311/etc/conda/activate.d/env_vars.sh
chmod +x ~/miniconda/envs/lean_py311/etc/conda/deactivate.d/env_vars.sh

# Test configuration
conda deactivate
conda activate lean_py311
echo $PYTHONNET_PYDLL
# Expected: /home/datu/miniconda/envs/lean_py311/lib/libpython3.11.so
```

**Alternative (Global .bashrc approach):**
```bash
echo 'export PYTHONNET_PYDLL="/home/datu/miniconda/envs/lean_py311/lib/libpython3.11.so"' >> ~/.bashrc
source ~/.bashrc
```

---

### Step 3.6: Build LEAN in WSL

```bash
cd /mnt/c/Projects/LEAN

# Ensure conda environment is activated
conda activate lean_py311

# Verify environment variables
echo $PYTHONNET_PYDLL
# Must show valid path

# Build LEAN
dotnet build QuantConnect.Lean.sln
```

**Expected Output:**
```
Build succeeded.
    0 Warning(s)
    0 Error(s)
```

**Performance Note:**
- Building on `/mnt/c` (9P filesystem) is 2-5x slower than native Linux filesystem
- First build may take 3-5 minutes
- For Claude Code's occasional builds, this is acceptable
- For frequent development, consider building on Windows instead

**Verify Build Artifacts:**
```bash
ls -l Launcher/bin/Debug/net9.0/QuantConnect.Lean.Launcher.dll
# Expected: File exists
```

---

### Step 3.7: Run LEAN in WSL

```bash
cd /mnt/c/Projects/LEAN/Launcher/bin/Debug/net9.0

# Ensure environment is activated and variable is set
conda activate lean_py311
echo $PYTHONNET_PYDLL

# Run LEAN
dotnet QuantConnect.Lean.Launcher.dll
```

**Expected Output:**
```
LEAN ALGORITHMIC TRADING ENGINE v2.x.x.x Launcher
...
Algorithm Id:(BasicTemplateFrameworkAlgorithm) completed in X.XX seconds
```

**Test Python Algorithm:**

1. Edit `Launcher/config.json` to use Python algorithm
2. Run again:
```bash
cd /mnt/c/Projects/LEAN/Launcher/bin/Debug/net9.0
dotnet QuantConnect.Lean.Launcher.dll
```

**Expected:** Python algorithm runs successfully

---

### Step 3.8: Create Helper Script for Claude Code

**Create run script:**

```bash
cat > /mnt/c/Projects/LEAN/run_lean.sh << 'EOF'
#!/bin/bash
# LEAN Runner Script for WSL
set -e

# Activate conda environment
source ~/miniconda/etc/profile.d/conda.sh
conda activate lean_py311

# Ensure PYTHONNET_PYDLL is set
if [ -z "$PYTHONNET_PYDLL" ]; then
    export PYTHONNET_PYDLL="$CONDA_PREFIX/lib/libpython3.11.so"
fi

# Navigate to LEAN directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Build if requested
if [ "$1" == "build" ]; then
    echo "Building LEAN..."
    dotnet build QuantConnect.Lean.sln
    if [ $? -ne 0 ]; then
        echo "Build failed!"
        exit 1
    fi
fi

# Run LEAN
echo "Running LEAN..."
cd Launcher/bin/Debug/net9.0
dotnet QuantConnect.Lean.Launcher.dll
EOF

chmod +x /mnt/c/Projects/LEAN/run_lean.sh
```

**Usage:**
```bash
# Build and run
/mnt/c/Projects/LEAN/run_lean.sh build

# Just run (assumes already built)
/mnt/c/Projects/LEAN/run_lean.sh
```

**Verify Script:**
```bash
/mnt/c/Projects/LEAN/run_lean.sh
# Expected: LEAN runs successfully
```

---

## Cross-Platform Considerations

### Shared Data Directory

**LEAN's data folder is configured in `Launcher/config.json`:**
```json
"data-folder": "../../../Data/",
```

**Recommendation: Single Data Folder on Windows**
- Location: `C:\Projects\LEAN\Data` (or `D:\Data\LEAN` for large datasets)
- Both Windows LEAN and WSL LEAN access same data via path
- Saves disk space, ensures consistency
- WSL accesses via `/mnt/c/Projects/LEAN/Data`

**Configuration is already correct** (relative path works for both platforms)

---

### Build Output Strategy

**SEPARATE builds required:**
- Windows build outputs to `Launcher/bin/Debug/net9.0` (Windows DLLs)
- WSL build outputs to same path but with Linux binaries
- .NET determines platform at build time
- **Do not mix build outputs** (causes runtime errors)

**Best Practice:**
```cmd
:: Clean before switching platforms
:: Windows:
dotnet clean QuantConnect.Lean.sln
```

```bash
# WSL:
dotnet clean QuantConnect.Lean.sln
```

---

### Performance Considerations

**Windows (Primary Development):**
- ✅ Native filesystem performance
- ✅ Fast builds (~1-2 minutes)
- ✅ PyCharm runs smoothly

**WSL (Automation):**
- ⚠️ Building on `/mnt/c` is slower (2-5x)
- ✅ Acceptable for Claude Code (infrequent builds)
- ✅ Reading source files is fast enough
- ✅ Git operations work fine

**Optimization: Windows Defender Exclusions**
1. Windows Settings → Windows Security → Virus & threat protection
2. Manage settings → Exclusions → Add an exclusion → Folder
3. Add: `C:\Projects\LEAN`
4. Add: `C:\Users\datu\.nuget` (NuGet cache)
5. **Result:** 20-40% faster builds on Windows

---

## Validation & Testing

### Windows Setup Verification Checklist

```cmd
:: 1. Git Configuration
git config --get core.autocrlf
:: Expected: false

:: 2. .NET SDK
dotnet --version
:: Expected: 9.x.x

:: 3. Python Environment
conda activate lean_py311
python --version
:: Expected: Python 3.11.11

:: 4. Environment Variable
echo %PYTHONNET_PYDLL%
:: Expected: C:\Users\datu\Miniconda3\envs\lean_py311\python311.dll

:: 5. Build LEAN
cd C:\Projects\LEAN
dotnet build QuantConnect.Lean.sln
:: Expected: Build succeeded

:: 6. Run C# Algorithm
cd Launcher\bin\Debug\net9.0
dotnet QuantConnect.Lean.Launcher.dll
:: Expected: Algorithm completes successfully

:: 7. Run Python Algorithm (after editing config.json)
dotnet QuantConnect.Lean.Launcher.dll
:: Expected: Python algorithm completes successfully
```

**All checks passing = Windows setup complete ✅**

---

### WSL Setup Verification Checklist

```bash
# 1. Git Configuration
git config --get core.autocrlf
# Expected: false

# 2. .NET SDK
dotnet --version
# Expected: 9.x.x

# 3. Python Environment
conda activate lean_py311
python --version
# Expected: Python 3.11.11

# 4. Environment Variable
echo $PYTHONNET_PYDLL
# Expected: /home/datu/miniconda/envs/lean_py311/lib/libpython3.11.so

# 5. Build LEAN
cd /mnt/c/Projects/LEAN
dotnet build QuantConnect.Lean.sln
# Expected: Build succeeded

# 6. Run C# Algorithm
cd Launcher/bin/Debug/net9.0
dotnet QuantConnect.Lean.Launcher.dll
# Expected: Algorithm completes successfully

# 7. Run Python Algorithm (after editing config.json)
dotnet QuantConnect.Lean.Launcher.dll
# Expected: Python algorithm completes successfully
```

**All checks passing = WSL setup complete ✅**

---

### Cross-Platform Consistency Test

**Test: Ensure git doesn't show false modifications**

```cmd
:: Windows
cd C:\Projects\LEAN
git status
:: Expected: No uncommitted changes (or only intentional changes)
```

```bash
# WSL (same repository via mount)
cd /mnt/c/Projects/LEAN
git status
# Expected: Identical output to Windows
```

**If git shows many modified files:** Line ending configuration is wrong, revisit Git setup steps

---

### End-to-End Algorithm Test

**Test: Run same algorithm on both platforms, verify identical results**

1. Configure `Launcher/config.json` for `BasicTemplateAlgorithm` (Python)
2. **Run on Windows:**
   ```cmd
   cd C:\Projects\LEAN\Launcher\bin\Debug\net9.0
   dotnet QuantConnect.Lean.Launcher.dll
   ```
   Note final equity value from output

3. **Run on WSL:**
   ```bash
   cd /mnt/c/Projects/LEAN/Launcher/bin/Debug/net9.0
   dotnet QuantConnect.Lean.Launcher.dll
   ```
   Note final equity value from output

4. **Compare:** Final equity values should match (proves algorithmic consistency)

---

## Troubleshooting Guide

### Common Issues

#### Issue: Git shows all files as modified

**Cause:** Line ending mismatch

**Solution:**
```bash
# Set autocrlf to false
git config --global core.autocrlf false

# Reset repository
git rm --cached -r .
git reset --hard

# Verify
git status
```

---

#### Issue: BadPythonDllException when running LEAN

**Cause:** `PYTHONNET_PYDLL` not set or incorrect

**Windows Solution:**
```cmd
:: Check if set
echo %PYTHONNET_PYDLL%

:: If blank or wrong, set it:
setx PYTHONNET_PYDLL "C:\Users\datu\Miniconda3\envs\lean_py311\python311.dll"

:: IMPORTANT: Open NEW command prompt (variable loads at session start)
```

**WSL Solution:**
```bash
# Check if set
echo $PYTHONNET_PYDLL

# If blank, ensure conda activation script exists:
cat ~/miniconda/envs/lean_py311/etc/conda/activate.d/env_vars.sh

# Recreate if missing (see Step 3.5)
# Then:
conda deactivate
conda activate lean_py311
echo $PYTHONNET_PYDLL
```

---

#### Issue: ModuleNotFoundError: No module named 'pandas'

**Cause:** Python environment not activated or packages not installed

**Solution:**
```bash
conda activate lean_py311
pip install pandas==2.2.3 wrapt==1.16.0
```

---

#### Issue: PyCharm doesn't detect conda environment

**Solution:**
1. File → Invalidate Caches → Invalidate and Restart
2. After restart: File → Settings → Python Interpreter
3. Click "Show All" → Remove old interpreter entry
4. Add new interpreter → Conda Environment → Existing → Select path

---

#### Issue: Slow builds on WSL

**Cause:** `/mnt/c` filesystem performance

**Workaround (for frequent builds):**
```bash
# Copy repository to native Linux filesystem
cp -r /mnt/c/Projects/LEAN ~/lean_dev
cd ~/lean_dev
dotnet build QuantConnect.Lean.sln
# Much faster, but requires syncing changes back to Windows
```

**Recommended:** Build on Windows (primary development), use WSL builds only for Claude Code

---

#### Issue: VS Code C# extension not activating

**Solution:**
```
Ctrl+Shift+P → "OmniSharp: Restart OmniSharp"
```

If still not working:
1. Uninstall C# Dev Kit extension
2. Restart VS Code
3. Reinstall C# Dev Kit
4. Open `QuantConnect.Lean.sln` (VS Code should detect it)

---

### Emergency Clean Build

**Windows:**
```cmd
cd C:\Projects\LEAN
dotnet clean QuantConnect.Lean.sln
rmdir /s /q Launcher\bin
rmdir /s /q Launcher\obj
dotnet restore QuantConnect.Lean.sln
dotnet build QuantConnect.Lean.sln
```

**WSL:**
```bash
cd /mnt/c/Projects/LEAN
dotnet clean QuantConnect.Lean.sln
rm -rf Launcher/bin Launcher/obj
dotnet restore QuantConnect.Lean.sln
dotnet build QuantConnect.Lean.sln
```

---

## Best Practices

### Development Workflow

**Daily Development:**
1. Open PyCharm (Windows)
2. Activate `lean_py311` conda environment in terminal
3. Work on Python algorithms or C# engine code
4. Test locally before committing
5. Use PyCharm Git integration or Git Bash for commits

**Testing with Claude Code:**
1. Commit changes from Windows
2. Claude Code accesses repository via WSL mount (`/mnt/c/Projects/LEAN`)
3. Claude builds/tests in WSL environment
4. Review findings, iterate

---

### Git Best Practices

**Commit from Windows (primary):**
```cmd
cd C:\Projects\LEAN
git add .
git commit -m "Your message"
git push
```

**Both Windows and WSL work** if `core.autocrlf = false` is configured on both

---

### DO's and DON'Ts

**✅ DO:**
- Use Windows for primary development (PyCharm)
- Use WSL for Claude Code automation
- Keep separate build outputs
- Set `core.autocrlf = false` on both platforms
- Test algorithms on both platforms for consistency
- Use LF line endings for all text files
- Exclude `C:\Projects\LEAN` from Windows Defender

**❌ DON'T:**
- Share conda environments between Windows and WSL
- Use `core.autocrlf = true`
- Edit same files simultaneously in Windows and WSL (race conditions)
- Frequently build on WSL (slow on `/mnt/c`)
- Forget to set `PYTHONNET_PYDLL` (causes runtime errors)
- Mix .NET versions (use .NET 9 everywhere)

---

## Quick Reference Commands

### Windows

```cmd
:: Activate environment
conda activate lean_py311

:: Build LEAN
cd C:\Projects\LEAN
dotnet build QuantConnect.Lean.sln

:: Run LEAN
cd Launcher\bin\Debug\net9.0
dotnet QuantConnect.Lean.Launcher.dll

:: Clean build
dotnet clean QuantConnect.Lean.sln

:: Check environment
echo %PYTHONNET_PYDLL%
dotnet --version
python --version
```

### WSL

```bash
# Activate environment
conda activate lean_py311

# Build LEAN
cd /mnt/c/Projects/LEAN
dotnet build QuantConnect.Lean.sln

# Run LEAN
cd Launcher/bin/Debug/net9.0
dotnet QuantConnect.Lean.Launcher.dll

# Or use helper script
/mnt/c/Projects/LEAN/run_lean.sh build

# Clean build
dotnet clean QuantConnect.Lean.sln

# Check environment
echo $PYTHONNET_PYDLL
dotnet --version
python --version
```

### Git (Both Platforms)

```bash
# Check status
git status

# Stage and commit
git add .
git commit -m "Message"

# Push
git push

# Pull latest
git pull

# View log
git log --oneline -10
```

---

## Time Estimates

| Phase | Task | Time |
|-------|------|------|
| **Windows Setup** | Prepare repository location | 5 min |
| | Install Git + configure | 10 min |
| | Install .NET 9 SDK | 10 min |
| | Install Miniconda + env | 30 min |
| | Set PYTHONNET_PYDLL | 5 min |
| | Build LEAN (first time) | 10 min |
| | Run and test LEAN | 15 min |
| | Install PyCharm | 15 min |
| | Configure PyCharm | 20 min |
| | Setup debugging | 15 min |
| **Windows Total** | | **~2.5 hours** |
| **VS Code Setup** | Install VS Code + extensions | 20 min |
| | Configure project | 15 min |
| | Create launch configs | 15 min |
| **VS Code Total** | | **~1 hour** |
| **WSL Setup** | Configure Git | 5 min |
| | Install .NET 9 | 15 min |
| | Setup Python env | 20 min |
| | Set PYTHONNET_PYDLL | 10 min |
| | Build LEAN | 15 min |
| | Run and test LEAN | 10 min |
| | Create helper scripts | 10 min |
| **WSL Total** | | **~1.5 hours** |
| **Grand Total** | **Complete Setup** | **~5 hours** |

**Realistic Total with Troubleshooting:** 6-8 hours

---

## Additional Resources

- **LEAN GitHub:** https://github.com/QuantConnect/Lean
- **LEAN Documentation:** https://www.lean.io/docs/
- **.NET 9 Download:** https://dotnet.microsoft.com/en-us/download/dotnet/9.0
- **Miniconda:** https://docs.conda.io/en/latest/miniconda.html
- **PyCharm:** https://www.jetbrains.com/pycharm/
- **VS Code:** https://code.visualstudio.com/
- **WSL Documentation:** https://learn.microsoft.com/en-us/windows/wsl/

---

## Success Criteria

**Setup is complete when:**

✅ Windows can build and run LEAN (C# and Python algorithms)
✅ PyCharm can debug Python algorithms with breakpoints
✅ VS Code can build and debug LEAN
✅ WSL can build and run LEAN independently
✅ Git status is consistent across Windows and WSL (no false modifications)
✅ Same algorithm produces identical results on both platforms
✅ Claude Code can access and test repository via WSL

---

**End of Setup Guide**

*Keep this guide accessible for reference. Update with any environment-specific discoveries.*
