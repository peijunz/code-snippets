import math
class Solution:
    def enough_time(self, boxes, m, t):
        idle = 0
        n = len(boxes)
        for x, b in zip(range(n, 0, -1), boxes[::-1]):
            reuse = min(idle, b)
            q = math.ceil((b-reuse)/(t-x))
            r = q*(t-x) - (b-reuse)
            m -= q
            idle = idle - reuse + r
            if m < 0: return False
        return True
    def min_time_move_box(self, boxes, m):
        n = len(boxes)
        left = n + 1
        right = sum(boxes)//m+n+1
        while left < right:
            mid = (left + right)//2
            if not self.enough_time(boxes, m, mid):
                left = mid + 1
            else:
                right = mid
        return left
print(Solution().min_time_move_box([3,5,2,7], 5))