from operator import add
class BIT:  
    def __init__(self, vals, combine=add, cons=int):
        if not isinstance(vals, list):
            vals = [cons() for i in range(vals)]
        n = len(vals)
        self.indexes = [vals]
        self.combine = combine
        self.cons = cons
        while n > 1:
            n = (n+1)//2
            i = len(self.indexes)
            self.indexes.append([self.recompute(i, k) for k in range(n)])

    def recompute(self, i, k):
        prev = self.indexes[i-1]
        if 2*k+1<len(prev):
            return self.combine(prev[2*k], prev[2*k+1])
        else:
            return prev[2*k]

    def __setitem__(self, k, v):
        self.indexes[0][k] = v
        for i, cur in enumerate(self.indexes[1:], 1):
            k //= 2
            cur[k] =  self.recompute(i, k)

    def __getitem__(self, i):
        return self.indexes[0][i]

    def __repr__(self):
        return '\n'.join(str(x) for x in self.indexes) 
    
    def prefix(self, i):
        s = self.cons()
        for index in self.indexes:
            if i and i&1:
                s = self.combine(s, index[i-1])
            i >>= 1
        return s
    
    def prefix_all(self):
        return [self.prefix(i) for i in range(len(self.indexes[0])+1)]

if __name__=='__main__':
    """
    Expected
    ========
    Array: [49, 97, 53, 5, 33, 65, 62, 51, 100]
    Sum: [0, 49, 146, 199, 204, 237, 302, 364, 415, 515]
    Max: [0, 49, 97, 97, 97, 97, 97, 97, 97, 100]
    Min: [inf, 49, 49, 49, 5, 5, 5, 5, 5, 5]
    """

    from random import randint, seed
    seed(0)

    psum = BIT(9)
    pmax = BIT(9, combine=max, cons=int)
    pmin = BIT(9, combine=min, cons=lambda:float('inf'))

    for i in range(9):
        psum[i] = pmax[i] = pmin[i] = randint(0, 100)

    print("Array:", psum.indexes[0])
    print("Sum:", psum.prefix_all())
    print("Max:", pmax.prefix_all())
    print("Min:", pmin.prefix_all())
