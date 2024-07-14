from __future__ import annotations

from typing import Any, Collection, Mapping

from typing_extensions import Self

from ._patches import Omit, Only, Patched

__all__ = ["Omit", "Only", "Patched"]


class _Predicate:
    def __call__(self) -> Self:
        return self


class Always(_Predicate):
    """A predicate that always evaluates to true.

    For example:

    >>> assert True == Always() is True
    >>> assert False == Always() is True
    >>> assert {} == Always() is True
    >>> assert None == Always() is True
    >>> assert 42 == Always() is True
    """

    def __call__(self) -> Self:
        return self

    def __eq__(self, other: Any) -> bool:
        return True

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "Always()"


Always = Always()  # type: ignore


class Never(_Predicate):
    """A predicate that always evaluates to false.

    For example:

    >>> assert True == Never() is False
    >>> assert False == Never() is False
    >>> assert {} == Never() is False
    >>> assert None == Never() is False
    >>> assert 42 == Never() is False
    """

    def __eq__(self, other: Any) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Never()"


Never = Never()  # type: ignore


class OneOf(_Predicate):
    """A predicate that match one of its values.

    For example:

    >>> assert 1 == OneOf(1, 2, 3)
    >>> assert 2 == OneOf(1, 2, 3)
    >>> assert 3 == OneOf(1, 2, 3)
    >>> assert 4 != OneOf(1, 2, 3)
    """

    values: Collection[Any]

    def __init__(self, *values: Any) -> None:
        self.values = values

    def __eq__(self, other: Any) -> bool:
        return any(value == other for value in self.values)

    def __bool__(self) -> bool:
        raise TypeError("OneOf cannot be inferred to boolean")

    def __repr__(self) -> str:
        return "OneOf()"


class contains:
    """Operand used to check what contains a mapping.

    Example:

    >>> assert {"foo": 42, "bar": True} == contains({"foo": 42})
    >>> assert {"foo": 42, "bar": True} != contains({"qux": "other"})
    """

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
