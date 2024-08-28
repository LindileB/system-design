# master.py
import socket
import threading

# Function to handle incoming worker connections
def handle_worker(conn, addr):
    global found, found_nonce_message
    print(f"Connected by {addr}")
    
    while not found:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        if message == "request_nonce_range":
            start_nonce, end_nonce = assign_nonce_range()
            conn.send(f"{start_nonce}-{end_nonce}".encode())
        elif message.startswith("found_nonce"):
            _, nonce = message.split(':')
            found_nonce_message = message
            found = True
    if found_nonce_message:
        conn.send(found_nonce_message.encode())
    conn.close()

# Function to assign nonce ranges
def assign_nonce_range():
    global current_nonce
    start_nonce = current_nonce
    end_nonce = start_nonce + nonce_increment
    current_nonce += nonce_increment
    return start_nonce, end_nonce

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

nonce_increment = 1000
current_nonce = 0
found = False
found_nonce_message = None

# Start the master node server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Master node started, waiting for worker nodes to connect...")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_worker, args=(conn, addr))
        thread.start()
