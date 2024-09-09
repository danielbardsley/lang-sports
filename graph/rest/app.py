import os
from flask import Flask, request

from graph.rest.services.eventsservice import EventsService

NEO_URI = os.getenv('NEO4J_URI')
NEO_USER = os.getenv('NEO4J_USER')
NEO_PASS = os.getenv('NEO4J_PASS')
app = Flask(__name__)
events_service = EventsService(NEO_URI, auth=(NEO_USER, NEO_PASS))


@app.route("/sports")
def sports():
    return events_service.sports()


@app.route("/live")
def live():
    return events_service.live()


@app.route("/competitions/<competition_id>/events")
def competition_events(competition_id):
    return events_service.competition_events(competition_id)
