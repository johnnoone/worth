# Worth

Worth is a Python library that helps you assert relevant object attributes


For example

```python
from worth import Omit

def test_something_like():
    a = Model(id=12345, name="Hoff")
    b = Model(id=67890, name="Hoff")
    assert a == b | Omit("id")
```


It implements some helpers

**Always**

`Always()` assertion is always true.

```python
assert "a string" == Always()
assert 42 == Always()
assert False == Always()
```

**Never**

`Never()` assertion is always false.

```python
assert "a string" == Never()
assert 42 == Never()
assert False == Never()
```


Things that applies to dataclasses

**Omit**

`Omit()` let you to exclude some properties of you model from the comparison.

```python
a = Model(id=12345, name="Hoff")
b = Model(id=67890, name="Hoff")
assert a == b | Omit("id")
```

**Only**

`Only()` let you to choose precisely which properties you want to compair.

```python
a = Model(id=12345, name="Hoff")
b = Model(id=67890, name="Hoff")
assert a == b | Only("name")
```


Things that applies to mappings

**contains**

`contains()` let you to compare some mapping items.

```python
assert {"foo": 42, "bar": True} == contains({"foo": 42})
assert {"foo": 42, "bar": True} != contains({"foo": "wrong"})
```


## TODO

- [x] dataclasses
- [x] attrs
- [x] msgspec
- [ ] vanilla
