import pytest
from event_systems.singleton.async_event_system import AsyncSingletonEventSystem

from tests.helpers.dummy_handlers import dummy_handler


@pytest.mark.asyncio
async def test_two_async_event_systems_are_identical(
    async_singleton_event_system: AsyncSingletonEventSystem,
) -> None:
    # given & when
    es_1 = async_singleton_event_system
    es_2 = async_singleton_event_system
    await es_1.subscribe("some_event", dummy_handler)

    # then AsyncEventSystem (singleton) references same object and hold same subscriptions
    assert id(es_1) == id(es_2)
    assert len(await es_1.get_subscriptions()) == len(await es_2.get_subscriptions())


@pytest.mark.asyncio
async def test_subscribe_when_not_initialized_calls_initialize(
    uninitialized_async_singleton_event_system: AsyncSingletonEventSystem,
) -> None:
    # given
    es = uninitialized_async_singleton_event_system

    # when
    await es.subscribe("some_event", dummy_handler)

    # then
    assert await es.get_instance() is not None


@pytest.mark.asyncio
async def test_post_raises_exception_if_not_initialized(
    uninitialized_async_singleton_event_system: AsyncSingletonEventSystem,
) -> None:
    # given
    es = uninitialized_async_singleton_event_system

    # when & then
    with pytest.raises(RuntimeError):
        await es.post("some_event", {"dummy_data": "some data"})
