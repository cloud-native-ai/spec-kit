<!-- Fixture case: acceptance-hardening/inherited-clean — dependency side.
     This is the detail of fixture Feature 901, the only dependency of fixture Feature 900. Declarative input:
     it describes no work performed in this repository.
     It carries the first of the three closed extraction sources: a `## Deferred` section with two bullets, each
     labelled, so the locator is `deferred:<label-lowercased-with-dashes>`.
     The same dependency side as `inherited-mutation`: the pair differs only in the plan's dispositions. -->

# Feature Detail: Acceptance Fixture — dependency 901

**Feature ID**: 901
**Name**: Acceptance fixture — dependency
**Description**: Declarative dependency side carrying the three closed inherited-blocker extraction sources.
**Status**: Blocked
**Created**: 2026-11-03
**Last Updated**: 2026-11-03

## Deferred

- **Warm-pool sizing** — per-tenant warm-pool sizing was deferred; the dependency ships one fixed pool size.
- **Retry budget** — a tunable per-tenant retry budget was deferred; the dependency ships a fixed budget.
