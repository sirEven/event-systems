from abc import ABC
from events_system.events_system import EventsSystem


class EventListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def setup_event_handlers(self, **kwargs):
        for event_type, function in kwargs.items():
            EventsSystem.subscribe(event_type, function)
