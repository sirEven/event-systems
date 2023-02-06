import threading
from typing import Callable, Dict, List, Any

# TODO: Replace Individual with a better name
class InternalEventSystem:
    """
    This implementation uses a factory pattern and allows individual objects to have their own event system, passed as a variable to each of their child objects.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, fn: Callable):
        with self._lock:
            if fn is not None:
                if event_type not in self._subscribers:
                    self._subscribers[event_type] = []
                self._subscribers[event_type].append(fn)

    def post(self, event_type: str, event_data: Any):
        if event_type in self._subscribers:
            for fn in self._subscribers[event_type]:
                fn(event_data)
