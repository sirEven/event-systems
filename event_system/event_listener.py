from abc import ABC
from event_system.event_system import EventSystem


class EventListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def setup_event_handlers(self, **kwargs):
        for event_type, function in kwargs.items():
            EventSystem.subscribe(event_type, function)
