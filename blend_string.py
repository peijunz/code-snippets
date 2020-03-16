def blend(p, q, s):
    m, n = len(p), len(q)
    # V[i][j] means s[:i+j] could be blended by p[:i], q[:j]
    V = [[False]*(n+1) for i in range(m+1)]
    V[0][0] = True
    for i in range(1, m+1):
        V[i][0] = V[i-1][0] and s[i-1]==p[i-1]
    for j in range(1, n+1):
        V[0][j] = V[0][j-1] and s[j-1]==q[j-1]
    for i in range(1, m+1):
        for j in range(1, n+1):
            V[i][j] |= V[i][j-1] and s[i+j-1]==q[j-1]
            V[i][j] |= V[i-1][j] and s[i+j-1]==p[i-1]
    return V[m][n]

blend("hello", "world", 'heworllold')