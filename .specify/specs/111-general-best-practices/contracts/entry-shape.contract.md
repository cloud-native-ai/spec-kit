# Contract — Entry Shape, Owner Files and the Seed

**Path**: the four owner files under `shared/best-practices/` and their mirrors. Guard pinning: `tests/contract/test_general_best_practices.py` legs (b), (c), (f).
**Rule owners cited, never restated**: the closed category set and document set — `contracts/manifest.contract.md`; observation, promotion and traceability — `contracts/accumulation.contract.md`.

**C-201** Entry shape.

An entry starts with a level-2 heading (`## `) and carries two mandatory bullet items: a `**实践**` bullet stating the operable practice (default plus exception), and a `**反例 / 证据**` bullet stating the real defect or observation that justifies it. An optional `**延伸**` bullet carries the boundary case. A promoted entry additionally carries a `**来源**` bullet (C-303). An entry missing either mandatory bullet is red. (FR-001, FR-002, FR-007(b))

**C-202** Owner-file identity and accumulation block.

Each owner file MUST carry exactly one H1 heading naming its category, and a blockquote block that points back to the manifest: a link to `README.md`, the literal 积累机制, and the entry-shape triple 标题 + 实践 + 反例/证据. The block is a pointer and MUST NOT restate the accumulation rules' content. (FR-002, FR-007(b))

**C-203** Placeholder ⇔ zero entries.

An owner file with no entries MUST carry exactly one italic placeholder line containing [[STR-006]] plus one scope sentence, and zero `## ` entry headings. An owner file with at least one entry MUST NOT carry the placeholder. The first promotion removes the placeholder in the same change. The guard MUST NOT freeze the number of placeholders at the delivery count; it judges the equivalence, not a count. (FR-002, FR-007(b), SC-001)

**C-204** Seed entry.

[[STR-005]] MUST carry the entry [[STR-007]] whose body states all three: (1) git clone URLs default to HTTPS; (2) a special repository that requires HTTP (or SSH) MUST be flagged with its protocol and credential requirement when install scripts or docs initiate the clone; (3) the counter-example — `~/.git-credentials` recorded HTTP credentials while the install flow cloned over HTTPS, and the protocol mismatch broke the clone. The entry MUST also carry the extension: when an intranet git service requires authentication over HTTPS while SSH with a key works, the install source URL SHOULD prefer SSH or state the authentication requirement explicitly. The seed is exempt from the `**来源**` bullet; the module text MUST NOT fabricate a feedback ID or source line. (FR-003, FR-007(c), SC-002)

**C-205** Semantic-truth boundary.

The guard judges structure, pointers and literal presence only. Whether an entry's claim is true, and whether an entry is hollow, are accumulation discipline and review judgements; the guard MUST NOT claim to decide them. (FR-007(b), SC-003)