import numpy as np

def fftconvolve(a, b):
    """Equivalent to scipy.signal.fftconvolve"""
    L = len(a) + len(b) - 1
    N = 2**int(np.ceil(np.log2(L)))
    return np.fft.ifft(np.fft.fft(a, N)*np.fft.fft(b, N))[:L]

def char2int(c):
    return ord(c) - ord('a')

@np.vectorize
def char2complex(c):
    return np.exp(1j*2*np.pi/26*char2int(c))

def str2vec(s):
    return char2complex(list(s))

def partial_palindrome(s, neg=False):
    l = len(s)
    v = str2vec(s)
    product = fftconvolve(v, v.conj())
    aim = np.arange(1, 2*l)
    aim[l:] = aim[:l-1][::-1]
    matched = np.abs(product - aim) < 1e-8
    ind = matched.nonzero()[0]+1
    offset = l if neg else l - 1
    ind = (ind+offset)%(2*l)-offset
    return ind

partial_palindrome('abababcbababa')