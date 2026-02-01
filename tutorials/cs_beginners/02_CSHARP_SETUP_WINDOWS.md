# Tutorial 02: C# Setup on Windows

**Duration:** 45 minutes (15 min reading + 30 min hands-on)
**Prerequisites:** Tutorial 01 completed, Windows 10/11
**Goal:** Install and configure C# development tools for LEAN

---

## 📋 Table of Contents

1. [Overview](#1-overview-5-min)
2. [.NET SDK Installation](#2-net-sdk-installation-10-min)
3. [IDE Selection Guide](#3-ide-selection-guide-10-min)
4. [Building LEAN from Command Line](#4-building-lean-from-command-line-10-min)
5. [Understanding LEAN's Project Structure](#5-understanding-leans-project-structure-5-min)
6. [Validation Checklist](#6-validation-checklist-5-min)

---

## 1. Overview (5 min)

### What You're Installing

**Core Requirement:**
- **.NET SDK 9.0+** - Compiler, runtime, and build tools for C#

**Optional (Choose One IDE):**
- **Visual Studio 2022** (Community) - Full-featured, heavyweight (~10GB)
- **JetBrains Rider** - Fast, commercial ($$$), excellent for Python+C#
- **VS Code** - Lightweight, free, already installed if following Phase 2

**Already Done** (from Phase 1):
- ✅ .NET 9 SDK installed
- ✅ LEAN builds successfully
- ✅ Repository at `C:\Projects\LEAN`

### What We'll Verify

```
✅ .NET SDK version 9.0+
✅ LEAN solution builds without errors
✅ Can run C# algorithm from command line
✅ IDE recognizes LEAN project structure
```

---

## 2. .NET SDK Installation (10 min)

### Check Existing Installation

**Open Command Prompt or PowerShell:**
```powershell
# Check .NET version
dotnet --version

# Expected output: 9.0.xxx
```

**If .NET 9 is already installed:**
```powershell
dotnet --list-sdks

# Output should include:
# 9.0.xxx [C:\Program Files\dotnet\sdk]
```

✅ **You already have .NET SDK from Phase 1 setup - skip to IDE selection**

---

### Fresh Installation (If Needed)

**Step 1: Download .NET SDK**

Visit: https://dotnet.microsoft.com/download/dotnet/9.0

1. Click **".NET SDK 9.0.xxx"** (get latest 9.0.x version)
2. Choose **"Windows x64 installer"**
3. Download `dotnet-sdk-9.0.xxx-win-x64.exe`

**Step 2: Run Installer**

1. Double-click downloaded installer
2. Accept license agreement
3. Click **"Install"**
4. Wait 2-3 minutes for installation
5. Click **"Close"**

**Step 3: Verify Installation**

Open **new** Command Prompt window:
```powershell
dotnet --version
# Should show: 9.0.xxx

dotnet --info
# Shows detailed SDK and runtime information
```

**Expected Output:**
```
.NET SDK:
 Version:           9.0.100
 Commit:            5535e31

Runtime Environment:
 OS Name:     Windows
 OS Version:  10.0.xxxxx

.NET SDKs installed:
  9.0.100 [C:\Program Files\dotnet\sdk]

.NET runtimes installed:
  Microsoft.AspNetCore.App 9.0.0
  Microsoft.NETCore.App 9.0.0
```

---

## 3. IDE Selection Guide (10 min)

### Option Comparison

| Feature | Visual Studio 2022 | JetBrains Rider | VS Code |
|---------|-------------------|-----------------|---------|
| **Price** | Free (Community) | $149/year | Free |
| **Size** | ~10 GB | ~2 GB | ~500 MB |
| **C# Support** | Excellent (native) | Excellent | Good (via extension) |
| **Python Support** | Basic | Excellent | Excellent |
| **Performance** | Slow startup | Fast | Very fast |
| **Learning Curve** | Moderate | Easy (if using PyCharm) | Easy |
| **LEAN Debugging** | Excellent | Excellent | Good |
| **Best For** | C#-heavy dev | Python+C# together | Lightweight, quick edits |

### Recommendation for LEAN

**If you have PyCharm Professional:**
→ **Use Rider** (same company, similar UI, trial available)
- Familiar interface
- Seamless Python + C# switching
- 30-day free trial

**If using VS Code for Python:**
→ **Continue with VS Code** (follow Tutorial 04)
- Already configured
- C# Dev Kit extension (free)
- Lightweight

**If primarily C# development:**
→ **Visual Studio 2022 Community**
- Best-in-class C# tooling
- Free for individual developers
- Microsoft's official IDE

---

### Option A: Visual Studio 2022 (Skip if using Rider/VS Code)

**Download:**
https://visualstudio.microsoft.com/downloads/

1. Download **"Visual Studio 2022 Community"**
2. Run installer
3. Select **".NET desktop development"** workload
4. Click **"Install"**
5. Wait ~30 minutes (large download)

**Open LEAN in Visual Studio:**
```
File → Open → Project/Solution
Navigate to: C:\Projects\LEAN\QuantConnect.Lean.sln
Click "Open"
```

**Build LEAN:**
```
Build → Build Solution (Ctrl+Shift+B)
Wait 1-2 minutes
Check Output window: "Build succeeded"
```

---

### Option B: JetBrains Rider (Recommended if using PyCharm)

**Download:**
https://www.jetbrains.com/rider/download/

1. Download **"Windows .exe (Intel)"**
2. Run installer
3. Accept defaults
4. Launch Rider
5. **Start 30-day trial** (or enter license)

**Open LEAN in Rider:**
```
File → Open
Navigate to: C:\Projects\LEAN\QuantConnect.Lean.sln
Click "Open"
```

**Configure Rider:**
```
File → Settings
├── Build, Execution, Deployment
│   └── Toolset and Build
│       └── Use: "MSBuild 17.0" or ".NET SDK"
└── OK
```

**Build LEAN:**
```
Build → Build Solution (Ctrl+F9)
Check Build tab: "Build completed successfully"
```

**Advantages for LEAN:**
- Navigate between C# and Python seamlessly
- Integrated debugger for both languages
- Better performance than Visual Studio

---

### Option C: VS Code (Already Configured in Phase 2)

**Verify C# Extension Installed:**
```
Extensions (Ctrl+Shift+X)
Search: "C# Dev Kit"
Should show: "C# Dev Kit" by Microsoft (installed)
```

**Open LEAN in VS Code:**
```
File → Open Folder
Navigate to: C:\Projects\LEAN
Click "Select Folder"
```

**Build LEAN:**
```
Terminal → Run Build Task (Ctrl+Shift+B)
Select: "dotnet: build"
Check output: "Build succeeded"
```

---

## 4. Building LEAN from Command Line (10 min)

### Why Command Line Matters

- **CI/CD:** Automated builds don't use IDEs
- **Troubleshooting:** Isolate IDE vs build issues
- **Speed:** Faster than opening large IDE
- **Claude Automation:** WSL builds use command line

---

### Exercise 1: Full Build (5 min)

**Navigate to LEAN directory:**
```powershell
cd C:\Projects\LEAN
```

**Clean previous build artifacts:**
```powershell
dotnet clean QuantConnect.Lean.sln
```

**Build entire solution:**
```powershell
dotnet build QuantConnect.Lean.sln

# Alternative with detailed output:
dotnet build QuantConnect.Lean.sln --verbosity normal
```

**Expected Output:**
```
Microsoft (R) Build Engine version 17.x.x
Copyright (C) Microsoft Corporation. All rights reserved.

  Determining projects to restore...
  All projects are up-to-date for restore.

  QuantConnect.Configuration -> C:\Projects\LEAN\Common\bin\Debug\QuantConnect.Configuration.dll
  QuantConnect.Lean.Engine -> C:\Projects\LEAN\Engine\bin\Debug\QuantConnect.Lean.Engine.dll
  QuantConnect.Lean.Launcher -> C:\Projects\LEAN\Launcher\bin\Debug\QuantConnect.Lean.Launcher.dll

Build succeeded.
    6858 Warning(s)
    0 Error(s)

Time Elapsed 00:01:32.45
```

**Understanding Output:**
- ✅ **0 Errors** - Build successful
- ⚠️ **6000-7000 Warnings** - Normal (nullable reference warnings)
- **Build artifacts** → `Launcher\bin\Debug\`

---

### Exercise 2: Build Specific Project (3 min)

**Build only Common (core library):**
```powershell
cd Common
dotnet build QuantConnect.csproj

# Or simply (auto-detects single .csproj in directory):
dotnet build
```

**Build only Launcher:**
```powershell
cd ..\Launcher
dotnet build QuantConnect.Lean.Launcher.csproj
```

**Note:** LEAN project file names don't always match folder names. Use `dir *.csproj` to find the actual filename.

**Incremental Build (faster):**
```powershell
# Only rebuilds changed projects
cd C:\Projects\LEAN
dotnet build QuantConnect.Lean.sln --no-restore
```

---

### Exercise 3: Run C# Algorithm (2 min)

**Navigate to build output:**
```powershell
cd C:\Projects\LEAN\Launcher\bin\Debug
```

**Run LEAN:**
```powershell
dotnet QuantConnect.Lean.Launcher.dll
```

**Expected Output:**
```
20250116 18:30:00 TRACE:: Config.Get(): Configuration key not found. Key: data-permission-manager
20250116 18:30:00 TRACE:: Engine.Run(): LEAN ALGORITHMIC TRADING ENGINE v2.5.xxx
...
20250116 18:30:05 TRACE:: BasicTemplateFrameworkAlgorithm: Algorithm initialized
...
STATISTICS::
  Total Trades: 1
  Average Win: 0%
  Average Loss: 0%
  ...
```

**Stop Execution:**
- Press `Ctrl+C`

---

### Build Configurations

**Debug (default):**
```powershell
dotnet build --configuration Debug

# Optimized for debugging (slower, more info)
# Output: bin\Debug\
```

**Release (production):**
```powershell
dotnet build --configuration Release

# Optimized for performance (faster, less info)
# Output: bin\Release\
```

**For LEAN development:**
- Use **Debug** during development (better stack traces)
- Use **Release** for performance benchmarking

---

## 5. Understanding LEAN's Project Structure (5 min)

### Solution File (.sln)

**File:** `QuantConnect.Lean.sln`

```xml
<!-- Solution contains multiple projects -->
Microsoft Visual Studio Solution File, Format Version 12.00
Project("{FAE04EC0-...}") = "QuantConnect.Configuration", "Common\QuantConnect.Configuration.csproj"
Project("{FAE04EC0-...}") = "QuantConnect.Lean.Engine", "Engine\QuantConnect.Lean.Engine.csproj"
...
```

**Purpose:**
- Groups related projects together
- Defines build order (dependencies)
- Shared across all IDEs

**Command:**
```powershell
# Build all projects in solution
dotnet build QuantConnect.Lean.sln
```

---

### Project Files (.csproj)

**Example:** `Common\QuantConnect.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
    <LangVersion>latest</LangVersion>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="NodaTime" Version="3.1.9" />
  </ItemGroup>
</Project>
```

**Key Elements:**
- `<TargetFramework>`: .NET version (net6.0, net9.0, etc.)
- `<PackageReference>`: NuGet dependencies
- `<ProjectReference>`: Dependencies on other LEAN projects

---

### Build Output Structure

```
Launcher\bin\Debug\
├── QuantConnect.Lean.Launcher.dll      # Main executable
├── QuantConnect.Lean.Engine.dll        # Engine library
├── QuantConnect.Common.dll             # Common library
├── Newtonsoft.Json.dll                 # NuGet dependency
├── config.json                         # Must copy manually!
└── ... (other dependencies)
```

**Critical:**
- `config.json` NOT copied automatically
- Must manually copy: `copy Launcher\config.json Launcher\bin\Debug\config.json`

---

### Dependency Graph (Simplified)

LEAN has 20+ projects. Here's a simplified view of the key dependencies:

```
Launcher (executable) ─── 17 direct dependencies
  │
  ├─→ Engine
  │    ├─→ Algorithm ──────┐
  │    ├─→ Brokerages ─────┼─→ Common ─┬─→ Configuration
  │    ├─→ AlgorithmFactory│           ├─→ Logging
  │    └─→ Indicators ─────┘           └─→ Compression
  │
  ├─→ Algorithm.Python ─→ Algorithm
  │
  └─→ Api, Messaging, Queues, Research, ToolBox...
```

**Note:** The `Data/` folder contains data files, not a project.

**Build Order:**
1. **Configuration, Logging, Compression** (foundational - no LEAN dependencies)
2. **Common** (depends on above three)
3. **Indicators, Api** (depend on Common)
4. **Algorithm** (depends on Common, Indicators)
5. **Brokerages, AlgorithmFactory** (depend on Common, Algorithm)
6. **Engine** (depends on most above)
7. **Launcher** (depends on everything)

---

### Quick Reference: Essential Commands

**Build Commands:**
```powershell
# Full solution build (Debug mode - default)
cd C:\Projects\LEAN
dotnet build QuantConnect.Lean.sln

# Build specific project (faster iteration)
cd Common
dotnet build

# Release build (optimized, for benchmarking)
dotnet build QuantConnect.Lean.sln --configuration Release

# Clean build (remove all artifacts first)
dotnet clean QuantConnect.Lean.sln
dotnet build QuantConnect.Lean.sln

# Incremental build (skip restore, faster)
dotnet build QuantConnect.Lean.sln --no-restore
```

**Config Management:**
```powershell
# Copy config to runtime location (REQUIRED after editing)
copy Launcher\config.json Launcher\bin\Debug\config.json

# Verify config is in place
dir Launcher\bin\Debug\config.json
```

**Run LEAN:**
```powershell
# Run from build output directory
cd C:\Projects\LEAN\Launcher\bin\Debug
dotnet QuantConnect.Lean.Launcher.dll

# Stop execution
Ctrl+C
```

**Combined Workflows:**
```powershell
# Build + copy config + run (full workflow)
cd C:\Projects\LEAN
dotnet build QuantConnect.Lean.sln && copy Launcher\config.json Launcher\bin\Debug\config.json && cd Launcher\bin\Debug && dotnet QuantConnect.Lean.Launcher.dll

# Quick rebuild + run (after code changes)
dotnet build --no-restore && copy Launcher\config.json Launcher\bin\Debug\config.json
```

**Diagnostics:**
```powershell
# Check .NET version
dotnet --version

# List installed SDKs
dotnet --list-sdks

# Find project files in a directory
dir *.csproj

# Restore NuGet packages (if build fails on dependencies)
dotnet restore QuantConnect.Lean.sln
```

---

## 6. Validation Checklist (5 min)

### Environment Setup
- [X] `.NET SDK 9.0+` installed and verified
- [X] `dotnet --version` returns 9.0.xxx
- [X] IDE installed (Visual Studio, Rider, or VS Code configured)

### LEAN Build
- [X] `dotnet build QuantConnect.Lean.sln` succeeds (0 errors)
- [X] Build completes in ~90 seconds
        ~152 seconds on laptop
- [X] 6000-7000 warnings present (expected)
- [X] Output directory exists: `Launcher\bin\Debug\`

### Running LEAN
- [X] `dotnet QuantConnect.Lean.Launcher.dll` starts without errors
- [X] Algorithm runs (BasicTemplateFrameworkAlgorithm)
- [X] Statistics printed at end
- [X] Can stop with Ctrl+C

### IDE Integration
- [X] IDE opens `QuantConnect.Lean.sln` successfully
- [X] Solution Explorer shows all projects (~30 projects)
      - **Visual Studio:** View → Solution Explorer (Ctrl+Alt+L)
      - **Rider:** View → Tool Windows → Solution (Alt+1)
      - **VS Code:** Look for "SOLUTION EXPLORER" in Explorer panel
      - **Command line alternative:** `dotnet sln list` (works without IDE)
- [X] Can build from IDE (Build → Build Solution)
- [X] IntelliSense works (code completion)

### Understanding
- [X] I know where build output goes (`bin\Debug\`)
- [X] I understand .sln vs .csproj files
- [X] I know how to build from command line
- [X] I can navigate LEAN project structure

---

## 🔧 Troubleshooting

### Issue: "dotnet command not found"

**Cause:** .NET SDK not in PATH

**Fix:**
1. Restart terminal (new PATH needed)
2. OR manually add to PATH:
   ```
   System Properties → Environment Variables → System Variables
   Edit "Path" → Add: C:\Program Files\dotnet\
   ```

---

### Issue: Build errors about missing packages

**Cause:** NuGet packages not restored

**Fix:**
```powershell
dotnet restore QuantConnect.Lean.sln
dotnet build QuantConnect.Lean.sln
```

---

### Issue: "Could not load file or assembly..."

**Cause:** Different .NET versions between projects

**Fix:**
```powershell
# Clean and rebuild
dotnet clean
dotnet build
```

---

### Issue: 7000+ warnings overwhelming output

**Suppress warnings (optional):**
```powershell
# Build with minimal warnings
dotnet build --verbosity minimal

# OR redirect warnings to file
dotnet build > build.log 2>&1
```

**Note:** Warnings are safe to ignore (nullable reference types)

---

## 📚 Further Reading

**Essential:**
- [.NET CLI Overview](https://learn.microsoft.com/en-us/dotnet/core/tools/)
- [MSBuild Reference](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild)

**IDE Guides:**
- [Visual Studio C# Debugging](https://learn.microsoft.com/en-us/visualstudio/debugger/debugger-feature-tour)
- [Rider Documentation](https://www.jetbrains.com/help/rider/)
- [VS Code C# Extension](https://code.visualstudio.com/docs/languages/csharp)

---

## 🎯 Key Takeaways

1. **.NET SDK is separate from IDE** - SDK required, IDE optional
2. **Command line builds = automation-ready** - Critical for CI/CD
3. **Solution (.sln) groups projects** - Build entire LEAN with one command
4. **Build output → bin\Debug\** - Know where executables go
5. **Warnings are normal** - 6000-7000 nullable warnings expected

---

## ⏭️ Next Tutorial

**Tutorial 03: C# Debugging in JetBrains IDEs**
- Set up Rider for C# debugging
- Debug C# algorithms with breakpoints
- Step through LEAN engine code
- Advanced debugging techniques

**OR**

**Tutorial 04: C# Debugging in VS Code**
- Configure C# Dev Kit
- Create launch configurations
- Debug C# and Python together
- Performance profiling

**Time to Complete:** 60-90 minutes each

---

**🎓 Congratulations!** You now have a working C# development environment for LEAN. You can build, run, and begin exploring the codebase.

*Mark this tutorial as complete in the main README.md*

---

*Last Updated: 2025-11-16*
