from typing import Protocol, Any, List, Dict, runtime_checkable

from event_systems.base.handler import Handler


# TODO: Have all public methods in here
# TODO: Find solution for Protocol not being able to be implemented via class methods and normal methods at the same time
class EventSystem(Protocol):
    async def subscribe(self, event_name: str, fn: Handler) -> None: ...

    async def post(self, event: str, event_data: Dict[str, Any]) -> None: ...

    async def get_subscriptions(self) -> Dict[str, List[Handler]]: ...


@runtime_checkable
class EventSystem(Protocol):
    async def subscribe(self, event_name: str, fn: Handler) -> None: ...

    async def post(self, event: str, event_data: Dict[str, Any]) -> None: ...

    async def get_subscriptions(self) -> Dict[str, List[Handler]]: ...
