class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        lval = self.left.val if self.left else None
        rval = self.right.val if self.right else None
        return "{} -> ({}, {})".format(self.val, lval, rval)
    def __str__(self):
        return repr(self)

class TreeStateTransition:
    start = 0
    end = 3
    def __init__(self, left=0, right=1, visit=2):
        self.left = left
        self.right = right
        self.visit = visit
    def forward(self, state):
        return state + 1


class Traversal:
    pre_order = TreeStateTransition(visit=0, left=1, right=2)
    in_order = TreeStateTransition(left=0, visit=1, right=2)
    post_order = TreeStateTransition(left=0, right=1, visit=2)
    def __init__(self, T, states=None):
        if states is None:
            states = self.pre_order
        self.states = states
        self.flag = False
        self.stack = [[T, self.states.start]]

    def has_elem(self):
        while not self.flag and self.stack:
            cur = self.stack[-1]
            if cur[0] is None or cur[-1] == self.states.end:
                self.stack.pop()
                continue
            if cur[-1] == self.states.visit:
                self.flag = True
            elif cur[-1] == self.states.left:
                self.stack.append([cur[0].left, self.states.start])
            elif cur[-1] == self.states.right:
                self.stack.append([cur[0].right, self.states.start])
            cur[-1] = states.forward(cur[-1])
        return self.flag

    def __iter__(self):
        return self

    def __next__(self):
        if self.has_elem():
            self.flag = False
            return self.stack[-1][0]
        else:
            raise StopIteration

def naive_tree(L):
    """Build Tree like
              0  
         1         2
       3   4     5   6
    """
    nodes = [TreeNode(i) for i in range(L)]
    for i, e in enumerate(nodes):
        if 2*i+1<L:
            e.left = nodes[2*i+1]
        if 2*i+2<L:
            e.right = nodes[2*i+2]
    return nodes[0]

if __name__ == "__main__":
    root = naive_tree(7)
    for states in [Traversal.pre_order, Traversal.in_order, Traversal.post_order]:
        it = Traversal(root, states)
        for i in it:
            print(i.val, end=', ')
        print()