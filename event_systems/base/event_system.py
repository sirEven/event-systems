from typing import Protocol, Any, List, Dict

from event_systems.base.handler import Handler


class EventSystem(Protocol):
    def subscribe(self, event_type: str, fn: Handler) -> None:
        ...

    def post(self, event_type: str, event_data: Any) -> None:
        ...

    def get_subscribers(self) -> Dict[str, List[Handler]]:
        ...
