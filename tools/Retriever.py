import boto3
from widget.WidgetRequestFactory import WidgetRequestFactory
import logging

logger = logging.getLogger("consumer")

class S3Retriever:
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