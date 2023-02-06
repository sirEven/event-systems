from abc import ABC, abstractmethod
from src.base.event_system import EventSystem
from src.internal.event_listener import EventListener


class DummyEmitterListener(EventListener, ABC):
    @abstractmethod
    def setup_DummyEmitter_event_handlers(
        self,
        event_system: EventSystem,
        event_emitted_handler=None,
        another_event_emitted_handler=None,
    ):
        subscription_dict = {
            f"DummyEmitter_event_emitted_event": event_emitted_handler,
            "DummyEmitter_another_event_emitted_event": another_event_emitted_handler,
        }
        super().setup_event_handlers(event_system, **subscription_dict)
