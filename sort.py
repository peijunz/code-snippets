def insertion_sort(l):
    L = len(l)
    for i in range(1, L):
        j = i
        while j>0 and l[j-1] > l[j]:
            l[j-1], l[j] = l[j], l[j-1]
            j -= 1
    return l

def sieve_down(l, j, L):
    while j < L//2:
        if (j<<1)+2<L and (l[(j<<1)+2] > l[(j<<1)+1]):
            k = (j<<1) + 2
        else:
            k = (j<<1) + 1
        if l[j] < l[k]:
            l[j], l[k] = l[k], l[j]
            j = k
        else:
            break

def max_heapify(l, L):
    for i in range(L//2-1, -1, -1):
        sieve_down(l, i, L)
    return l

def heap_sort(l):
    L = len(l)
    max_heapify(l, L)
    for i in range(L-1, 0, -1):
        l[i], l[0] = l[0], l[i]
        sieve_down(l, 0, i)
    return l
