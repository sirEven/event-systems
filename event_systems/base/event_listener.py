from abc import ABC
from typing import Dict, Type
from event_systems.base.event_system import EventSystem
from event_systems.base.handler import Handler


class EventListener(ABC):
    def setup_event_handlers(
        self,
        event_system: EventSystem | Type[EventSystem],
        subscriptions: Dict[str, Handler],
    ) -> None:
        for event_type, function in subscriptions.items():
            if isinstance(event_system, type):
                event_system().subscribe(event_type, function)
            else:
                event_system.subscribe(event_type, function)
