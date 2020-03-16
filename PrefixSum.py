import math
def pbound(l):
    return int(math.ceil(math.log2(l)))

class PrefixSum:
    def __init__(self, L):
        self.D = pbound(len(L))
        self.N = 1<<self.D
        self.presum = [0]*(self.N-1) + L + [0]*(self.N-len(L))
        for i in range(self.N-2, -1, -1):
            self.presum[i] = self.presum[2*i+1] + self.presum[2*i+2]
        self.L = L
        self.presum = self.presum[1:self.N-1:2]
    def __repr__(self):
        return str(self.L)
    def find(self, k):
        mask, i = self.N//2, 0
        while mask>1:
            status = (mask&k)!=0
            yield i, status
            i = 2*i+1+status
            mask >>= 1
    def query(self, k):
        if k<0: return 0
        k = min(k, len(self.L)-1)
        pre = [self.presum[j] for j, status in self.find(k) if status]
        S = sum(pre) + self.L[k]
        if (k&1):
            S += self.L[k-1]
        return S
    def __getitem__(self, k):
        return self.L[k]
    def __setitem__(self, k, v):
        delta = v - self.L[k]
        for j, status in self.find(k):
            if status == 0:
                self.presum[j] += delta
        self.L[k] += delta
