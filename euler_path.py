from collections import defaultdict, Counter
def odd_vertices(G, directed=False):
    """G is connected"""
    if directed:
        c = Counter()
        for cur, dests in G.items():
            for dest in dests:
                c[cur] += 1
                c[dest] -= 1
        return [(cur, degree>0) for cur, degree in c.items() if degree%2 == 1]
    else:
        return [cur for cur, dest in G.items() if len(dest)%2 == 1]

def euler_path(g, start, bi=False):
    stack, route = [start], []
    while stack:
        cur = stack[-1]
        if g[cur]:
            dest = g[cur].pop()
            if bi: g[dest].remove(cur)
            stack.append(dest)
        else:
            route.append(cur)
            stack.pop()
    return route[::-1]


def password_graph(n, k):
    edges = [0]
    M = k**(n-1)
    for i in range(n):
        edges = [s*k+tail for s in edges for tail in range(k)]
    G = defaultdict(set)
    for e in edges:
        G[e//k].add(e%M)
    return G

def crack(n, k):
    if n==1: return ''.join(str(i) for i in range(k))
    G = password_graph(n, k)
    path = euler_path(G, 0)
    tails = [str(i%k) for i in path]
    return "0"*(n-2)+''.join(tails)

crack(10, 2)