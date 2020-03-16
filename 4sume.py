def four_sum(L, target):
    N = len(L)
    S = set()
    for k in range(2, N):
        for i in range(k-1):
            S.add(L[i]+L[k-1])
        print(k, S)
        for l in range(k+1, N):
            n = target - L[k] - L[l]
            if n in S:
                print("Found at k={}, l={}".format(k, l))
                return True
    return False

L = [2, 3, 5, 6, 14, 19, 28, 32]
print("L", L)
four_sum(L, 60)