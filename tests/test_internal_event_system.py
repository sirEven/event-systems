from event_systems.internal.event_system import InternalEventSystem
from tests.helpers.dummy_emitter import DummyEmitter
from tests.helpers.dummy_subscriber import (
    DummySubscriber_zero,
    DummySubscriber_one,
    DummySubscriber_two,
)


def test_events_system_subscribe_zero_subscription_results_in_zero_entries():
    # given
    es = InternalEventSystem()
    _ = DummyEmitter(es)

    # when
    _ = DummySubscriber_zero(es)

    # then
    assert len(es._subscribers) == 0


def test_events_system_subscribe_one_subscription_results_in_one_entry():
    # given
    es = InternalEventSystem()
    _ = DummyEmitter(es)

    # when
    _ = DummySubscriber_one(es)

    # then
    assert len(es._subscribers) == 1


def test_events_system_subscribe_two_subscriptions_results_in_two_entries():
    # given
    es = InternalEventSystem()
    _ = DummyEmitter(es)

    # when
    _ = DummySubscriber_two(es)

    # then
    assert len(es._subscribers) == 2


def test_events_system_post_zero_subscriptions_results_in_zero_events_handled(capsys):
    # given
    es = InternalEventSystem()
    emitter = DummyEmitter(es)
    _ = DummySubscriber_zero(es)

    # when
    emitter.emit_event()

    # then
    out, err = capsys.readouterr()
    expected = ""
    assert expected == out


def test_events_system_post_one_subscription_results_in_one_event_handled(capsys):
    # given
    es = InternalEventSystem()
    emitter = DummyEmitter(es)
    _ = DummySubscriber_one(es)

    # when
    emitter.emit_event()

    # then
    out, err = capsys.readouterr()
    expected = "DummySubscriber_one - event handeled\n"
    assert expected == out


def test_events_system_post_two_subscriptions_results_in_two_events_handled(capsys):
    # given
    es = InternalEventSystem()
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


def test_post_with_event_data_one_subscription_results_in_one_event_handled_with_data(
    capsys,
):
    # given
    es = InternalEventSystem()
    emitter = DummyEmitter(es)
    _ = DummySubscriber_one(es)

    # when
    emitter.emit_event("some event data")

    # then
    out, err = capsys.readouterr()
    expected = "DummySubscriber_one - event handeled some event data\n"
    assert out == expected


def test_events_system_initialize_two_objects_results_in_seperate_identities():
    # given
    event_system_1 = InternalEventSystem()
    event_system_2 = InternalEventSystem()

    # when
    object_id_1 = id(event_system_1)
    object_id_2 = id(event_system_2)

    assert object_id_1 != object_id_2


def test_subscribe_to_two_instances_results_in_each_having_one_subscription():
    # given
    es_1 = InternalEventSystem()
    es_2 = InternalEventSystem()

    # when
    _ = DummySubscriber_one(es_1)
    _ = DummySubscriber_one(es_2)

    # then
    assert len(es_1._subscribers) == 1
    assert len(es_2._subscribers) == 1
