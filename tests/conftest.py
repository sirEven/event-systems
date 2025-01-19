from typing import Any, AsyncGenerator, Generator, List
import pytest
import pytest_asyncio
from event_systems.internal.event_system import InternalEventSystem

from event_systems.shared.event_system import SharedEventSystem

import nest_asyncio

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


@pytest_asyncio.fixture
async def shared_event_system() -> AsyncGenerator[SharedEventSystem, Any]:
    es = SharedEventSystem
    await es.start()
    yield es
    await es.stop()


@pytest_asyncio.fixture
async def uninitialized_shared_event_system() -> AsyncGenerator[SharedEventSystem, Any]:
    es = SharedEventSystem
    yield es
    await es.stop()


@pytest_asyncio.fixture
async def internal_event_system() -> AsyncGenerator[InternalEventSystem, Any]:
    es = InternalEventSystem()
    await es.start()
    yield es
    await es.stop()
