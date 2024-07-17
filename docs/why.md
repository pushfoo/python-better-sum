# Why make this?

[mkdocs]: https://www.mkdocs.org/
[\_\_radd\_\_]: https://docs.python.org/3/reference/datamodel.html#object.__radd__

**TL;DR:** I like nice types and I wanted to try [mkdocs][].

## Python's Sum

Python's current [sum][] function requires types to choose one of
the following:

```python
# The bad: verbose calls
sum(iterable, start_value)
```
This allows type annotations to be clean, but it feels bad.

```python
# The ugly: gross type annotations
class SupportsSum:

    # int is ugly
    def __radd__(self, other: int | SupportsSum):
        if other == 0:
            return self
        ...
```
This allows short [sum][] calls, but it feels wrong from a type
checking perspective.

## Trying Mkdocs

[Arcade]: https://api.arcade.academy/en/latest/
[pyglet]: https://pyglet.readthedocs.io/en/latest/

I've used Sphinx while working on [Arcade][] and [pyglet], but I wanted to
explore other documentation systems.

## Other Inspiration

[pyglet.math]: https://pyglet.readthedocs.io/en/development/modules/math.html#pyglet.math.Vec2

As of pyglet 2.1's dev previews, [pyglet.math][] contains:

1. comments explaining how Pythons' [sum][] uses `0` as a start value
2. [pyglet.math][] types which support [sum][] by allowing [\_\_radd\_\_][object.__radd__]
   to take an [int][] value.

