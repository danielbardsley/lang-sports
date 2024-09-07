class Event:
    def __init__(self, data):
        self.id = data.get('eventId')
        self.competition_id = data.get('competitionId')
        self.promoted = data.get('promoted')
        self.marquee = data.get('marquee')
        self.display_from = data.get('displayFrom')
        self.display_to = data.get('displayTo')
        self.markets = data.get('markets')
        self.display_order = data.get('displayOrder')
