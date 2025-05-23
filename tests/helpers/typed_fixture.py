from typing import Type, TypeVar, Union
import pytest

from event_systems.instanced.async_event_system import AsyncEventSystem
from event_systems.instanced.threaded_event_system import ThreadedEventSystem
from event_systems.singleton.async_event_system import AsyncSingletonEventSystem

T = TypeVar("T")


def get_async_event_system_fixture(
    request: pytest.FixtureRequest,
    fixture_name: str,
    fixture_type: Union[Type[T], T],
) -> Union[AsyncEventSystem, Type[AsyncSingletonEventSystem]]:
    value = request.getfixturevalue(fixture_name)

    if fixture_type is AsyncEventSystem:
        # Assert wether value is instance of InternalEventSystem.
        assert isinstance(value, AsyncEventSystem), (
            f"Fixture {fixture_name} is not an instance of InternalEventSystem."
        )
    elif fixture_type is AsyncSingletonEventSystem:
        # Assert wether value of signleton type SharedEventSystem.
        assert value is AsyncSingletonEventSystem, (
            f"Fixture {fixture_name} is not a singleton class of SharedEventSystem."
        )

    else:
        raise ValueError(f"Unsupported fixture type: {fixture_type}")

    return value


def get_threaded_event_system_fixture(
    request: pytest.FixtureRequest,
    fixture_name: str,
    fixture_type: Union[Type[T], T],
) -> ThreadedEventSystem:
    value = request.getfixturevalue(fixture_name)

    if fixture_type is AsyncEventSystem:
        # Assert wether value is instance of InternalEventSystem.
        assert isinstance(value, ThreadedEventSystem), (
            f"Fixture {fixture_name} is not an instance of InternalEventSystem."
        )

    return value
