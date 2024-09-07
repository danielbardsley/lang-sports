from apis.models.sc.competition import Competition


class Sport:
    def __init__(self, data):
        self.id = data.get('sportId')
        self.name = data.get('name')
        self.competitions = [Competition(x) for x in data.get('competitions')]