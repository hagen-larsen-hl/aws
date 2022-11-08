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
    def __init__(self, queue_name):
        self.sqs = boto3.resource('sqs', region_name='us-east-1')
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
    
    def retrieve(self):
        messages = self.queue.receive_messages(MaxNumberOfMessages=1)
        for message in messages:
            factory = WidgetRequestFactory()
            request = factory.fromJson(message.body)
            logger.info("Deleting message from SQS")
            message.delete()
            return request

    def close(self):
        pass
