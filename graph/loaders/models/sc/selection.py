from graph.loaders.models.sc.price import Price


class Selection:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name').replace('|', '')
        self.price = Price.default() if data.get('price') is None else Price(data.get('price'))

