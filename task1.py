import mmh3
import numpy as np


class BloomFilter:
    def __init__(self, capacity):
        self.capacity = capacity
        self.array_size = (capacity + 31) // 32
        self.array = np.zeros(self.array_size, dtype=np.uint32)
        self.bit_count = 0

    def _compute_hash(self, element):
        return mmh3.hash(element) % self.capacity

    def put(self, element):
        bit_index = self._compute_hash(element)
        array_index = bit_index // 32
        bit_offset = bit_index % 32
        if not (self.array[array_index] & (1 << bit_offset)):
            self.array[array_index] |= (1 << bit_offset)
            self.bit_count += 1

    def get(self, element):
        bit_index = self._compute_hash(element)
        array_index = bit_index // 32
        bit_offset = bit_index % 32
        return (self.array[array_index] & (1 << bit_offset)) != 0

    def size(self):
        return self.bit_count