---
id: "feedback-intake-repo-root-feedback-holds-feedback-zip-proces"
scope: "knowledge"
source: "/speckit.instructions"
tags: ["convention", "feedback", "intake", "instructions"]
title: "Feedback intake: repo-root feedback/ holds feedback-*.zip, processed as one batch"
created: "2026-08-13T11:42:25Z"
summary: "User decision (2026-08-13): the repo-root `feedback/` directory is the single central intake for feedback collected from users in this spec-kit repo. Each received bundle is stored as `feedback/feedba"
---

User decision (2026-08-13): the repo-root `feedback/` directory is the single central intake for feedback collected from users in this spec-kit repo. Each received bundle is stored as `feedback/feedback-*.zip` (the package format produced downstream by feedback-utils.py --action package: entry Markdown + MANIFEST.md). Root .gitignore ignores *.zip while feedback/.gitignore re-includes feedback-*.zip so bundles stay trackable. Binding processing rule: all pending bundles are processed together as ONE consolidated batch, never one zip at a time — cross-bundle reconciliation is what surfaces factual conflicts between reporters and keeps a single mechanism fitting different user environments. Recorded in .specify/instructions.md (Key Directories + Documentation Map Feedback System row).
