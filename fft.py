def fft_base(p, sign=1):
    if len(p) == 1: return p
    alpha, beta = fft_base(p[::2], sign), fft_base(p[1::2], sign)
    beta *= np.exp(np.arange(len(p)/2)*sign*np.pi*2j/len(p))
    return np.concatenate((alpha + beta, alpha - beta))

def pad(p):
    n = 2**int(ceil(np.log2(len(p))))
    return np.concatenate((p, [0]*(n-len(p)))).astype('complex')

def fft(p):
    return fft_base(pad(p), 1)

def ifft(p):
    return fft_base(pad(p), -1)/len(p)