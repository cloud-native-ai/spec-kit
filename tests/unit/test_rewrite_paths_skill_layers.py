"""Unit tests for rewrite_paths two-branch skills layer mapping.

Source form (framework repo):   skills/external/<name>/...  and  skills/internal/<name>/...
Runtime form (installed):       .specify/skills/<name>/...  and  .specify/skills/internal/<name>/...

Skill-name grammar: [a-z0-9-]+. The lookbehind (?<![\\w./-]) guarantees a ref
only rewrites when it STARTS a path reference, making the transform idempotent.
"""

import pytest

from specify_cli import rewrite_paths


class TestSkillsBranches:
    def test_external_flattens_to_runtime_form(self):
        assert (
            rewrite_paths("skills/external/draw-mermaid/SKILL.md")
            == ".specify/skills/draw-mermaid/SKILL.md"
        )

    def test_internal_stays_nested(self):
        assert (
            rewrite_paths("skills/internal/create-team/scripts/x.py")
            == ".specify/skills/internal/create-team/scripts/x.py"
        )

    def test_hyphen_and_digit_names(self):
        assert (
            rewrite_paths("skills/external/git-workspace2/ref.md")
            == ".specify/skills/git-workspace2/ref.md"
        )

    def test_uppercase_name_not_matched(self):
        # Grammar is [a-z0-9-]+; names outside it are left untouched.
        src = "skills/external/NotALegalName/SKILL.md"
        assert rewrite_paths(src) == src


class TestIdempotence:
    @pytest.mark.parametrize(
        "src",
        [
            "skills/external/demo/SKILL.md",
            "skills/internal/demo/SKILL.md",
            "memory/constitution.md",
            ".specify/skills/external/demo/SKILL.md",
        ],
    )
    def test_apply_twice_equals_apply_once(self, src):
        once = rewrite_paths(src)
        assert rewrite_paths(once) == once


class TestLookbehindSafety:
    def test_word_prefixed_ref_untouched(self):
        src = "xskills/external/a/SKILL.md"
        assert rewrite_paths(src) == src

    def test_slash_prefixed_ref_untouched(self):
        # Nested position: preceded by '/' -> lookbehind blocks the rewrite.
        src = "backup/skills/internal/a/SKILL.md"
        assert rewrite_paths(src) == src

    def test_already_specify_prefixed_untouched(self):
        src = ".specify/skills/internal/a/SKILL.md"
        assert rewrite_paths(src) == src

    def test_dot_prefixed_untouched(self):
        src = "./skills/external/a/SKILL.md"
        assert rewrite_paths(src) == src


class TestDelimiterContexts:
    def test_backticks_parens_space_and_line_start(self):
        src = (
            "run `skills/internal/create-team/scripts/x.py`\n"
            "(skills/external/draw-mermaid/server)\n"
            "see skills/external/x/SKILL.md\n"
            "skills/internal/y/SKILL.md at line start"
        )
        out = rewrite_paths(src)
        assert "`skills/" not in out
        assert "(skills/" not in out
        assert out.count(".specify/skills/internal/") == 2
        assert out.count(".specify/skills/") == 4  # incl. the two nested internal hits

    def test_prose_and_code_fence(self):
        src = (
            "The engine lives at skills/internal/team-run/scripts/run.py.\n"
            "```bash\n"
            "python3 skills/external/draw-mermaid/scripts/render.py\n"
            "```\n"
        )
        out = rewrite_paths(src)
        assert (
            ".specify/skills/internal/team-run/scripts/run.py" in out
        )  # nested scripts/ segment must NOT be double-prefixed
        assert ".specify/scripts" not in out
        assert ".specify/.specify/" not in out
        assert "python3 .specify/skills/draw-mermaid/scripts/render.py" in out


class TestExistingSegmentsUnaffected:
    def test_four_segments_still_rewrite(self):
        assert rewrite_paths("memory/x") == ".specify/memory/x"
        assert rewrite_paths("scripts/x") == ".specify/scripts/x"
        assert rewrite_paths("templates/x") == ".specify/templates/x"
        assert rewrite_paths("shared/x") == ".specify/shared/x"

    def test_nested_segments_inside_skills_ref_not_double_rewritten(self):
        out = rewrite_paths("skills/internal/create-team/scripts/x.py")
        assert out == ".specify/skills/internal/create-team/scripts/x.py"

    def test_flat_runtime_skills_ref_untouched(self):
        # Runtime-form refs already inside shipped content must survive.
        src = ".specify/skills/create-team/SKILL.md"
        assert rewrite_paths(src) == src
