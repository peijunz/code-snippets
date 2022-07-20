from typing import Callable

def bisect(predicate: Callable[[int], bool], left: int, right: int):
    """Search the smallest x in [left, right) such that predicate(x) is True"""
    while left < right:
        mid = (left + right)//2
        if not predicate(mid):
            left = mid + 1
        else:
            right = mid
    return left

def sqrt_ceil(n):
    return bisect(lambda x: x*x >= n, 0, n)

if __name__ == "__main__":
    for i in range(10):
        print(i, sqrt_ceil(i))
