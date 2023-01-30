
from tests.helpers.dummy_emitter_listener import DummyEmitterListener

class DummySubscriber_not_subscribing(DummyEmitterListener):
    def __init__(self):
        pass
    
    def setup_DummyEmitter_event_handlers(self, event_emitted_handler=None):
        return super().setup_DummyEmitter_event_handlers(event_emitted_handler)

class DummySubscriber_zero(DummyEmitterListener):
    def __init__(self):
        pass
        self.setup_DummyEmitter_event_handlers(None)
    
    def setup_DummyEmitter_event_handlers(self, event_emitted_handler=None):
        return super().setup_DummyEmitter_event_handlers(event_emitted_handler)

class DummySubscriber_one(DummyEmitterListener):
    def __init__(self):
        self.setup_DummyEmitter_event_handlers(self.handle_DummyEmitter_event_emitted_event)

    def handle_DummyEmitter_event_emitted_event(self, event_data=None):
        print(f"{type(self).__name__} - event handeled {event_data}")
    
    def setup_DummyEmitter_event_handlers(self, event_emitted_handler=None):
        return super().setup_DummyEmitter_event_handlers(event_emitted_handler)

class DummySubscriber_two(DummyEmitterListener):
    def __init__(self):
        self.setup_DummyEmitter_event_handlers(self.handle_DummyEmitter_event_emitted_event, self.handle_DummyEmitter_another_event_emitted_event)

    def handle_DummyEmitter_event_emitted_event(self, event_data=None):
        print(f"{type(self).__name__} - event handeled {event_data}")
    
    def handle_DummyEmitter_another_event_emitted_event(self, event_data=None):
        print(f"{type(self).__name__} - another event handeled {event_data}")
    
    def setup_DummyEmitter_event_handlers(self, event_emitted_handler=None, another_event_emitted_handler=None):
        return super().setup_DummyEmitter_event_handlers(event_emitted_handler, another_event_emitted_handler)