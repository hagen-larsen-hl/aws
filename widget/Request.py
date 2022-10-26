import json

class Request:
    def toJson(self):
        return json.dumps(self.__dict__)

    def fromJson(self, jsonStr):
        self.__dict__ = json.loads(jsonStr)

class CreateRequest(Request):
    def __init__(self, widget, owner, label, description):
        self.widget = widget
        self.owner = owner
        self.label = label
        self.description = description

class UpdateRequest(Request):
    def __init__(self, widget, label, description):
        self.widget = widget
        self.label = label
        self.description = description
