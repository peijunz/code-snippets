# size of grid
N = 1000000

def sign(x):
    return (x>0) - (x<0)

class Solution:
    def online(self, p):
        return ((p[0] == self.X and self.y[0] <= p[1] <= self.y[1])
                or
                (p[1] == self.Y and self.x[0] <= p[0] <= self.x[1]))

    def inside(self, p):
        return sign(p[0] - self.X) == self.xsign and sign(p[1] - self.Y) == self.ysign

    def step_cross(self, cur, nxt):
        if self.online(cur):
            return int(self.inside(nxt))
        if self.online(nxt):
            return -int(self.inside(cur))
        return 0

    def neighbors(self, cur):
        if cur == (-1, -1):
            for k, v in self.boundary_cross.items():
                yield k, v
        else:
            x, y = cur
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if (dx==0 and dy==0):
                        continue
                    crossed = self.step_cross(cur, (x+dx, y+dy))
                    if not (0<=x+dx<N and 0<=y+dy<N):
                        n = (-1, -1)
                    else:
                        n = (x+dx, y+dy)
                    if n in self.block_set:
                        yield n, crossed

    def set_boundary(self):
        self.boundary_cross = {}
        self.block_set.add((-1, -1))
        for b in self.blocked:
            if (1<=b[0]<N-1 and 1<=b[1]<N-1):
                continue
            for n,c in self.neighbors(b):
                if n==(-1, -1):
                    self.boundary_cross[tuple(b)] = -c
        self.blocked.append([-1, -1])
        self.blocked = map(tuple, self.blocked[::-1])

    def set_line(self):
        self.X = self.src[0]
        self.Y = self.dst[1]
        self.x = tuple(sorted((self.src[0], self.dst[0])))
        self.y = tuple(sorted((self.src[1], self.dst[1])))
        self.xsign = sign((self.x[0]+self.x[1])/2-0.1 - self.X)
        self.ysign = sign((self.y[0]+self.y[1])/2-0.1 - self.Y)
        
    def isEscapePossible(self, blocked, source, target):
        self.blocked = blocked
        self.block_set = set(map(tuple, blocked))
        self.src = tuple(source)
        self.dst = tuple(target)

        self.set_line()
        self.set_boundary()

        visit_cnt = {}
        for b in self.blocked:
            if b in visit_cnt:
                continue
            stack = [b]
            visit_cnt[b] = 0
            while stack:
                cur = stack.pop()
                for n, c in self.neighbors(cur):
                    if n in visit_cnt:
                        if visit_cnt[n] != visit_cnt[cur] + c:
                            return False
                    else:
                        visit_cnt[n] = visit_cnt[cur] + c
                        stack.append(n)
        return True

s = Solution()

print(s.isEscapePossible([[0,2],[2,0],[1,1]], [0,0], [2,2]))
print(s.isEscapePossible([[0,2],[2,0],[1,0]], [0,0], [2,2]))
