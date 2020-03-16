def common_prefix(s, t):
    i = 0
    L = min(len(s), len(t))
    while i < L and (s[i]==t[i] or t[i]=='.'):
        i += 1
    return i

def left_stamps(stamp, target):
    offset = 0
    lseq = []
    high = []
    target = list(target)
    while len(target[offset:])>=len(stamp):
        print(target[offset:])
        l = common_prefix(stamp, target[offset:])
        lseq.append(offset)
        if l < len(stamp):
            offset += l if target[offset]!='.' else 1
        else:
            for i in range(offset+1, offset+l):
                target[i] = '.'
            offset += 1
    return lseq