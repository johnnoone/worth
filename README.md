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
