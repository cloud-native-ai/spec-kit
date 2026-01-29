# Feature Detail: Add Instructions and Skills Commands

**Feature ID**: 1000-add-instr-skills-cmds
**Name**: Add Instructions and Skills Commands
**Description**: Add /speckit.instructions and /speckit.skills commands to help users manage AI instructions and skills.
**Status**: Planned
**Created**: 2026-01-28
**Last Updated**: 2026-01-28

## Overview

This feature introduces two new commands to the spec-kit CLI/Agent interface. `/speckit.instructions` generates the `.ai/instructions.md` file and symlinks for various AI tools (Cline, Lingma, etc.). `/speckit.skills` generates scaffold for new Agent Skills in `.github/skills/`.

## Latest Review

Initial creation upon Spec #1000.

## Key Changes

1. Defined specification for implementation of `/speckit.instructions`.
2. Defined specification for implementation of `/speckit.skills`.

## Implementation Notes

- Commands should be implemented as markdown prompt templates in `templates/commands/`.
- Instructions generation relies on logic similar to `copilot_generate_instructions` script.
- Skills generation relies on `skills.md` capabilities standard.

## Future Evolution Suggestions

- Add interactive wizard for tailoring instructions.
- Add skill registry browsing.
