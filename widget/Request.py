import json

class Request:
    def __init__(self, requestId, widgetId, owner):
        self.requestId = requestId
        self.widgetId = widgetId
        self.owner = owner

    def toJson(self):
        return json.dumps(self.__dict__)


class CreateRequest(Request):
    def __init__(self, requestId, widgetId, owner, label, description, otherAttributes=[]):
        self.type = 'create'
        super().__init__(requestId, widgetId, owner)
        self.label = label
        self.description = description
        self.otherAttributes = {}
        for attribute in otherAttributes:
            self.otherAttributes[attribute['name']] = attribute['value']

    
class UpdateRequest(Request):
    def __init__(self, request):
        self.type = 'update'
        super().__init__(request['requestId'], request['widgetId'], request['owner'])
        del request['type']
        del request['requestId']
        del request['widgetId']
        del request['owner']
        updates = {}
        for attribute in request:
            if attribute != "otherAttributes":
                updates[attribute] = request[attribute]
        
        if "otherAttributes" in request:
            for attribute in request["otherAttributes"]:
                updates[attribute['name']] = attribute['value']

        self.updates = updates


class DeleteRequest(Request):
    def __init__(self, requestId, widgetId, owner):
        self.type = 'delete'
        super().__init__(requestId, widgetId, owner)        
