'''Gaussian elimination method to solve linear equation or invert matrix'''
import numpy as np
import itertools as it
from fractions import Fraction

Fraction.__repr__ = Fraction.__str__
fractize = np.vectorize(Fraction)

def triangulate(M):
    ortho = []
    space = []
    n = M.shape[0]
    type_ = M[0, 0].__class__
    for x in range(n):
        rems = list(range(x, n)) + ortho
        for i in rems:
            if M[i, x] != 0:
                break
        if M[i, x] == 0:
            M[x, x] = type_(-1)
            ortho.append(x)
            continue
        space.append(x)
        if x != i:
            M[[i, x]] = M[[x, i]]

        p = 1/M[x, x]
        if p is None:
            M[x, x:] /= M[x, x]
        else:
            M[x, x:] *= p

        for i in rems[1:]:
            M[i, x:] -= M[x, x:]*M[i, x]
    return ortho, space


def solve_triangular(M, b=None, space=None, ortho=()):
    if b is not None:
        M = np.hstack((M, b))
    n = M.shape[0]
    if space is None:
        space = list(reversed(range(M.shape[0])))
    for k, x in enumerate(space):
        if M[x, x] != 1:
            M[x, x:] /= M[x, x]
        for i in space[k+1:]:
            # Equivalent to but less operations:
            # M[i, x:] -= M[x, x:]*M[i, x]
            cols = [j for j in ortho if j>x]
            if cols:
                M[i, cols] -= M[x, cols]*M[i, x]
            M[i, n:] -= M[x, n:]*M[i, x]
            M[i, x] = M[0, 0].__class__(0)
    return M[:, :n], M[:, n:]


def linear_solver(A, b):
    '''Solve linear equations Ax=b with Gaussian elimination
    Args:
        A   Transformation matrix
        b   Inhomogenous term
    Return:
        ortho   The index that is not linearly independent
        solution
        kernel  The orthogonal complementary space of A

    Ref:
        https://en.wikipedia.org/wiki/Orthogonal_complement
        https://en.wikipedia.org/wiki/Kernel_(linear_algebra)
    '''
    n = A.shape[0]
    M = np.hstack((A, b.reshape(n, -1)))
    ortho, space = triangulate(M)
    space.reverse()
    solve_triangular(M, space=space, ortho=ortho)
    return ortho, M[:, n:], M[:, ortho]


def apply_sol(sol, b):
    '''Apply solution to inhomogenous vector term b
    Args:
        sol     Solution returned by linear_solver
        b       inhomogenous vector term
    Return:
        res     solution vector
        ortho   General solution
    '''
    ortho, M, ker = sol
    print(M, b)
    res = np.dot(M, b)#np.einsum('ij, j->i', M, b)
    if not all(res[ortho] == 0):
        return None, ker
    return res, ker


def invr(m):
    '''Invert matrix with null space l'''
    im = np.vectorize(m[0, 0].__class__)(np.eye(m.shape[0], dtype='int'))
    return linear_solver(m, im)


def test_elimination():
    a = np.array([[1, 1, 1, 1],
                  [0, 0, 1, 1],
                  [0, 0, 3, 3],
                  [0, 0, 2, 2]], dtype='double')
    a = fractize(a)
    ortho, sol, ker = invr(a)
    print("Null space", ortho)
    print("Solution", sol, sep='\n')
    print("Kernel space", ker, sep='\n')


if __name__ == "__main__":
    test_elimination()
