from neo4j import GraphDatabase
import requests
import os
from dotenv import load_dotenv
import logging

from graph.loaders.eventloader import EventLoader
from graph.loaders.metadataloader import MetaDataLoader
from graph.metadatacatalog import MetaDataCatalog
from graph.sportscatalog import SportsCatalog
from graph.sportsgraph import SportsGraph

load_dotenv()
logging.basicConfig(level=logging.INFO)

SPORTS_CATALOG_BASE = os.getenv('SPORTS_CATALOG_BASE')
NEO_URI = os.getenv('NEO4J_URI')
NEO_USER = os.getenv('NEO4J_USER')
NEO_PASS = os.getenv('NEO4J_PASS')

METADATA_CATALOG_BASE = os.getenv('METADATA_CATALOG_BASE')


class DataLoader:
    def __init__(self):
        self.sports_catalog = SportsCatalog(SPORTS_CATALOG_BASE)
        self.metadata_catalog = MetaDataCatalog(METADATA_CATALOG_BASE)
        self.sports_graph = SportsGraph(NEO_URI,  auth=(NEO_USER, NEO_PASS))

        self.event_loader = EventLoader(self.sports_catalog, self.sports_graph)
        self.metadata_loader = MetaDataLoader(self.sports_catalog, self.metadata_catalog, self.sports_graph)

    def load(self):
        self.event_loader.load_catalog()
        self.metadata_loader.load_promoted_events_metadata()


if __name__ == '__main__':
    loader = DataLoader()
    loader.load()
