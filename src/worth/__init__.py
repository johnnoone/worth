from __future__ import annotations

from typing import Any, Mapping

from ._patches import Omit, Only, Patched

__all__ = ["Omit", "Only", "Patched"]


class Always:
    def __eq__(self, other: Any) -> bool:
        return True

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "Always()"


class Never:
    def __eq__(self, other: Any) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Never()"


class contains:
    def __init__(self, data: Mapping[Any, Any]) -> None:
        self.data: Mapping[Any, Any] = data

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Mapping):
            raise TypeError("Omit object is not comparable")
        return self.data.items() <= other.items()

    def __lt__(self, other: Any) -> bool:
        raise TypeError("Operator < is not supported by contains")

    def __le__(self, other: Any) -> bool:
        raise TypeError("Operator <= is not supported by contains")

    def __gt__(self, other: Any) -> bool:
        raise TypeError("Operator > is not supported by contains")

    def __ge__(self, other: Any) -> bool:
        raise TypeError("Operator >= is not supported by contains")
