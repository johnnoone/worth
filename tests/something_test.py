from dataclasses import dataclass

from _pytest.assertion.util import assertrepr_compare
import pytest
from worth import Always, Never, Omit, Only, contains
from worth.pytest_plugin import pytest_assertrepr_compare


def test_always():
    assert (1 == Always()) is True
    assert ({} == Always()) is True
    assert ({"foo": 42} == Always()) is True

    assert Model("foo", "bar") == Model("foo", "bar")
    assert Model("foo", "bar") == Model(Always(), "bar")


def test_always_boolean():
    assert bool(Always()) is True


def test_never():
    assert (1 == Never()) is False
    assert ({} == Never()) is False
    assert ({"foo": 42} == Never()) is False

    assert Model("foo", "bar") != Model(Never(), "bar")


def test_never_boolean():
    assert bool(Never()) is False


def test_omit():
    assert Model("foo", "bar") == Model("foo", "OTHER") | Omit("email")


def test_only():
    assert Model("foo", "bar") == Model("foo", "OTHER") | Only("name")


@dataclass
class Model:
    name: str
    email: str


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
