inf = float('inf')
def highbit_range(n):
    for h in range(n):
        for i in range(1<<h, 1<<(h+1)):
            yield h, i

def last_two_bits(h, cur):
    l = [k for k in range(h) if (1<<k)&cur] 
    if not l: return []
    l.append(h)
    return ((i, j) for i in l for j in l if i!=j)

def simple_tsp(s, e, M):
    n = len(M)
    dp = [[inf]*(2**n) for i in range(n)]
    for i in range(n):
        dp[i][1<<i] = s[i]
    for h, cur in highbit_range(n):
        for last, last2 in last_two_bits(h, cur):
            prev = cur^(1<<last)
            dp[last][cur] = min(dp[last2][prev]+M[last2][last], dp[last][cur])
    complete = (1<<n)-1
    return min(dp[last][complete]+e[last] for last in range(n))

#s = simple_tsp([1,2,3], [3,4,5], [[0,4,2],[4,0,2],[2,2,0]])
n = 15
from numpy import arange
import time
start = time.perf_counter()
s = simple_tsp(arange(n), arange(n), arange(n*n).reshape(n, n))
end = time.perf_counter()
print(s, end-start)
