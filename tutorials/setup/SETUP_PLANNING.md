# LEAN Development Setup Plan for Energy Markets Team

## Executive Summary

**Recommended Approach:** **Phased Hybrid Strategy**
- **Phase 1 (Months 1-3):** Native Installation for engine modifications
- **Phase 2 (Month 3+):** Transition to DevContainer for team standardization
- **Complementary:** Jupyter for research throughout

**Rationale:** Your project REQUIRES engine modifications (EPEX brokerage, custom data types, 24/7 market hours) which eliminates LEAN CLI as an option. Native development provides maximum flexibility initially, then DevContainer ensures team consistency.

---

## Setup Approaches Analysis

### ✅ RECOMMENDED: Native Installation (Primary - Months 1-3)

**Why This First:**
- ✅ **CRITICAL:** Can implement EPEX brokerage plugin (IBrokerage interface)
- ✅ **CRITICAL:** Can create PowerPrice/GasPrice custom data types
- ✅ **CRITICAL:** Can extend MarketHoursDatabase for 24/7 trading
- ✅ Full C# debugger access for troubleshooting
- ✅ Fastest iteration speed for engine modifications
- ✅ VS Code and PyCharm both supported

**Setup Requirements:**
- .NET 9 SDK (or .NET 6 minimum)
- Python 3.11.11 via Conda
- `PYTHONNET_PYDLL` environment variable
- pandas=2.2.3, wrapt=1.16.0

**Pros for Your Use Case:**
- Engine team can work at full speed
- No Docker overhead during intensive debugging
- Direct file system access to data
- Maximum flexibility for experimentation

**Cons:**
- Each developer needs manual setup (~1-2 hours)
- Environment consistency requires discipline
- "Works on my machine" risk

**When to Use:** Engine modifications, custom brokerage development, initial integration

---

### ✅ RECOMMENDED: DevContainer (Team Standard - Month 3+)

**Why Transition to This:**
- ✅ Team consistency (identical environments)
- ✅ Easy onboarding (<10 min for new developers)
- ✅ Still allows C# engine modifications
- ✅ VS Code first-class support
- ✅ CI/CD ready

**Setup Requirements:**
- Docker Desktop/Engine
- VS Code + Remote Containers extension
- Existing `.devcontainer/` config (already in repo)

**Pros for Your Use Case:**
- Eliminates environment drift across team
- Algorithm developers get consistent setup
- Scales better as team grows
- Natural path to production containerization

**Cons:**
- Docker overhead (minimal on modern hardware)
- VS Code dependency (PyCharm less ideal)
- 30-second startup time per session
- WSL2 + Docker adds complexity layer

**When to Use:** Team collaboration phase, algorithm development, new team members

---

### ✅ COMPLEMENTARY: Jupyter Research Environment

**Why Use This:**
- ✅ Perfect for exploring EPEX orderbook data
- ✅ Rapid strategy prototyping before coding
- ✅ Interactive visualization of delivery periods
- ✅ Team knowledge sharing via notebooks

**Setup:** `lean research` command or `docker run quantconnect/research`

**When to Use:** Data analysis, strategy brainstorming, documentation

---

### ❌ NOT RECOMMENDED: LEAN CLI (Algorithms Only)

**Why Not Primary:**
- ❌ **BLOCKER:** Cannot modify engine (pre-built Docker images)
- ❌ **BLOCKER:** Cannot add EPEX brokerage
- ❌ **BLOCKER:** Cannot add PowerPrice/GasPrice data types
- ❌ Limited IDE integration for debugging

**Future Use:** After engine adaptations complete, algorithm-only developers can use LEAN CLI

---

## Detailed Implementation Plan

### Phase 1: Initial Setup & Validation (Week 1)

**Objective:** Get LEAN building and running with native installation

#### Step 1.1: Resolve Environment Blockers
```bash
# Install .NET 9 SDK (or verify if in Conda)
wget https://dot.net/v1/dotnet-install.sh
chmod +x dotnet-install.sh
./dotnet-install.sh --channel 9.0

# Create Python 3.11 Conda environment
conda create -n qc_lean python=3.11.11 pandas=2.2.3 wrapt=1.16.0
conda activate qc_lean

# Set PYTHONNET_PYDLL environment variable
export PYTHONNET_PYDLL="$HOME/miniconda3/envs/qc_lean/lib/libpython3.11.so"
echo 'export PYTHONNET_PYDLL="$HOME/miniconda3/envs/qc_lean/lib/libpython3.11.so"' >> ~/.bashrc
```

**Expected Outcome:**
- ✅ `dotnet --version` shows 9.x or 6.x
- ✅ `python --version` shows 3.11.11
- ✅ `echo $PYTHONNET_PYDLL` shows path to libpython

#### Step 1.2: Build LEAN Solution
```bash
cd /mnt/c/Users/datu/ReposWSL/LEAN
dotnet build QuantConnect.Lean.sln
```

**Expected Outcome:**
- ✅ Build succeeds with 0 errors
- ✅ Binaries in `Launcher/bin/Debug/`

#### Step 1.3: Run POC Algorithm (Validate End-to-End)
```bash
cd Launcher/bin/Debug
dotnet QuantConnect.Lean.Launcher.dll
```

**Expected Outcome:**
- ✅ SimpleMovingAveragePOC.py runs successfully
- ✅ Backtest completes with results
- ✅ Confirms Python integration works

#### Step 1.4: Document Setup
- Create `docs/SETUP_NATIVE.md` with exact steps taken
- Include any workarounds or OS-specific issues
- Create setup script for future developers

---

### Phase 2: Team Developer Setup (Week 1-2)

**For Each Developer:**

#### Option A: Native Installation (Engine Developers)
Follow Phase 1 steps on their machines

#### Option B: VS Code DevContainer (Algorithm Developers)
```bash
# 1. Install prerequisites
# - Docker Desktop (Windows) or Docker Engine (Linux)
# - VS Code + Remote Containers extension

# 2. Clone repository
git clone https://github.com/darionturner/Lean.git
cd Lean

# 3. Open in VS Code
code .

# 4. Click "Reopen in Container" when prompted
# (VS Code reads .devcontainer/devcontainer.json automatically)

# 5. Wait for container build (~5-10 min first time)

# 6. Verify setup
dotnet --version  # Inside container
python --version  # Inside container
```

---

### Phase 3: Configure IDE Settings (Week 1-2)

#### VS Code Configuration (Both Native & DevContainer)

**Create/Update `.vscode/launch.json`:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug LEAN (C#)",
      "type": "coreclr",
      "request": "launch",
      "preLaunchTask": "build",
      "program": "${workspaceFolder}/Launcher/bin/Debug/net6.0/QuantConnect.Lean.Launcher.dll",
      "args": [],
      "cwd": "${workspaceFolder}/Launcher/bin/Debug",
      "stopAtEntry": false
    },
    {
      "name": "Attach to Python Algorithm",
      "type": "python",
      "request": "attach",
      "port": 5678,
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "${workspaceFolder}"
        }
      ]
    }
  ]
}
```

**Create/Update `.vscode/tasks.json`:**
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

#### PyCharm Configuration (Native Only)

**For Python Algorithm Debugging:**
1. Run → Edit Configurations → Add Python Remote Debug
2. Host: `localhost`, Port: `5678`
3. Path mappings: Map workspace to workspace
4. Start debug server before running LEAN

**For C# Engine Work:**
- Use VS Code or Visual Studio for C# debugging
- PyCharm primarily for Python algorithm editing

---

### Phase 4: Validate All Workflows (Week 2)

#### Test 1: Python Algorithm Development
```bash
# Create new algorithm
touch Algorithm.Python/TestEpexStrategy.py

# Edit in IDE (VS Code or PyCharm)
# Update config.json to point to TestEpexStrategy.py

# Run (no build needed for Python-only changes)
cd Launcher/bin/Debug
dotnet QuantConnect.Lean.Launcher.dll

# Iterate: Edit Python → Re-run → ~10 seconds
```

**Expected:** Fast iteration on Python strategies

#### Test 2: C# Engine Modification
```bash
# Create placeholder brokerage
mkdir -p Brokerages/Epex
touch Brokerages/Epex/EpexBrokerage.cs

# Edit C# code in VS Code
# Add basic class skeleton

# Build
dotnet build QuantConnect.Lean.sln

# Run
cd Launcher/bin/Debug
dotnet QuantConnect.Lean.Launcher.dll

# Iterate: Edit C# → Build → Run → ~60 seconds
```

**Expected:** Can modify and build engine components

#### Test 3: Mixed C#/Python Development
```python
# C#: Create custom data type in Common/Data/Custom/PowerPrice.cs
# Build C# project

# Python: Use new data type in algorithm
from QuantConnect.Data.Custom import PowerPrice
self.AddData(PowerPrice, "EPEX_DE")

# Run algorithm (Python uses compiled C# DLL)
```

**Expected:** Python algorithms can use C# classes seamlessly

---

### Phase 5: Git Workflow Setup (Week 2)

#### Repository Structure
```
Lean/ (forked from QuantConnect/Lean)
├── .github/workflows/          # CI/CD pipelines
├── .vscode/                    # Team VS Code settings
├── Brokerages/
│   └── Epex/                   # Custom EPEX integration (NEW)
├── Common/Data/Custom/
│   └── Power/                  # PowerPrice, GasPrice (NEW)
├── Algorithm.Python/
│   └── EnergyStrategies/       # Team algorithms (NEW)
├── Data/custom/
│   └── power/                  # Energy market data (NEW)
├── docs/
│   ├── SETUP_NATIVE.md         # Setup guide (NEW)
│   └── ENERGY_MARKET_DESIGN.md # Architecture doc (NEW)
└── JOURNAL.md                  # Project journal (EXISTING)
```

#### Branching Strategy
```bash
# Main branch: master (tracks upstream)
# Development branch: develop
# Feature branches: feature/epex-brokerage, feature/power-data-type

# Example workflow:
git checkout -b feature/epex-brokerage
# ... make changes ...
git commit -m "feat: Add EPEX WebSocket connection"
git push origin feature/epex-brokerage
# Create PR to develop branch
```

#### Syncing with Upstream
```bash
# Add upstream remote
git remote add upstream https://github.com/QuantConnect/Lean.git

# Periodically sync
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

---

### Phase 6: Development Workflow Documentation (Week 2)

**Create `docs/DEVELOPMENT_WORKFLOW.md`:**

```markdown
# Energy Markets LEAN Development Workflow

## Daily Workflow

### Engine Developers (C#)
1. Pull latest changes: `git pull origin develop`
2. Create feature branch: `git checkout -b feature/my-feature`
3. Edit C# code in VS Code
4. Build: `dotnet build` (or Ctrl+Shift+B)
5. Run tests: `dotnet test`
6. Run LEAN with test algorithm
7. Commit changes
8. Create PR to develop

### Algorithm Developers (Python)
1. Pull latest changes
2. Create feature branch
3. Edit Python algorithm in VS Code/PyCharm
4. Run LEAN (no build needed)
5. Iterate rapidly
6. Commit changes
7. Create PR to develop

## Debugging Workflows

### Debug Python Algorithm
1. Set `"debugging": true` in config.json
2. Set breakpoints in VS Code
3. Run LEAN
4. Attach debugger (F5 → "Attach to Python")

### Debug C# Engine
1. Open LEAN in VS Code
2. Set breakpoints in C# code
3. F5 → "Debug LEAN (C#)"
4. Step through engine code

## Common Tasks

### Add New Python Package
- Native: `conda install package-name`
- DevContainer: Edit `.devcontainer/Dockerfile`, rebuild

### Add New Brokerage
1. Create `Brokerages/[Name]/` directory
2. Implement `IBrokerage` interface
3. Create factory class
4. Register in config.json
5. Write unit tests

### Add Custom Data Type
1. Create class in `Common/Data/Custom/`
2. Inherit from `BaseData`
3. Implement `Reader()` and `GetSource()`
4. Build Common project
5. Use in Python algorithm
```

---

## Migration Timeline

### Month 1: Foundation (Native)
**Who:** All developers
**Setup:** Native installation
**Focus:**
- EPEX brokerage skeleton
- PowerPrice data type
- Market hours extension
- Initial algorithm prototypes

**Deliverables:**
- Working EPEX connection (even if simulated)
- Can load custom power price data
- Sample algorithm runs end-to-end

---

### Month 2: Integration (Native → DevContainer Transition)
**Who:**
- Engine team: Stays on Native (if preferred)
- Algorithm team: Transitions to DevContainer

**Focus:**
- Complete EPEX API integration
- Real data integration
- Strategy development begins

**Deliverables:**
- EPEX brokerage functional
- Historical data loaded
- 2-3 test strategies running

---

### Month 3+: Standardization (DevContainer Default)
**Who:** All new developers start with DevContainer
**Focus:**
- Algorithm development scales up
- Jupyter for research
- Prepare for containerized deployment

**Deliverables:**
- 5+ strategies in development
- Research notebooks documenting findings
- CI/CD pipeline for backtesting

---

## IDE Recommendations by Role

### Engine Developers (C# Focus)
**Recommended:** VS Code or Visual Studio
- VS Code: Lightweight, devcontainer support
- Visual Studio: Best C# debugging (Windows only)

**Workflow:** Native installation or DevContainer

### Algorithm Developers (Python Focus)
**Recommended:** VS Code with DevContainer
- Consistent environment
- Integrated debugging
- Git integration

**Alternative:** PyCharm with native installation
- Better Python IDE features
- Manual environment setup

### Hybrid Developers (C# + Python)
**Recommended:** VS Code with Native installation initially
- Maximum flexibility
- Both debuggers work well
- Can transition to DevContainer later

### Research/Quants
**Recommended:** Jupyter via `lean research` or Docker
- Interactive development
- Visualization tools
- No IDE setup needed

---

## Recommendations Summary

### ✅ DO THIS:
1. **Week 1:** Set up native installation for all developers
2. **Week 1:** Validate LEAN builds and POC runs
3. **Week 2:** Configure VS Code launch/tasks for team
4. **Week 2:** Document exact setup steps taken
5. **Month 2:** Evaluate DevContainer transition
6. **Ongoing:** Use Jupyter for research and prototyping

### ⚠️ CONSIDER:
- Python 3.12 compatibility testing (may work despite docs saying 3.11)
- Docker Desktop licensing for teams >250 employees
- CI/CD early for automated testing

### ❌ AVOID:
- LEAN CLI as primary approach (can't modify engine)
- Mandating single IDE (VS Code + PyCharm both viable)
- Containerization too early (adds complexity before benefits)

---

## Next Immediate Steps

**After this plan is approved:**

1. **Verify .NET SDK** (5 min)
   - Check if .NET 6+ exists in Conda environment
   - If not, install .NET 9

2. **Create Python 3.11 Environment** (10 min)
   - `conda create -n qc_lean python=3.11.11 pandas=2.2.3 wrapt=1.16.0`

3. **Set PYTHONNET_PYDLL** (2 min)
   - Export environment variable
   - Add to shell profile

4. **Build LEAN** (5-10 min)
   - `dotnet build QuantConnect.Lean.sln`
   - Fix any build errors

5. **Run POC Algorithm** (2 min)
   - Validate end-to-end works
   - Confirms Python integration

6. **Document Setup** (30 min)
   - Create SETUP_NATIVE.md
   - Include all commands and workarounds

**Total Time:** ~1 hour to validated working environment

---

## Questions to Resolve Before Proceeding

1. **Python Version:** Should we strictly use 3.11.11 or test 3.12.3 compatibility first?
2. **Team Size:** How many developers initially? (Affects DevContainer priority)
3. **IDE Preference:** Any strong preference for VS Code vs. PyCharm?
4. **Timeline:** When do you need first EPEX algorithm running? (Affects prioritization)

**Recommendation:** Proceed with native setup this week, gather team feedback, then decide on DevContainer timeline.
