# Quickstart: Feature Management Workflow

## Overview

This quickstart guide demonstrates the complete feature management workflow using the new `/speckit.feature` command and integrated SDD commands.

## Prerequisites

- Specify CLI installed (`specify init` completed)
- Git installed and configured
- AI assistant with slash command support (Copilot, Claude, etc.)

## Step 1: Create Feature Index

Start by creating your project's feature index:

```bash
/speckit.feature "Add user authentication system"
```

This creates `.specify/memory/features.md` with your first feature:

```markdown
# Project Feature Index

**Last Updated**: November 17, 2025
**Total Features**: 1

## Features

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
| 001 | user authentication system | Add user authentication system | Draft | (Not yet created) | 2025-11-17 |
```

The change is automatically staged in git. Commit with your own message:

```bash
git commit -m "Add user authentication feature to index"
```

## Step 2: Create Specification

Create a detailed specification for your feature:

```bash
/speckit.specify "Add email/password login with OAuth2 support for Google and GitHub"
```

This:
- Creates branch `001-user-authentication-system`
- Generates `.specify/specs/001-user-authentication-system/spec.md`
- Updates `.specify/memory/features.md` status to "Planned" and records spec path
- Automatically stages the `.specify/memory/features.md` change

Commit the specification:

```bash
git add .
git commit -m "Specify user authentication requirements"
```

## Step 3: Create Implementation Plan

Generate an implementation plan:

```bash
/speckit.plan
```

This:
- Creates `.specify/specs/001-user-authentication-system/plan.md`
- Updates `.specify/memory/features.md` status to "Implemented"
- Automatically stages the `.specify/memory/features.md` change

## Step 4: Generate Tasks

Create actionable tasks:

```bash
/speckit.tasks
```

This:
- Creates `.specify/specs/001-user-authentication-system/tasks.md`
- Maintains "Implemented" status in `.specify/memory/features.md`
- Automatically stages the `.specify/memory/features.md` change

## Step 5: Implement Feature

Execute the implementation:

```bash
/speckit.implement
```

This:
- Implements the feature based on tasks
- Maintains "Implemented" status in `.specify/memory/features.md`
- Automatically stages the `.specify/memory/features.md` change

## Step 6: Validate with Checklist

Validate the implementation:

```bash
/speckit.checklist
```

This:
- Creates quality checklist and runs validation
- Updates `.specify/memory/features.md` status to "Ready for Review"
- Automatically stages the `.specify/memory/features.md` change

## Concurrent Feature Management

You can manage multiple features simultaneously:

```bash
/speckit.feature "Implement payment processing with credit cards"
/speckit.feature "Create admin dashboard for user management"
```

Each feature gets a sequential ID (002, 003, etc.) and can progress independently through the SDD workflow.

## Handling Merge Conflicts

If multiple team members update the same feature entry simultaneously, git will create a merge conflict in `.specify/memory/features.md`. Resolve the conflict manually during the merge process - this is the expected behavior for concurrent updates.

## Performance Expectations

- Feature index creation/update: < 1 second for typical usage
- SDD command integration overhead: < 200ms per command
- Maximum supported features: 100 features with < 5 second total execution time

## Backward Compatibility

Existing projects without `.specify/memory/features.md` continue to work exactly as before. Feature tracking is only enabled when `.specify/memory/features.md` exists in the project.