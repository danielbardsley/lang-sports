from apis.models.mdm.event import Event


class Sport:
    def __init__(self, data):
        self.id = data.get('sportId')
        self.events = [Event(x) for x in data.get('events')]
