class BitcoinDifficulty:
    def __init__(self, current_difficulty, actual_time_seconds, target_time_seconds):
        self.current_difficulty = current_difficulty
        self.actual_time_seconds = actual_time_seconds
        self.target_time_seconds = target_time_seconds

    def calculate_new_difficulty(self):
        new_difficulty = self.current_difficulty * (self.actual_time_seconds / self.target_time_seconds)
        self._update_curr_difficulty(new_difficulty)
        return new_difficulty

    def _update_curr_difficulty(self, new_difficulty):
        self.current_difficulty = new_difficulty


# Example usage:
if __name__ == '__main__':
# Previous difficulty, actual time taken to mine last 2016 blocks, target time to mine 2016 blocks
    current_difficulty = 8.6871474313762e13
    actual_time_seconds = 1050000  # Actual time in seconds (e.g., it took slightly less than 2 weeks)
    target_time_seconds = 1209600  # Target time in seconds (2 weeks)

    difficulty_adjuster = BitcoinDifficulty(current_difficulty, actual_time_seconds, target_time_seconds)
    difficulty_adjuster.calculate_new_difficulty()

    print(f"New Difficulty: {difficulty_adjuster.current_difficulty}")
