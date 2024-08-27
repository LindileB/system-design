from flask import Flask, jsonify

from limiters import TokenBucket
from limiters import LeakyBucket
from limiters import SlidingWindowCounter
from middleware import RateLimitMiddleware

app = Flask(__name__)

# limiter = TokenBucket(rate=1, capacity=2)
# limiter = LeakyBucket(capacity=2, leak_rate=1)
limiter = SlidingWindowCounter(limit=5, window_size=2, sub_window_size=2)

RateLimitMiddleware(app=app, rate_limiter=limiter)


@app.route("/api/resource", methods=['GET'])
def get_resource():
    return jsonify({"message": "Request allowed"}), 200

if __name__ == '__main__':
    app.run(debug=True)