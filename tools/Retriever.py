import boto3, logging
from widget.WidgetRequestFactory import WidgetRequestFactory

logger = logging.getLogger("consumer")

class Retriever:
    def retrieve(self):
        pass

class S3Retriever(Retriever):
    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(bucket_name)
    
    def retrieve(self):
        objects = self.bucket.objects.limit(count=1)
        for obj in objects:
            factory = WidgetRequestFactory()
            request = factory.fromJson(obj.get()['Body'].read().decode('utf-8'))
            logger.info("Deleting object from S3")
            obj.delete()
            return request

    def close(self):
        pass

class SQSRetriever(Retriever):
    def __init__(self, url):
        self.client = boto3.client('sqs')
        self.url = url
        self.cache = []
    
    def retrieve(self):
        messages = self.client.receive_message(QueueUrl=self.url, MaxNumberOfMessages=10)
        self.cache.append(messages['Messages'])
        if len(self.cache) > 0:
            message = self.cache.pop(0)
            factory = WidgetRequestFactory()
            request = factory.fromJson(message['Body'])
            logger.info("Deleting message from SQS")
            self.client.delete_message(QueueUrl=self.url, ReceiptHandle=message['ReceiptHandle'])
            return request

    def close(self):
        pass
