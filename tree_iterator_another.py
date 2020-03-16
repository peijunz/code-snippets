class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    @staticmethod
    def build_bst(arr, start=0, end=None):
        if end==None: end = len(arr)
        if start == end:
            return None
        mid = (start+end)//2
        root = TreeNode(arr[mid])
        root.left = TreeNode.build_bst(arr, start, mid)
        root.right = TreeNode.build_bst(arr, mid+1, end)
        return root

    def __repr__(self):
        val = self.val
        lval = self.left.val if self.left else None
        rval = self.right.val if self.right else None
        return "({} -> ({}, {}))".format(val, lval, rval)

    def head(self):
        cur, stack = self, []
        while cur:
            stack.append(cur)
            cur = cur.left
        return TreeIterator(stack)

    def tail(self):
        cur, stack = self, []
        while cur:
            stack.append(cur)
            cur = cur.right
        return TreeIterator(stack)

    def end(self):
        return TreeIterator([])

class TreeIterator:
    def __init__(self, stack):
        self.stack = stack

    def __eq__(self, rhs):
        return self.stack == rhs.stack

    def prev(self):
        if self.stack and self.stack[-1].left:
            self.stack.append(self.stack[-1].left)
            while self.stack[-1].right:
                self.stack.append(self.stack[-1].right)
        else:
            last = None
            while self.stack and self.stack[-1].left == last:
                last = self.stack.pop()
    def next(self):
        if self.stack and self.stack[-1].right:
            self.stack.append(self.stack[-1].right)
            while self.stack[-1].left:
                self.stack.append(self.stack[-1].left)
        else:
            last = None
            while self.stack and self.stack[-1].right == last:
                last = self.stack.pop()

    def val(self):
        if self.stack:
            return self.stack[-1].val

if __name__ == "__main__":
    vals = [i+1 for i in range(7)]
    tree = TreeNode.build_bst(vals)
    it, end = tree.head(), tree.end()
    for i in range(6):
        print(it.val())
        it.next()
    for i in range(7):
        print(it.val())
        it.prev()
