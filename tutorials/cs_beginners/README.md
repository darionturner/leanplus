# C# for Beginners - LEAN Energy Trading Project

**Target Audience:** Python developers learning C# for LEAN engine development
**Project Context:** European intraday energy trading system
**Learning Approach:** Hands-on tutorials with LEAN-specific examples
**Estimated Time:** 8-10 hours total (self-paced)

---

## Tutorial Series Overview

This guide takes you from C# beginner to proficient LEAN developer, with focus on:
- Understanding C# fundamentals through LEAN examples
- Setting up efficient debugging workflows
- Environment and dependency management
- Professional development workflows

---

## Learning Path

### Foundation (2-3 hours)

- [ ] **Tutorial 01: Core C# Knowledge for LEAN** (~90 minutes)
  - C# vs Python comparison
  - Type system and memory management
  - Key concepts for LEAN development
  - Reading LEAN source code effectively

- [ ] **Tutorial 02: C# Setup on Windows** (~45 minutes)
  - .NET SDK installation and verification
  - Visual Studio vs VS Code vs Rider
  - Building LEAN from command line
  - Understanding project structure

### Development Environment (3-4 hours)

- [ ] **Tutorial 03: C# Debugging in JetBrains IDEs** (~90 minutes)
  - Rider vs PyCharm Professional
  - Setting up C# debugging in Rider
  - Debugging LEAN algorithms
  - Advanced debugging techniques

- [ ] **Tutorial 04: C# Debugging in VS Code** (~60 minutes)
  - C# Dev Kit configuration
  - Launch configurations for LEAN
  - Debugging C# and Python simultaneously
  - Performance profiling basics

- [ ] **Tutorial 05: Environment Management on Windows** (~45 minutes)
  - .NET SDK versioning
  - NuGet package management
  - Solution and project file management
  - Dependency resolution

### Professional Workflows (2 hours)

- [ ] **Tutorial 06: Project Planning and CI/CD for C#** (~2 hours)
  - Architecture planning for C# components
  - Automated testing with xUnit
  - GitHub Actions for LEAN
  - Deployment strategies
  - Performance benchmarking

---

## Learning Objectives

By completing this series, you will be able to:

- Read and understand LEAN's C# codebase confidently
- Debug C# code in multiple IDEs (Rider, VS Code, Visual Studio)
- Write new C# components for LEAN (security types, data handlers)
- Manage .NET environments and dependencies
- Set up CI/CD pipelines for LEAN extensions

---

## Prerequisites

**Required:**
- Windows 10/11 machine
- Basic programming experience (Python proficiency assumed)
- LEAN repository cloned
- Git installed

**Helpful (but not required):**
- PyCharm Professional or Rider
- Understanding of algorithmic trading concepts

---

## Time Commitment

| Tutorial | Reading | Hands-On | Total |
|----------|---------|----------|-------|
| 01 - Core C# Knowledge | 30 min | 60 min | 90 min |
| 02 - Windows Setup | 15 min | 30 min | 45 min |
| 03 - JetBrains Debugging | 20 min | 70 min | 90 min |
| 04 - VS Code Debugging | 15 min | 45 min | 60 min |
| 05 - Environment Management | 20 min | 25 min | 45 min |
| 06 - CI/CD & Planning | 40 min | 80 min | 120 min |
| **TOTAL** | **2.3 hrs** | **5.2 hrs** | **7.5 hrs** |

---

## Quick Reference Links

**LEAN Documentation:**
- [LEAN GitHub Repository](https://github.com/QuantConnect/Lean)
- [QuantConnect Documentation](https://www.quantconnect.com/docs/v2)

**C# Learning Resources:**
- [Microsoft C# Documentation](https://learn.microsoft.com/en-us/dotnet/csharp/)
- [C# Programming Guide](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/)

---

## Getting Started

1. **Quick Environment Check**
   ```bash
   # Verify .NET SDK installed
   dotnet --version
   # Should show: 10.0.x or higher

   # Verify LEAN builds
   cd /path/to/LEANplus
   dotnet build QuantConnect.Lean.sln
   # Should complete without errors
   ```

2. **Open Tutorial 01**
   - Read: `01_CORE_CSHARP_KNOWLEDGE.md`
   - Time: Set aside 90 minutes
   - Goal: Understand C# fundamentals through LEAN lens

3. **Track Your Progress**
   - Mark checkboxes in this README as you complete tutorials
   - Experiment beyond the exercises - explore LEAN code!

---

*Last Updated: 2026-02-01*
