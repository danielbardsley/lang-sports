from neo4j import GraphDatabase
import requests
import os
from dotenv import load_dotenv
import logging

from graph.sportscatalog import SportsCatalog
from graph.sportsgraph import SportsGraph

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

SPORTS_CATALOG_BASE = os.getenv('SPORTS_CATALOG_BASE')
NEO_URI = os.getenv('NEO4J_URI')
NEO_USER = os.getenv('NEO4J_USER')
NEO_PASS = os.getenv('NEO4J_PASS')


class DataLoader:
    def __init__(self):
        self.sports_catalog = SportsCatalog(SPORTS_CATALOG_BASE)
        self.sports_graph = SportsGraph(NEO_URI,  auth=(NEO_USER, NEO_PASS))

    def load(self):
        sports = self.sports_catalog.sports()
        for sport in sports:
            self.sports_graph.add_sport(sport.id, sport.name)
            for competition in sport.competitions:
                self.sports_graph.add_competition(sport.id, competition.id, competition.name)
                for event in self.sports_catalog.events(competition.id):
                    self.sports_graph.add_event(competition.id, event.id, event.name, event.start_time)


if __name__ == '__main__':
    loader = DataLoader()
    loader.load()

