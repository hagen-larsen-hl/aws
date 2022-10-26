import json
from widget.Request import CreateRequest

class WidgetRequestFactory:
    def fromJson(self, jsonStr):
        request = json.loads(jsonStr)
        request = self.create(request)
        return request

    def create(self, request):
        if request['type'] == 'create':
            if 'otherAttributes' in request:
                return CreateRequest(request['requestId'], request['widgetId'], request['owner'], request['label'], request['description'], request['otherAttributes'])
            else:
                return CreateRequest(request['requestId'], request['widgetId'], request['owner'], request['label'], request['description'])
    