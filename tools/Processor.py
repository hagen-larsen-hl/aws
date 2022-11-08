import boto3, logging
from widget.WidgetFactory import WidgetFactory

logger = logging.getLogger("consumer")

class Processor:
    def process(self):
        pass

class S3Processor(Processor):
    def __init__(self, bucket_name):
        self.client = boto3.client('s3', region_name='us-east-1')
        self.bucket_name = bucket_name

    def process(self, request):
        if request.type == 'create':
            logger.info("processing create request with S3")
            self.processCreate(request)
        elif request.type == 'update':
            logger.info("processing update request with S3")
            self.processUpdate(request)
        elif request.type == 'delete':
            logger.info("processing delete request with S3")
            self.processDelete(request)
            
    def processCreate(self, request):
        key = "widgets/" + (request.owner.replace(' ', '-') + '/' + request.widgetId).lower()
        widget = WidgetFactory().createWidget(request)
        self.client.put_object(Body=widget.toJson(), Bucket=self.bucket_name, Key=key)
        logger.info("widget " + key + " successfully created in S3 bucket " + self.bucket_name)

    def processUpdate(self, request):
        key = "widgets/" + (request.owner.replace(' ', '-') + '/' + request.widgetId).lower()
        try:
            widget = self.client.get_object(Bucket=self.bucket_name, Key=key)
            widget = widget['Body'].read().decode('utf-8')
            widget = WidgetFactory().updateWidget(widget, request.updates)
            self.client.put_object(Body=widget, Bucket=self.bucket_name, Key=key)
            logger.info("widget " + key + " successfully updated in bucket " + self.bucket_name)
        except:
            logger.warn("widget " + key + " not found in bucket " + self.bucket_name)

    def close(self):
        self.client.close()


class DynamoDBProcessor(Processor):
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
        logger.info("widget " + widget.id + " successfully created in DynamoDB")
