import logging
from widget.Widget import Widget


logger = logging.getLogger("consumer")

class WidgetFactory:
    def createWidget(self, createRequest):
        widget = Widget(id=createRequest.widgetId, owner=createRequest.owner, label=createRequest.label, description=createRequest.description, attributes=createRequest.otherAttributes)
        return widget

    def updateWidget(self, widgetBody, updates):
        for update in updates:
            if update == 'label':
                widgetBody['label'] = updates[update]
            elif update == 'description':
                widgetBody['description'] = updates[update]
            else:
                if update in widgetBody['otherAttributes']:
                    widgetBody['otherAttributes'][update] = updates[update]
        widget = Widget(id=widgetBody['id'], owner=widgetBody['owner'], label=widgetBody['label'], description=widgetBody['description'], attributes=widgetBody['otherAttributes'])

        return widget

    def parseDataFromDynamoDBItem(self, item):
        data = {
            'id': item['id']['S'],
            'owner': item['owner']['S'],
            'label': item['label']['S'],
            'description': item['description']['S'],
            'otherAttributes': {}
        }
        for key in item:
            if key != 'id' and key != 'owner' and key != 'label' and key != 'description':
                data['otherAttributes'][key] = item[key]['S']
            
        return data
