import threading
from typing import Dict, List, Any

from event_systems.base.handler import Handler


class InternalEventSystem:
    """
    This implementation uses a factory pattern and allows individual objects to have
    their own event system, passed as a variable to each of their child objects.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subscribers: Dict[str, List[Handler]] = {}

    def subscribe(self, event_type: str, fn: Handler) -> None:
        with self._lock:
            if fn is not None:
                if event_type not in self._subscribers:
                    self._subscribers[event_type] = []
                self._subscribers[event_type].append(fn)

    def post(self, event_type: str, event_data: Any) -> None:
        if event_type in self._subscribers:
            for fn in self._subscribers[event_type]:
                if fn:
                    fn(event_data)

    def get_subscribers(self) -> Dict[str, List[Handler]]:
        return self._subscribers
