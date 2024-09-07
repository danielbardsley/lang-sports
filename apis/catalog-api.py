import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

from apis.models.sc.event import Event

load_dotenv()

app = Flask(__name__)
sc_base = os.getenv('SPORTS_CATALOG_BASE')
eventsByDate = '/events?isFuture=false&dateFrom={date_from}&state=open'  # &bypassLimits=true
sports_url = '/sports?eventsWithActiveMarkets=true'


@app.route("/sports")
def sports():
    response = requests.get(sc_base + sports_url)
    return [x.get('name') for x in response.json()]

@app.route("/sports/<sport>/competitions")
def competitions(sport):
    response = requests.get(sc_base + sports_url)
    result = next(item for item in response.json() if item["sportId"] == sport)
    return result


@app.route("/events")
def events():
    date_from = request.args.get('dateFrom')
    query_url = eventsByDate.format(date_from=date_from)

    response = requests.get(sc_base + query_url)
    return [Event(x).to_json() for x in response.json()]
