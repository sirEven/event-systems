from typing import Any, Dict
import pytest


from event_systems.internal.event_system import InternalEventSystem
from tests.helpers.dummy_handlers import async_dummy_handler, dummy_handler

# TODO: write tests for all public methods. Not covered yet: start and stop methods.


@pytest.mark.asyncio
async def test_subscribe_results_in_one_subscription(
    internal_event_system: InternalEventSystem,
) -> None:
    # given
    es = internal_event_system
    event = "some_event"
    handler = dummy_handler

    # when
    await es.subscribe(event, handler)

    # then
    assert len(es._subscriptions[event]) == 1


@pytest.mark.asyncio
async def test_post_with_synchronous_handler_results_in_handler_call(
    internal_event_system: InternalEventSystem,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es = internal_event_system
    event = "some_event"
    handler = dummy_handler
    await es.subscribe(event, handler)

    # when
    expected = "event_handeled"
    await es.post(event, {"dummy_data": expected})
    await es._event_queue.join()  # Wait for all events to be processed

    # then
    out, _ = capsys.readouterr()
    assert out == expected + "\n"


@pytest.mark.asyncio
async def test_post_with_asynchronous_handler_results_in_handler_call(
    internal_event_system: InternalEventSystem,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es = internal_event_system
    event = "some_event"
    handler = async_dummy_handler
    await es.subscribe(event, handler)

    # when
    expected = "event_handeled"
    await es.post(event, {"dummy_data": expected})
    await es._event_queue.join()  # Wait for all events to be processed

    # then
    out, _ = capsys.readouterr()
    assert out == expected + "\n"


# Continue covering it and setting up this project with uv and async -.-
