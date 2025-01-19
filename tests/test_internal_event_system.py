from typing import Any, Dict
import pytest


from event_systems.internal.event_system import InternalEventSystem
from tests.helpers.dummy_handlers import async_dummy_handler, dummy_handler


# TODO: Move eligible tests to parametrized test suite in test_event_systems (if not yet covered there - then remove).


@pytest.mark.asyncio
async def test_two_internal_event_systems_are_independent() -> None:
    # given & when
    es_1 = InternalEventSystem()
    es_2 = InternalEventSystem()
    await es_1.subscribe("some_event", dummy_handler)

    # then different InterrnralEventSystem (instance) objects hold different subscriptions
    assert id(es_1) != id(es_2)
    assert len(await es_1.get_subscriptions()) != len(await es_2.get_subscriptions())
