import hashlib
import random

def is_prime(a):
    if a < 2:
        return False
    for i in range(2, int(a**0.5) + 1):
        if a % i == 0:
            return False
    return True

def gcd(a, m):
    while m != 0:
        a, m = m, a % m
    return a

def add(m, n, p, a):
    if m == (float('inf'), float('inf')):
        return n
    if n == (float('inf'), float('inf')):
        return m
    x1, y1 = m
    x2, y2 = n
    if m != n:
        if (x1 - x2) % p == 0:
            return (float('inf'), float('inf'))
        else:
            k = ((y1 - y2) * gcd(x1 - x2, p)) % p
    else:
        k = ((3 * (x1 ** 2) + a) * gcd(2 * y1, p)) % p
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return x3, y3

def multiply(n, l, p, a):
    result = (float('inf'), float('inf'))
    while n > 0:
        if n % 2 == 1:
            result = add(result, l, p, a)
        l = add(l, l, p, a)
        n //= 2
    return result

def ecdsa_sign(m, n, G, d, k, p, a):
    e = int(hashlib.sha256(m.encode()).hexdigest(), 16)
    R = multiply(k, G, p, a)
    r = R[0] % n
    s = (gcd(k, n) * (e + d * r)) % n
    return r, s

def ecdsa_verify(m, n, G, r, s, P, p, a):
    e = int(hashlib.sha256(m.encode()).hexdigest(), 16)
    w = gcd(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = add(multiply(v1, G, p, a), multiply(v2, P, p, a), p, a)
    if w == (float('inf'), float('inf')):
        print('false')
    else:
        if w[0] % n == r:
            print('true')
        else:
            print('false')

a = 2
b = 18
p = 17
m = 'hello'
G = (5, 1)
n = 19
k = 2
d = 5
P = multiply(d, G, p, a)
r, s = ecdsa_sign(m, n, G, d, k, p, a)
print("签名为:", r, s)
print("验证结果：")
ecdsa_verify(m, n, G, r, s, P, p, a)
