#!/usr/bin/env python3
"""Harness triple check (fixture copy of ``scripts/python/harness-triple-check.py``).

It answers the one calling surface ``non-disposable-check.py`` uses (``--action verify``) and
prints the three finding lines corpus A2 reads: the record claims ``unclassified 0`` while the
verification reports three unclassified candidates.
"""
import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description="fixture verifier")
    parser.add_argument("--action", default="verify")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    print("# harness-triple-check — %s" % args.action)
    print("declarations: 2")
    print("candidates: 3")
    print("findings: 3")
    print("finding: unclassified-candidate: docs/editable-configuration.md")
    print("finding: unclassified-candidate: docs/authority-model.md")
    print("finding: unclassified-candidate: docs/natural-language-acceptance.md")
    return 1


if __name__ == "__main__":
    sys.exit(main())
