from typing import Protocol, Any, List, Dict, runtime_checkable

from event_systems.base.handler import Handler


# TODO: Update heavily:  Pull in all new public methods from internal and shared event systems
@runtime_checkable
class EventSystem(Protocol):
    async def subscribe(self, event: str, fn: Handler) -> None: ...

    async def post(self, event: str, event_data: Dict[str, Any]) -> None: ...

    async def get_subscribers(self) -> Dict[str, List[Handler]]: ...
