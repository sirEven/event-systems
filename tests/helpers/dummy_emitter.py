from events_system.events_system import EventsSystem
class DummyEmitter():
    
    def emit_event(self, event_data=None):
        EventsSystem.post("DummyEmitter_event_emitted_event", event_data)
    
    def emit_another_event(self, event_data=None):
        EventsSystem.post("DummyEmitter_another_event_emitted_event", event_data)