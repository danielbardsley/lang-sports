from graph.loaders.models.mdm.competitions import Competitions
from graph.loaders.models.mdm.event import Event


class Sport:
    def __init__(self, data):
        self.id = data.get('sportId')
        self.events = [Event(x) for x in data.get('events', [])]
        self.competitions = [Competitions(x) for x in data.get('competitions', [])]
