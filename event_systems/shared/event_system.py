import asyncio
import contextlib
from typing import Optional, Dict, List, Any

from event_systems.base.event_system import EventSystem
from event_systems.base.handler import Handler


# TODO: Enable async handlers as well here, same as InternalEventSystem


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
        if hasattr(cls, "_task") and cls._task:
            cls._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await cls._task

        # Reset the Singleton state
        cls._instance = None
        cls._subscriptions = {}
        if hasattr(cls, "_event_queue"):
            del cls._event_queue  # Remove the queue since it's no longer needed
        if hasattr(cls, "_task"):
            del cls._task  # Remove the task since it's cancelled

        cls._running = False

    @classmethod
    async def subscribe(cls, event_name: str, fn: Handler) -> None:
        if not cls._instance:
            await cls.initialize()
        async with cls._lock:
            if fn is not None:
                if event_name not in cls._subscriptions:
                    cls._subscriptions[event_name] = []
                cls._subscriptions[event_name].append(fn)

    @classmethod
    async def post(cls, event_name: str, event_data: Dict[str, Any]) -> None:
        """
        Posts an event to the internal event queue.

        Args:
            event_name: The name of event to be posted.
            event_data: The data to be passed to handlers subscribed with the event.

        Raises:
            RuntimeError: If no subscriptions have been registered before posting or if instance is None.
        """
        if cls._instance is None:
            msg = f"{cls.__name__} must be initialized before posting events."
            raise RuntimeError(msg)
        if event_name not in cls._subscriptions:
            msg = f"No subscription found with '{event_name}'."
            raise ValueError(msg)
        if not cls._subscriptions[event_name]:
            msg = f"No handlers registered for event '{event_name}'."
            raise ValueError(f"No handlers registered for event '{event_name}'.")

        await cls._event_queue.put((event_name, event_data))

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
