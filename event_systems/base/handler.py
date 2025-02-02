from typing import Callable, Any, Coroutine

Handler = Callable[..., Any] | Coroutine[Any, Any, Any]
