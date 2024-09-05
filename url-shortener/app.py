from flask import Flask, request, redirect, render_template
import sqlite3
import hashlib
import base64
from pybloom_live import BloomFilter

app = Flask(__name__)

# Initialize Bloom filter
bloom_filter = BloomFilter(capacity=10000, error_rate=0.001)

# Database setup
def init_db():
    with sqlite3.connect('url_shortener.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS urls
                     (id INTEGER PRIMARY KEY, original_url TEXT, short_url TEXT)''')
        conn.commit()

# Load existing URLs into the Bloom filter in chunks
def load_bloom_filter(chunk_size=10000):
    with sqlite3.connect('url_shortener.db') as conn:
        c = conn.cursor()
        c.execute("SELECT original_url, short_url FROM urls")
        while True:
            rows = c.fetchmany(chunk_size)
            if not rows:
                break
            for row in rows:
                bloom_filter.add(row[0])
                bloom_filter.add(row[1])

# Generate a short URL using hashing and Base62 encoding
def generate_short_url(original_url):
    # Create a SHA-256 hash of the original URL
    hash_object = hashlib.sha256(original_url.encode())
    # Encode the hash using Base64
    base64_encoded = base64.urlsafe_b64encode(hash_object.digest()).decode('utf-8')
    # Use only the first 7 characters and ensure it fits within the character set [0-9, a-z, A-Z]
    short_url = base64_encoded[:7]
    return short_url

# Insert URL into the database
def insert_url(original_url, short_url):
    with sqlite3.connect('url_shortener.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
        conn.commit()

# Retrieve original URL from the database
def get_original_url(short_url):
    with sqlite3.connect('url_shortener.db') as conn:
        c = conn.cursor()
        c.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url,))
        result = c.fetchone()
        return result[0] if result else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        
        # Check if the URL is already in the Bloom filter
        if original_url in bloom_filter:
            return render_template('index.html', error="URL already exists")
        
        short_url = generate_short_url(original_url)
        
        # Handle collisions
        while short_url in bloom_filter:
            short_url = generate_short_url(original_url)
        
        insert_url(original_url, short_url)
        bloom_filter.add(original_url)
        bloom_filter.add(short_url)
        
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = get_original_url(short_url)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    init_db()
    load_bloom_filter()
    app.run(debug=True)
