import boto3
from widget.WidgetRequestFactory import WidgetRequestFactory

class S3Processor:
    def __init__(self, bucket_name):
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name

    def process(self, rawRequest):
        factory = WidgetRequestFactory()
        request = factory.fromJson(rawRequest.get()['Body'].read().decode('utf-8'))
        if request.type == 'create':
            self.processCreate(request)
    
    def processCreate(self, request):
        print("Ready to process")

    def processUpdate(self, request):
        pass

class DynamoDBProcessor:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb')
        self.table_name = table_name
    
    def processCreate(self, request):
        pass

    def processUpdate(self, request):
        pass