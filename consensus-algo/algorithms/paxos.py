import random

class PaxosProposer:
    def __init__(self, id, quorum_size):
        self.id = id
        self.quorum_size = quorum_size

    def propose(self, value, acceptors):
        proposal_number = random.randint(1, 100)
        promises = 0
        accepted_value = None

        # Phase 1: Prepare
        for acceptor in acceptors:
            promise, last_accepted_value = acceptor.prepare(proposal_number)
            if promise:
                promises += 1
                if last_accepted_value is not None:
                    accepted_value = last_accepted_value

        # Phase 2: Accept
        if promises >= self.quorum_size:
            if accepted_value is None:
                accepted_value = value
            accepted = 0
            for acceptor in acceptors:
                if acceptor.accept(proposal_number, accepted_value):
                    accepted += 1
            if accepted >= self.quorum_size:
                return accepted_value
        return None

class PaxosAcceptor:
    def __init__(self):
        self.promised_id = None
        self.accepted_id = None
        self.accepted_value = None

    def prepare(self, proposal_number):
        if self.promised_id is None or proposal_number > self.promised_id:
            self.promised_id = proposal_number
            return True, self.accepted_value
        return False, None

    def accept(self, proposal_number, value):
        if self.promised_id is None or proposal_number >= self.promised_id:
            self.promised_id = proposal_number
            self.accepted_id = proposal_number
            self.accepted_value = value
            return True
        return False

# Example usage
if __name__ == '__main__':
    proposer = PaxosProposer(id=1, quorum_size=2)
    acceptors = [PaxosAcceptor() for _ in range(3)]
    value = proposer.propose('value', acceptors)
    print('Consensus value:', value)
