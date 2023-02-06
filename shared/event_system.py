import threading
from typing import Optional, Callable, Dict, List, Any


class SharedEventSystem:
    """
    This implementation uses a singleton pattern and maintains one global dictionary for all objects to store their subscriptions and run their event system.
    """

    _instance: Optional["SharedEventSystem"] = None
    _lock = threading.Lock()
    _subscribers: Dict[str, List[Callable]]

    def __init__(self):
        if not SharedEventSystem._instance:
            SharedEventSystem._instance = self

    @classmethod
    def initialize(cls):
        if not cls._instance:
            with cls._lock:
                cls._instance = cls()
                cls._subscribers = {}

    @classmethod
    def subscribe(cls, event_type: str, fn: Callable):
        if not cls._instance:
            cls.initialize()
        if fn is not None:
            if event_type not in cls._subscribers:
                cls._subscribers[event_type] = []
            cls._subscribers[event_type].append(fn)

    @classmethod
    def post(cls, event_type: str, event_data: Any):
        """
        Post an event to all subscribers of a specified event type.

        Raises:
            Exception: If an instance of EventsSystem has not been initialized.
            Note: This happens, if post() is being called before subscribe() has not been called at least once, which leads to the instance of EventsSystem being None.
        """
        if cls._instance is None:
            raise Exception(
                "At least one subscription needs to be registered before posting events."
            )

        if event_type in cls._subscribers:
            for fn in cls._subscribers[event_type]:
                fn(event_data)
