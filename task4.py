import numpy as np
import mmh3


class HyperLogLog:
    def __init__(self, k, n):
        self.k = k
        self.n = n
        self.buckets = np.zeros(self.n, dtype=np.uint8)

    def _hash(self, s):
        hash_value = mmh3.hash(s, 42)
        return format(hash_value, '032b')

    def put(self, s):
        hash_bin = self._hash(s)
        bucket_index = int(hash_bin[:self.k], 2)
        remaining_bits = hash_bin[self.k:]
        leading_zeros = len(remaining_bits) - len(remaining_bits.lstrip('0'))
        self.buckets[bucket_index] = max(self.buckets[bucket_index], leading_zeros + 1)

    def est_size(self):
        Z = 0
        for bucket in self.buckets:
            Z += 2 ** -bucket 
        
        alpha_m = 0.7213 / (1 + 1.079 / self.n)
        raw_estimate = alpha_m * self.n ** 2 / Z
        
        if raw_estimate <= 2.5 * self.n:
            V = sum(1 for x in self.buckets if x == 0)
            if V > 0:
                raw_estimate = self.n * math.log(self.n / V)
        
        return int(raw_estimate)