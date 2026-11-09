import sys, subprocess
sys.path.insert(0, '/storage/project/cloud-native-ai/spec-kit')
from pathlib import Path
from tests.fixtures.git_closeout import derive_closeout
from tests.fixtures.git_closeout.block import parse_block

root = Path('/storage/project/cloud-native-ai/spec-kit')
for label, strategy in (("declared", None), ("ask", "ask")):
    block = parse_block((root / ".specify/workflow/git.md").read_text())
    model = block.model
    strategy_value = strategy or block.strategy
    plan = derive_closeout(
        model=model,
        strategy=strategy_value,
        remotes=block.remotes,
        readonly=block.readonly,
    )
    print("=" * 78)
    print("declared model   : %s" % model)
    print("strategy value   : %s%s" % (strategy_value, "" if strategy is None else "  (dry-run override)"))
    print("push targets     : %s   read-only: %s" % (plan.push_branches, block.readonly))
    print("terminal state   : %s" % plan.terminal_state)
    for i, step in enumerate(plan.steps, 1):
        print("  %2d. %-7s %s :: %s" % (i, step.kind, step.target, step.detail))
    print("  receipt steps  : %s" % (plan.skipped,))
