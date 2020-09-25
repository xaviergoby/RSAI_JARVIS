




class Event:
    """
    Event is base class providing an interface for all subsequent
    (inherited) events, that will trigger further events in the
    trading infrastructure.
    """
    pass


class MouseStateEvent(Event):

    def __init__(self):
        self.type = "MOUSE_CLICKED"


class KeyboardStateEvent(Event):

    def __init__(self):
        self.type = "KEY_PRESSED"


class Paused(Event):

    def __init__(self):
        self.type = "PAUSED"


class Unpaused(Event):

    def __init__(self):
        self.type = "UNPAUSED"
















