from event_systems.base.event_system import EventSystem


class DummyEmitter:
    def __init__(self, event_system: EventSystem) -> None:
        self.event_system = event_system

    def emit_event(self, event_data=None):
        self.event_system.post("DummyEmitter_event_emitted_event", event_data)

    def emit_another_event(self, event_data=None):
        self.event_system.post("DummyEmitter_another_event_emitted_event", event_data)
