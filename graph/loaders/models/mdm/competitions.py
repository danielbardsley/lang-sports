class Competitions:
    def __init__(self, data):
        self.competition_id = data.get('competitionId')
        self.collection_name = data.get('collectionDisplayName')
