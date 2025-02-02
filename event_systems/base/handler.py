from typing import Any, Callable, Coroutine

Handler = Callable[[Any], Any] | Coroutine[Any, Any, Any]
