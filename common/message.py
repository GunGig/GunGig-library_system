class Message:

    ERROR = -1
    OK = 1

    def __init__(self):
        self.type = 0
        self.text = None

    def set_error(self, text):
        self.type = -1
        self.text = text

    def set_ok(self, text):
        self.type = 1
        self.text = text
