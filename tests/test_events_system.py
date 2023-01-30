from events_system.events_system import EventsSystem
from tests.helpers.dummy_emitter import DummyEmitter
from tests.helpers.dummy_subscriber import DummySubscriber_not_subscribing, DummySubscriber_zero, DummySubscriber_one, DummySubscriber_two


def test_events_system_not_subscribing_results_in_Eventsystem_not_initialized():
    # given 
    emitter = DummyEmitter()
    
    # when
    subscriber = DummySubscriber_not_subscribing()

    # then
    assert EventsSystem._instance == None

    # clean up
    EventsSystem._instance = None

def test_events_system_subscribe_zero_subscription_results_in_zero_entries():
    # given 
    emitter = DummyEmitter()
    
    # when
    subscriber = DummySubscriber_zero()

    # then
    assert len(EventsSystem._instance.subscribers) == 0

    # clean up
    EventsSystem._instance = None

def test_events_system_subscribe_one_subscription_results_in_one_entry():
    # given 
    emitter = DummyEmitter()
    
    # when
    subscriber = DummySubscriber_one()

    # then
    assert len(EventsSystem._instance.subscribers) == 1

    # clean up
    EventsSystem._instance = None

def test_events_system_subscribe_two_subscriptions_results_in_two_entries():
    # given 
    emitter = DummyEmitter()
    
    # when
    subscriber = DummySubscriber_two()

    # then
    assert len(EventsSystem._instance.subscribers) == 2

    # clean up
    EventsSystem._instance = None

def test_events_system_post_zero_subscriptions_results_in_zero_events_handled(capsys):
    # given 
    emitter = DummyEmitter()
    subscriber = DummySubscriber_zero()

    # when
    emitter.emit_event()

    # then
    out, err = capsys.readouterr()
    expected = ""
    assert expected in out

    # clean up
    EventsSystem._instance = None

def test_events_system_post_one_subscription_results_in_one_event_handled(capsys):
    # given 
    emitter = DummyEmitter()
    subscriber = DummySubscriber_one()

    # when
    emitter.emit_event()

    # then
    out, err = capsys.readouterr()
    expected = "DummySubscriber_one - event handeled"
    assert expected in out

    # clean up
    EventsSystem._instance = None


def test_events_system_post_two_subscriptions_results_in_two_events_handled(capsys):
    # given 
    emitter = DummyEmitter()
    subscriber = DummySubscriber_two()

    # when
    emitter.emit_event()
    emitter.emit_another_event()

    # then
    out, err = capsys.readouterr()
    expected = "DummySubscriber_two - event handeled"
    assert expected in out

    expected = "DummySubscriber_two - another event handeled"
    assert expected in out

    # clean up
    EventsSystem._instance = None

def test_events_system_post_with_event_data_one_subscription_results_in_one_event_handled_with_event_data(capsys):
    # given 
    emitter = DummyEmitter()
    subscriber = DummySubscriber_one()

    # when
    emitter.emit_event("some event data")

    # then
    out, err = capsys.readouterr()
    expected = "DummySubscriber_one - event handeled some event data\n"
    assert expected == out

    # clean up
    EventsSystem._instance = None