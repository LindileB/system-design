import random
import time

class RaftNode:
    def __init__(self, id, peers):
        self.id = id
        self.peers = peers
        self.state = 'follower'
        self.voted_for = None

    def request_vote(self, term, candidate_id):
        if self.voted_for is None:
            self.voted_for = candidate_id
            return True
        return False

    def become_candidate(self):
        self.state = 'candidate'
        self.voted_for = self.id
        votes = 1
        for peer in self.peers:
            if peer.request_vote(1, self.id):
                votes += 1
        if votes > len(self.peers) // 2:
            self.state = 'leader'
        return self.state

# Example usage
if __name__ == '__main__':
    nodes = [RaftNode(id=i, peers=[]) for i in range(5)]
    for node in nodes:
        node.peers = [n for n in nodes if n.id != node.id]

    leader = None
    for node in nodes:
        if node.state == 'follower' and random.random() < 0.5:
            result = node.become_candidate()
            if result == 'leader':
                leader = node
                break

    print('Elected leader:', leader.id if leader else None)
