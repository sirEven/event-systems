# Events System
- EventsSystem
    - A singleton based thread-safe event system, which components can use to subscribe and post to other components. 
    - install: `pip install events-system`
    - import: `import EventsSystem`
    - import `EventListener`: `from events_system.event_listener import EventListener`
    - subscribe: `EventsSystem.subscribe("event_type", function)`
    - post: `EventsSystem.post(event_type)`
    - example usage: Create an abstract class as listener to a component by subclassing `EventListener` and defining an abstract function along the lines of `setup_Component_listener` - for example, if you have a `Calculator` component and want to be notified about finished calculations, create an abstract class `CalculatorListener(EventListener, ABC)`. In its abstract function (for example `setup_Calculator_event_handlers`), it must call `super().setup_event_handlers()` to which a subscription dictionary `{"event_type":function}` is passed - for example `{"Calculator_calculation_finished_event": calculation_finished_handler}`. Whatever other component needs to be informed about these events, can now implement that component listener and pass their desired event handlers to their concrete implementation of the setup function. 
    The only thing missing now is calling `EventsSystem.post("Calculator_calculation_finished_event", event_data)` at the desired place in your `Calculator`component, where it finishes its calculation.
    TL/DR: Check out the test cases and their illustrating helper classes.