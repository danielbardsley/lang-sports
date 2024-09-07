from apis.models.sc.market import Market


class Event:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name').replace('|', '')
        self.start_time = data.get('startTime')
        self.started = data.get('started')
        self.markets = [Market(x) for x in data.get('markets')]

    def to_json(self):
        return {"name": self.name, "start_time": self.start_time}