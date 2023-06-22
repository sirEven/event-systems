from typing import Protocol, Callable, Any, List, Dict


class EventSystem(Protocol):
    def subscribe(self, event_type: str, fn: Callable):
        ...

    def post(self, event_type: str, event_data: Any):
        ...

    def get_subscribers(self) -> Dict[str, List[Callable]]:
        ...
