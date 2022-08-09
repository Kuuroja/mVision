class TestSubject():
    def __init__(self, testData = None, bData = None):
        self.testData = testData
        self.bData = bData
    def Reset(self):
        self.testData = None
        self.bData = None