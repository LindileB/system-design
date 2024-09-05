import hashlib
import math
from bitarray import bitarray

class BloomFilter:
    def __init__(self, n, p):
        """
        n: Expected number of elements in the Bloom filter
        p: Desired false positive probability
        """
        self.size = self._get_size(n, p)
        self.hash_count = self._get_hash_count(self.size, n)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)
        self.hash_functions = [hashlib.md5, hashlib.sha1, hashlib.sha256, hashlib.sha512]

    def _get_size(self, n, p):
        """
        Calculate the size of the bit array (m) using the formula:
        m = -(n * ln(p)) / (ln(2)^2)
        """
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    def _get_hash_count(self, m, n):
        """
        Calculate the number of hash functions (k) using the formula:
        k = (m / n) * ln(2)
        """
        k = (m / n) * math.log(2)
        return int(k)

    def _hashes(self, item):
        hash_values = []
        item = str(item).encode()
        for i in range(self.hash_count):
            hash_func = self.hash_functions[i % len(self.hash_functions)]
            hash_value = int(hash_func(item).hexdigest(), 16)
            hash_values.append(hash_value % self.size)
        return hash_values

    def add(self, item):
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

    def check(self, item):
        for hash_value in self._hashes(item):
            if self.bit_array[hash_value] == 0:
                return False
        return True

# Example usage
n = 1000  # Expected number of elements
p = 0.01  # Desired false positive probability
bloom = BloomFilter(n, p)
bloom.add("apple")
print(bloom.check("apple"))  # Output: True
print(bloom.check("banana"))  # Output: False
