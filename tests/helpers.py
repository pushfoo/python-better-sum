"""Contains test helpers.

These are "contagious" the same way pyglet.math's vectors are as of
pyglet's 2.1 dev previews: adding an instance of one of the Summable
types to any other compatible type will return an instance of the
Summable type.
"""

from __future__ import annotations

from typing import Iterable, Generator, TypeVar, TYPE_CHECKING, overload, cast, NamedTuple

_T = TypeVar('_T')


def generator(iterable: Iterable[_T]) -> Generator[_T, None, None]:
    for i in iterable:
        yield i


class SummableTuple(NamedTuple):
    """Non-addition operations omitted for brevity."""

    x: float = 0.0
    y: float = 0.0

    def __radd__(self, other: tuple[float, float]) -> SummableTuple:
        """Support for passing ints is no longer needed!"""
        other_x, other_y = other
        return self.__class__(other_x + self.x, other_y + self.y)

    def __add__(self, other: tuple[float, float]) -> SummableTuple:
        other_x, other_y = other
        return self.__class__(other_x + self.x, other_y + self.y)


class SummableClass:
    """A roughly mutable vector-like class.

    This is for testing:

    1. The class attribute features
    2. The decorator
    3. Registering the type directly


    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self._inner: list[float] = [x, y]

    @property
    def x(self) -> float:
        return self._inner[0]

    @x.setter
    def x(self, new_x: float):
        if not isinstance(new_x, (float, int)):
            raise TypeError("new_x is not an int or float")

        self._inner[0] = new_x * 1.0

    @property
    def y(self) -> float:
        return self._inner[0]

    @y.setter
    def y(self, new_y: float):
        if not isinstance(new_y, (float, int)):
            raise TypeError("new_y is not an int or float")

        self._inner[1] = new_y * 1.0

    def __iter__(self) -> Generator[float, None, None]:
        for v in self._inner:
            yield v

    if TYPE_CHECKING:
        @overload
        def __getitem__(self, index: slice) -> list[float]: ...

        @overload
        def __getitem__(self, index: int) -> float: ...

    def __getitem__(self, index: int | slice) -> list[float] | float:
        if isinstance(index, int):
            return cast(float,
                        self._inner[index])
        elif isinstance(index, slice):
            return cast(list[float], self._inner[index])
        else:
            raise TypeError(f"Can't index by type of {index}")

    def __eq__(self, other: tuple[float, float] | SummableClass) -> bool:
        return other[0] == self.x and other[1] == self.y

    def __add__(self, other: tuple[float, float] | SummableClass) -> SummableClass:
        other_x, other_y = other
        return self.__class__(self.x + other_x, self.y + other_y)

    def __radd__(self, other: tuple[float, float] | SummableClass) -> SummableClass:
        other_x, other_y = other
        return self.__class__(other_x + self.x + other_x, other_y + self.y)

    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"
