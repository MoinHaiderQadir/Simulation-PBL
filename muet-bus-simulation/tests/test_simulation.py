"""pytest wrapper: runs the verification checks in verify.py as one test."""
import runpy
from pathlib import Path


def test_verification_checks_pass():
    # verify.py asserts internally; any failure raises AssertionError
    runpy.run_path(str(Path(__file__).with_name("verify.py")), run_name="__main__")
