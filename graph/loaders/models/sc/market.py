from graph.loaders.models.sc.selection import Selection


class Market:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name').replace('|', '')
        self.selections = [Selection(x) for x in data.get('selections', [])]
