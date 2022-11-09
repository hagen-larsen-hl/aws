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
        
        """
        {
            'height-unit': {'S': 'cm'}, 
            'quantity': {'S': '932'}, 
            'rating': {'S': '2.8458407'}, 
            'width': {'S': '346'}, 
            'label': {'S': 'YYQGJIAXU'}, 
            'length-unit': {'S': 'cm'}, 
            'owner': {'S': 'Henry Hops'}, 
            'size-unit': {'S': 'cm'}, 
            'description': {'S': 'MNPCOHGEDHWDAKTYUCGXUBSMMCXVIRERFHURAZRESJOSLPICGMVOPJL'}, 
            'id': {'S': 'db132190-a390-47bf-bf01-a17d41cf3b0c'}, 
            'color': {'S': 'orange'}}, 
            'ResponseMetadata': {
                'RequestId': 'IB5E03EURR89P7002KTMRI59EBVV4KQNSO5AEMVJF66Q9ASUAAJG', 
                'HTTPStatusCode': 200, 
                'HTTPHeaders': {
                    'server': 'Server', 
                    'date': 'Wed, 09 Nov 2022 03:13:41 GMT', 
                    'content-type': 'application/x-amz-json-1.0', 
                    'content-length': '357', 
                    'connection': 'keep-alive', 
                    'x-amzn-requestid': 'IB5E03EURR89P7002KTMRI59EBVV4KQNSO5AEMVJF66Q9ASUAAJG', 
                    'x-amz-crc32': '3505522127'
                }, 
                'RetryAttempts': 0
            }
        }
        """