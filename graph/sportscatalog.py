import requests
import logging

from apis.models.sc.event import Event
from apis.models.sc.sport import Sport


class SportsCatalog:
    def __init__(self, base_url):
        self.events_by_competition_url = base_url + ('/events?active=true&state=open&includeMarkets=true&competitionId'
                                                     '={competition_id}&bypassLimits=true&isFuture=false')
        # &bypassLimits=true
        self.sports_url = base_url + '/sports?eventsWithActiveMarkets=true'

    def sports(self):
        logging.info('Getting all sports')
        response = requests.get(self.sports_url)
        return [Sport(x) for x in response.json()]

    def events(self, competition_id):
        logging.info('Getting all events for competition {}'.format(competition_id))
        query_url = self.events_by_competition_url.format(competition_id=competition_id)
        response = requests.get(query_url)
        return [Event(x) for x in response.json()]
