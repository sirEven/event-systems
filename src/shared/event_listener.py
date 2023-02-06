from abc import ABC
from src.shared.event_system import SharedEventSystem


class EventListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def setup_event_handlers(self, **kwargs):
        for event_type, function in kwargs.items():
            SharedEventSystem.subscribe(event_type, function)
