import time 
from threading import Lock, Thread
from .rate_limit import RateLimit

class TokenBucket(RateLimit):
    def __init__(self, rate, capacity, refill_interval=5) -> None:
        self.rate = rate  # tokens per second
        self.capacity = capacity  # maximum number of tokens
        self.tokens = capacity  # current number of tokens
        self.refill_interval = refill_interval  # interval in seconds to refill tokens
        self.lock = Lock()
        self._start_refill_thread()
        

    def _start_refill_thread(self):
        def refill_loop():
            while True:
                time.sleep(self.refill_interval)
                self._refill()

        refill_thread = Thread(target=refill_loop, daemon=True)
        refill_thread.start()


    def _refill(self):
        with self.lock:
            self.tokens = min(self.capacity, self.tokens + self.rate * self.refill_interval)

    def allow_request(self) -> bool:
        with self.lock:
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                return False 