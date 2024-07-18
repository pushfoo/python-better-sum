import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
sys.path.append(str(HERE.parent))


from helpers import generator


@pytest.fixture(scope="session")
def helpers():
    import helpers
    return helpers


@pytest.fixture(params=(
        list,
        tuple,
        iter,
        generator
))
def iterable_factory(request):
    return request.param


@pytest.fixture
def empty_iterable(iterable_factory):
    return iterable_factory(tuple())

# @pytest.fixture()
# def base_summable_class():
