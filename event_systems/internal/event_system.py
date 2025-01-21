import asyncio
import contextlib
from typing import Dict, List, Any, Tuple

from event_systems.base.event_system import EventSystem
from event_systems.base.handler import Handler

from event_systems.common_strings import NO_SUBSCRIPTION_FOUND


# TODO: Move code in init to an initialize method, that we also call in start.
class InternalEventSystem(EventSystem):
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._subscriptions: Dict[str, List[Handler]] = {}
        self._event_queue: asyncio.Queue[Tuple[str, Dict[str, Any]]] = asyncio.Queue()

    async def start(self) -> None:
        self._is_running = True
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

        self._is_running = False

    async def subscribe(self, event_name: str, fn: Handler) -> None:
        async with self._lock:
            # if fn is None: # TODO: Check if this is ok
            #     raise ValueError(HANDLER_CANT_BE_NONE)
            if event_name not in self._subscriptions:
                self._subscriptions[event_name] = []
            self._subscriptions[event_name].append(fn)

    async def post(self, event_name: str, event_data: Dict[str, Any]) -> None:
        if event_name not in self._subscriptions:
            raise ValueError(NO_SUBSCRIPTION_FOUND.format(event=event_name))

        await self._event_queue.put((event_name, event_data))

    async def get_subscriptions(self) -> Dict[str, List[Handler]]:
        return self._subscriptions

    @property
    def is_running(self) -> bool:
        return self._is_running

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
                    # if handler: # TODO: Check if this is ok
                    await self._run_handler(handler, event_data)
            self._event_queue.task_done()

    async def _run_event_loop(self) -> None:
        while self._is_running:
            await self._process_events()
            await asyncio.sleep(0.1)  # Prevent busy waiting
