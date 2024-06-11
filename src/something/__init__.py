from __future__ import annotations

import dataclasses
from typing import Any, Generic, Mapping, TypeVar

T = TypeVar("T")


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


class Omit:
    def __init__(self, *attrs: str) -> None:
        self.attrs = frozenset(attrs)

    def __ror__(self, obj: T) -> Patched[T]:
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            changes = dict.fromkeys(self.attrs, Always())
            wrapped = dataclasses.replace(obj, **changes)
            return Patched(obj, wrapped)  # type: ignore
        else:
            raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        raise Exception("Omit object is not comparable")


class Only:
    def __init__(self, *attrs: str) -> None:
        self.attrs = frozenset(attrs)

    def __ror__(self, obj: T) -> Patched[T]:
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            all_fields = set()
            for field in dataclasses.fields(obj):
                all_fields.add(field.name)
            changes = dict.fromkeys(all_fields - self.attrs, Always())
            wrapped = dataclasses.replace(obj, **changes)
            return Patched(obj, wrapped)  # type: ignore
        else:
            raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        raise Exception("Only object is not comparable")


class Patched(Generic[T]):
    def __init__(self, obj: T, wrapped: T) -> None:
        self.obj = obj
        self.wrapped = wrapped

    def __eq__(self, other: Any) -> bool:
        return self.wrapped == other


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
