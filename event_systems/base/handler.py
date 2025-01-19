from typing import Any, Callable

# TODO: Might we enforce here that handlers can't be None?
Handler = Callable[[Any], Any]
