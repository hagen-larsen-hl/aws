import boto3
import logging
from widget.WidgetFactory import WidgetFactory
import logging

logger = logging.getLogger("consumer")

class S3Processor:
    def __init__(self, bucket_name):
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name

    def process(self, request):
        if request.type == 'create':
            logger.info("Processing create request with S3")
            self.processCreate(request)
            
    def processCreate(self, request):
        key = "widgets/" + (request.owner.replace(' ', '-') + '/' + request.widgetId).lower()
        widget = WidgetFactory().createWidget(request)
        self.client.put_object(Body=widget.toJson(), Bucket=self.bucket_name, Key=key)
        logger.info("Widget successfully created in S3")

    def close(self):
        self.client.close()


class DynamoDBProcessor:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb', region_name='us-east-1')
        self.table_name = table_name

    def process(self, request):
        if request.type == 'create':
            logger.info("Processing create request with DynamoDB")
            self.processCreate(request)
    
    def processCreate(self, request):
        widget = WidgetFactory().createWidget(request)
        self.client.put_item(TableName=self.table_name, Item=widget.toDynamoDBItem())
        logger.info("Widget successfully created in DynamoDB")
