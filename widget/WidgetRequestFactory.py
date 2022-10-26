import json
from widget.Request import CreateRequest

class WidgetRequestFactory:
    def toJson(self, widgetRequest):
        return json.dumps(self.__dict__)

    def fromJson(self, jsonStr):
        request = json.loads(jsonStr)
        request = self.create(request)
        return request

    def create(self, request):
        if request['type'] == 'create':
            return CreateRequest(request['requestId'], request['widgetId'], request['owner'], request['label'], request['description'])
    