import boto3

class S3Processor:
    def __init__(self, bucket_name):
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name
    
    def processCreate(self, request):
        pass

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