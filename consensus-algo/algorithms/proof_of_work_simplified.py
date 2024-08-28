import hashlib
import time

# Function that simulates proof of work
def proof_of_work(block_data, difficulty):
    nonce = 0
    start_time = time.time()
    
    while True:
        # Combine block data with the nonce
        combined_data = f"{block_data}{nonce}".encode()
        
        # Calculate the hash of the combined data
        hash_result = hashlib.sha256(combined_data).hexdigest()
        
        # Check if the hash meets the difficulty target
        if hash_result.startswith('0' * difficulty):
            end_time = time.time()
            print(f"Valid nonce found: {nonce}")
            print(f"Hash: {hash_result}")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            return nonce, hash_result
        
        # Increment the nonce
        nonce += 1

# Function to validate the nonce
def validate_nonce(block_data, nonce, difficulty):
    combined_data = f"{block_data}{nonce}".encode()
    hash_result = hashlib.sha256(combined_data).hexdigest()
    return hash_result.startswith('0' * difficulty)

def get_bitcoin_difficulty():
    url = "https://blockchain.info/q/getdifficulty"
    response = requests.get(url)
    difficulty = response.text
    return difficulty


# Example usage
if __name__ == '__main__':
    block_data = "some block data"
    difficulty = 4  # Number of leading zeros required in the hash
    # difficulty = get_bitcoin_difficulty()
    # Find a valid nonce
    nonce, valid_hash = proof_of_work(block_data, difficulty)

    # Validate the nonce
    is_valid = validate_nonce(block_data, nonce, difficulty)
    print(f"Nonce validation result: {is_valid}")
