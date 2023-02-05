from abc import ABC


class EventListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def setup_event_handlers(self, event_system, **kwargs):
        for event_type, function in kwargs.items():
            event_system.subscribe(event_type, function)
