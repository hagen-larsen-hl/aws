import json
from widget.Attribute import Attribute

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
        self.otherAttributes = []
        for attribute in otherAttributes:
            self.otherAttributes.append(Attribute(attribute['name'], attribute['value']))

    
class UpdateRequest(Request):
    def __init__(self, request):
        self.type = 'update'
        super().__init__(request['requestId'], request['widgetId'], request['owner'])
        del request['type']
        del request['requestId']
        del request['widgetId']
        del request['owner']
        self.updates = request

    """
        Updates should grap the widget, update the values, and then put it back.
        Only update values that are passed in the request body. If not mentioned in the
        request body, then leave the value as is.

        Sample Update Request:
        {
            'type': 'update', 
            'requestId': 'c19094ea-7cc3-460b-92e1-e5eaf7aaf16a', 
            'widgetId': '6835d207-3ab9-4792-9795-eaea350b8912', 
            'owner': 'Mary Matthews', 
            'label': 'C', 
            'description': 'WYU', '
            otherAttributes': [
                {
                    'name': 'color', 
                    'value': 'yellow'
                }, 
                {
                    'name': 'size', 
                    'value': '119'
                }, 
                {
                    'name': 'size-unit', 
                    'value': 'cm'
                }, 
                {
                    'name': 'height-unit', 
                    'value': 'cm'
                }, 
                {
                    'name': 'length-unit', 
                    'value': 'cm'
                }, 
                {
                    'name': 'price', 
                    'value': '47.63'
                }, 
                {
                    'name': 'note', 
                    'value': 'TUVDDCAGJKGUCUGQQABOWSJPADYRCZPCVQEXNMPCMDFMFZFNCKOIJHNGUHHUXXNTQTXNJQGQDYWIGUBHLWOJRQJXJTNHAIFNC'
                }]}
        """
