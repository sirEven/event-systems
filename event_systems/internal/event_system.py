import asyncio
from typing import Dict, List, Any, Tuple

from event_systems.base.protocols import Instanced
from event_systems.base.handler import Handler

from event_systems.common_strings import NO_SUBSCRIPTION_FOUND


class InternalEventSystem(Instanced):
    def __init__(self, asyncio_loop: asyncio.AbstractEventLoop | None = None) -> None:
        self._setup_initial_state(asyncio_loop)

    def _setup_initial_state(
        self, asyncio_loop: asyncio.AbstractEventLoop | None
    ) -> None:
        self._is_running = False
        self._lock = asyncio.Lock()
        self._asyncio_loop = (
            asyncio_loop if asyncio_loop is not None else asyncio.get_event_loop()
        )
        self._subscriptions: Dict[str, List[Handler]] = {}
        self._event_queue: asyncio.Queue[Tuple[str, Dict[str, Any]]] = asyncio.Queue()

    async def start(self) -> None:
        assert self._is_running is False, "Event system is already running."
        assert hasattr(self, "_asyncio_loop"), "Event system has no asyncio loop."
        assert self._asyncio_loop, "Asyncio loop is None."

        self._is_running = True
        self._task = self._asyncio_loop.create_task(self._run_event_loop())

    async def stop(self) -> None:
        self._is_running = False
        if hasattr(self, "_event_queue"):
            await self._event_queue.join()

        if hasattr(self, "_task"):
            self._task.cancel()
            try:
                # Run wait_for in the context of the custom loop but don't await the result
                self._asyncio_loop.run_until_complete(
                    asyncio.wait_for(self._task, timeout=1.0)
                )
            except asyncio.CancelledError:
                pass  # Task was successfully cancelled
            except asyncio.TimeoutError:
                pass

        # Clean up resources
        if hasattr(self, "_event_queue"):
            del self._event_queue
        if hasattr(self, "_task"):
            del self._task

        # Reset state
        self._setup_initial_state(self._asyncio_loop)

    async def subscribe(self, event_name: str, fn: Handler) -> None:
        async with self._lock:
            if event_name not in self._subscriptions:
                self._subscriptions[event_name] = []
            self._subscriptions[event_name].append(fn)

    async def post(self, event_name: str, event_data: Dict[str, Any]) -> None:
        if event_name not in self._subscriptions:
            raise ValueError(NO_SUBSCRIPTION_FOUND.format(event=event_name))

        await self._event_queue.put((event_name, event_data))

    async def get_subscriptions(self) -> Dict[str, List[Handler]]:
        return self._subscriptions

    async def is_running(self) -> bool:
        return self._is_running

    async def process_all_events(self) -> None:
        if not hasattr(self, "_event_queue"):
            return
        # Ensure we're in the correct loop context
        if asyncio.get_running_loop() != self._asyncio_loop:
            raise RuntimeError(
                "This method must be called from the same loop as the event system was initialized with."
            )

        # Since we're already in the correct loop context, we can simply await
        await self._event_queue.join()

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
                    await self._run_handler(handler, event_data)
            self._event_queue.task_done()

    async def _run_event_loop(self) -> None:
        while self._is_running:
            await self._process_events()
            await asyncio.sleep(0.1)  # Prevent busy waiting
