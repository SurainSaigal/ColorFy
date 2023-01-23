import time


class Stopwatch:

    def __init__(self):
        self.startTime = 0
        self.stopTime = 0

    def start(self):
        self.startTime = time.time()

    def stop(self):
        self.stopTime = time.time()

    def time(self):
        return self.stopTime - self.startTime
