from typing import Any

import pytest
from _pytest.assertion.util import assertrepr_compare

import something


def pytest_assertrepr_compare(
    config: pytest.Config, op: str, left: Any, right: Any
) -> list[str] | None:
    if isinstance(left, something.Always | something.Never):
        return [f"{right!r} never match"]
    if isinstance(right, something.Always | something.Never):
        return [f"{left!r} never match"]

    rewrite = False
    if isinstance(left, something.Patched):
        rewrite = True
        left = left.wrapped
    if isinstance(right, something.Patched):
        rewrite = True
        right = right.wrapped

    if rewrite:
        return assertrepr_compare(config, op, left, right)

    return None
