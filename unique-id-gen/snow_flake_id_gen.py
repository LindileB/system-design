import time

class SnowflakeIDGenerator:
    def __init__(self, datacenter_id, worker_id, custom_epoch=1577836800000):
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.custom_epoch = custom_epoch

        self.sequence = 0
        self.last_timestamp = -1

        # Bit lengths for each component
        self.timestamp_bits = 41
        self.datacenter_id_bits = 5
        self.worker_id_bits = 5
        self.sequence_bits = 12

        # Maximum values for each component
        self.max_datacenter_id = (1 << self.datacenter_id_bits) - 1
        self.max_worker_id = (1 << self.worker_id_bits) - 1
        self.max_sequence = (1 << self.sequence_bits) - 1

        # Bit shifts for each component
        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.worker_id_shift + self.worker_id_bits
        self.timestamp_shift = self.datacenter_id_shift + self.datacenter_id_bits

        # Validate datacenter_id and worker_id
        if self.datacenter_id > self.max_datacenter_id or self.datacenter_id < 0:
            raise ValueError(f"datacenter_id must be between 0 and {self.max_datacenter_id}")
        if self.worker_id > self.max_worker_id or self.worker_id < 0:
            raise ValueError(f"worker_id must be between 0 and {self.max_worker_id}")

    def _current_timestamp(self):
        return int(time.time() * 1000)

    def _wait_for_next_millisecond(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate_id(self):
        timestamp = self._current_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate id")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.max_sequence
            if self.sequence == 0:
                timestamp = self._wait_for_next_millisecond(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        snowflake_id = ((timestamp - self.custom_epoch) << self.timestamp_shift) | \
                       (self.datacenter_id << self.datacenter_id_shift) | \
                       (self.worker_id << self.worker_id_shift) | \
                       self.sequence

        return snowflake_id

    @staticmethod
    def extract_components(snowflake_id):
        timestamp_bits = 41
        datacenter_id_bits = 5
        worker_id_bits = 5
        sequence_bits = 12

        sequence_mask = (1 << sequence_bits) - 1
        worker_id_mask = ((1 << worker_id_bits) - 1) << sequence_bits
        datacenter_id_mask = ((1 << datacenter_id_bits) - 1) << (worker_id_bits + sequence_bits)
        timestamp_mask = ((1 << timestamp_bits) - 1) << (datacenter_id_bits + worker_id_bits + sequence_bits)

        sequence = snowflake_id & sequence_mask
        worker_id = (snowflake_id & worker_id_mask) >> sequence_bits
        datacenter_id = (snowflake_id & datacenter_id_mask) >> (worker_id_bits + sequence_bits)
        timestamp = (snowflake_id & timestamp_mask) >> (datacenter_id_bits + worker_id_bits + sequence_bits)

        return {
            "timestamp": timestamp,
            "datacenter_id": datacenter_id,
            "worker_id": worker_id,
            "sequence": sequence
        }

# Example usage
if __name__ == '__main__':
    datacenter_id = 1
    worker_id = 1
    generator = SnowflakeIDGenerator(datacenter_id, worker_id)

    # Generate a Snowflake ID
    snowflake_id = generator.generate_id()
    print(f"Generated Snowflake ID: {snowflake_id}")

    # Extract components from the Snowflake ID
    components = SnowflakeIDGenerator.extract_components(snowflake_id)
    print(f"Extracted Components: {components}")
