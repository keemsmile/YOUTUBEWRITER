# Swarm Integration Reference Commands

## Current Branch Information
```bash
# Failed attempt branch name:
feature/swarm-integration
```

## How to Access Documentation
```powershell
# Copy docs back to your working directory
Copy-Item -Path "c:/Users/keems/Desktop/JohnRoman/swarm_integration_docs/*" -Destination "./docs" -Recurse

# Or view them directly
code "c:/Users/keems/Desktop/JohnRoman/swarm_integration_docs"
```

## Complete Workflow

### 1. Save Current Branch (Already Done)
```bash
# Current failed attempt is saved in branch:
git checkout feature/swarm-integration
```

### 2. Switch to Main and Create New Branch
```bash
# Switch to main
git checkout main

# Create new integration branch
git checkout -b feature/swarm-integration-v2
```

### 3. Create Docs Directory and Copy Reference Docs
```powershell
# Create docs directory
New-Item -ItemType Directory -Force -Path "./docs"

# Copy all documentation
Copy-Item -Path "c:/Users/keems/Desktop/JohnRoman/swarm_integration_docs/*" -Destination "./docs" -Recurse
```

### 4. View Documentation
```bash
# Open in VS Code
code ./docs

# Or view individual files
code ./docs/01_LESSONS_LEARNED.md
code ./docs/02_INTEGRATION_PLAN.md
```

### 5. If You Need to Reference Failed Attempt
```bash
# View failed attempt code
git checkout feature/swarm-integration

# Return to new attempt
git checkout feature/swarm-integration-v2
```

## Emergency Recovery
If you ever lose track of the docs:
```powershell
# Restore from backup location
Copy-Item -Path "c:/Users/keems/Desktop/JohnRoman/swarm_integration_docs/*" -Destination "./docs" -Recurse
```

## Important Paths
- Documentation Backup: `c:/Users/keems/Desktop/JohnRoman/swarm_integration_docs/`
- Failed Attempt Branch: `feature/swarm-integration`
- Main Branch: `main`
- New Attempt Branch: `feature/swarm-integration-v2`

## Remember
1. The documentation is safely stored at `c:/Users/keems/Desktop/JohnRoman/swarm_integration_docs/`
2. You can always copy it back using the PowerShell commands above
3. The failed attempt code is preserved in branch `feature/swarm-integration`
4. Start fresh from `main` with a new branch name
