import threading
from typing import Optional, Dict, List, Any

from event_systems.base.handler import Handler


# TODO: Enable async handlers as well here, same as InternalEventSystem
class SharedEventSystem:
    """
    This implementation uses a singleton pattern and maintains one global dictionary
    for all objects to store their subscriptions and run their event system.
    """

    _instance: Optional["SharedEventSystem"] = None
    _lock = threading.Lock()
    _subscriptions: Dict[str, List[Handler]] = {}

    @classmethod
    def initialize(cls) -> None:
        if not cls._instance:
            with cls._lock:
                cls._instance = cls()
                cls._subscriptions = {}

    @classmethod
    async def subscribe(cls, event_type: str, fn: Handler) -> None:
        if not cls._instance:
            cls.initialize()
        if fn is not None:
            if event_type not in cls._subscriptions:
                cls._subscriptions[event_type] = []
            cls._subscriptions[event_type].append(fn)

    @classmethod
    async def post(cls, event_type: str, event_data: Any) -> None:
        """
        Post an event to all subscribers of a specified event type.

        Raises:
            Exception: If an instance of EventsSystem has not been initialized.
            Note: This happens, if post() is being called before subscribe() has not
            been called at least once, which leads to the instance of EventsSystem being
            None.
        """
        if cls._instance is None:
            raise RuntimeError(
                "At least one subscription has to be registered before posting events."
            )

        if event_type in cls._subscriptions:
            for fn in cls._subscriptions[event_type]:
                if fn:
                    fn(event_data)

    @classmethod
    async def get_subscriptions(cls) -> Dict[str, List[Handler]]:
        return cls._subscriptions
