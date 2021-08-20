from operator import add
class BIT:
    def __init__(self, n, combine=add, cons=int):
        self.indexes = []
        self.combine = combine
        self.cons = cons
        
        while n > 0:
            self.indexes.append([self.cons() for i in range(n)])
            if n==1:
                break
            n = (n+1)//2

    def __setitem__(self, k, v):
        self.indexes[0][k] = v
        for prev, cur in zip(self.indexes[:-1], self.indexes[1:]):
            k //= 2
            if 2*k+1<len(prev):
                cur[k] = self.combine(prev[2*k], prev[2*k+1])
            else:
                cur[k] = prev[2*k]

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
