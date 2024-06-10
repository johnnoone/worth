# Something


Something is a Python library that helps you assert relevant object attributes

For example


```python
from something import Omit

def test_something_like():
    a = Model(id=12345, name="Hoff")
    b = Model(id=67890, name="Hoff")
    assert a == b | Omit("id")
```


It implemtents some helpers

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

**Always**

`Always()` assertion is always true.

```python
assert a == Always()
```

**Never**

`Never()` assertion is always false.

```python
assert a != Never()
```
