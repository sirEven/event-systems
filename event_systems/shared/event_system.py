import asyncio
from typing import Optional, Dict, List, Any

from event_systems.base.event_system import EventSystem
from event_systems.base.handler import Handler


# TODO: Enable async handlers as well here, same as InternalEventSystem
# TODO: Try setting the running flag to True in start instead of init.


class SharedEventSystem(EventSystem):
    """
    This implementation uses a singleton pattern and maintains one global dictionary
    for all objects to store their subscriptions and run their event system.
    """

    _instance: Optional["SharedEventSystem"] = None
    _lock = asyncio.Lock()

    _subscriptions: Dict[str, List[Handler]]
    _event_queue: asyncio.PriorityQueue

    @classmethod
    async def initialize(cls) -> None:
        if not cls._instance:
            async with cls._lock:
                cls._instance = cls()
                cls._subscriptions = {}
                cls._event_queue = asyncio.Queue()

    @classmethod
    async def start(cls) -> None:
        cls._running = True
        if not cls._instance:
            await cls.initialize()
        cls._task = asyncio.create_task(cls._run_event_loop())

    @classmethod
    async def stop(cls) -> None:
        # Wait for all items in the queue to be processed
        if cls._event_queue:
            await cls._event_queue.join()

        # Cancel the task if it exists
        if cls._task:
            cls._task.cancel()

        # Reset the Singleton state
        cls._instance = None
        cls._subscriptions = {}
        if hasattr(cls, "_event_queue"):
            del cls._event_queue  # Remove the queue since it's no longer needed
        if hasattr(cls, "_task"):
            del cls._task  # Remove the task since it's cancelled

        cls._running = False

    @classmethod
    async def subscribe(cls, event_type: str, fn: Handler) -> None:
        if not cls._instance:
            await cls.initialize()
        async with cls._lock:
            if fn is not None:
                if event_type not in cls._subscriptions:
                    cls._subscriptions[event_type] = []
                cls._subscriptions[event_type].append(fn)

    @classmethod
    async def post(cls, event: str, event_data: Dict[str, Any]) -> None:
        """
        Posts an event to the internal event queue.

        Args:
            event_type: The type of event to be posted.
            event_data: The data to be posted with the event.

        Raises:
            RuntimeError: If no subscriptions have been registered before posting or if instance is None.
        """
        if cls._instance is None or not cls._subscriptions:
            raise RuntimeError(
                "At least one subscription has to be registered before posting events."
            )
        if event not in cls._subscriptions or not cls._subscriptions[event]:
            raise ValueError(f"No handlers registered for event '{event}'.")
        await cls._event_queue.put((event, event_data))

    @classmethod
    async def get_subscriptions(cls) -> Dict[str, List[Handler]]:
        return cls._subscriptions

    @classmethod
    async def _run_handler(cls, handler: Handler, event_data: Dict[str, Any]) -> None:
        if asyncio.iscoroutinefunction(handler):
            # If it's an async function, await it
            await handler(event_data)
        else:
            # If it's a sync function, run it in a thread
            await asyncio.to_thread(handler, event_data)

    @classmethod
    async def _process_events(cls) -> None:
        while True:
            event_type, event_data = await cls._event_queue.get()
            if event_type in cls._subscriptions:
                for handler in cls._subscriptions[event_type]:
                    if handler:
                        await cls._run_handler(handler, event_data)
            cls._event_queue.task_done()

    @classmethod
    async def _run_event_loop(cls) -> None:
        while cls._running:
            await cls._process_events()
            await asyncio.sleep(0.1)  # Prevent busy waiting
