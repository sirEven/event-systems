from abc import ABC
from typing import Dict
from event_systems.base.handler import Handler
from event_systems.shared.event_system import SharedEventSystem


class EventListener(ABC):
    def __init__(self) -> None:
        super().__init__()

    def setup_event_handlers(self, subscriptions: Dict[str, Handler]) -> None:
        for event_type, function in subscriptions.items():
            SharedEventSystem.subscribe(event_type, function)
