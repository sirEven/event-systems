from typing import Any, Dict, List, Protocol
from event_systems.base.handler import Handler

# TODO: Unsubscribe
class InstancedThreaded(Protocol):
    def start(self) -> None: ...

    def stop(self) -> None: ...

    def subscribe(self, event_name: str, fn: Handler) -> Dict[str, Any]: ...

    def post(self, event_name: str, event_data: Dict[str, Any]) -> None: ...

    def get_subscriptions(self) -> Dict[str, List[Handler]]: ...

    def process_all_events(self) -> None: ...

    def is_running(self) -> bool: ...
