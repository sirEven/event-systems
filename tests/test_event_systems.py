from typing import Dict, Type
import pytest
from event_systems.base.protocols import Instanced
from event_systems.internal.event_system import InternalEventSystem
from event_systems.shared.event_system import SharedEventSystem
from tests.helpers.dummy_handlers import (
    async_dummy_handler,
    call_counting_dummy_handler,
    dummy_handler,
    dummy_handler_two,
)

from tests.helpers.typed_fixture import get_event_system_fixture

# NOTE: The parametrized implementations dictionary would actually translate to a string
#       by itself via parameetrization. However, for readability we call list on its keys.

implementations: Dict[str, Type[Instanced]] = {
    "internal_event_system": InternalEventSystem,
    "shared_event_system": SharedEventSystem,
}


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_events_system_initialization_results_in_no_subscriptions(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given & when
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])

    # then
    assert len(await es.get_subscriptions()) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_subscribe_results_in_one_subscription(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])

    # when
    await es.subscribe("some_event", dummy_handler)

    # then
    assert len(await es.get_subscriptions()) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_subscribe_twice_results_in_two_handlers_to_same_event(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])

    # when
    test_event = "test_event"
    await es.subscribe(test_event, dummy_handler)
    await es.subscribe(test_event, dummy_handler)

    # then
    all_registered_events = await es.get_subscriptions()
    handlers_on_test_event = all_registered_events[test_event]
    assert len(all_registered_events) == 1
    assert len(handlers_on_test_event) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_post_without_subscriptions_raises_error(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])

    # when
    with pytest.raises(ValueError):
        await es.post("some_event", {"dummy_data": "some data"})


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_post_one_event_with_one_handler_calls_one_handler_once(
    request: pytest.FixtureRequest,
    fixture_name: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # given
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])

    await es.subscribe("some_event", call_counting_dummy_handler)

    # when
    count = 0
    initial = f"event handeled {count} times"
    await es.post("some_event", {"dummy_data": initial})
    await es.process_all_events()  # Wait for all events to be processed

    # then
    expected = f"event handeled {count + 1} times" + "\n"
    out, _ = capsys.readouterr()
    assert out == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_post_two_different_events_with_individual_handlers_results_in_two_called_individual_handlers(
    request: pytest.FixtureRequest,
    fixture_name: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # given
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])
    await es.subscribe("first_event", dummy_handler)
    await es.subscribe("second_event", dummy_handler_two)

    # when
    expected_1 = "first data"
    expected_2 = "second data"
    await es.post("first_event", {"dummy_data": expected_1})
    await es.post("second_event", {"dummy_data": expected_2})
    await es.process_all_events()  # Wait for all events to be processed

    # then
    expected = expected_1 + "\n" + expected_2 + "\n"
    out, _ = capsys.readouterr()
    assert out == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_post_with_with_asynchronous_handler_calls_handler(
    request: pytest.FixtureRequest,
    fixture_name: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # given
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])

    await es.subscribe("some_event", async_dummy_handler)

    # when
    expected = "event handeled"
    await es.post("some_event", {"dummy_data": expected})
    await es.process_all_events()  # Wait for all events to be processed

    # then
    out, _ = capsys.readouterr()
    assert out == expected + "\n"


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_stop_results_in_clean_state(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])
    await es.subscribe("some_event", dummy_handler)

    # when
    await es.stop()

    # then
    assert len(await es.get_subscriptions()) == 0
    assert await es.is_running() == False
    assert not hasattr(es, "_task")


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_stop_and_start_results_in_clean_state(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given
    es = get_event_system_fixture(request, fixture_name, implementations[fixture_name])
    await es.subscribe("some_event", dummy_handler)
    await es.stop()

    # when
    await es.start()

    # then
    assert len(await es.get_subscriptions()) == 0
    assert await es.is_running() == True
    assert hasattr(es, "_task")
