import pytest
from event_systems.instanced.threaded_event_system import ThreadedEventSystem
from tests.helpers.dummy_handlers import dummy_handler


def test_two_instances_with_different_threads_dont_interfere(
    capsys: pytest.CaptureFixture[str],
) -> None:
    # given
    es_1 = ThreadedEventSystem()
    es_2 = ThreadedEventSystem()

    # when
    es_1.subscribe("some_event", dummy_handler)
    es_2.subscribe("some_event", dummy_handler)

    # then
    assert len(es_1.get_subscriptions()) == 1
    assert len(es_2.get_subscriptions()) == 1

    # when
    es_1.start()
    es_2.start()

    es_1.post("some_event", {"dummy_data": "data 1"})
    es_1.process_all_events()
    es_2.post("some_event", {"dummy_data": "data 2"})
    es_2.process_all_events()

    es_1.stop()
    es_2.stop()

    # then
    assert len(es_1.get_subscriptions()) == 0
    assert len(es_2.get_subscriptions()) == 0
    out, _ = capsys.readouterr()
    assert out == "data 1\ndata 2\n"
