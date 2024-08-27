import time 
from threading import Lock
from collections import defaultdict
from .rate_limit import RateLimit

class FixedWindowCounter(RateLimit):
    def __init__(self, limit: int, window_size: int) -> None:
        self.limit = limit  # maximum number of requests per window
        self.window_size = window_size  # size of the window in seconds
        self.requests = defaultdict(lambda: [0, 0])  # dictionary to store request counts per client
        self.lock = Lock()

    def _get_current_window(self):
        return int(time.now() // self.window_size)
    
    def allow_request(self, client_id: str) -> bool:
        current_window = self._get_current_window()
        with self.lock:
            if self.requests[client_id][0] != current_window:
                # Reset the counter for the new window
                self.requests[client_id] = [current_window, 0]
            if self.requests[client_id][1] < self.limit:
                self.requests[client_id][1] += 1
                print(f"Request allowed for client {client_id}, count: {self.requests[client_id][1]}")
                return True
            else:
                print(f"Request denied for client {client_id}, count: {self.requests[client_id][1]}")
                return False