import mmh3


class CountingBloomFilter:
    def __init__(self, k, n, cap):
        self.filter_size = n
        self.filter = 0
        self.cap = cap
        self.num_of_funcs = k
        self.filled_mask = (1 << cap) - 1

    def _get_counter(self, index):
        shift = index * self.cap
        return (self.filter >> shift) & self.filled_mask

    def _set_counter(self, index, value):
        shift = index * self.cap
        self.filter &= ~(self.filled_mask << shift)
        self.filter |= (value & self.filled_mask) << shift

    def put(self, s):
        for i in range(self.num_of_funcs):
            index = mmh3.hash(s, i) % self.filter_size
            current_counter = self._get_counter(index)
            if current_counter + 1 < (1 << self.cap):
                self._set_counter(index, current_counter + 1)

    def get(self, s, theta):
        for i in range(self.num_of_funcs):
            index = mmh3.hash(s, i) % self.filter_size
            current_counter = self._get_counter(index)
            if current_counter < theta:
                return False
        return True

    def size(self):
        total = 0
        for i in range(self.filter_size):
            total += self._get_counter(i)
        return total / self.num_of_funcs