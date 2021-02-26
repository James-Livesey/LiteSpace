class Response:
    def __init__(self, status, data, extension = "txt"):
        self.status = status
        self.data = data
        self.extension = extension