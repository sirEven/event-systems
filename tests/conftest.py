from typing import Any, AsyncGenerator, Generator, List, Type
import pytest
import pytest_asyncio
from event_systems.instanced.async_event_system import AsyncInternalEventSystem

from event_systems.instanced.threaded_event_system import ThreadedInternalEventSystem
from event_systems.singleton.async_event_system import AsyncSharedEventSystem

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
async def async_shared_event_system() -> AsyncGenerator[Type[AsyncSharedEventSystem], Any]:
    es = AsyncSharedEventSystem
    await es.start()
    yield es
    await es.stop()


@pytest_asyncio.fixture  # type: ignore
async def uninitialized_async_shared_event_system() -> AsyncGenerator[
    Type[AsyncSharedEventSystem],
    Any,
]:
    es = AsyncSharedEventSystem
    yield es
    await es.stop()


@pytest_asyncio.fixture  # type: ignore
async def async_internal_event_system() -> AsyncGenerator[AsyncInternalEventSystem, Any]:
    es = AsyncInternalEventSystem()
    await es.start()
    yield es
    await es.stop()

@pytest.fixture
def threaded_internal_event_system() -> Generator[ThreadedInternalEventSystem, None, None]:
    es = ThreadedInternalEventSystem()
    es.start()
    yield es
    es.stop()