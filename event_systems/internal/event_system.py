import asyncio
import contextlib
from typing import Dict, List, Any

from event_systems.base.handler import Handler


class InternalEventSystem:
    """
    This implementation uses a factory pattern and allows individual objects to have
    their own event system, passed as a variable to each of their child objects.
    It is organized around an asyncio Queue and can execute synchronous and asynchronous handlers.
    """

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._subscriptions: Dict[str, List[Handler]] = {}
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._running = True  # Flag to control the running state of the event loop

    async def start(self) -> None:
        self._task = asyncio.create_task(self._run_event_loop())

    async def stop(self) -> None:
        self._running = False
        await (
            self._event_queue.join()
        )  # Wait for all items in the queue to be processed
        # Cancel any remaining tasks if needed
        if hasattr(self, "_task"):
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task

    async def get_subscriptions(self) -> List[Handler]:
        return self._subscriptions

    async def subscribe(self, event_type: str, fn: Handler) -> None:
        async with self._lock:
            if fn is not None:
                if event_type not in self._subscriptions:
                    self._subscriptions[event_type] = []
                self._subscriptions[event_type].append(fn)

    async def post(self, event_type: str, event_data: Dict[str, Any]) -> None:
        await self._event_queue.put((event_type, event_data))

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
