import threading


class EventsSystem:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if not EventsSystem._instance:
            self.subscribers = {}
            EventsSystem._instance = self

    @classmethod
    def initialize(cls):
        if not cls._instance:
            with cls._lock:
                instance = cls()
                cls._instance = instance

    @classmethod
    def subscribe(cls, event_type, fn):
        if not cls._instance:
            cls.initialize()
        if fn:
            if event_type not in cls._instance.subscribers:
                cls._instance.subscribers[event_type] = []
            cls._instance.subscribers[event_type].append(fn)

    @classmethod
    def post(cls, event_type, event_data):
        if event_type in cls._instance.subscribers:
            for fn in cls._instance.subscribers[event_type]:
                fn(event_data)
