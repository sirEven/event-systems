from typing import Protocol, Callable


class EventSystem(Protocol):
    def subscribe(self, event_type: str, fn: Callable):
        pass

    def post(self):
        pass

    def gaga(self):
        pass
