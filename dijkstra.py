inf = float('inf')

def pop_min(grey):
    """用 min 函数拿到最小的 u,d 组合"""
    u, d = min(grey.items(), key=lambda u_d: u_d[1])
    del grey[u]
    return u, d
    
def dijkstra_slow(G, start):
    """Run Dijkstra from a starting point
    
    复杂度是 O(V*V + E) = O(V*V)，因为 E <= V(V-1)/2
    """
    # black 已经展开，也就是确定是最短距离了
    # grey  待展开
    black = {}
    grey = {start: 0}
    while grey:
        # 灰色的最接近起点的可以转化为黑色
        u, d_u = pop_min(grey)
        black[u] = d_u
        for v, d_uv in G[u].items():
            if v not in black:
                grey[v] = min(grey.get(v, inf), d_u + d_uv)
    return black

if __name__ == "__main__":
    G = {
        1: {2:5, 3:6, 4:10},
        2: {1:5, 4:3},
        3: {1:6, 4:1},
        4: {1:10, 2: 3, 3:1},
        }
    print(dijkstra_slow(G, start=1))
