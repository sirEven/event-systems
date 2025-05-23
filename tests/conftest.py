from typing import Any, AsyncGenerator, Generator, List, Type
import pytest
import pytest_asyncio
from event_systems.instanced.async_event_system import AsyncEventSystem

from event_systems.instanced.threaded_event_system import ThreadedEventSystem
from event_systems.singleton.async_event_system import AsyncSingletonEventSystem

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
async def async_singleton_event_system() -> AsyncGenerator[
    Type[AsyncSingletonEventSystem], Any
]:
    es = AsyncSingletonEventSystem
    await es.start()
    yield es
    await es.stop()


@pytest_asyncio.fixture  # type: ignore
async def uninitialized_async_singleton_event_system() -> AsyncGenerator[
    Type[AsyncSingletonEventSystem],
    Any,
]:
    es = AsyncSingletonEventSystem
    yield es
    await es.stop()


@pytest_asyncio.fixture  # type: ignore
async def async_event_system() -> AsyncGenerator[AsyncEventSystem, Any]:
    es = AsyncEventSystem()
    await es.start()
    yield es
    await es.stop()


@pytest.fixture
def threaded_event_system() -> Generator[ThreadedEventSystem, None, None]:
    es = ThreadedEventSystem()
    es.start()
    yield es
    es.stop()
