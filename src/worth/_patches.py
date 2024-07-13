from __future__ import annotations

import dataclasses
from collections.abc import Callable
from contextlib import suppress
from functools import cached_property
from typing import Any, ClassVar, Generic, Protocol, TypeGuard, TypeVar, cast

T = TypeVar("T")


@dataclasses.dataclass(kw_only=True, slots=True)
class Implementation(Generic[T]):
    is_type: Callable[[Any], TypeGuard[T]]
    get_fields: Callable[[T], set[str]]
    replace: Callable[[T, dict[str, Any]], T]


implementations: list[Implementation] = []


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[Any]]]


implementations.append(
    Implementation[DataclassInstance](
        is_type=lambda x: dataclasses.is_dataclass(x) and not isinstance(x, type),  # type: ignore
        get_fields=lambda x: {field.name for field in dataclasses.fields(x)},
        replace=lambda x, changes: dataclasses.replace(x, **changes),
    )
)


implementations.append(
    Implementation[dict](
        is_type=lambda x: isinstance(x, dict), # type: ignore
        get_fields=lambda x: set(x),
        replace=lambda x, changes: x | changes,
    )
)

with suppress(ImportError):
    import attrs

    implementations.append(
        Implementation[attrs.AttrsInstance](
            is_type=lambda x: attrs.has(x) and not isinstance(x, type),  # type: ignore
            get_fields=lambda x: {field.name for field in attrs.fields(type(x))},
            replace=lambda x, changes: attrs.evolve(x, **changes),  # type: ignore
        )
    )


with suppress(ImportError):
    import msgspec

    implementations.append(
        Implementation[msgspec.Struct](
            is_type=lambda x: isinstance(x, msgspec.Struct),  # type: ignore
            get_fields=lambda x: {field.name for field in msgspec.structs.fields(x)},
            replace=lambda x, changes: msgspec.structs.replace(x, **changes),
        )
    )


class Patch:
    pass


class Omit(Patch):
    attrs: frozenset[str]
    __match_args__ = ("attrs",)

    def __init__(self, *attrs: str) -> None:
        self.attrs = frozenset(attrs)

    def __ror__(self, other):
        if isinstance(other, Patch):
            return compose_patch(self, other)

        return Patched(other, self)


class Only(Patch):
    attrs: frozenset[str]
    __match_args__ = ("attrs",)

    def __init__(self, *attrs: str) -> None:
        self.attrs = frozenset(attrs)

    def __ror__(self, other):
        if isinstance(other, Patch):
            return compose_patch(self, other)

        return Patched(other, self)


class Patched(Generic[T]):
    obj: T
    patch: Patch

    def __init__(self, obj: T, patch: Patch) -> None:
        if isinstance(obj, type):
            raise ValueError
        if isinstance(obj, Patched):
            patch, obj = (
                compose_patch(cast(Patched, obj).patch, patch),
                cast(Patched, obj).obj,
            )
        self.obj = obj
        self.patch = patch

    @cached_property
    def wrapped(self) -> Any:
        from . import Always

        obj = self.obj
        for implem in implementations:
            if implem.is_type(obj):
                match self.patch:
                    case Omit(attrs):
                        changes = dict.fromkeys(attrs, Always())
                        return implem.replace(obj, changes)
                    case Only(attrs):
                        all_fields = implem.get_fields(obj)
                        changes = dict.fromkeys(all_fields - attrs, Always())

                        return implem.replace(obj, changes)
                    case _:
                        raise NotImplementedError
        else:
            raise NotImplementedError(f"Not implemented for {type(self.obj)}")

    def __eq__(self, other: Any) -> bool:
        return other == self.wrapped


def compose_patch(lhs: Patch, rhs: Patch) -> Patch:
    match [lhs, rhs]:
        case Omit(attrs=omit_attrs), Only(attrs=only_attrs):
            attrs = only_attrs - omit_attrs
            return Only(*list(attrs))
        case Only(attrs=only_attrs), Omit(attrs=omit_attrs):
            attrs = only_attrs - omit_attrs
            return Only(*list(attrs))
        case Only(attrs=attrs_x), Only(attrs=attrs_y):
            attrs = attrs_x & attrs_y
            return Only(*list(attrs))
        case Omit(attrs=attrs_x), Omit(attrs=attrs_y):
            attrs = attrs_x | attrs_y
            return Omit(*list(attrs))
    raise ValueError
