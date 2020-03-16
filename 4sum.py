def four_sum(L, target):
    N = len(L)
    S = set() # set of all i, j combination sum
    for k in range(2, N):
        j = k-1
        for i in range(j):
            S.add(L[i]+L[j])
        for l in range(k+1, N):
            n = target - L[k] - L[l]
            if n in S:
                return True
    return False

L = [2, 3, 5, 6, 14, 19, 28, 32]
print(four_sum(L, 60))
print(four_sum(L, 61))