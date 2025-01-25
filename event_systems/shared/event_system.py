import asyncio
import contextlib
from typing import Optional, Dict, List, Any, Tuple

from event_systems.base.protocols import Singleton
from event_systems.base.handler import Handler

from event_systems.common_strings import (
    NEEDS_INITIALIZATION,
    NO_SUBSCRIPTION_FOUND,
)


class SharedEventSystem(Singleton):
    _instance: Optional["SharedEventSystem"] = None
    _lock = asyncio.Lock()

    _is_running: bool
    _subscriptions: Dict[str, List[Handler]]
    _event_queue: asyncio.Queue[Tuple[str, Dict[str, Any]]]

    @classmethod
    async def start(cls) -> None:
        cls._is_running = True
        async with cls._lock:
            if not cls._instance:
                await cls._initialize()
        cls._task = asyncio.create_task(cls._run_event_loop())

    @classmethod
    async def stop(cls) -> None:
        # Wait for all items in the queue to be processed, then remove
        if hasattr(cls, "_event_queue"):
            await cls._event_queue.join()
            del cls._event_queue

        # Cancel the task if it exists, then remove
        if hasattr(cls, "_task") and cls._task:
            cls._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await cls._task
            del cls._task

        # Reset state
        cls._instance = None
        cls._subscriptions = {}
        cls._is_running = False

    @classmethod
    async def subscribe(cls, event_name: str, fn: Handler) -> None:
        if not cls._instance:
            await cls._initialize()

        async with cls._lock:
            if event_name not in cls._subscriptions:
                cls._subscriptions[event_name] = []
            cls._subscriptions[event_name].append(fn)

    @classmethod
    async def post(cls, event_name: str, event_data: Dict[str, Any]) -> None:
        if cls._instance is None:
            raise RuntimeError(NEEDS_INITIALIZATION.format(class_name=cls.__name__))
        if event_name not in cls._subscriptions:
            raise ValueError(NO_SUBSCRIPTION_FOUND.format(event=event_name))

        await cls._event_queue.put((event_name, event_data))

    @classmethod
    async def get_subscriptions(cls) -> Dict[str, List[Handler]]:
        return cls._subscriptions

    @classmethod
    async def is_running(cls) -> bool:
        return cls._is_running

    @classmethod
    async def process_all_events(cls) -> None:
        if not hasattr(cls, "_event_queue"):
            return
        await cls._event_queue.join()

    @classmethod
    async def _initialize(cls) -> None:
        if not cls._instance:
            cls._instance = cls()
            cls._subscriptions = {}
            cls._event_queue = asyncio.Queue()

    @classmethod
    async def get_instance(cls) -> Optional["SharedEventSystem"]:
        return cls._instance

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
        while hasattr(cls, "_event_queue"):
            event_type, event_data = await cls._event_queue.get()
            if event_type in cls._subscriptions:
                for handler in cls._subscriptions[event_type]:
                    # if handler: TODO: Check if this is ok
                    await cls._run_handler(handler, event_data)
            cls._event_queue.task_done()

    @classmethod
    async def _run_event_loop(cls) -> None:
        while cls._is_running:
            await cls._process_events()
            await asyncio.sleep(0.1)  # Prevent busy waiting
