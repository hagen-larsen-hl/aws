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
            logger.info(request.type + " request " + request.requestId + " retrieved from S3")
            logger.info("deleting " + obj.key + " from S3 + " + self.bucket.name)
            obj.delete()
            return request

    def close(self):
        pass

class SQSRetriever(Retriever):
    def __init__(self, url):
        self.client = boto3.client('sqs', region_name='us-east-1')
        self.url = url
        self.cache = []
    
    def retrieve(self):
        if len(self.cache) == 0:
            messages = self.client.receive_message(QueueUrl=self.url, MaxNumberOfMessages=10, WaitTimeSeconds=10)
            if 'Messages' in messages:
                logger.info("caching " + str(len(messages['Messages'])) + " messages")
                for message in messages['Messages']:
                    self.cache.append(message)

        if len(self.cache) > 0:
            message = self.cache.pop(0)
            factory = WidgetRequestFactory()
            request = factory.fromJson(message['Body'])
            logger.info("deleting " + message['MessageId'] + " from SQS at " + self.url)
            self.client.delete_message(QueueUrl=self.url, ReceiptHandle=message['ReceiptHandle'])
            return request
        else:
            return None

    def close(self):
        pass
