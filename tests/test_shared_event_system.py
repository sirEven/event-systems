from event_systems.shared.event_system import SharedEventSystem
from tests.helpers.dummy_emitter import DummyEmitter
from tests.helpers.dummy_subscriber import (
    DummySubscriber_zero,
    DummySubscriber_one,
    DummySubscriber_two,
)


def test_events_system_subscribe_zero_subscription_results_in_zero_entries():
    # given
    _ = create_emitter()

    # when
    _ = DummySubscriber_zero(SharedEventSystem)

    # then
    assert len(SharedEventSystem._subscribers) == 0

    # clean up
    SharedEventSystem._instance = None


def test_events_system_subscribe_one_subscription_results_in_one_entry():
    # given
    _ = create_emitter()

    # when
    _ = DummySubscriber_one(SharedEventSystem)

    # then
    assert len(SharedEventSystem._subscribers) == 1

    # clean up
    SharedEventSystem._instance = None


def test_events_system_subscribe_two_subscriptions_results_in_two_entries(capsys):
    # given
    _ = create_emitter()

    # when
    _ = DummySubscriber_two(SharedEventSystem)

    # then
    assert len(SharedEventSystem._subscribers) == 2

    # clean up
    SharedEventSystem._instance = None
    SharedEventSystem._subscribers = None


def test_events_system_post_zero_subscriptions_results_in_zero_events_handled(capsys):
    # given
    emitter = create_emitter()
    _ = DummySubscriber_zero(SharedEventSystem)

    # when
    emitter.emit_event()

    # then
    out, err = capsys.readouterr()
    expected = ""
    assert expected == out

    # clean up
    SharedEventSystem._instance = None


def test_events_system_post_one_subscription_results_in_one_event_handled(capsys):
    # given
    emitter = create_emitter()
    _ = DummySubscriber_one(SharedEventSystem)

    # when
    emitter.emit_event()

    # then
    out, err = capsys.readouterr()
    expected = "DummySubscriber_one - event handeled\n"
    assert expected == out

    # clean up
    SharedEventSystem._instance = None


def test_events_system_post_two_subscriptions_results_in_two_events_handled(capsys):
    # given
    emitter = create_emitter()
    _ = DummySubscriber_two(SharedEventSystem)

    # when
    emitter.emit_event()
    emitter.emit_another_event()

    # then
    out, _ = capsys.readouterr()
    expected_1 = "DummySubscriber_two - event handeled\n"
    expected_2 = "DummySubscriber_two - another event handeled\n"
    assert out == expected_1 + expected_2

    # clean up
    SharedEventSystem._instance = None


def test_post_with_event_data_one_subscription_results_in_one_event_handled_with_data(
    capsys,
):
    # given
    emitter = create_emitter()
    _ = DummySubscriber_one(SharedEventSystem)

    # when
    emitter.emit_event("some event data")

    # then
    out, _ = capsys.readouterr()
    expected = "DummySubscriber_one - event handeled some event data\n"
    assert out == expected

    # clean up
    SharedEventSystem._instance = None


def test_events_system_post_raises_exception_if_not_initialized_beforehand(capsys):
    # given
    emitter = create_emitter()

    # when
    try:
        emitter.emit_event()
    except Exception as e:
        print(e)

    # then
    out, err = capsys.readouterr()
    expected = "At least one subscription has to be registered before posting events.\n"
    assert out == expected

    # clean up
    SharedEventSystem._instance = None


def create_emitter():
    return DummyEmitter(SharedEventSystem)
