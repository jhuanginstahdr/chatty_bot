class CustomEvent:
    def __init__(self, name, data):
        self.name = name
        self.data = data

class CustomEventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name, callback):
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)

    def unsubscribe(self, event_name, callback):
        if event_name in self.subscribers:
            self.subscribers[event_name].remove(callback)

    def publish(self, event : CustomEvent):
        event_name = event.name
        if event_name in self.subscribers:
            for callback in self.subscribers[event_name]:
                callback(event)

def EventDecorator(event_name):
    def decorator(func):
        func._event_name = event_name
        return func
    return decorator

def GetEventName(func):
    return getattr(func, '_event_name', None)