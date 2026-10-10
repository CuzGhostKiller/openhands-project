---
name: GitHub Project Manager
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - github project
  - pull project
  - push project
  - merge project
  - github workflow
---

# GitHub Project Manager Microagent

This microagent helps manage GitHub projects by performing pull, push, and merge operations.

## Capabilities

- Pull changes from GitHub repositories
- Push local changes to GitHub repositories  
- Merge branches in GitHub repositories
- Manage GitHub workflows and CI/CD processes

## Usage Examples

### Pulling a GitHub Project
```
pull github project from CuzGhostKiller/openhands-project
```

### Pushing Changes to GitHub
```
push my changes to CuzGhostKiller/openhands-project
```

### Merging Branches in GitHub
```
merge feature-branch into main for CuzGhostKiller/openhands-project
```

## Environment Variables and Authentication

This microagent requires:
- `GITHUB_TOKEN` environment variable with appropriate permissions
- Access to the target repository

## Error Handling

- If authentication fails, check your `GITHUB_TOKEN` 
- If branch doesn't exist, create it first before pushing
- If merge conflicts occur, resolve them manually before merging

## Limitations

- Cannot directly execute code in repositories
- Requires proper permissions for repository operations
- Only works with public or accessible private repositories