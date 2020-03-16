import numpy as np


def GCD(a, b):
    m = np.array([1, 0])
    n = np.array([0, 1])
    while b:
        p, r = divmod(a, b)
        m, n = n, m-p*n
        a, b = b, r
    return a, m


def divmodr(b, m, n=None):
    if n is None:
        return divmod(b, m)
    k, (c, d) = GCD(m, n)
    p, r = divmod(b, k)
    return (p*c) % n, r


class RingBase:
    _base = 1
    _verbose = True

    def __init__(self, arg=0):
        if isinstance(arg, RingBase):
            self.val = arg.val % self._base
        else:
            self.val = arg % self._base

    def __int__(self):
        return int(self.val)

    def __str__(self):
        if self._verbose:
            return "{} (mod {})".format(self.val, self._base)
        else:
            return str(self.val)

    def __repr__(self):
        return str(self)

    def __add__(self, rhs):
        rhs = self.__class__(rhs)
        return self.__class__(self.val+rhs.val)

    def __radd__(self, lhs):
        lhs = self.__class__(lhs)
        return self.__class__(self.val+lhs.val)

    def __sub__(self, rhs):
        rhs = self.__class__(rhs)
        return self.__class__(self.val-rhs.val)

    def __rsub__(self, lhs):
        lhs = self.__class__(lhs)
        return self.__class__(lhs.val-self.val)

    def __mul__(self, rhs):
        rhs = self.__class__(rhs)
        return self.__class__(self.val*rhs.val)

    def __rmul__(self, lhs):
        lhs = self.__class__(lhs)
        return self.__class__(self.val*lhs.val)

    def __truediv__(self, rhs):
        rhs = self.__class__(rhs)
        p, r = divmodr(self.val, rhs.val, self._base)
        if r:
            raise ZeroDivisionError("Unsolvable congrunce division")
        return self.__class__(p)

    def __rtruediv__(self, lhs):
        lhs = self.__class__(lhs)
        return lhs/self

    def __floordiv__(self, rhs):
        rhs = self.__class__(rhs)
        p, r = divmodr(self.val, rhs.val, self._base)
        return self.__class__(p)

    def __rfloordiv__(self, lhs):
        lhs = self.__class__(lhs)
        p, r = divmodr(lhs.val, self.val, self._base)
        return self.__class__(p)

    def __mod__(self, rhs):
        rhs = self.__class__(rhs)
        p, r = divmodr(self.val, rhs.val, self._base)
        return self.__class__(r)

    def __rmod__(self, lhs):
        lhs = self.__class__(lhs)
        p, r = divmodr(lhs.val, self.val, self._base)
        return self.__class__(r)

    def __eq__(self, rhs):
        rhs = self.__class__(rhs)
        return rhs.val == self.val

    def __pow__(self, rhs):
        if isinstance(rhs, RingBase):
            return self.__class__(self.val**rhs.val)
        else:
            return self.__class__(self.val**rhs)


def Ring(base, verbose=True):
    class _R(RingBase):
        _base = base
        _verbose = verbose
    return _R
