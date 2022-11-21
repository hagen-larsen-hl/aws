import json, boto3

class SQSProducer:
    def __init__(self):
        self.client = boto3.client('sqs', region_name='us-east-1')
        self.queue_url = "https://sqs.us-east-1.amazonaws.com/713236084914/cs5260-requests"
        
    def sendMessage(self, event):
        try:
            response = self.client.send_message(QueueUrl=self.queue_url, MessageBody=json.dumps(event))
            return {
                'statusCode': 200,
                'response': json.dumps(response)
            }
        except Exception as e:
            return {
                'statusCode': 400,
                'response': json.dumps(str(e))
            }
        

def lambda_handler(event, context):
    producer = SQSProducer()
    return producer.sendMessage(event)

