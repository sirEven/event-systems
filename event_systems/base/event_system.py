from typing import Protocol, Callable, Any


class EventSystem(Protocol):
    def subscribe(self, event_type: str, fn: Callable):
        ...

    def post(self, event_type: str, event_data: Any):
        ...
