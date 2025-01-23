import asyncio
from typing import Any, AsyncGenerator, List, Type
import pytest
import pytest_asyncio
from event_systems.internal.event_system import InternalEventSystem

from event_systems.shared.event_system import SharedEventSystem

import nest_asyncio  # type: ignore

# region - Testing Setup
# Prevent asyncio "runloop already running" error
nest_asyncio.apply()  # type: ignore


# NOTE: Marks all tests inside an integration directory as integration tests, which we exclude in CI.
def pytest_collection_modifyitems(
    config: pytest.Config,
    items: List[pytest.Item],
) -> None:
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)


@pytest_asyncio.fixture  # type: ignore
async def shared_event_system() -> AsyncGenerator[Type[SharedEventSystem], Any]:
    es = SharedEventSystem
    await es.start()
    yield es
    await es.stop()


@pytest_asyncio.fixture  # type: ignore
async def uninitialized_shared_event_system() -> AsyncGenerator[
    Type[SharedEventSystem],
    Any,
]:
    es = SharedEventSystem
    yield es
    await es.stop()


@pytest_asyncio.fixture  # type: ignore
async def internal_event_system() -> AsyncGenerator[InternalEventSystem, Any]:
    es = InternalEventSystem()
    await es.start()
    yield es
    await es.stop()


@pytest_asyncio.fixture  # type: ignore
async def internal_event_system_custom_loop() -> AsyncGenerator[
    InternalEventSystem,
    Any,
]:
    loop = asyncio.new_event_loop()
    es = InternalEventSystem(asyncio_loop=loop)
    await es.start()

    yield es

    # Stop the event system
    await es.stop()

    # Cancel all pending tasks in the custom loop
    for task in asyncio.all_tasks(loop):
        task.cancel()

    # Wait for all tasks to be cancelled
    loop.run_until_complete(
        asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)
    )

    # Close the loop
    loop.close()
