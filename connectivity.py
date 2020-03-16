from collections import defaultdict
class Solution:
    def criticalConnections(self, n, connections):
        G = defaultdict(list)
        for a,b in connections:
            G[a].append(b)
            G[b].append(a)
        time = 0
        visited, disc, low = [0]*n, [0]*n, [0]*n
        bridges, articulation = [], set()
        def dfs(x, p):
            nonlocal time
            visited[x] = True
            disc[x] = low[x] = time
            time += 1
            components = p>=0
            for nei in G[x]:
                if nei == p: continue
                new = not visited[nei]
                components += new
                if new:
                    dfs(nei, x)
                    if low[nei] > disc[x]:
                        bridges.append([x, nei])
                    if low[nei] >= disc[x] and components>=2:
                        articulation.add(x)
                low[x] = min(low[x], low[nei])
        dfs(0, -1)
        return bridges