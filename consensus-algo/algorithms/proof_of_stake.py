import random

class Validator:
    def __init__(self, id, stake):
        self.id = id
        self.stake = stake

def select_validator(validators):
    total_stake = sum(v.stake for v in validators)
    pick = random.uniform(0, total_stake)
    current = 0
    for validator in validators:
        current += validator.stake
        if current > pick:
            return validator

# Example usage
if __name__ == '__main__':
    validators = [Validator(id=i, stake=random.uniform(1, 100)) for i in range(5)]
    selected_validator = select_validator(validators)
    print('Selected validator:', selected_validator.id)
