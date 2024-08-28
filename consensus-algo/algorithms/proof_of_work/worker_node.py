# worker.py
import hashlib
import socket

# Proof of Work function
def proof_of_work(start, end, block_data, difficulty):
    nonce = start
    while nonce < end:
        combined_data = f"{block_data}{nonce}".encode()
        hash_result = hashlib.sha256(combined_data).hexdigest()
        if hash_result.startswith('0' * difficulty):
            return nonce, hash_result
        nonce += 1
    return None, None

def get_bitcoin_difficulty():
    url = "https://blockchain.info/q/getdifficulty"
    response = requests.get(url)
    difficulty = response.text
    return difficulty

HOST = '127.0.0.1'  # Master node IP
PORT = 65432        # Master node port

block_data = "example block data"
difficulty = 4 # get_bitcoin_difficulty()

# Connect to the master node
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to master node, requesting nonce range...")
    while True:
        # Request nonce range from master node
        s.sendall(b"request_nonce_range")
        data = s.recv(1024).decode()
        if not data:
            break
        if data.startswith("found_nonce"):
            _, nonce = data.split(':')
            print(f"Terminating search: valid nonce found {nonce}")
            break
        start_nonce, end_nonce = map(int, data.split('-'))
        print(f"Received nonce range: {start_nonce}-{end_nonce}")
        
        # Perform mining task
        nonce, valid_hash = proof_of_work(start_nonce, end_nonce, block_data, difficulty)
        if nonce is not None:
            print(f"Found valid nonce {nonce} with hash {valid_hash}")
            # Notify master node of success
            s.sendall(f"found_nonce:{nonce}".encode())
            s.recv(1024)  # Wait for the broadcast confirmation
            break
