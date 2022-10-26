import json

class Request:
    def __init__(self, requestId, widgetId, owner):
        self.requestId = requestId
        self.widgetId = widgetId
        self.owner = owner

    def execute(self):
        pass

class CreateRequest(Request):
    def __init__(self, requestId, widgetId, owner, label, description):
        self.type = 'create'
        super().__init__(requestId, widgetId, owner)
        self.label = label
        self.description = description

    
class UpdateRequest(Request):
    pass
