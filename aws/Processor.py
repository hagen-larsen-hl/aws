import boto3
from widget.WidgetRequestFactory import WidgetRequestFactory
from widget.WidgetFactory import WidgetFactory

class S3Processor:
    def __init__(self, bucket_name):
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name

    def process(self, request):
        if request.type == 'create':
            self.processCreate(request)
    
    def processCreate(self, request):
        key = "widgets/" + (request.owner.replace(' ', '-') + '/' + request.widgetId).lower()
        widget = WidgetFactory().createWidget(request)
        self.client.put_object(Body=widget.toJson(), Bucket=self.bucket_name, Key=key)

    def processUpdate(self, request):
        pass

class DynamoDBProcessor:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb', region_name='us-east-1')
        self.table_name = table_name

    def process(self, request):
        if request.type == 'create':
            self.processCreate(request)
    
    def processCreate(self, request):
        widget = WidgetFactory().createWidget(request)
        self.client.put_item(TableName=self.table_name, Item=widget.toDynamoDBItem())
        pass

    def processUpdate(self, request):
        pass