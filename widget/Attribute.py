import json
from widget.CustomJSONEncoder import CustomJSONEncoder

class Attribute:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def toJson(self):
        return json.dumps(self.__dict__, cls=CustomJSONEncoder)