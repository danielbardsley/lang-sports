import requests

from apis.models.event import Event
from apis.models.sport import Sport


class SportsCatalog:
    def __init__(self, base_url):
        self.events_by_competition_url = base_url + '/events?active=true&state=open&includeMarkets=false&competitionId={competition_id}&bypassLimits=true&isFuture=false'  # &bypassLimits=true
        self.sports_url = base_url + '/sports?eventsWithActiveMarkets=true'

    def sports(self):
        response = requests.get(self.sports_url)
        return [Sport(x) for x in response.json()]

    def competitions(self, sport):
        response = requests.get(self.sports_url)
        result = next(item for item in response.json() if item["sportId"] == sport)
        return result

    def events(self, competition_id):
        query_url = self.events_by_competition_url.format(competition_id=competition_id)
        response = requests.get(query_url)
        return [Event(x) for x in response.json()]
