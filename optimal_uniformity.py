"""Find the most uniform subset of a given set

According to Rearrangement inequality (排序不等式),
two set of numbers has the minimum L2 error:

    sum_i (x_i-y_i)**2= sum_ x_i**2 + sum_i y_i**2 - 2 sum_i x_i y_i

when both arrays are sorted.

So this is simplified to a DP problem like 0-1 knapsack problem
"""
inf = float('inf')
def optimal_uniformity(nums, k):
    """nums is sorted"""
    if len(nums) <= k:
        return nums
    s, e = nums[0], nums[-1]
    x = nums[1:-1]
    y = [s + i*(e-s)/(k-1) for i in range(1, k-1)]
    m, n = len(x), len(y)
    # select a set of x to match y
    cost = [inf if i else 0 for i in range(n+1)]
    pick = set()
    for i, a in enumerate(x):
        for j in range(n-1, -1, -1):
            pick_cost = (y[j]-a)**2 + cost[j]
            if pick_cost < cost[j+1]:
                cost[j+1] = pick_cost
                pick.add((j, i))
    # reconstruct the optimal solution
    j, i = n-1, m-1
    path = []
    while j >= 0 and i >= 0:
        if (j,i) in pick:
            path.append(x[i])
            j -= 1
        i -= 1
    return path[::-1], cost[n]

print(optimal_uniformity([0,2,3,4,53,100], 3))

print(optimal_uniformity([0,2,3,20,53,66,100], 4))

print(optimal_uniformity([0,1,2,3,4,100], 5))
