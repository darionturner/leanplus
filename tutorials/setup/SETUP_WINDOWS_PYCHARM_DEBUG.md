# LEAN Development Environment Setup Guide
## Windows 10 + PyCharm Native Installation

**Target Configuration:**
Windows 10 Enterprise + PyCharm Professional Python Dev & Debugging


## 1: Windows Native Setup (Primary Development)

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
