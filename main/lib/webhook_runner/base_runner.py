import json


class BaseRunner():
    def __init__(self, payload: str):
        self.payload = json.loads(payload)

    def run(self):
        pass
