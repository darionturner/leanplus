# Tutorial 05: Environment Management on Windows

**Duration:** 45 minutes (20 min reading + 25 min hands-on)
**Prerequisites:** Tutorial 02 completed
**Goal:** Manage .NET SDKs, NuGet packages, and dependencies for LEAN

---

> **Shell Compatibility:** All `dotnet` commands work in both **Command Prompt (cmd)** and **PowerShell**. File operations differ - alternatives shown where needed.

---

## 📋 Table of Contents

1. [Overview](#1-overview-5-min)
2. [.NET SDK Versioning](#2-net-sdk-versioning-10-min)
3. [NuGet Package Management](#3-nuget-package-management-10-min)
4. [Solution and Project Management](#4-solution-and-project-management-10-min)
5. [Dependency Resolution](#5-dependency-resolution-5-min)
6. [Validation Checklist](#6-validation-checklist-5-min)

---

## 1. Overview (5 min)

### What is Environment Management?

**In Python:**
```python
# Virtual environments, conda
conda create -n myenv python=3.11
conda activate myenv
pip install pandas==2.2.3
```

**In C#:**
```
# SDK versions, project targeting
dotnet --list-sdks  # Multiple SDKs can coexist
# Package management via NuGet
# Target framework in .csproj files
```

---

### Key Differences from Python

| Aspect | Python | C# / .NET |
|--------|--------|-----------|
| **Environment Isolation** | Virtual envs (venv, conda) | Global SDK + project-level targeting |
| **Package Manager** | pip, conda | NuGet |
| **Dependency File** | requirements.txt | .csproj (PackageReference) |
| **Version Locking** | Manual (==) | Automatic (lock files) |
| **Environment Activation** | Required (activate) | Automatic (SDK used by project) |

---

## 2. .NET SDK Versioning (10 min)

### Multiple SDK Versions

**Check installed SDKs:**
```
dotnet --list-sdks

# Output:
6.0.425 [C:\Program Files\dotnet\sdk]
8.0.404 [C:\Program Files\dotnet\sdk]
9.0.100 [C:\Program Files\dotnet\sdk]
```

**All SDKs coexist:**
- No activation needed
- Projects specify which to use

---

### global.json - Project SDK Selection

**Create:** `C:\Projects\LEAN\global.json`

```json
{
  "sdk": {
    "version": "9.0.300",
    "rollForward": "latestPatch"
  }
}
```

**Settings:**
- `version`: Minimum SDK required
- `rollForward`: How to select SDK version
  - `disable`: Exact version only (fails if not installed)
  - `latestPatch`: Highest patch in same feature band (9.0.3xx)
  - `latestFeature`: Highest feature band in same major.minor (9.0.xxx)
  - `latestMinor`: Highest minor in same major (9.x.xxx)
  - `latestMajor`: Highest available SDK

**SDK version format:** `major.minor.featureband+patch` (e.g., 9.0.306 = feature band 3, patch 06)

**Verify:**
```
cd C:\Projects\LEAN
dotnet --version
# Shows: 9.0.306 (highest patch in 9.0.3xx)
```

---

### Installing Additional SDKs

**Why multiple SDKs?**
- Different projects need different versions
- Test compatibility across versions
- Legacy project support

**Install .NET 8 (example):**
```
Download: https://dotnet.microsoft.com/download/dotnet/8.0
Install: dotnet-sdk-8.0.xxx-win-x64.exe
Verify: dotnet --list-sdks
```

**Both SDKs available:**
```
8.0.404 [C:\Program Files\dotnet\sdk]
9.0.100 [C:\Program Files\dotnet\sdk]
```

---

## 3. NuGet Package Management (10 min)

### Understanding NuGet

**NuGet** = Python's `pip` equivalent for .NET

```
pip install pandas         ↔   dotnet add package Newtonsoft.Json
pip list                   ↔   dotnet list package
pip show pandas            ↔   dotnet list package --include-transitive
```

---

### Package References in .csproj

**File:** `Common/QuantConnect.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.2" />
    <PackageReference Include="NodaTime" Version="3.0.5" />
    <PackageReference Include="MathNet.Numerics" Version="5.0.0" />
    <PackageReference Include="QuantConnect.pythonnet" Version="2.0.48" />
  </ItemGroup>
</Project>
```

**Equivalent Python:**
```python
# requirements.txt
newtonsoft-json==13.0.2
nodatime==3.0.5
mathnet-numerics==5.0.0
```

---

### Exercise 1: Adding a Package (5 min)

**Add package to Common project:**

```
cd C:\Projects\LEAN\Common
dotnet add package CsvHelper --version 30.0.1
```

**What happens:**
1. Package downloaded to global cache
2. `.csproj` file updated:
   ```xml
   <PackageReference Include="CsvHelper" Version="30.0.1" />
   ```
3. Package available in code

**Verify:**
```
dotnet list package

# Output:
Project 'QuantConnect.Common' has the following package references
   [net9.0]:
   Top-level Package      Requested   Resolved
   > CsvHelper            30.0.1      30.0.1
   > Newtonsoft.Json      13.0.2      13.0.2
   ...
```

---

### Exercise 2: Updating Packages (3 min)

**List outdated packages:**
```
dotnet list package --outdated
```

**Update specific package:**
```
dotnet add package Newtonsoft.Json --version 13.0.4
```

**Update all packages in project:**
```
# No built-in command, manual in .csproj
# OR use dotnet-outdated tool:
dotnet tool install --global dotnet-outdated-tool
dotnet outdated --upgrade
```

---

### NuGet Cache Location

**Global package cache:**
```
C:\Users\{username}\.nuget\packages\
```

**Similar to:**
```python
# pip cache
%LOCALAPPDATA%\pip\cache
```

**Clear cache if issues:**
```
dotnet nuget locals all --clear
```

---

## 4. Solution and Project Management (10 min)

### Solution Structure

**Solution (.sln)** = Container for projects

```
LEAN Solution
├── Common (project)
├── Engine (project)
├── Launcher (project)
└── Algorithm.CSharp (project)
```

**Python equivalent:**
```
LEAN/
├── common/
├── engine/
├── launcher/
└── algorithm/
```

No formal "solution" concept in Python

---

### Exercise 3: Adding Project to Solution (5 min)

**Create new project:**

```
cd C:\Projects\LEAN
dotnet new classlib -n Custom.PowerDelivery
```

**Add to solution:**
```
dotnet sln QuantConnect.Lean.sln add Custom.PowerDelivery/Custom.PowerDelivery.csproj
```

**Verify:**
```
dotnet sln list

# Output includes:
Custom.PowerDelivery\Custom.PowerDelivery.csproj
```

---

### Project References (Dependencies)

**Add project reference:**

```
cd Custom.PowerDelivery
dotnet add reference ../Common/QuantConnect.csproj
```

**Creates dependency:**
```xml
<!-- Custom.PowerDelivery.csproj -->
<ItemGroup>
  <ProjectReference Include="..\Common\QuantConnect.csproj" />
</ItemGroup>
```

**Python equivalent:**
```python
# In setup.py or similar
install_requires=['quantconnect-common']
```

---

### Cleanup: Remove Practice Project

**Important:** This exercise is for learning. Remove the practice project to keep the LEAN repo clean. We'll create a properly configured PowerDelivery project during implementation phase.

**Remove from solution:**
```
cd C:\Projects\LEAN
dotnet sln QuantConnect.Lean.sln remove Custom.PowerDelivery/Custom.PowerDelivery.csproj
```

**Delete the project folder:**
```
# PowerShell:
Remove-Item -Recurse -Force Custom.PowerDelivery

# Command Prompt (cmd):
rmdir /s /q Custom.PowerDelivery
```

**Verify removal:**
```
dotnet sln list
# Custom.PowerDelivery should no longer appear

# Check folder is gone:
# PowerShell: Test-Path Custom.PowerDelivery  (returns False)
# cmd: dir Custom.PowerDelivery  (returns "File Not Found")
```

**Why cleanup?**
- Keeps repo aligned with upstream LEAN
- Avoids git tracking practice files
- Real implementation will have proper configuration (dependencies, namespaces, target framework)

---

### Exercise 4: Target Framework (3 min)

**Every project specifies target:**

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
  </PropertyGroup>
</Project>
```

**Common targets:**
- `net6.0` - .NET 6
- `net8.0` - .NET 8
- `net9.0` - .NET 9
- `netstandard2.0` - Cross-platform library

**LEAN uses:** `net9.0`

**Multi-targeting:**
```xml
<TargetFrameworks>net6.0;net8.0</TargetFrameworks>
```

Builds for both frameworks

---

## 5. Dependency Resolution (5 min)

### How .NET Resolves Dependencies

**Build process:**
```
1. Read .csproj files
2. Resolve NuGet packages
3. Check version conflicts
4. Create dependency graph
5. Download missing packages
6. Compile in dependency order
```

---

### Dependency Conflicts

**Scenario:** Two projects need different versions

```
Project A → Newtonsoft.Json 13.0.3
Project B → Newtonsoft.Json 12.0.1
```

**.NET Resolution:**
- Uses **highest version** (13.0.3)
- Warns if incompatible

**Python equivalent:**
```python
# pip installs latest unless pinned
# Can cause runtime issues if incompatible
```

---

### Lock Files (obj/)

**After build:**
```
Common/obj/project.assets.json  # Dependency lock file
Common/obj/project.nuget.cache  # NuGet cache
```

**Similar to:**
```python
# Pipfile.lock, poetry.lock
```

**Contains:**
- Exact resolved versions
- Transitive dependencies
- Package hashes

**Safe to delete (forces re-resolution):**
```
# PowerShell:
Remove-Item -Recurse -Force obj, bin

# Command Prompt (cmd):
rmdir /s /q obj
rmdir /s /q bin

# Then restore:
dotnet restore
```

---

## 6. Validation Checklist (5 min)

### SDK Management
- [X] I can list installed SDKs (`dotnet --list-sdks`)
- [X] I understand global.json purpose
- [X] I can install multiple SDK versions
- [X] I know SDK selection is automatic per project

### NuGet Packages
- [X] I can add packages (`dotnet add package`)
- [X] I can list packages (`dotnet list package`)
- [X] I understand .csproj PackageReference
- [X] I know where packages are cached (`~/.nuget/packages`)
- [X] I can clear NuGet cache if needed

### Projects & Solutions
- [X] I understand .sln vs .csproj
- [X] I can add project to solution
- [X] I can add project references (dependencies)
- [X] I know what TargetFramework means
- [X] I can create new projects (`dotnet new`)

### Dependency Management
- [X] I understand how .NET resolves conflicts (highest version)
- [X] I know obj/ contains lock files
- [X] I can force dependency re-resolution (`dotnet restore`)

---

## 🔧 Common Commands Reference

> All `dotnet` commands below work in both **cmd** and **PowerShell**.

```
# SDK Management
dotnet --list-sdks                    # List installed SDKs
dotnet --version                      # SDK used by current project

# Package Management
dotnet add package <name>             # Add NuGet package
dotnet list package                   # List packages
dotnet list package --outdated        # Check for updates
dotnet restore                        # Download packages

# Solution Management
dotnet sln list                       # List projects in solution
dotnet sln add <project.csproj>       # Add project to solution
dotnet sln remove <project.csproj>    # Remove from solution

# Project Management
dotnet new classlib -n <name>         # New class library
dotnet new console -n <name>          # New console app
dotnet add reference <project.csproj> # Add project dependency

# Build & Clean
dotnet build                          # Build solution/project
dotnet clean                          # Clean build artifacts
dotnet restore                        # Restore packages

# File Operations (shell-specific)
# PowerShell: Remove-Item -Recurse -Force <folder>
# cmd:        rmdir /s /q <folder>
```

---

## 🎯 Key Takeaways

1. **Multiple SDKs coexist** - No manual activation needed
2. **global.json selects SDK** - Per-project SDK version control
3. **NuGet = pip** - Package management for .NET
4. **PackageReference in .csproj** - Like requirements.txt but XML
5. **Highest version wins** - Automatic conflict resolution

---

## ⏭️ Next Tutorial

**Tutorial 06: C# Setup on WSL for Claude**
- Install .NET SDK on WSL
- Build LEAN in Linux environment
- Enable Claude Code automation
- Path translation strategies

**Time to Complete:** 90 minutes

---

**🎓 Congratulations!** You now understand C# environment management. You can manage SDKs, packages, and dependencies like a pro.

*Mark this tutorial as complete in the main README.md*

---

*Last Updated: 2025-11-16*
