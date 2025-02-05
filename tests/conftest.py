from typing import Any, AsyncGenerator, List, Type
import pytest
import pytest_asyncio
from event_systems.instanced.asyncio.event_system import InternalEventSystem

from event_systems.singleton.asyncio.event_system import SharedEventSystem

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
