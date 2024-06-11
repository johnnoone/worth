from typing import Any, Mapping

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

    patched = False
    if isinstance(left, something.Patched):
        patched = True
        left = left.wrapped
    if isinstance(right, something.Patched):
        patched = True
        right = right.wrapped

    if patched:
        return assertrepr_compare(config, op, left, right)

    contained = False
    if isinstance(left, Mapping) and isinstance(right, something.contains):
        contained = True
        right = dict(left) | dict(right.data)
    if isinstance(left, something.contains) and isinstance(right, Mapping):
        contained = True
        left = dict(right) | dict(left.data)

    if contained:
        message = assertrepr_compare(config, op, left, right) or []
        if op == "==":
            message.insert(0, f"{left} contains {right}")
        elif op == "!=":
            message.insert(0, f"{left} does not contain {right}")
        return message

    return None
