import numpy as np

def padded_size(L):
    return 2**int(np.ceil(np.log2(L)))

def convolve(a, b):
    """Equivalent to scipy.signal.fftconvolve"""
    L = len(a) + len(b) - 1
    N = padded_size(L)
    return np.fft.ifft(np.fft.fft(a, N)*np.fft.fft(b, N))[:L]

multiply = convolve

def power(p, k):
    """Calculate coefficients for p(x)**k"""
    L = k*len(p)-k+1
    N = padded_size(L)
    return np.fft.ifft(np.fft.fft(p, N)**k)[:L]

def xpower(p, k):
    """Calculate coefficients for p(x**k)"""
    L = k*len(p)-k+1
    p_xk = np.zeros(L, dtype='int')
    p_xk[::k] = p
    return p_xk

def from_terms(l):
    m = max(l)
    p = np.zeros(m+1, dtype='int')
    for i in l:
        p[i] += 1
    return p

def threeSumDuplicate(l):
    p = from_terms(l)
    return power(p, 3).real.round().astype('int')

def threeSumUnique(l):
    p = from_terms(l)
    p_x2 = xpower(p, 2)
    p_x3 = xpower(p, 3)
    ans = power(p, 3) - 3*multiply(p_x2, p) + 2*p_x3
    return ans.real.round().astype('int')//6

if __name__ == "__main__":
    print(threeSumDuplicate([1,3,4,2,3,1,6,4,8,7,6,8,8]))
    print(threeSumUnique([1,3,4,2,3,1,6,4,8,7,6,8,8]))
