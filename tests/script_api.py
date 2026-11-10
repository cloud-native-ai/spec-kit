from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import inspect
import io
import re
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from typer.testing import CliRunner

from specify_cli import app

ROOT = Path(__file__).resolve().parents[1]
RUNNER = CliRunner()


def _load_module(name: str, file_name: str):
    module_path = ROOT / "scripts" / "python" / file_name
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


tools_utils = _load_module("tools_utils", "tools-utils.py")
skills_utils = _load_module("skills_utils", "skills-utils.py")
memory_utils = _load_module("memory_utils", "memory-utils.py")
probe_utils = _load_module("probe_utils", "probe-utils.py")
feedback_utils = _load_module("feedback_utils", "feedback-utils.py")
history_utils = _load_module("history_utils", "history-utils.py")
sanitize_utils = _load_module("sanitize_utils", "sanitize-utils.py")
renumber_utils = _load_module("renumber_utils", "renumber-utils.py")


class InProcessResult:
    """The ``subprocess.CompletedProcess`` subset an in-process engine call reproduces.

    Converted assertions read ``returncode`` / ``stdout`` / ``stderr`` exactly as they
    read a completed subprocess, so the same behaviour assertions run before and after
    (contract inprocess-conversion C-003).
    """

    def __init__(self, args, returncode: int, stdout: str, stderr: str) -> None:
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def check_returncode(self) -> None:
        if self.returncode:
            raise subprocess.CalledProcessError(
                self.returncode, self.args, self.stdout, self.stderr
            )

    def __repr__(self) -> str:
        return "<InProcessResult args=%r returncode=%r>" % (self.args, self.returncode)


_ENGINE_MODULES: dict[Path, object] = {}


def load_engine_module(engine_path):
    """Import an engine script by path, once per path in this process."""
    resolved = Path(engine_path).resolve()
    cached = _ENGINE_MODULES.get(resolved)
    if cached is not None:
        return cached
    digest = hashlib.sha256(str(resolved).encode("utf-8")).hexdigest()[:12]
    stem = re.sub(r"[^0-9A-Za-z_]", "_", resolved.stem)
    name = "_engine_%s_%s" % (stem, digest)
    spec = importlib.util.spec_from_file_location(name, resolved)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load engine from %s" % resolved)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    _ENGINE_MODULES[resolved] = module
    return module


def run_engine_in_process(engine_path, args: Sequence[str] = ()) -> InProcessResult:
    """Call an engine's ``main`` in this process, capturing stdout/stderr and the exit code.

    ``main(argv)`` engines receive ``args`` directly; the few engines whose ``main()``
    reads ``sys.argv`` by hand get a temporary ``sys.argv`` that names the engine, so
    their own parser sees the same line a subprocess would. ``SystemExit`` (argparse's
    ``--help`` / usage errors) is folded back into the return code, exactly as the
    process exit status would carry it.
    """
    module = load_engine_module(engine_path)
    main = getattr(module, "main", None)
    if not callable(main):
        raise RuntimeError("engine has no callable main: %s" % engine_path)
    argv = [str(arg) for arg in args]
    takes_argv = len(inspect.signature(main).parameters) >= 1
    out, err = io.StringIO(), io.StringIO()
    saved_argv = sys.argv
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                if takes_argv:
                    code = main(argv)
                else:
                    sys.argv = [str(engine_path), *argv]
                    try:
                        code = main()
                    finally:
                        sys.argv = saved_argv
            except SystemExit as exc:
                if isinstance(exc.code, int):
                    code = exc.code
                elif exc.code is None:
                    code = 0
                else:
                    print(exc.code, file=sys.stderr)
                    code = 1
    finally:
        sys.argv = saved_argv
    if code is None:
        code = 0
    if not isinstance(code, int):
        code = 1
    return InProcessResult([str(engine_path), *argv], code, out.getvalue(), err.getvalue())


def run_specify_init(args: list[str]):
    return RUNNER.invoke(app, ["init", *args])


def run_specify_check():
    return RUNNER.invoke(app, ["check"])


def run_generate_instructions(cwd: Path):
    script = ROOT / "scripts" / "bash" / "generate-instructions.sh"
    return subprocess.run([str(script)], cwd=cwd, check=False, capture_output=True, text=True)
