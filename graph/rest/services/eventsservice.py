from graph.sportsgraph import SportsGraph


class EventsService:
    def __init__(self, uri, auth):
        self.graph = SportsGraph(uri, auth)

    def live(self):
        return self.graph.get_live_events()

    def sports(self):
        return self.graph.get_sports()

    def competition_events(self, competition_id):
        return self.graph.get_competition_events(competition_id)
