import threading

# TODO: Have a protocol that forces custom event systems to have a type specific subscribe and post function
class EventSystem:
    def __init__(self):
        self._lock = threading.Lock()
        self._subscribers = {}

    def subscribe(self, event_type: str, fn: callable):
        with self._lock:
            if fn:
                if event_type not in self._subscribers:
                    self._subscribers[event_type] = []
                self._subscribers[event_type].append(fn)

    def post(self, event_type: str, event_data):
        if event_type in self._subscribers:
            for fn in self._subscribers[event_type]:
                fn(event_data)