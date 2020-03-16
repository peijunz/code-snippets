def gcd2(a, b):
    A, B = (1, 0), (0, 1)
    while b:
        a, (p, b) = b, divmod(a, b)
        A, B = B, (A[0]-p*B[0], A[1]-p*B[1])
    return A, a

(p,q),d = gcd2(34, 24)

assert p*34+q*24 == d