import pytest
from event_systems.shared.event_system import SharedEventSystem

from tests.helpers.dummy_emitter import DummyEmitter


def test_events_system_post_raises_exception_if_not_initialized_beforehand(
    capsys: pytest.CaptureFixture,
) -> None:
    # given
    emitter = DummyEmitter(SharedEventSystem)

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
