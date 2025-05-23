import asyncio
from typing import Any, Coroutine
import pytest


from event_systems.instanced.async_event_system import AsyncEventSystem
from tests.helpers.dummy_handlers import dummy_handler


def run_in_loop(
    coro: Coroutine[Any, Any, None],
    loop: asyncio.AbstractEventLoop,
) -> None:
    """Helper function to run a coroutine in a specified loop from the test context."""
    # Since run_until_complete is meant for synchronous context, we don't await it
    loop.run_until_complete(coro)


@pytest.mark.asyncio
async def test_two_event_systems_are_independent() -> None:
    # given & when
    es_1 = AsyncEventSystem()
    es_2 = AsyncEventSystem()
    await es_1.subscribe("some_event", dummy_handler)

    # then different instance objects hold different subscriptions
    assert id(es_1) != id(es_2)
    assert len(await es_1.get_subscriptions()) != len(await es_2.get_subscriptions())


@pytest.mark.asyncio
async def test_custom_loop_stop_results_in_clean_state() -> None:
    # given
    custom_loop = asyncio.new_event_loop()
    es = AsyncEventSystem(asyncio_loop=custom_loop)
    await es.subscribe("some_event", dummy_handler)
    await es.start()

    # when
    await es.stop()

    # then
    assert len(await es.get_subscriptions()) == 0
    assert await es.is_running() == False
    assert not hasattr(es, "_task")


@pytest.mark.asyncio
async def test_system_with_custom_loop_can_be_reused(
    capsys: pytest.CaptureFixture[str],
) -> None:
    # given
    custom_loop = asyncio.new_event_loop()
    try:
        es = AsyncEventSystem(asyncio_loop=custom_loop)
        await es.subscribe("some_event", dummy_handler)
        await es.start()
        await es.stop()

        # when
        expected = "some different data"
        await es.subscribe("some_other_event", dummy_handler)
        await es.start()

        await es.subscribe("some_different_event", dummy_handler)
        await es.post("some_different_event", {"dummy_data": expected})
        run_in_loop(es.process_all_events(), custom_loop)

        # then
        out, _ = capsys.readouterr()
        assert out == expected + "\n"
        assert len(await es.get_subscriptions()) == 2
        assert await es.is_running() == True
        assert hasattr(es, "_task")
    finally:
        # Reset to the default loop for pytest
        asyncio.set_event_loop(asyncio.get_event_loop())
        # Ensure all tasks are cancelled before closing the loop
        for task in asyncio.all_tasks(custom_loop):
            task.cancel()
        custom_loop.run_until_complete(custom_loop.shutdown_asyncgens())
        custom_loop.close()


@pytest.mark.asyncio
async def test_get_loop_returns_correct_loop() -> None:
    # given
    custom_loop = asyncio.new_event_loop()
    try:
        es = AsyncEventSystem(asyncio_loop=custom_loop)

        # when
        loop = es.get_loop()

        # then
        assert loop is custom_loop
    finally:
        asyncio.set_event_loop(asyncio.get_event_loop())
        # Ensure all tasks are cancelled before closing the loop
        for task in asyncio.all_tasks(custom_loop):
            task.cancel()
        custom_loop.run_until_complete(custom_loop.shutdown_asyncgens())
        custom_loop.close()
