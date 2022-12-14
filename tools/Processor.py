import boto3, logging, json
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
            widgetData = widget['Body'].read().decode('utf-8')
            widgetData = json.loads(widgetData)
            widget = WidgetFactory().updateWidget(widgetData, request.updates)
            self.client.put_object(Body=widget.toJson(), Bucket=self.bucket_name, Key=key)
            logger.info("widget " + key + " successfully updated in bucket " + self.bucket_name)
        except Exception as e:
            logger.warn("widget " + key + " not found in bucket " + self.bucket_name)

    def processDelete(self, request):
        key = "widgets/" + (request.owner.replace(' ', '-') + '/' + request.widgetId).lower()
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info("widget " + key + " successfully deleted from bucket " + self.bucket_name)
        except Exception as e:
            logger.warn("widget " + key + " not found in bucket " + self.bucket_name)

    def close(self):
        self.client.close()


class DynamoDBProcessor(Processor):
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb', region_name='us-east-1')
        self.table_name = table_name

    def process(self, request):
        if request.type == 'create':
            logger.info("processing create request with DynamoDB")
            self.processCreate(request)
        elif request.type == 'update':
            logger.info("processing update request with DynamoDB")
            self.processUpdate(request)
        elif request.type == 'delete':
            logger.info("processing delete request with DynamoDB")
            self.processDelete(request)
    
    def processCreate(self, request):
        widget = WidgetFactory().createWidget(request)
        self.client.put_item(TableName=self.table_name, Item=widget.toDynamoDBItem())
        logger.info("widget " + widget.id + " successfully created in DynamoDB")

    def processUpdate(self, request):
        try:
            widget = self.client.get_item(TableName=self.table_name, Key={'id': {'S': request.widgetId}})
            widget = WidgetFactory().parseDataFromDynamoDBItem(widget['Item'])
            widget = WidgetFactory().updateWidget(widget, request.updates)
            self.client.put_item(TableName=self.table_name, Item=widget.toDynamoDBItem())
            logger.info("widget " + request.widgetId + " successfully updated in DynamoDB")
        except:
            logger.warn("widget " + request.widgetId + " not found in DynamoDB")

    def processDelete(self, request):
        try:
            self.client.delete_item(TableName=self.table_name, Key={'id': {'S': request.widgetId}})
            logger.info("widget " + request.widgetId + " successfully deleted from DynamoDB")
        except Exception as e:
            raise e
            logger.warn("widget " + request.widgetId + " not found in DynamoDB")

    def close(self):
        self.client.close()
