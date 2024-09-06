class Competition:
    def __init__(self, data):
        self.id = data.get('competitionId')
        self.name = data.get('name')