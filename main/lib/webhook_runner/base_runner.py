import json


class BaseRunner():
    def __init__(self, payload: str):
        print('Initilize Base Runnner.')
        self.payload = json.loads(payload)

    def run(self):
        print('Run Base Runnner.')
        print('run')
