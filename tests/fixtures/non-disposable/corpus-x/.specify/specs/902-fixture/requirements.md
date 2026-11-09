# Requirements Specification: fixture 902

**Requirement Branch**: `902-fixture`
**Created**: 2026-11-09
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "a fixture specification for the detection engine's contract test."

## Related Feature *(mandatory)*

**Feature ID**: 902
**Feature Name**: fixture 902

## Overview

A fixture specification. It exists so the closure checker has a record to read, and so the
detection engine has a registry row to compare that reading against.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - a fixture story (Priority: P1)

The fixture's one story.

**Acceptance Scenarios**:

1. **Given** a tree, **When** read, **Then** the fixture answers.

## Requirements

- **FR-001**: The fixture MUST answer the reader.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|----|----------|
| RS-001 | Python 3 interpreter | signed-contract | CPython upstream (consumed only) | `requires-python = ">=3.8"` | `.specify/specs/902-fixture/contracts/implemented.contract.md` | the fixture runs on the declared interpreter | FR-001 | EP-001 |
