System-design real world implementations

System design concepts and real world implementations

# Rate Limiters

### The intent of this app is to test the implementation of rate limiters.
- Token Bucket
- Leaky Bucket
- Fixed Window Counter
- Sliding Window Log
- Sliding Window Counter

#### Starting the app
1. activate the venv
   ```
   .\rate-limiter\Scripts\activate
   ```
2. start application
   ```
   python app.py
   ````

#### Test API using curl
1. bash
    ```
    for i in {1..20}; do curl -i  http://127.0.0.1:5000/api/resource; done
    ```
    or execite shell script
    ```
    .\test\test_rate_limiter.sh
    ```
    
2. windows - execute powershell script
    ```
    .\test\test_rate_limiter.ps1

# Consensus Algorithms

### Simplified implementation of the below listed consensus algorithms
- Paxos
- Raft
- Byzantine Fault Tolerance (BFT)
- Proof of Work (PoW)
- Proof of Stake (PoS)

# Unique ID Generation for Distributed System

Design an ID gen solution that meets the following conditions:

- IDs must be unique.
- IDs are numerical values only.
- IDs fit into 64-bit.
- IDs are ordered by date.
- Ability to generate over 10,000 unique IDs per second.
