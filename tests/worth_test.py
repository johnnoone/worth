from dataclasses import dataclass

import attrs
import msgspec
import pytest
from _pytest.assertion.util import assertrepr_compare

from worth import Always, Never, Omit, OneOf, Only, contains
from worth.pytest_plugin import pytest_assertrepr_compare


def test_always_as_callable():
    assert (1 == Always()) is True
    assert ({} == Always()) is True
    assert ({"foo": 42} == Always()) is True

    assert Model("foo", "bar") == Model("foo", "bar")
    assert Model("foo", "bar") == Model(Always(), "bar")


def test_always_as_constant():
    assert (1 == Always) is True
    assert ({} == Always) is True
    assert ({"foo": 42} == Always) is True

    assert Model("foo", "bar") == Model("foo", "bar")
    assert Model("foo", "bar") == Model(Always, "bar")


def test_always_boolean():
    assert bool(Always()) is True
    assert bool(Always) is True


def test_never_as_callable():
    assert (1 == Never()) is False
    assert ({} == Never()) is False
    assert ({"foo": 42} == Never()) is False

    assert Model("foo", "bar") != Model(Never(), "bar")


def test_never_as_constant():
    assert (1 == Never) is False
    assert ({} == Never) is False
    assert ({"foo": 42} == Never) is False

    assert Model("foo", "bar") != Model(Never, "bar")


def test_never_boolean():
    assert bool(Never()) is False
    assert bool(Never) is False


def test_one_of():
    assert 1 == OneOf(1, 2, 3)
    assert 2 == OneOf(1, 2, 3)
    assert 3 == OneOf(1, 2, 3)
    assert 4 != OneOf(1, 2, 3)


def test_one_of_boolean():
    with pytest.raises(TypeError):
        bool(OneOf(1, 2, 3))


@dataclass
class Model:
    name: str
    email: str


@attrs.define
class AttrsModel:
    name: str
    email: str


class MessageSpecModel(msgspec.Struct):
    name: str
    email: str


models = [Model, AttrsModel, MessageSpecModel, dict]


@pytest.mark.parametrize("Model", models)
def test_omit(Model):
    assert Model(name="foo", email="bar") == Model(name="foo", email="OTHER") | Omit(
        "email"
    )


@pytest.mark.parametrize("Model", models)
def test_only(Model):
    assert Model(name="foo", email="bar") == Model(name="foo", email="OTHER") | Only(
        "name"
    )


def test_plugin(request):
    config = request.config
    assert pytest_assertrepr_compare(config, "==", 1, Always()) == ["1 never match"]
    assert pytest_assertrepr_compare(config, "==", 1, Never()) == ["1 never match"]
    assert pytest_assertrepr_compare(
        config, "==", 1, Model("x", "y") | Only("name")
    ) == assertrepr_compare(config, "==", 1, (Model("x", "y") | Only("name")).wrapped)
    assert pytest_assertrepr_compare(
        config, "==", 1, Model("x", "y") | Omit("name")
    ) == assertrepr_compare(config, "==", 1, (Model("x", "y") | Omit("name")).wrapped)
    assert pytest_assertrepr_compare(
        config, "==", Model("a", "b"), Model("x", "y") | Omit("name")
    ) == assertrepr_compare(
        config, "==", Model("a", "b"), (Model("x", "y") | Omit("name")).wrapped
    )


def test_contains():
    assert {"foo": 24, "bar": "baz", "qux": None} == contains({"foo": 24})
    assert {"foo": 24, "bar": "baz", "qux": None} != contains({"foo": 42})
    assert ({"foo": 24, "bar": "baz", "qux": None} == contains({"foo": 42})) is False


def test_contains_non_supported_operations():
    with pytest.raises(TypeError):
        {} < contains({})
    with pytest.raises(TypeError):
        {} <= contains({})
    with pytest.raises(TypeError):
        {} > contains({})
    with pytest.raises(TypeError):
        {} >= contains({})


def test_contains_composition():
    assert {"foo": {"bar": 42}, "baz": 100} == contains(
        {"foo": contains({"bar": Always})}
    )
