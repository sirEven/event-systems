# Events System
- EventsSystem
    - A singleton based thread-safe event system, which components can use to subscribe and post to other components. 
    - install: `pip install events-systems`
    - import `EventListener`: `from events_system.event_listener import EventListener`
    - subscribe: `EventsSystem.subscribe("event_type", function)`
    - post: `EventsSystem.post(event_type)`