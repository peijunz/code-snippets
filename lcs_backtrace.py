def LCSeq(s, t):
    dp = [[0 for j in range(len(t)+1)] for i in range(len(s)+1)]
    for i in range(1, len(s)+1):
        for j in range(1, len(t)+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = 1+dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp

def backtrace_dp(s, t, dp):
    i, j= len(s), len(t)
    rev = []
    while i>0 and j>0:
        if s[i-1] == t[j-1]:
            rev.append(s[i-1])
            i -= 1
            j -= 1
        else:
            if dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
    return ''.join(rev[::-1])

s, t = 'hello', 'heo'
dp = LCSeq(s, t)

backtrace_dp(s, t, dp)