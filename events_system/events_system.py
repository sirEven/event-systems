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
        """
        Post an event to all subscribers of a specified event type.
        
        Raises:
            Exception: If an instance of EventsSystem has not been initialized. 
            Note: This happens, if post() is being called before subscribe() has not been called at least once, which leads to the instance of EventsSystem being None. 
        """
        if cls._instance is None:
            raise Exception("At least one subscription needs to be registered before posting events.")

        if event_type in cls._instance.subscribers:
            for fn in cls._instance.subscribers[event_type]:
                fn(event_data)
