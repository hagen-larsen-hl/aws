import time
import logging
logging.basicConfig(filename="consumer.log",format="%(asctime)s : %(message)s", encoding='utf-8', level=logging.INFO)
logger = logging.getLogger("consumer")

class Poller:

    def __init__(self, retriever, processor):
        self.retriever = retriever
        self.processor = processor
        self.timeout = 2


    def poll(self, timeout=None):
        logger.info("Start polling...")
        if timeout is None:
            timeout = self.timeout
        while True:
            request = self.retriever.retrieve()
            if request is not None:
                logger.info("Request received!")
                self.processor.process(request)
            else:
                logger.info("No request available. Waiting...")
                time.sleep(timeout)
