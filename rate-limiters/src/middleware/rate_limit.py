from flask import request, jsonify, Flask
from limiters import RateLimit

class RateLimitMiddleware:
    def __init__(self, app: Flask, rate_limiter: RateLimit) -> None:
        self.app = app
        self.rate_limiter = rate_limiter
        self.app.before_request(self.check_rate_limit)


    def check_rate_limit(self):
        if not self.rate_limiter.allow_request():
            print("Rate limit exceeded")
            return jsonify({"message": "Too many requests"}), 429