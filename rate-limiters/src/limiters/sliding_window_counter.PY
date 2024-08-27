import time 
from threading import Lock
from collections import deque
from .rate_limit import RateLimit

class SlidingWindowCounter(RateLimit):
    def __init__(self, limit, window_size, sub_window_size) -> None:
        self.limit = limit  # maximum number of requests per window
        self.window_size = window_size  # size of the main window in seconds
        self.sub_window_size = sub_window_size  # size of each sub-window in seconds
        self.sub_windows = deque()  # deque to store request counts for sub-windows
        self.lock = Lock()

    def _get_current_time(self):
        return int(time.time())
    
    def _remove_old_sub_windows(self, current_time):
        while self.sub_windows and self.sub_windows[0][0] <= current_time - self.window_size:
            self.sub_windows.popleft()
    
    def allow_request(self) -> bool:
        current_time = self._get_current_time()
        with self.lock:
            self._remove_old_sub_windows(current_time)
            current_sub_window = current_time // self.sub_window_size

            if self.sub_windows and self.sub_windows[-1][0] == current_sub_window:
                self.sub_windows[-1][1] += 1
            else:
                self.sub_windows.append([current_sub_window, 1])

            total_requests = sum(count for _, count in self.sub_windows)
            if total_requests <= self.limit:
                print(f"Request allowed, total requests in window: {total_requests}")
                return True
            else:
                print(f"Request denied, total requests in window: {total_requests}")
                return False