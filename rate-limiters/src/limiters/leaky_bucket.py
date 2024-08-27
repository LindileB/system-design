import time
from threading import Lock, Thread

from .rate_limit import RateLimit

class LeakyBucket(RateLimit):
    def __init__(self, capacity: int, leak_rate: int) -> None:
        self.capacity = capacity  # maximum number of requests
        self.leak_rate = leak_rate  # requests per second
        self.requests = 0  # current number of requests in the bucket
        self.lock = Lock()
        self._start_leak_thread()

    def _leak(self):
        with self.lock:
            if self.requests > 0:
                self.requests -=1 
                print(f"Leaked a request, remaining: {self.requests}")

    def _start_leak_thread(self):
        def leak_loop():
            while True:
                time.sleep(1/ self.leak_rate)
                self._leak()

        leak_thread = Thread(target=leak_loop, daemon=True)
        leak_thread.start()

    def allow_request(self) -> bool:
        with self.lock:
            if self.requests < self.capacity:
                self.requests +=1
                print(f"Request allowed, current requests: {self.requests}")
                return True
            else:
                print("Request denied, bucket full")
                return False