# 1. Paxos
#### Overview
Paxos is a family of protocols for solving consensus in a network of unreliable processors (i.e., nodes that may fail). It's known for its robustness and theoretical foundations.

#### Key Concepts
- Proposers: Nodes that propose values.
- Acceptors: Nodes that decide on whether to accept a proposal.
- Learners: Nodes that learn the chosen value.
#### Process
1. A proposer selects a proposal number and sends a prepare request to a majority of acceptors.
2. If the acceptors have not already promised to another proposal number, they promise not to accept a proposal with a lower number and respond with the highest-numbered proposal they have accepted so far.
3. The proposer sends an accept request with the proposal number and value to the majority of acceptors.
4. Acceptors accept the proposal if they have not promised to a higher-numbered proposal.
5. Once a majority has accepted the value, the value is chosen.

# 2. Raft
#### Overview
Raft is designed to be more understandable compared to Paxos while providing a similar consistency model. It's widely adopted in projects like etcd and Consul.

#### Key Concepts
- Leader: The node that handles all client interactions, replicates log entries to followers, and manages consistency.
- Follower: Nodes that receive log entries from the leader and apply them to their local state.
- Candidate: Node that transitions to this state when starting an election to become a leader.
#### Process
1. Election: A follower becomes a candidate and requests votes from other nodes. The node that receives a majority of votes becomes the leader.
2. Log Replication: The leader receives log entries from clients, appends them to its log, and replicates it to followers. Once a majority acknowledge the entry, it's committed.
3. Heartbeats: The leader periodically sends heartbeats to followers to maintain authority and prevent new elections.

# 3. Byzantine Fault Tolerance (BFT)
#### Overview
BFT is designed to tolerate Byzantine faults, where nodes may fail and give conflicting information to different parts of the system. Practical Byzantine Fault Tolerance (PBFT) is a widely known BFT algorithm.

#### Key Concepts
- Client: Initiates a request expecting the system to agree on an outcome.
- Primary (or Leader): A designated node that coordinates consensus rounds.
- Replicas: Other nodes in the system that replicate and validate the requests.
#### Process
1. A client sends a request to the primary.
2. The primary multicasts the request to all replicas.
3. Replicas execute the request and send a response to the client.
4. The client waits for (2f+1) matching responses out of (3f+1) total replicas to ensure consistency, where (f) is the maximum number of faulty nodes.

# 4. Proof of Work (PoW)
#### Overview
PoW is a widely used consensus algorithm in blockchain networks like Bitcoin. It relies on computational effort to prevent malicious actions.

#### Key Concepts
- Mining: The process of validating transactions and adding them to the blockchain.
- Nonce: A value that miners adjust to meet difficulty criteria.
- Difficulty: A measure of how hard it is to find a valid nonce.
#### Process
1. Miners collect transactions into a block.
2. Miners hash the block header in a way that meets the network's difficulty target.
3. The first miner to find a valid nonce broadcasts the block to the network.
4. Other nodes validate the block and add it to their blockchain.

#### Simplified Impl Explanation

##### `proof_of_work` Function

1. Starts with a nonce value of 0.
2. Combines the block data with the nonce and hashes the result using SHA-256.
3. Checks if the resulting hash starts with the required number of leading zeros.
4. If the hash meets the difficulty target, the nonce and hash are returned.
5. If not, the nonce is incremented, and the process repeats.

##### `validate_nonce` Function

1. Takes the block data, nonce, and difficulty as inputs.
2. Recalculates the hash for the provided nonce.
3. Checks if the hash meets the difficulty target.

# 5. Proof of Stake (PoS)
#### Overview
PoS is an energy-efficient alternative to PoW, used in some blockchain networks like Ethereum 2.0.

#### Key Concepts
- Validators: Nodes that create new blocks and validate transactions.
- Stake: The amount of cryptocurrency that validators lock up as collateral.
- Random Selection: Validators are chosen to create new blocks based on their stake and some randomness.
#### Process
1. Validators propose new blocks based on their stake.
2. Other validators attest to the validity of the new block.
3. The block is added to the blockchain once enough attestations are obtained.