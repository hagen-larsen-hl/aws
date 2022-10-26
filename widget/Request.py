import json
from widget.Attribute import Attribute

class Request:
    def __init__(self, requestId, widgetId, owner):
        self.requestId = requestId
        self.widgetId = widgetId
        self.owner = owner

    def toJson(self):
        return json.dumps(self.__dict__)

    def execute(self):
        pass

class CreateRequest(Request):
    def __init__(self, requestId, widgetId, owner, label, description, otherAttributes=[]):
        self.type = 'create'
        super().__init__(requestId, widgetId, owner)
        self.label = label
        self.description = description
        self.otherAttributes = []
        for attribute in otherAttributes:
            self.otherAttributes.append(Attribute(attribute['name'], attribute['value']))

    
class UpdateRequest(Request):
    pass
