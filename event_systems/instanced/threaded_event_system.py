import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, Future, wait, FIRST_COMPLETED
from typing import Dict, List, Any, Set, Tuple
from queue import Queue

from event_systems.base.threading_protocols import InstancedThreaded
from event_systems.base.handler import Handler

from event_systems.common_expressions import (
    NO_SUBSCRIPTION_FOUND,
    subscription_failure,
    subscription_success,
)

# TODO: Write a few more complex tests, with different event systems more complex scenarios

class ThreadedInternalEventSystem(InstancedThreaded):
    def __init__(self):
        self._setup_initial_state()

    def _setup_initial_state(self) -> None:
        self._is_running = False
        self._lock = threading.Lock()
        self._subscriptions: Dict[str, List[Handler]] = {}
        self._event_queue: Queue[Tuple[str, Dict[str, Any]]] = Queue()

        self._futures_not_done: Set[Future[Any]] = set()
        self._futures_done: Set[Future[Any]] = set()


    # NOTE: The way we calculate worker count suggests, that starting the event system should be done after subscriptions have beend registered.
    def start(self) -> None:
        assert not self._is_running, "Event system is already running."
        self._is_running = True
        n = "event_processing_loop"
        worker_count = self._calculate_worker_count()
        self._executor = ThreadPoolExecutor(max_workers=worker_count)
        t = threading.Thread(
            name=n,
            target=self._execution_loop,
            args=[worker_count],
        )
        t.start()

    def stop(self) -> None:
        self._is_running = False
        self._event_queue.join()
        self._executor.shutdown(wait=True)
        self._setup_initial_state()

    def subscribe(self, event_name: str, fn: Handler) -> Dict[str, Any]:
        with self._lock:
            try:
                if event_name not in self._subscriptions:
                    self._subscriptions[event_name] = []
                self._subscriptions[event_name].append(fn)

                return subscription_success(event_name)
            except Exception as e:
                return subscription_failure(event_name, e)

    def post(self, event_name: str, event_data: Dict[str, Any]) -> None:
        assert self._is_running, "Event system is not running."
        if event_name not in self._subscriptions:
            raise ValueError(NO_SUBSCRIPTION_FOUND.format(event=event_name))
        self._event_queue.put((event_name, event_data))

    def get_subscriptions(self) -> Dict[str, List[Handler]]:
        return self._subscriptions

    def is_running(self) -> bool:
        return self._is_running

    def _calculate_worker_count(self) -> int:
        total_handlers = sum(len(handlers) for handlers in self._subscriptions.values())
        avg_handlers_per_event = max(
            1,
            total_handlers // len(self._subscriptions) if self._subscriptions else 1
        )

        return max(1, len(self._subscriptions) * avg_handlers_per_event)

    def _adjust_worker_count(self) -> None:
        new_worker_count = max(1, len(self._subscriptions))
        current_worker_count = self._executor._max_workers

        if new_worker_count != current_worker_count:
            # Creating a new executor with the new worker count
            new_executor = ThreadPoolExecutor(max_workers=new_worker_count)

            # Transfer tasks or wait for current tasks to finish before replacing the executor
            # Here's a simple approach:
            self._executor.shutdown(
                wait=True
            )  # Don't wait for completion, just stop accepting new tasks
            self._executor = new_executor

    
    def _run_handler(self, handler: Handler, event_data: Dict[str, Any]) -> None:
        if not callable(handler):
            raise TypeError("Handler is not callable.")
        if asyncio.iscoroutinefunction(handler):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(handler(event_data))
            finally:
                loop.close()
        else:
            # For synchronous functions, call them directly in the worker thread
            handler(event_data)


    def process_all_events(self) -> None:
    # Wait for all events in the queue to be processed
        self._event_queue.join()
        
        # Wait for any currently running handlers to complete
        self._wait_for_all_futures_to_complete()

    def _wait_for_all_futures_to_complete(self):
        while self._futures_not_done or self._futures_done:
            # Process futures that are not done
            if self._futures_not_done:
                done, self._futures_not_done = wait(self._futures_not_done, return_when=FIRST_COMPLETED)
                for future in done:
                    try:
                        future.result()  # This will raise an exception if one occurred
                    except Exception as e:
                        # Log the exception or handle it appropriately
                        print(f"Exception in future: {e}")
                    finally:
                        self._futures_done.add(future)
            
            # Clean up done futures
            self._cleanup_completed_futures()


    def _execution_loop(self, max_concurrent: int) -> None:
        prefix = "event_system_execution"

        with ThreadPoolExecutor(
            max_workers=max_concurrent,
            thread_name_prefix=prefix,
        ) as executor:
            while self._is_running:
                if self._event_queue.empty():
                    continue
                event_publication = self._event_queue.get()

                # Not done futures grows with every submission
                event_type, event_data = event_publication
                if event_type in self._subscriptions:
                    for handler in self._subscriptions[event_type]:
                        self._futures_not_done.add(executor.submit(self._run_handler, handler, event_data))
                
                self._event_queue.task_done()
                # Once it is bigger than max concurrent, separate all done futures out of it
                # and clean up to release memory
                if len(self._futures_not_done) >= max_concurrent:
                    done, self._futures_not_done = wait(
                        self._futures_not_done,
                        return_when=FIRST_COMPLETED,
                    )
                    self._futures_done.update(done)
                    self._cleanup_completed_futures()

    def _cleanup_completed_futures(self) -> None:
        completed_futures_to_remove: Set[Future[Any]] = set()

        for future in self._futures_done:
            if future.done():
                future.result()
                completed_futures_to_remove.add(future)

        # Remove completed futures from self._futures_done
        self._futures_done -= completed_futures_to_remove
