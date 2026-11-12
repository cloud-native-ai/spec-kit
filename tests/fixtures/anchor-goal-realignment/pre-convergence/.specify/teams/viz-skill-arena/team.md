---
name: Fixture team viz-skill-arena
slug: viz-skill-arena
description: fixture input for the pre-convergence tree (bound-dangling)
scope: spec
lifecycle_state: active
anchor_slug: visualization-skill-selection
goal: >
  Run the fixture arena loop — task in, semantic spec, parallel syntax engines, two judging
  rounds — and accumulate the champion-skill matching ledger while improving the semantic layer.
territory:
  write:
    - .specify/specs/viz-skill-arena/**
---
# viz-skill-arena

## Goal

Fixture arena: turn each drawing task into a champion skill and append the match to the ledger.

成功标准：
1. each round yields a champion skill and appends a match row to the ledger
2. adopted skill changes pass the second judging round with no regression

Fixture definition: the body cites the binding field name `goal_slug` in prose too.
