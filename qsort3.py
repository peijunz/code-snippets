from numpy.random import randint
def partition(a, start=0, end=None, pivot=None):
    if end is None: end = len(a)
    if pivot is None: pivot = a[randint(start, end)]

    i,j,k = start,start,end
    while j<k:
        if a[j] > pivot:
            a[j],a[k-1]=a[k-1],a[j]
            k-=1
        elif a[j] < pivot:
            a[i],a[j]=a[j],a[i]
            i+=1
            j+=1
        else:
            j+=1
    return pivot,i,j

def qsort(a, start=0, end=None):
    if end is None: end = len(a)
    if end-start<=1: return

    p,i,j=partition(a, start, end)
    qsort(a, start,i)
    qsort(a, j, end)

a = [1,5,3,1,65,25,4,21,4,83,1,91,3,47,8,9,1]

partition(a,5,9)

qsort(a)

print(a)