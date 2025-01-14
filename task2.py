import numpy as np
import mmh3


class BloomFilter:
    def __init__(self, capacity, k):
        self.capacity = capacity
        self.k = k
        self.array_size = (capacity + 31) // 32
        self.array = np.zeros(self.array_size, dtype=np.uint32)
        self.bit_count = 0

    def _compute_hashes(self, element):
        return [mmh3.hash(element, seed=i) % self.capacity for i in range(self.k)]

    def put(self, element):
        for bit_index in self._compute_hashes(element):
            array_index = bit_index // 32
            bit_offset = bit_index % 32
            if not (self.array[array_index] & (1 << bit_offset)):
                self.array[array_index] |= (1 << bit_offset)
                self.bit_count += 1

    def get(self, element):
        for bit_index in self._compute_hashes(element):
            array_index = bit_index // 32
            bit_offset = bit_index % 32
            if not (self.array[array_index] & (1 << bit_offset)):
                return False
        return True

    def size(self):
        return self.bit_count / self.k