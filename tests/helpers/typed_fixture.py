from typing import Type, TypeVar, Union
import pytest

from event_systems.instanced.async_event_system import AsyncInternalEventSystem
from event_systems.instanced.threaded_event_system import ThreadedInternalEventSystem
from event_systems.singleton.asyncio_event_system import AsyncSharedEventSystem

T = TypeVar("T")


def get_async_event_system_fixture(
    request: pytest.FixtureRequest,
    fixture_name: str,
    fixture_type: Union[Type[T], T],
) -> Union[AsyncInternalEventSystem, Type[AsyncSharedEventSystem]]:
    value = request.getfixturevalue(fixture_name)

    if fixture_type is AsyncInternalEventSystem:
        # Assert wether value is instance of InternalEventSystem.
        assert isinstance(value, AsyncInternalEventSystem), (
            f"Fixture {fixture_name} is not an instance of InternalEventSystem."
        )
    elif fixture_type is AsyncSharedEventSystem:
        # Assert wether value of signleton type SharedEventSystem.
        assert value is AsyncSharedEventSystem, (
            f"Fixture {fixture_name} is not a singleton class of SharedEventSystem."
        )

    else:
        raise ValueError(f"Unsupported fixture type: {fixture_type}")

    return value

def get_threaded_event_system_fixture(
    request: pytest.FixtureRequest,
    fixture_name: str,
    fixture_type: Union[Type[T], T],
) -> ThreadedInternalEventSystem:
    value = request.getfixturevalue(fixture_name)

    if fixture_type is AsyncInternalEventSystem:
        # Assert wether value is instance of InternalEventSystem.
        assert isinstance(value, ThreadedInternalEventSystem), (
            f"Fixture {fixture_name} is not an instance of InternalEventSystem."
        )

    return value
