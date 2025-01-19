import asyncio
import contextlib
from typing import Dict, List, Any

from event_systems.base.event_system import EventSystem
from event_systems.base.handler import Handler


# TODO: Try setting the running flag to True in start instead of init.
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
        # Wait for all items in the queue to be processed &  # Cancel any remaining tasks if needed
        await self._event_queue.join()

        if hasattr(self, "_task"):
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task

        self._running = False

    async def subscribe(self, event: str, fn: Handler) -> None:
        async with self._lock:
            if fn is not None:
                if event not in self._subscriptions:
                    self._subscriptions[event] = []
                self._subscriptions[event].append(fn)

    async def post(self, event: str, event_data: Dict[str, Any]) -> None:
        if event not in self._subscriptions or not self._subscriptions[event]:
            raise ValueError(f"No handlers registered for event '{event}'.")
        await self._event_queue.put((event, event_data))

    async def get_subscriptions(self) -> List[Handler]:
        return self._subscriptions

    async def _run_handler(self, handler: Handler, event_data: Dict[str, Any]) -> None:
        if asyncio.iscoroutinefunction(handler):
            # If it's an async function, await it
            await handler(event_data)
        else:
            # If it's a sync function, run it in a thread
            await asyncio.to_thread(handler, event_data)

    async def _process_events(self) -> None:
        while True:
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
