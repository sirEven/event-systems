# Events System
- EventsSystem
    - A singleton based thread-safe event system, which components can use to subscribe and post to other components. 
    - install: `pip install events-system`
    - import: `import EventsSystem`
    - import `EventListener`: `from events_system.event_listener import EventListener`
    - subscribe: `EventsSystem.subscribe("event_type", function)`
    - post: `EventsSystem.post(event_type)`
    - example use: Create an abstract class as listener to a concrete component by subclassing `EventListener` and defining an abstract function along the lines of `setup_ConcreteComponent_listener`. In its abstract function, this component listener must call `super().setup_event_handlers()` to which the subscription dictionary `{"event_type":function}` is passed. Whatever other component needs to be informed about these events, can now implement that component listener and pass their subscription dictionary to the function.