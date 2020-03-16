""" Establish ordering between sets. lc711 """
def cmp_set(s, t):
    if len(s) != len(t):
        return len(s) - len(t)
    S, T = set(s), set(t)
    sym_diff = S.symmetric_difference(T)
    if not sym_diff: return 0
    mini = min(sym_diff)
    return -1 if mini in S else 1

def std_island(blocks):
    xmin = min(b[0] for b in blocks)
    ymin = min(b[1] for b in blocks)
    blocks = [(b[0]-xmin, b[1]-ymin) for b in blocks]
    width = max(b[0] for b in blocks)
    height = max(b[1] for b in blocks)
    std = blocks
    for i in range(4):
        blocks = [(b[1], b[0]) for b in blocks]
        width, height = height, width
        #print(blocks)
        if cmp_set(std, blocks) > 0:
            std = blocks
        blocks = [(b[0], height - b[1]) for b in blocks]
        #print(blocks)
        if cmp_set(std, blocks) > 0:
            std = blocks
    return std
if __name__ == "__main__":
    print(std_island([(3,3), (4,3), (5,3), (4, 4)]))
