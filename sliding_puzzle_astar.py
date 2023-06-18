def make_tuples(x):
    return tuple(tuple(row) for row in x)

def make_lists(x):
    return list(list(row) for row in x)

def locate_zero(puzzle):
    m,n = len(puzzle), len(puzzle[0])
    for i in range(m):
        for j in range(n):
            if puzzle[i][j] == 0:
                return i,j

def neighbors(puzzle, i, j):
    puzzle = make_lists(puzzle)
    m,n = len(puzzle), len(puzzle[0])
    for di,dj in [(0,1),(0,-1),(-1,0),(1,0)]:
        if not (0<=i+di<m and 0<=j+dj<n):
            continue
        puzzle[i][j], puzzle[i+di][j+dj] = puzzle[i+di][j+dj], puzzle[i][j]
        yield make_tuples(puzzle), (i+di, j+dj), 
        puzzle[i][j], puzzle[i+di][j+dj] = puzzle[i+di][j+dj], puzzle[i][j]

def manhattan_distance(p, q):
    return sum(abs(x-y) for x,y in zip(p,q))

def distance_from(puzzle):
    m,n = len(puzzle), len(puzzle[0])
    locs = [0]*(m*n)
    for i in range(m):
        for j in range(n):
            locs[puzzle[i][j]] = (i, j)
    def distance_to(dest):
        distance = 0
        for i in range(m):
            for j in range(n):
                if dest[i][j] == 0:
                    continue
                distance += manhattan_distance((i,j), locs[dest[i][j]])
        return distance
    return distance_to

from functools import reduce
from operator import add
def parity(puzzle):
    m,n = len(puzzle), len(puzzle[0])
    flat = list(reduce(add, puzzle))
    index = {x:i for i,x in enumerate(flat)}
    swaps = 0
    for i in range(m*n):
        swaps += (flat[i] != i)
        j = index[i]
        index[flat[i]] = j
        flat[j] = flat[i]
    return (swaps + sum(locate_zero(puzzle)))%2==0

def astar_solve(puzzle, dest):
    heuristic = distance_from(dest)
    if parity(puzzle) != parity(dest):
        return -1, []
    heap = [(heuristic(puzzle), make_tuples(puzzle), locate_zero(puzzle), None)]
    visited = {}
    while heap:
        if heap[0][1] in visited:
            heapq.heappop(heap)
            continue
        dist, puzzle, loc, src = heapq.heappop(heap)
        g_puzzle = dist - heuristic(puzzle)
        visited[puzzle] = (g_puzzle, src)
        if heuristic(puzzle) == 0:
            break
        for neighbor, nei_loc in neighbors(puzzle, *loc):
            if neighbor not in visited:
                heapq.heappush(heap, (g_puzzle+1+heuristic(neighbor), neighbor, nei_loc, puzzle))
    answer = visited[dest][0]
    path = []
    while dest:
        path.append(dest)
        g, dest = visited[dest]
    return answer, path[::-1]
    
class Solution:
    def slidingPuzzle(self, puzzle: List[List[int]]) -> int:
        return astar_solve(puzzle, ((1,2,3),(4,5,0)))[0]
