from __future__ import annotations

import pytest

import better_sum


@pytest.fixture(
    params=[better_sum.sum.starts_at_instance, better_sum.sum_starts_at_instance])
def decorator_source(request):
    return request.param


def create_via_decorator_call_noargs(base_class, decorator_source):
    @decorator_source()
    class SubClassWithNoArgs(base_class):
        ...
    return SubClassWithNoArgs


def create_via_decorator_call_args(base_class, decorator_source):
    @decorator_source(0.0, 0.0)
    class SubClassWithArgs(base_class):
        ...
    return SubClassWithArgs


@pytest.fixture(params=[create_via_decorator_call_args, create_via_decorator_call_noargs])
def subclass_created(helpers, request, decorator_source):
    return request.param(helpers.SummableClass, decorator_source)


def test_decorators_register_instance(subclass_created):
    instance = better_sum._sum_start_defaults[subclass_created]
    assert isinstance(instance, subclass_created)
    assert instance.x == 0
    assert instance.y == 0



