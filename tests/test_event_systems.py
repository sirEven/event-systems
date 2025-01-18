from typing import Any, Dict
import pytest
from event_systems.base.event_system import EventSystem
from event_systems.internal.event_system import InternalEventSystem
from event_systems.shared.event_system import SharedEventSystem
from tests.helpers.dummy_emitter import DummyEmitter
from tests.helpers.dummy_handlers import (
    call_counting_dummy_handler,
    dummy_handler,
    dummy_handler_two,
)
from tests.helpers.dummy_subscriber import (
    DummySubscriber_zero,
    DummySubscriber_one,
    DummySubscriber_two,
)
from tests.helpers.typed_fixture import get_typed_fixture

# TODO: These tests we should actually run with parametrization for both implementations
# TODO: Remove weird unreadable tests with emitter dummies and so on.
# TODO: Write tests for individual types (Internal / Shared EventSystem) where coverage is not given by these tests here.
# TODO: These old tests cover a conveniece object called EventListener, where multiple subscriptions (a dict) can be packed into one setup call - if we want to keep that, let's test this object separately.
# TODO: instead of just instantiating into es var, fetch the fixture by type
implementations = {
    "internal_event_system": InternalEventSystem,
    "shared_event_system": SharedEventSystem,
}


# NOTE: The parametrized implementations dictionary would actually translate to a string by itself via parameetrization - however for readability we call list on its keys.
@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_events_system_init_results_in_no_subscribers(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given & when
    es = get_typed_fixture(request, fixture_name, implementations[fixture_name])

    # then
    assert len(await es.get_subscriptions()) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_subscribe_results_in_one_subscriber(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given
    es = get_typed_fixture(request, fixture_name, implementations[fixture_name])

    # when
    await es.subscribe("some_event", dummy_handler)

    # then
    assert len(await es.get_subscriptions()) == 1


# TODO: Revisit this case as well, think of an Exception instead (Why have the same (===) fn be called multiple times?)
@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_subscribe_twice_results_in_two_handlers_to_same_event(
    request: pytest.FixtureRequest,
    fixture_name: str,
) -> None:
    # given
    es = get_typed_fixture(request, fixture_name, implementations[fixture_name])

    # when
    test_event = "test_event"
    await es.subscribe(test_event, dummy_handler)
    await es.subscribe(test_event, dummy_handler)

    # then
    all_registered_events_with_their_handlers = await es.get_subscriptions()
    handlers_on_test_event = all_registered_events_with_their_handlers[test_event]
    assert len(all_registered_events_with_their_handlers) == 1
    assert len(handlers_on_test_event) == 2


# TODO: Revisit this case, think of Exception instead (Why subscribe to an event, with no handler? That's like going to the Dentist without opening my mouth.)
@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_post_event_without_handler_calls_no_handler(
    request: pytest.FixtureRequest,
    fixture_name: str,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es = get_typed_fixture(request, fixture_name, implementations[fixture_name])
    await es.subscribe("some_event", None)

    # when
    await es.post("some_event", {"dummy_data": "some data"})

    # then
    out, _ = capsys.readouterr()
    expected = ""
    assert expected == out


@pytest.mark.asyncio
@pytest.mark.parametrize("fixture_name", list(implementations.keys()))
async def test_post_one_event_with_one_handler_calls_one_handler_once(
    request: pytest.FixtureRequest,
    fixture_name: str,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es = get_typed_fixture(request, fixture_name, implementations[fixture_name])

    await es.subscribe("some_event", call_counting_dummy_handler)

    # when
    count = 0
    initial = f"event handeled {count} times"
    await es.post("some_event", {"dummy_data": initial})
    await es._event_queue.join()  # Wait for all events to be processed

    # then
    expected = f"event handeled {count + 1} times" + "\n"
    out, _ = capsys.readouterr()
    assert out == expected


@pytest.mark.asyncio
async def test_post_two_different_events_with_individual_handlers_results_in_two_called_individual_handlers(
    shared_event_system: SharedEventSystem,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es = shared_event_system
    await es.subscribe("first_event", dummy_handler)
    await es.subscribe("second_event", dummy_handler_two)

    # when
    expected_1 = "first data"
    expected_2 = "second data"
    await es.post("first_event", {"dummy_data": expected_1})
    await es.post("second_event", {"dummy_data": expected_2})

    # then
    expected = expected_1 + "\n" + expected_2 + "\n"
    out, _ = capsys.readouterr()
    assert out == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("event_system", implementations)
async def test_create_two_objects_of_same_event_system_results_correct_object_identites(
    event_system: EventSystem,
) -> None:
    # given & when
    es_1 = event_system()
    es_2 = event_system()
    await es_1.subscribe("some_event", dummy_handler)

    # then different SharedEventSystem (singleton) objects hold same subscriptions
    if isinstance(es_1, type(SharedEventSystem)):
        assert id(es_1) != id(es_2)
        assert len(es_1.get_subscriptions()) == len(es_2.get_subscriptions())

    # then different InterrnralEventSystem (instance) objects hold different subscriptions
    if isinstance(es_1, type(SharedEventSystem)):
        assert id(es_1) != id(es_2)
        assert len(es_1.get_subscriptions()) != len(es_2.get_subscriptions())
