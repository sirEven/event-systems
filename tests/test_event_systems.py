import pytest
from event_systems.base.event_system import EventSystem
from tests.helpers.dummy_emitter import DummyEmitter
from tests.helpers.dummy_subscriber import (
    DummySubscriber_zero,
    DummySubscriber_one,
    DummySubscriber_two,
)

event_systems = ["shared_event_system", "internal_event_system"]


@pytest.mark.parametrize("event_system", event_systems)
def test_events_system_subscribe_zero_subscription_results_in_zero_entries(
    event_system: str,
    request: pytest.FixtureRequest,
) -> None:
    # given
    es: EventSystem = request.getfixturevalue(event_system)
    _ = DummyEmitter(es)

    # when
    _ = DummySubscriber_zero(es)

    # then
    assert len(es.get_subscribers()) == 0


@pytest.mark.parametrize("event_system", event_systems)
def test_events_system_subscribe_one_subscription_results_in_one_entry(
    event_system: str,
    request: pytest.FixtureRequest,
) -> None:
    # given
    es: EventSystem = request.getfixturevalue(event_system)
    _ = DummyEmitter(es)

    # when
    _ = DummySubscriber_one(es)

    # then
    assert len(es.get_subscribers()) == 1


@pytest.mark.parametrize("event_system", event_systems)
def test_events_system_subscribe_two_subscriptions_results_in_two_entries(
    event_system: str,
    request: pytest.FixtureRequest,
) -> None:
    # given
    es: EventSystem = request.getfixturevalue(event_system)
    _ = DummyEmitter(es)

    # when
    _ = DummySubscriber_two(es)

    # then
    assert len(es.get_subscribers()) == 2


@pytest.mark.parametrize("event_system", event_systems)
def test_events_system_post_zero_subscriptions_results_in_zero_events_handled(
    event_system: str,
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es: EventSystem = request.getfixturevalue(event_system)
    emitter = DummyEmitter(es)
    _ = DummySubscriber_zero(es)

    # when
    emitter.emit_event()

    # then
    out, err = capsys.readouterr()
    expected = ""
    assert expected == out


@pytest.mark.parametrize("event_system", event_systems)
def test_events_system_post_one_subscription_results_in_one_event_handled(
    event_system: str,
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es: EventSystem = request.getfixturevalue(event_system)
    emitter = DummyEmitter(es)
    _ = DummySubscriber_one(es)

    # when
    emitter.emit_event()

    # then
    out, err = capsys.readouterr()
    expected = "DummySubscriber_one - event handeled\n"
    assert expected == out


@pytest.mark.parametrize("event_system", event_systems)
def test_events_system_post_two_subscriptions_results_in_two_events_handled(
    event_system: str,
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es: EventSystem = request.getfixturevalue(event_system)
    emitter = DummyEmitter(es)
    _ = DummySubscriber_two(es)

    # when
    emitter.emit_event()
    emitter.emit_another_event()

    # then
    out, err = capsys.readouterr()
    expected_1 = "DummySubscriber_two - event handeled\n"
    expected_2 = "DummySubscriber_two - another event handeled\n"
    assert out == expected_1 + expected_2


@pytest.mark.parametrize("event_system", event_systems)
def test_post_with_event_data_one_subscription_results_in_one_event_handled_with_data(
    event_system: str,
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    es: EventSystem = request.getfixturevalue(event_system)
    emitter = DummyEmitter(es)
    _ = DummySubscriber_one(es)

    # when
    emitter.emit_event("some event data")

    # then
    out, err = capsys.readouterr()
    expected = "DummySubscriber_one - event handeled some event data\n"
    assert out == expected


@pytest.mark.parametrize("event_system", event_systems)
def test_create_two_objects_of_same_event_system_results_correct_object_identites(
    event_system: str,
    request: pytest.FixtureRequest,
) -> None:
    # given
    event_system_1: EventSystem = request.getfixturevalue(event_system)
    event_system_2: EventSystem = request.getfixturevalue(event_system)

    # when
    object_id_1 = id(event_system_1)
    object_id_2 = id(event_system_2)

    # then
    if isinstance(event_system, type):
        # SharedEventSystem (singleton)
        assert object_id_1 != object_id_2
    else:
        # InternalEventSystem (instance)
        assert object_id_1 == object_id_2


@pytest.mark.parametrize("event_system", event_systems)
def test_subscribe_to_two_instances_results_in_each_having_one_subscription(
    event_system: str,
    request: pytest.FixtureRequest,
) -> None:
    # given
    es_1: EventSystem = request.getfixturevalue(event_system)
    es_2: EventSystem = request.getfixturevalue(event_system)

    # when
    _ = DummySubscriber_one(es_1)
    _ = DummySubscriber_one(es_2)

    # then
    assert len(es_1.get_subscribers()) == 1
    assert len(es_2.get_subscribers()) == 1
