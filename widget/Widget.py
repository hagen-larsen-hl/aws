import json
from widget.CustomJSONEncoder import CustomJSONEncoder

class Widget:
    def __init__(self, id, owner, label, description, attributes):
        self.id = id
        self.owner = owner
        self.label = label
        self.description = description
        self.otherAttributes = attributes

    def toJson(self):
        res = json.dumps(self.__dict__, cls=CustomJSONEncoder)
        print(json.loads(res))
        return res