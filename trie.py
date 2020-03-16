class Trie:
    def __init__(self, root=None):
        if root is None:
            self.root = dict()
        else:
            self.root = root

    def add(self, s):
        T = self.root
        for c in s:
            if c not in T:
                T[c] = dict()
            T = T[c]
        T[''] = True

    def __getitem__(self, s):
        T = self.root
        for c in s:
            if c not in T:
                return None
            T = T[c]
        return T

    def __contains__(self, s):
        sub = self[s]
        return (sub is not None) and ('' in sub)

    def matches(self, s):
        T = self.root
        for i, c in enumerate(s):
            if c not in T:
                return None
            T = T[c]
            if '' in T:
                yield i+1

    def firstmatch(self, s):
        for i in self.matches(s):
            return i

    def __repr__(self):
        return "Trie({})".format(repr(self.root))

if __name__ == "__main__":
    trie = Trie()
    trie.add('hell')
    trie.add('hello,')
    trie.add('he')
    assert 'he' in trie
    assert 'hell' in trie
    assert 'hel' not in trie
    assert '' not in trie
    s = 'hello, world'
    for i in trie.matches(s):
        print('Found prefix', s[:i])
    print(trie)
    print(trie['hell'])
