from abc import ABC
from src.base.event_system import EventSystem


class EventListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def setup_event_handlers(self, event_system: EventSystem, **kwargs):
        for event_type, function in kwargs.items():
            event_system.subscribe(event_type, function)
