# better-sum

[decorator]: usage.md#decorator
[class attribute]: usage.md#class-attribute

Python's [sum][], minus [ugly annotations and extra arguments](why.md)

1. `pip install better-sum`
2. Use it via [decorator][] or `__sum_start__` [class attribute][].


```{.python hl_lines="5 24"}
from typing import NamedTuple
from better_sum import sum, sum_starts_at_instance


@sum_starts_at_instance(with_args=(0.0, 0.0))
class Vec2(NamedTuple):
    """Non-addition operations omitted."""

    x: float = 0.0
    y: float = 0.0

    # Support for passing ints is no longer needed!
    def __radd__(self, other: tuple[float, float]) -> Vec2:
        other_x, other_y = other
        return self.__class__(other_x + self.x, other_y + self.y)
   
    def __add__(self, other: tuple[float, float]) -> Vec2:
        other_x, other_y = other
        return self.__class__(self.x + other_x, self.y + other_y)
    

# If the type supports adding with tuples, only the
# very first value has to be of the registered type.
print(sum([Vec2(), (1.0, 1.0)]))
```

Output:
```
Vec(x=1.0, y=1.0)
```
