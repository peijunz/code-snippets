"""支持惰性删除元素的堆。以及基于双堆的动态获取中位数"""
from collections import Counter
import heapq
class Heap:
    def __init__(self):
        self.heap = []
        self.size = 0
        self.pending = Counter()
    def __len__(self):
        return self.size
    def push(self, x):
        heapq.heappush(self.heap, x)
        self.size += 1
    def remove(self, x):
        self.size -= 1
        self.pending[x] += 1
    def _clean(self):
        while self.heap and self.heap[0] in self.pending:
            x = heapq.heappop(self.heap)
            if self.pending[x] == 1:
                del self.pending[x]
            else:
                self.pending[x] -= 1
    def top(self):
        self._clean()
        return self.heap[0] if self.heap else float('-inf')
    def pop(self):
        self._clean()
        self.size -= 1
        return heapq.heappop(self.heap)

class MedianLocator:
    def __init__(self):
        self.upper = Heap()
        self.lower = Heap()
    def balance(self):
        if len(self.upper) - len(self.lower) > 1:
            self.lower.push(-self.upper.pop())
        if len(self.lower) - len(self.upper) > 1:
            self.upper.push(-self.lower.pop())
    def add(self, n):
        if len(self.upper) and n >= self.upper.top():
            self.upper.push(n)
        else:
            self.lower.push(-n)
        self.balance()
    def remove(self, n):
        if len(self.upper) and n >= self.upper.top():
            self.upper.remove(n)
        else:
            self.lower.remove(-n)
        self.balance()
    def median(self):
        if len(self.upper) == len(self.lower):
            return (self.upper.top() - self.lower.top())/2
        elif len(self.upper) > len(self.lower):
            return self.upper.top()
        else:
            return -self.lower.top()