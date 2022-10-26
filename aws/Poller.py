import time

class Poller:

    def __init__(self, retriever, processor):
        self.retriever = retriever
        self.processor = processor
        self.timeout = 10


    def poll(self, timeout=None):
        print("Polling...")
        if timeout is None:
            timeout = self.timeout
        while True:
            request = self.retriever.retrieve()
            if request is not None:
                self.processor.process(request)
            else:
                time.sleep(timeout)
