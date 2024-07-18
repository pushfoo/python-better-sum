from unittest.mock import sentinel

import pytest

import better_sum


def test_sum_returns_start_value_on_empty_iterable(empty_iterable):
    start = sentinel.start_value
    assert better_sum.sum(empty_iterable, start)


def test_sum_returns_0_early_when_empty_iterable_and_no_args(empty_iterable):
    assert better_sum.sum(empty_iterable) == 0


def test_sum_exits_early_on_empty_iterable(empty_iterable, monkeypatch):
    def raise_runtime_error():
        raise RuntimeError("Should never happen!")
    monkeypatch.setattr(better_sum, "_builtin_sum", raise_runtime_error)
    _ = better_sum.sum(empty_iterable)


@pytest.fixture
def summable_class_with_attribute(helpers):
    class UsesAttribute(helpers.SummableClass):
        ...

    setattr(UsesAttribute, better_sum.SUM_SIGNAL_CLASS_ATTR, (5.0, 5.0))

    return UsesAttribute


@pytest.fixture
def summable_class_iterable(helpers, summable_class_with_attribute, iterable_factory):
    return iterable_factory([summable_class_with_attribute(1.0, 1.0)])


def test_sum_instantiates_and_registers(helpers, iterable_factory, summable_class_with_attribute):

    iterable = [summable_class_with_attribute(1.0, 1.0)]
    better_sum.sum(iterable_factory(iterable))
    assert summable_class_with_attribute in better_sum._sum_start_defaults

    value_created = better_sum._sum_start_defaults[summable_class_with_attribute]
    assert value_created.x == 5.0
    assert value_created.y == 5.0


def test_sum_uses_existing_values_in_mapping(
        helpers, monkeypatch,
        iterable_factory, summable_class_with_attribute,
        summable_class_iterable
):
    instance_set = summable_class_with_attribute(-3.0, -3.0)
    monkeypatch.setitem(better_sum._sum_start_defaults, summable_class_with_attribute, instance_set)
    returned = better_sum.sum(summable_class_iterable)

    assert returned.x == -2.0
    assert returned.y == -2.0
