import requests

from apis.models.mdm.sport import Sport


class MetaDataCatalog:
    def __init__(self, base_url):
        self.events_url = base_url + '/universes/wh-ny/events?sportIds={sportIds}&filterDisplayed=true'

    def events(self, sport_ids):
        sports = ','.join(sport_ids)
        response = requests.get(self.events_url.format(sportIds=sports))
        return [Sport(x) for x in response.json().get('data')]

