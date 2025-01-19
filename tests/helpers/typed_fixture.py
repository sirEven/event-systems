from typing import Type, TypeVar, Union
import pytest

from event_systems.internal.event_system import InternalEventSystem
from event_systems.shared.event_system import SharedEventSystem

T = TypeVar("T")


def get_typed_fixture(
    request: pytest.FixtureRequest,
    fixture_name: str,
    fixture_type: Union[Type[T], T],
) -> Union[T, Type[T]]:
    value = request.getfixturevalue(fixture_name)

    if fixture_type is InternalEventSystem:
        # Assert wether value is instance of InternalEventSystem.
        assert isinstance(value, InternalEventSystem), (
            f"Fixture {fixture_name} is not an instance of InternalEventSystem."
        )
    elif fixture_type is SharedEventSystem:
        # Assert wether value of signleton type SharedEventSystem.
        assert value is SharedEventSystem, (
            f"Fixture {fixture_name} is not a singleton class of SharedEventSystem."
        )

    else:
        raise ValueError(f"Unsupported fixture type: {fixture_type}")

    return value
