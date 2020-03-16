from numpy import array, eye

fib = array([[0,1], [1,1]])
init = array([0, 1])

def fast_pow(M, n):
    ans = eye(len(M), dtype='int')
    while n:
        if n&1:
            ans = ans@M
        n//=2
        M = M@M
    return ans

def fast_fib(n):
    cur = fast_pow(fib, n)@init
    return cur[0]

if __name__ == "__main__":
    for i in range(10):
        print(i, fast_fib(i))
