import threading


class EventSystem:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if not EventSystem._instance:
            self.subscribers = {}
            EventSystem._instance = self
            print(f"__init__ id: {id(self._instance)}")

    @classmethod
    def initialize(cls):
        if not cls._instance:
            with cls._lock:
                instance = cls()
                cls._instance = instance
                print(f"initialize id: {id(cls._instance)}")

    @classmethod
    def subscribe(cls, event_type, fn):
        if not cls._instance:
            cls.initialize()
        if fn:
            print(f"subscribing id: {id(cls._instance)}, {event_type}")
            if event_type not in cls._instance.subscribers:
                cls._instance.subscribers[event_type] = []
            cls._instance.subscribers[event_type].append(fn)

    @classmethod
    def post(cls, event_type, event_data):
        print(f"posting id: {id(cls._instance)}, {event_type}")
        if event_type in cls._instance.subscribers:
            for fn in cls._instance.subscribers[event_type]:
                fn(event_data)
