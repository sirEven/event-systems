# TODO: Remove this crap
# from typing import Any, Type, Union

# from tests.helpers.dummy_emitter_listener import DummyEmitterListener
# from event_systems.base.event_system import EventSystem
# from event_systems.base.handler import Handler


# class DummySubscriber_zero(DummyEmitterListener):
#     def __init__(self, event_system: EventSystem):
#         self.setup_DummyEmitter_event_handlers(event_system)

#     def setup_DummyEmitter_event_handlers(
#         self,
#         event_system: Union[EventSystem, Type[EventSystem]],
#         event_emitted_handler: Handler = None,
#         another_event_emitted_handler: Handler = None,
#     ) -> None:
#         return super().setup_DummyEmitter_event_handlers(
#             event_system,
#             event_emitted_handler,
#             another_event_emitted_handler,
#         )


# class DummySubscriber_one(DummyEmitterListener):
#     def __init__(self, event_system: EventSystem):
#         self.setup_DummyEmitter_event_handlers(
#             event_system,
#             self.handle_DummyEmitter_event_emitted_event,
#         )

#     def handle_DummyEmitter_event_emitted_event(self, event_data: Any = None) -> None:
#         text = "- event handeled"
#         print_post_output(self, text, event_data)

#     def setup_DummyEmitter_event_handlers(
#         self,
#         event_system: Union[EventSystem, Type[EventSystem]],
#         event_emitted_handler: Handler = None,
#         another_event_emitted_handler: Handler = None,
#     ) -> None:
#         return super().setup_DummyEmitter_event_handlers(
#             event_system,
#             event_emitted_handler,
#             another_event_emitted_handler,
#         )


# class DummySubscriber_two(DummyEmitterListener):
#     def __init__(self, event_system: EventSystem):
#         self.setup_DummyEmitter_event_handlers(
#             event_system,
#             self.handle_DummyEmitter_event_emitted_event,
#             self.handle_DummyEmitter_another_event_emitted_event,
#         )

#     def handle_DummyEmitter_event_emitted_event(self, event_data: Any = None) -> None:
#         text = "- event handeled"
#         print_post_output(self, text, event_data)

#     def handle_DummyEmitter_another_event_emitted_event(
#         self,
#         event_data: Any = None,
#     ) -> None:
#         text = "- another event handeled"
#         print_post_output(self, text, event_data)

#     def setup_DummyEmitter_event_handlers(
#         self,
#         event_system: Union[EventSystem, Type[EventSystem]],
#         event_emitted_handler: Handler = None,
#         another_event_emitted_handler: Handler = None,
#     ) -> None:
#         return super().setup_DummyEmitter_event_handlers(
#             event_system,
#             event_emitted_handler,
#             another_event_emitted_handler,
#         )


# def print_post_output(
#     emitter: Union[DummySubscriber_one, DummySubscriber_two], text: str, event_data: Any
# ) -> None:
#     none_text = f"{type(emitter).__name__} {text}"
#     if not event_data:
#         print(none_text)
#     else:
#         print(f"{none_text} {event_data}")
