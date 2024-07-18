# Usage

There are two ways to set per-type sum start values:

| Approach                                                | Strength            |
|---------------------------------------------------------|---------------------|
| [Decorator](#decorator)                                 | Performance         |
| The `__sum_start__` [class attribute](#class-attribute) | Heritable defaults  |

Both keep things simple:

* No [MRO resolution][] is attempted
* Python's built-in [sum][] is left unchanged

## Fallback Behavior

For backward-compatibility and efficiency, [better_sum.sum][]
returns `0` when:

* the passed iterable is empty
* the first element's [type][] has neither:
    * a default value already registered via [decorator](#decorator)
    * a [`__sum_start__` class attribute](#class-attribute)

## Decorator

This is a more elaborate version of the example posted elsewhere.

The "proper" approach is to import the following:

| Import                                | Purpose                                     |
|---------------------------------------|---------------------------------------------|
| [better_sum.sum_starts_at_instance][] | Create a default instance                   |
| [better_sum.sum][]                    | Type-aware replacement for Python's [sum][] |

A shorter "improper" approach will be detailed after the code below:

```python
from typing import NamedTuple
from better_sum import sum, sum_starts_at_instance

@sum_starts_at_instance(0.0, 0.0)
class Vec2(NamedTuple):
    """Non-addition operations omitted for brevity."""

    x: float = 0.0
    y: float = 0.0
    
    # For more strictness, you could type other as Self
    def __radd__(self, other: tuple[float, float]) -> Vec2:
        """Support for passing ints is no longer needed!"""
        other_x, other_y = other
        return self.__class__(other_x + self.x, other_y + self.y)
   
    def __add__(self, other: tuple[float, float]) -> Vec2:
        other_x, other_y = other
        return self.__class__(self.x + other_x, self.y + other_y)


if __name__ == "__main__":
     print("Same type addition  :", sum([Vec2(1.0, 1.0), Vec2(1.0, 1.0)]))
     # Mixed type addition only works when Vec2 is the starting type
     print("Mixed type addition :", sum([Vec2(1.0, 1.0), (1.0, 1.0)]))
```

Since the decorator creates an instance of the wrapped class *immediately*,
it can be beneficial in the rare cases when you're optimizing Python code:

* Controlling bursts of instantiation matters ([pyglet][], [Arcade][], etc)
* You will be summing a large volume of dynamically generated types


### Shorthand Form

For the moment, you can use `sum.starts_at_instance` as shorthand:

```python
from better_sum import sum

@sum.starts_at_instance()
class Vec2(NamedTuple):
    ...
```

In theory, this is better as a classmethod or something else. However,
the following are also true about this project:

* it's making a point about type annotations in the standard library
* this is a `development` branch choice not released on PyPI
* the project is pre-1.0 and still exploring API design


## Class attribute

You can also set a `__sum_start__` class attribute.

Instead of creating a default instance immediately like the [decorator](#decorator),
[better_sum.sum][] will create it the first time it encounters an instance of the
type.

Instead of creating a default instance up front, this approach waits
until the first time an instance of a type is passed. This may be worse
when object creation is slow or if you have a lot of summable types.


```python
from __future__ import annotations
from better_sum import sum


class Vec2:

    __sum_start__ = (0.0, 0.0)

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self._values: list[float] = [x, y]
    
    @property
    def x(self) -> float:
        return self._values[0]

    @property
    def y(self) -> float:
        return self._values[1]

    def __radd__(self, other: tuple[float, float]) -> Vec2:
        """Support for passing ints is no longer needed!"""
        other_x, other_y = other
        return self.__class__(other_x + self[0], other_y + self[1])
   
    def __add__(self, other: tuple[float, float]) -> Vec2:
        other_x, other_y = other
        return self.__class__(self[0] + other_x, self[1] + other_y)

    
if __name__ == "__main__":
     print("Same type addition  :", sum([Vec2(1.0, 1.0), Vec2(1.0, 1.0)]))
     print("Mixed type addition :", sum([Vec2(1.0, 1.0), (1.0, 1.0)]))
```

As above, the mixed-type addition only works when a `Vec2` is the first
item summed.

