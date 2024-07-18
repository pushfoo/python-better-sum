# Why make this?

[\_\_radd\_\_]: https://docs.python.org/3/reference/datamodel.html#object.__radd__

**TL;DR:** I like nice types and I wanted to [try Mkdocs](#trying-mkdocs).

## Python's sum has nasty typing

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

## Why care about this?

**TL;DR:** Working on new [pyglet][] and [Arcade][] has been an adventure 

#### The state of pyglet

The pyglet codebase is nearly 20 years old. This means adding type annotations
is a slow work in progress given that:

* the project contained circular depdendencies and import tricks which
  annoy type checkers
* [pyright][] has reported hundreds of errors I've had to fix
* [mypy][] refuses to support [typing.NamedTuple][]at alll

For pyglet 2.1's dev previews, [pyglet.math][] was my focus. It contains:

1. comments explaining how Pythons' [sum][] uses `0` as a start value
2. vector types which support [sum][] via [\_\_radd\_\_][object.__radd__]
   to taking an [int][] value.

Also, pretty much everything in it is a [typing.NamedTuple][].

[kindness]: https://github.com/python/mypy/issues/1279#issuecomment-396622608

#### Really, mypy refuses?

[this comment]: https://github.com/python/mypy/issues/5944#issuecomment-441285456

Yes. Despite the [kindness of the Python's creator][kindness],
mypy's contributors hold an understandable yet harshly phrased
stance due to being sick of the problem:

> Duplicate of #5613, still low priority, better use dataclasses, as suggested above.

*From [this comment]*

## Trying Mkdocs

I've used Sphinx while working on [Arcade][] and [pyglet], but I wanted to
explore other documentation systems.
