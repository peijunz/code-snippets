def linear_sieve(n):
    primes = []
    factor = [i for i in range(n+1)]
    for i in range(2, n+1):
        if factor[i] == i:
            primes.append(i)
        for p in primes:
            if p > factor[i] or p*i >= n+1:
                break
            # Executed for count of composite numbers times
            factor[p*i] = p
    return factor, primes

print(len(linear_sieve(1000000)[1]))

print(1000000/log(1000000))
