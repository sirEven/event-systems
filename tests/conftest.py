from typing import Any, Generator
import pytest
from event_systems.internal.event_system import InternalEventSystem

from event_systems.shared.event_system import SharedEventSystem


@pytest.fixture
def shared_event_system() -> Generator[type[SharedEventSystem], Any, Any]:
    yield SharedEventSystem
    SharedEventSystem._instance = None
    SharedEventSystem._subscribers = {}


@pytest.fixture
def internal_event_system() -> Generator[InternalEventSystem, Any, Any]:
    yield InternalEventSystem()
