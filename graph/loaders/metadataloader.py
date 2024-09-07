import logging
logging.basicConfig(level=logging.INFO)


class MetaDataLoader:
    def __init__(self, sports_catalog, metadata_catalog, sports_graph):
        self.sports_catalog = sports_catalog
        self.metadata_catalog = metadata_catalog
        self.sports_graph = sports_graph

    def load_promoted_events_metadata(self):
        sports = [x.id for x in self.sports_catalog.sports()]
        sports = self.metadata_catalog.events(sports)
        for sport in sports:
            for event in sport.events:
                self._load_event_meta(event)

    def _load_event_meta(self, event):
        self.sports_graph.add_event_meta(event.competition_id, event.id)


