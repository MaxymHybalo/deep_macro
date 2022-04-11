import time

class Wait:

    def __init__(self, wait):
        self.wait = wait
        self.process = "wait"

    def delay(self):
        time.sleep(self.wait)