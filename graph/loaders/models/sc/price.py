class Price:
    def __init__(self, data):
        self.a = data.get('a')
        self.d = data.get('d')
        self.f = data.get('f')

    @staticmethod
    def default():
        return Price({'a': 0, 'd': 0, 'f': 0})
