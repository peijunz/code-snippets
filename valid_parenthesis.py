def accumulate(L):
    D, tot = 0, 0
    for D_sub, tot_sub in L:
        D = max(D, tot+D_sub)
        tot += tot_sub
    return D, tot # max diff and cumulated diff

def valid_parenthesis(s):
    C = 2
    ans = [(1,1) if c==')' else (-1, -1)  for c in s]
    while len(ans) > 1:
        ans = [accumulate(ans[start:start+C]) for start in range(0, len(ans), C)]
    D, cur = ans[0]
    return D==0 and cur==0
  
valid_parenthesis("()((()())")
valid_parenthesis("()(((())))")