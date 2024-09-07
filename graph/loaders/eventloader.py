import logging
logging.basicConfig(level=logging.INFO)


class EventLoader:
    def __init__(self, sports_catalog, sports_graph):
        self.sports_catalog = sports_catalog
        self.sports_graph = sports_graph

    def load_catalog(self):
        sports = self.sports_catalog.sports()
        for sport in sports:
            self._load_sport(sport)

    def _load_sport(self, sport):
        self.sports_graph.add_sport(sport.id, sport.name)
        for competition in sport.competitions:
            self._load_competition(sport.id, competition)

    def _load_competition(self, sport_id, competition):
        self.sports_graph.add_competition(sport_id, competition.id, competition.name)
        events = self.sports_catalog.events(competition.id)
        for event in events:
            self._load_event(competition.id, event)

    def _load_event(self, competition_id, event):
        self.sports_graph.add_event(competition_id, event.id, event.name, event.start_time, event.started)
        for market in event.markets:
            self._load_market(event.id, market)

    def _load_market(self, event_id, market):
        self.sports_graph.add_market(event_id, market.id, market.name)
