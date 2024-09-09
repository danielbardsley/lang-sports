import requests
import logging

from graph.loaders.models.mdm.sport import Sport


class MetaDataCatalog:
    def __init__(self, base_url):
        self.events_url = base_url + '/universes/wh-ny/events?sportIds={sportIds}&filterDisplayed=true'
        self.competitions_url = base_url + '/universes/wh-ny/competitions?sportIds={sportIds}'

    def events(self, sport_ids):
        logging.info('Getting promoted events for all sports from metadata catalog')
        sports = ','.join(sport_ids)
        response = requests.get(self.events_url.format(sportIds=sports))
        return [Sport(x) for x in response.json().get('data')]

    def competition_collections(self, sport_ids):
        logging.info('Getting all competition groups from metadata catalog')
        sports = ','.join(sport_ids)
        response = requests.get(self.competitions_url.format(sportIds=sports))
        return [Sport(x) for x in response.json().get('data')]



