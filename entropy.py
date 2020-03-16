import numpy as np
import bisect

class EntropyExtractor:
    def __init__(self, src):
        self.bound = np.array([0., 1.])
        self.src = src

    def pick(self, lo, hi):
        self.bound = np.array([[1-lo, lo], [1-hi, hi]])@self.bound

    def __getitem__(self, cdf):
        while True:
            i = bisect.bisect_right(cdf, self.bound[0])-1
            j = bisect.bisect_left(cdf, self.bound[1])-1
            if i != j:
                info, cdf_src = self.src()
                if self.bound.sum() < cdf[i+1] + cdf[j]:
                    self.pick(1-cdf_src[info+1], 1-cdf_src[info])
                else:
                    self.pick(cdf_src[info], cdf_src[info+1])
            else:
                self.bound = (self.bound-cdf[i])/(cdf[i+1]-cdf[i])
                return i


class DiscreteAdaptor(EntropyExtractor):
    """Adapt a RNG with distribution (p, 1-p) to (1/2, 1/2)"""

    def __init__(self, src, arg):
        """arg is pdf or cdf"""
        pdf = np.diff(arg) if arg[-1] == 1 else arg
        cvt = sorted(range(len(pdf)), key=lambda i: pdf[i])
        cdf = np.cumsum([0]+list(sorted(pdf)))

        def src_(): return cvt[src()], cdf
        super().__init__(src_)


if __name__ == "__main__":
    def p_37(): return int(np.random.rand() >= 0.3)
    pool = DiscreteAdaptor(p_37, [0.3, 0.7])

    l = np.array([pool[0, 0.5, 1] for i in range(4000)])
    print(l.sum(), (l[1:]*l[:-1]).sum())
