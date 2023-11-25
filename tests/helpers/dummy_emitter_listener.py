from abc import ABC, abstractmethod
from typing import Type, Dict
from event_systems.base.event_system import EventSystem
from event_systems.internal.event_listener import EventListener
from event_systems.base.handler import Handler


class DummyEmitterListener(EventListener, ABC):
    @abstractmethod
    def setup_DummyEmitter_event_handlers(
        self,
        event_system: EventSystem | Type[EventSystem],
        event_emitted_handler: Handler = None,
        another_event_emitted_handler: Handler = None,
    ) -> None:
        subscription_dict: Dict[str, Handler] = {
            "DummyEmitter_event_emitted_event": event_emitted_handler,
            "DummyEmitter_another_event_emitted_event": another_event_emitted_handler,
        }
        super().setup_event_handlers(event_system, subscription_dict)
