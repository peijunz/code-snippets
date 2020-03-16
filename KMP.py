def prefix_function(s):
    # P[i] is Longest prefix length of s[:i]
    L = len(s)
    P = [0 for i in range(L+1)]
    prefix_length = 0
    for length in range(2, L+1):
        while prefix_length >0 and s[prefix_length-1] != s[length-1]:
            prefix_length = P[prefix_length]
        P[length] = prefix_length
        prefix_length +=1
    return P

def kmp_iterator(s, p, P=None):
    if P is None:
        P = prefix_function(p)
    L = len(s)
    prefix_length = 1
    todo = 0
    for todo in range(1, L+1):
        while prefix_length != 0 and p[prefix_length-1] != s[todo-1]:
            prefix_length = P[prefix_length]
        yield todo, prefix_length
        if prefix_length >= len(p):
            prefix_length = P[prefix_length]
        prefix_length += 1

def kmp_match_all(s, p):
    return [i-len(p) for i, pref in kmp_iterator(s, p) if len(p)==pref]

def kmp_match_once(s, p):
    for i, pref in kmp_iterator(s, p):
        if len(p)==pref:
            return i-len(p)

def min_period(s):
    p = prefix_function(s)[-1]
    if len(s)%(len(s)-p) == 0:
        return len(s)-p
    else:
        return len(s)

def tail_palindromes(s):
    P = prefix_function(s[::-1])
    result = list(kmp_iterator(s, s[::-1], P))
    if not result: return []
    l = []
    length = result[-1]
    while length>0:
        l.append(length)
        length = P[length]
    return l

if __name__ == "__main__":
    print(tail_palindrome('abadaba'))
    print(kmp_match_all('abcabcabc', 'abc'))
    print(kmp_match_once('abcabcabc', 'abc'))
    print(min_period('abcabcabcabc'))