import asyncio
import contextlib
from typing import Dict, List, Any

from event_systems.base.event_system import EventSystem
from event_systems.base.handler import Handler


# TODO: Extract string values and reuse in both implementations
# TODO: CONTINUE adapting method implementations of Internal to the ones of Shared. BUT: Monitor closely with tests, when issues start arising (infinite loops...)
class InternalEventSystem(EventSystem):
    """
    This implementation uses a factory pattern and allows individual objects to have
    their own event system, passed as a variable to each of their child objects.
    It is organized around an asyncio Queue and can execute synchronous and asynchronous handlers.
    """

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._subscriptions: Dict[str, List[Handler]] = {}
        self._event_queue: asyncio.Queue = asyncio.Queue()

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._run_event_loop())

    async def stop(self) -> None:
        # Wait for all items in the queue to be processed
        if hasattr(self, "_event_queue"):
            await self._event_queue.join()

        # Cancel any remaining tasks if needed
        if hasattr(self, "_task"):
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task

        # Reset state
        self._subscriptions = {}
        if hasattr(self, "_event_queue"):
            del self._event_queue  # Remove the queue since it's no longer needed
        if hasattr(self, "_task"):
            del self._task  # Remove the task since it's cancelled

        self._running = False

    async def subscribe(self, event_name: str, fn: Handler) -> None:
        async with self._lock:
            if fn is None:
                raise ValueError("Handler can't be None.")
            if event_name not in self._subscriptions:
                self._subscriptions[event_name] = []
            self._subscriptions[event_name].append(fn)

    async def post(self, event_name: str, event_data: Dict[str, Any]) -> None:
        if event_name not in self._subscriptions:
            raise ValueError(f"No subscription found with '{event_name}'.")

        await self._event_queue.put((event_name, event_data))

    async def get_subscriptions(self) -> Dict[str, List[Handler]]:
        return self._subscriptions

    async def _run_handler(self, handler: Handler, event_data: Dict[str, Any]) -> None:
        if asyncio.iscoroutinefunction(handler):
            # If it's an async function, await it
            await handler(event_data)
        else:
            # If it's a sync function, run it in a thread
            await asyncio.to_thread(handler, event_data)

    async def _process_events(self) -> None:
        while hasattr(self, "_event_queue"):
            event_type, event_data = await self._event_queue.get()
            if event_type in self._subscriptions:
                for handler in self._subscriptions[event_type]:
                    if handler:
                        await self._run_handler(handler, event_data)
            self._event_queue.task_done()

    async def _run_event_loop(self) -> None:
        while self._running:
            await self._process_events()
            await asyncio.sleep(0.1)  # Prevent busy waiting
