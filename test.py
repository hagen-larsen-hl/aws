import unittest
import consumer

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

if __name__ == '__main__':
    unittest.main()