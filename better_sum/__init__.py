"""Python's sum, minus ugly annotations and extra arguments.

Unlike the current built-in version, this one allows per-type default
start values so you don't have to pollute `__radd__` by accepting `0`.
"""
from __future__ import annotations
from typing import Type, TypeVar, Iterable, overload, Callable, Final, Protocol, Any


SUM_SIGNAL_CLASS_ATTR: Final[str] = '__sum_start__'


# Used to set up the _HasAdd Protocol + a few other annotations below
_T = TypeVar('_T')
_T_co = TypeVar('_T_co', covariant=True)
_T_contra = TypeVar('_T_contra', contravariant=True)


class _HasAdd(Protocol[_T_contra, _T_co]):
    """We only need __add__ since user-provided objects have __radd__."""

    def __add__(self, __a: _T_contra) -> _T_co: ...


# Adding-related types
_A = TypeVar('_A', bound=_HasAdd)
_SumResult = TypeVar('_SumResult', bound=_HasAdd)  # Result sum type


class _SumFunc(Protocol[_A, _SumResult]):
    """Annotates [`sum`][better_sum.sum] as a Protocol type annotation.

    This is an attempt to cover variadic callables on Python <= 3.9
    well enough to pass pyright's type checking. Although this is
    cobbled together from builtins.pyi and Protocol:

    * It probably works on Python 3.8
    * It will hold things over until typing improvements from
      later Python versions becomes generally available instead
      of the weak typing-extensions versions

    """

    @overload
    def __call__(self, __iterable: Iterable[_SumResult]) -> _A | int:
        ...

    @overload
    def __call__(self, __iterable: Iterable[_A], __start: _SumResult | int) -> _SumResult:
        ...

    def __call__(self, *args) -> _A | int | _SumResult:
        ...


# Preserve this for later use since we'll need it
# TODO: pyright does NOT like it when Final is around this!
# may need to be filed as a bug.
_builtin_sum: _SumFunc = sum


# Although pyright claims the line below is meaningless, it
# expresses the idea of mapping a type to an instance of it
_sum_start_defaults: dict[Type, Any] = {
    int: 0
}


def sum_starts_at_instance(
    *decorated_args,
    **decorated_kwargs
) -> Callable[[Type[_T]], Type[_T]]:
    """Register a type's start value for [sum][better_sum.sum].

    Call this decorator with the same positional and keyword arguments
    the wrapped class would take if you were creating the default
    instance directly.

    ```python
    from sum import sum_starts_at_instance

    @sum_starts_at_instance(1, 2)
    class MyType:
        def __init__(a: int, b: int, optional_value: str | None = None):
            ...
    ```

    For an in-depth example, please see the [Decorator](usage.md#decorator)
    example in the [Usage Guide](usage.md)

    Args:
        decorated_args:
            The same positional the decorated class would take to create
            the default instance you want [better_sum.sum][] to start at.
        decorated_kwargs:
            The same keyword arguments the decorated class would take to
            create the default instance you want [better_sum.sum][] to
            start at.

    Returns:
        The decorated [type][] without any modifications.
    """
    def _registering_func(wrapped_class: Type[_T]) -> Type[_T]:
        _sum_start_defaults[wrapped_class] = wrapped_class(
            *decorated_args,
            **decorated_kwargs)
        return wrapped_class

    return _registering_func


def sum(__iterable: Iterable[_A], /, __start: _SumResult = 0) -> _SumResult:
    """A type-aware yet backward-compatible wrapper for Python's [sum][].

    To register a default sum start value for a type, choose one:

    * Decorate a class with [better_sum.sum_starts_at_instance][]
      ([full example](usage.md#decorator))
    * Add a `__sum_start__` class attribute
      ([full example](usage.md#class-attribute))

    When no start value is passed, this function tries to find one
    based on the [type][] of the first value of the function.

    1. If the iterable is empty, return `0` immediately
    2. Get the [type][] of the first item
    3. If there's a default instance for the type, use it as the start
       value
    4. If the type has a `__sum_start__` class attribute:
        1. Initialize a new instance of the type with those arguments
        2. Set it as the default instance for both this call and future
          ones

    !!! note

        To avoid premature optimization and unneeded features, this
        function does not currently attempt to walk the class hierarchy.

    Args:
        __iterable (Iterable[_A]): An iterable to sum the contents of.
        __start (_SumResult): An optional overriding start value, just as in the
            original sum.
    Returns:
        The sum of the passed items, if any.
    """
    iter_wrapper = iter(__iterable)  # Adapt Sequences for next() iteration
    try:
        first = next(iter_wrapper)
        first_type = type(first)
    except StopIteration:
        return __start

    # A default start was registered via decorator or instantiation
    if first_type in _sum_start_defaults:
        start: _SumResult = \
            _sum_start_defaults[first_type] + first  # type: ignore

    # The class has a __sum_start__ class attribute
    elif hasattr(first_type, SUM_SIGNAL_CLASS_ATTR):
        start_args = getattr(first_type, SUM_SIGNAL_CLASS_ATTR)
        _start_raw = first_type(*start_args)
        _sum_start_defaults[first_type] = _start_raw
        start = _start_raw + first
    else:
        start = __start

    return _builtin_sum(iter_wrapper, start)


# Silence report of spurious issue
sum.starts_at_instance = (  # type: ignore  # pending OOP or other fix
    sum_starts_at_instance
)
"""A shortcut binding of [better_sum.sum_starts_at_instance][].

This is an ugly trick, but it should work.
"""
