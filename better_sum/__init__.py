"""Python's sum, minus ugly annotations and extra arguments.

Unlike the current built-in version, this one allows per-type default
start values so you don't have to pollute `__radd__` by accepting `0`.
"""
from __future__ import annotations
from typing import Type, TypeVar, Iterable, overload, Callable, Final, Protocol


try:
    from typing_extensions import Self
except ImportError:
    from typing_extensions import Self
try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec


_SUM_SIGNAL_CLASS_ATTR: Final[str] = '__sum_starts__'


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
_SummableInstanceParams = ParamSpec('_SummableInstanceParams')


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
_builtin_sum: Final[_SumFunc] = sum


# Although pyright claims the line below is meaningless, it
# expresses the idea of mapping a type to an instance of it
_sum_start_defaults: dict[Type[_T], _T] = {}  # type: ignore


def sum_starts_at_instance(
    *args: _SummableInstanceParams.args,  # type: ignore
    **kwargs: _SummableInstanceParams.kwargs
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
        args:
            The same positional the decorated class would take to create
            the default instance you want [better_sum.sum] to start at.
        kwargs:
            The same keyword arguments the decorated class would take to
            create the default instance you want [better_sum.sum][] to
            start at.

    Returns:
        The decorated [type][] without any modifications.
    """
    def _registering_func(wrapped_class: Type[_T]) -> Type[_T]:
        _sum_start_defaults[wrapped_class] = wrapped_class(*args, **kwargs)
        return wrapped_class

    return _registering_func


@overload
def sum(__iterable: Iterable[_A]) -> _A | int:
    ...


@overload
def sum(__iterable: Iterable[_A], __start: _SumResult) -> _A | _SumResult:
    ...


def sum(__iterable: Iterable[_A], *maybe_start):
    """A type-aware yet backward-compatible wrapper for Python's [sum][].

    To register a default sum start value for a type, choose one:

    * Decorate a class with [better_sum.sum_starts_at_instance][]
      ([full example](usage.md#decorator))
    * Add a `__sum_start__` class attribute
      ([full example](usage.md#class-attribute))

    When no start value is passed, this function tries to find one as
    follows:

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
        __iterable: An iterable to sum the contents of.
        __start: An optional overriding start value, just as in the
            original sum.
    Returns:
        The sum of the passed items, if any.
    """
    maybe_start_len = len(maybe_start)
    if maybe_start_len == 1:
        return _builtin_sum(__iterable, maybe_start[0])
    elif maybe_start_len > 1:
        raise TypeError("sum takes an iterable and an optional start argument")

    nonexhaustion_wrapper = iter(__iterable)
    first = next(nonexhaustion_wrapper)
    first_type = type(first)

    # It's been added via the decorator args
    if first_type in _sum_start_defaults:
        start: _A = \
            _sum_start_defaults[first_type] + first  # type: ignore

    # The class has a sum signal class attribute
    elif hasattr(first_type, _SUM_SIGNAL_CLASS_ATTR):
        start = getattr(first_type, _SUM_SIGNAL_CLASS_ATTR) + first

    # It's an ordinary boring class, so fall back to classic behavior
    else:
        # TODO: check if this is a pyright bug (0 has __add__?)
        start = 0  # type: ignore

    return _builtin_sum(nonexhaustion_wrapper, start)
