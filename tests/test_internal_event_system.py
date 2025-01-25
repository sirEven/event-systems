import asyncio
import pytest


from event_systems.internal.event_system import InternalEventSystem
from tests.helpers.dummy_handlers import dummy_handler


@pytest.mark.asyncio
async def test_two_internal_event_systems_are_independent() -> None:
    # given & when
    es_1 = InternalEventSystem()
    es_2 = InternalEventSystem()
    await es_1.subscribe("some_event", dummy_handler)

    # then different InterrnralEventSystem (instance) objects hold different subscriptions
    assert id(es_1) != id(es_2)
    assert len(await es_1.get_subscriptions()) != len(await es_2.get_subscriptions())


# TODO: Cover much more crazy use cases with loop shenanigans
@pytest.mark.asyncio
async def test_custom_loop_has_no_issues_WIP() -> None:
    # given
    custom_loop = asyncio.new_event_loop()
    es = InternalEventSystem(asyncio_loop=custom_loop)
    await es.subscribe("some_event", dummy_handler)
    await es.start()

    # when
    await es.stop()

    # then
    assert len(await es.get_subscriptions()) == 0
    assert await es.is_running() == False
    assert not hasattr(es, "_task")
