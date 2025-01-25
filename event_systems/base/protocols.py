from typing import Optional, Protocol, Any, List, Dict, runtime_checkable

from event_systems.base.handler import Handler


@runtime_checkable
class Instanced(Protocol):
    async def start(self) -> None: ...

    async def stop(self) -> None: ...

    async def subscribe(self, event_name: str, fn: Handler) -> None: ...

    async def post(self, event_name: str, event_data: Dict[str, Any]) -> None: ...

    async def get_subscriptions(self) -> Dict[str, List[Handler]]: ...

    async def process_all_events(self) -> None: ...

    async def is_running(self) -> bool: ...


class Singleton(Protocol):
    @classmethod
    async def start(cls) -> None: ...

    @classmethod
    async def stop(cls) -> None: ...

    @classmethod
    async def subscribe(cls, event_name: str, fn: Handler) -> None: ...

    @classmethod
    async def post(cls, event_name: str, event_data: Dict[str, Any]) -> None: ...

    @classmethod
    async def get_subscriptions(cls) -> Dict[str, List[Handler]]: ...

    @classmethod
    async def process_all_events(cls) -> None: ...

    @classmethod
    async def is_running(cls) -> bool: ...

    @classmethod
    async def get_instance(cls) -> Optional[object]: ...
