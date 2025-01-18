from typing import Type, TypeVar
import pytest

T = TypeVar("T")


def get_typed_fixture(
    request: pytest.FixtureRequest,
    fixture_name: str,
    fixture_type: Type[T],
) -> T:
    instance = request.getfixturevalue(fixture_name)
    assert isinstance(instance, fixture_type), (
        f"Fixture {fixture_name} is not of type {fixture_type}: {instance}"
    )
    return instance
