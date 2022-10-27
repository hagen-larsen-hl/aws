import boto3, consumer, json, unittest
from tools import Retriever, Processor, Poller
from widget import WidgetRequestFactory, WidgetFactory, Widget

class TestWidgetRequestFactory(unittest.TestCase):
    def setUp(self):
        self.factory = WidgetRequestFactory.WidgetRequestFactory()

    def testWidgetRequestFactory(self):
        requestJson = json.dumps({
            "type": "create",
            "requestId": "1234",
            "widgetId": "5678",
            "owner": "John Doe",
            "label": "Widget 1",
            "description": "This is a widget",
            "otherAttributes": [{
                "name": "color",
                "value": "red"
            }]
        })
        request = self.factory.fromJson(requestJson)
        self.assertEqual(request.type, "create")
        self.assertEqual(request.requestId, "1234")
        self.assertEqual(request.widgetId, "5678")
        self.assertEqual(request.owner, "John Doe")
        self.assertEqual(request.label, "Widget 1")
        self.assertEqual(request.description, "This is a widget")

class TestWidgetFactory(unittest.TestCase):
    def setUp(self):
        self.factory = WidgetFactory.WidgetFactory()

    def testWidgetFactory(self):
        requestJson = json.dumps({
            "type": "create",
            "requestId": "1234",
            "widgetId": "5678",
            "owner": "John Doe",
            "label": "Widget 1",
            "description": "This is a widget",
            "otherAttributes": [{
                "name": "color",
                "value": "red"
            }]
        })
        request = WidgetRequestFactory.WidgetRequestFactory().fromJson(requestJson)
        widget = self.factory.createWidget(request)
        self.assertEqual(widget.id, "5678")
        self.assertEqual(widget.owner, "John Doe")
        self.assertEqual(widget.label, "Widget 1")
        self.assertEqual(widget.description, "This is a widget")
        self.assertEqual(widget.otherAttributes[0].name, "color")
        self.assertEqual(widget.otherAttributes[0].value, "red")

class TestS3Processor(unittest.TestCase):
    def setUp(self):
        self.requestFactory = WidgetRequestFactory.WidgetRequestFactory()
        self.widgetFactory = WidgetFactory.WidgetFactory()
        self.client = boto3.client('s3')
        self.bucket_name = 'usu-cs5260-hagen-test'
        requestJson = json.dumps({
            "type": "create",
            "requestId": "1234",
            "widgetId": "5678",
            "owner": "John Doe",
            "label": "Widget 1",
            "description": "This is a widget",
            "otherAttributes": [{
                "name": "color",
                "value": "red"
            }]
        })
        self.request = self.requestFactory.fromJson(requestJson)
        self.retriever = Retriever.S3Retriever(self.bucket_name)
        self.bucket = boto3.resource('s3').Bucket(self.bucket_name)

    def testProcessor(self):
        processor = Processor.S3Processor(self.bucket_name)
        processor.process(self.request)
        widgetObj = self.bucket.objects.limit(count=1)
        for obj in widgetObj:
            widgetDict = json.loads(obj.get()['Body'].read().decode('utf-8'))
            self.assertEqual(widgetDict['id'], "5678")
            self.assertEqual(widgetDict['owner'], "John Doe")
            self.assertEqual(widgetDict['label'], "Widget 1")
            
class TestDynamoProcessor(unittest.TestCase):
    def setUp(self):
        self.requestFactory = WidgetRequestFactory.WidgetRequestFactory()
        self.widgetFactory = WidgetFactory.WidgetFactory()
        self.client = boto3.client('dynamodb', 'us-east-1')
        self.table_name = 'widgets'
        self.processor = Processor.DynamoDBProcessor(self.table_name)
        request = json.dumps({
            "type": "create",
            "requestId": "1234",
            "widgetId": "5678",
            "owner": "John Doe",
            "label": "Widget 1",
            "description": "This is a widget",
            "otherAttributes": [{
                "name": "color",
                "value": "red"
            }]
        })
        self.request = self.requestFactory.fromJson(request)

    def testProcessor(self):
        self.processor.process(self.request)
        item = self.client.get_item(
            TableName=self.table_name,
            Key={
                'id': {
                    'S': '5678'
                }
            }
        )
        self.assertEqual(item['Item']['id']['S'], "5678")
        self.assertEqual(item['Item']['owner']['S'], "John Doe")
        self.assertEqual(item['Item']['label']['S'], "Widget 1")
        self.assertEqual(item['Item']['description']['S'], "This is a widget")
        self.assertEqual(item['Item']['color']['S'], "red")

class TestRetriever(unittest.TestCase):

    def setUp(self):
        self.requestFactory = WidgetRequestFactory.WidgetRequestFactory()
        self.widgetFactory = WidgetFactory.WidgetFactory()
        self.client = boto3.client('s3')
        self.bucket_name = 'usu-cs5260-hagen-test'
        requestJson = json.dumps({
            "type": "create",
            "requestId": "1234",
            "widgetId": "5678",
            "owner": "John Doe",
            "label": "Widget 1",
            "description": "This is a widget",
            "otherAttributes": [{
                "name": "color",
                "value": "red"
            }]
        })
        self.client.put_object(Bucket=self.bucket_name, Key='test.json', Body=requestJson)
        self.retriever = Retriever.S3Retriever(self.bucket_name)

    def testRetriever(self):
        request = self.retriever.retrieve()
        self.assertEqual(request.type, "create")
        self.assertEqual(request.requestId, "1234")
        self.assertEqual(request.widgetId, "5678")
        self.assertEqual(request.owner, "John Doe")

class TestPoller(unittest.TestCase):
    def setUp(self):
        self.s3_retriever = Retriever.S3Retriever("usu-cs5260-hagen-requests")
        self.s3_processor = Processor.S3Processor("usu-cs5260-hagen-web")
    
    def testPoller(self):
        poller = Poller.Poller(self.s3_retriever, self.s3_processor)
        self.assertEqual(poller.retriever.bucket.name, "usu-cs5260-hagen-requests")
        self.assertEqual(poller.processor.bucket_name, "usu-cs5260-hagen-web")

class TestConsumer(unittest.TestCase):
    def testInvalidArgs(self):
        with self.assertRaises(Exception):
            consumer.main(["consumer.py", "asdf", "asdf", "asdf"])

    def testValidArgs(self):
        try:
            consumer.main(["consumer.py", "s3", "usu-cs5260-hagen-requests", "s3", "usu-cs5260-hagen-web"])
        except SystemExit:
            pass
        except:
            self.fail("consumer.main() exited unexpectedly!")

        try:
            consumer.main(["consumer.py", "--help"])
        except SystemExit:
            pass
        except:
            self.fail("consumer.main() exited unexpectedly!")
        

if __name__ == '__main__':
    unittest.main()