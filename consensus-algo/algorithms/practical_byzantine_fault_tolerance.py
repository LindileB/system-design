class PBFTNode:
    def __init__(self, id):
        self.id = id
        self.state = 'normal'
        self.log = []

    def request(self, client_id, operation):
        self.log.append((client_id, operation))
        return self.pre_prepare(operation)

    def pre_prepare(self, operation):
        return self.prepare(operation)

    def prepare(self, operation):
        return self.commit(operation)

    def commit(self, operation):
        return True

# Example usage
if __name__ == '__main__':
    nodes = [PBFTNode(id=i) for i in range(4)]
    client_id = 1
    operation = 'op'

    for node in nodes:
        result = node.request(client_id, operation)
        if result:
            print(f'Node {node.id} committed the operation.')
