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
    config: pytest.Config, items: List[pytest.Item]
) -> None:
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)


@pytest.fixture
def shared_event_system() -> Generator[type[SharedEventSystem], Any, Any]:
    yield SharedEventSystem()
    SharedEventSystem._instance = None
    SharedEventSystem._subscriptions = {}


@pytest_asyncio.fixture
async def internal_event_system() -> AsyncGenerator[InternalEventSystem, Any]:
    es = InternalEventSystem()
    await es.start()
    yield es
    await es.stop()
