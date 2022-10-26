from curses import BUTTON1_CLICKED
import boto3

class S3Retriever:
    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(bucket_name)
    
    def retrieve(self):
        objects = self.bucket.objects.all()
        print(objects)
