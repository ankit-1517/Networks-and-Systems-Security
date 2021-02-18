import sys
import math
from random import randint
from fractions import gcd

def primes(n):
	b = [True] * (n + 1)
	for p in range(2, n + 1):
		if b[p]:
			for i in range(p, n + 1, p):
				b[i] = False
			yield p
	return

def modular_inv(a, b):
	if b == 0:
		return 1, 0, a
	q, r = divmod(a, b)
	x, y, g = modular_inv(b, r)
	return y, x - q * y, g

def elliptic_add(p, q, a, b, m):
	if p[2] == 0: return q
	if q[2] == 0: return p
	if p[0] == q[0]:
		if (p[1] + q[1]) % m == 0:
			return 0, 1, 0  # Infinity
		num = (3 * p[0] * p[0] + a) % m
		denom = (2 * p[1]) % m
	else:
		num = (q[1] - p[1]) % m
		denom = (q[0] - p[0]) % m
	inv, _, g = modular_inv(denom, m)
	if g > 1:
		return 0, 0, denom  # failed
	z = (num * inv * num * inv - p[0] - q[0]) % m
	return z, (num * inv * (p[0] - z) - p[1]) % m, 1

def elliptic_mul(k, p, a, b, m):
	r = (0, 1, 0)  # Infinity
	while k > 0:
		if p[2] > 1:
			return p
		if k % 2 == 1:
			r = elliptic_add(p, r, a, b, m)
		k = k // 2
		p = elliptic_add(p, p, a, b, m)
	return r

def lenstra(n, limit):
	# check if its a square
	sqr = int(math.sqrt(n))
	if sqr**2 == n:
		return sqr
	
	# else, continue with normal lenstra factorisation
	g = n
	while g == n:
		q = randint(0, n - 1), randint(0, n - 1), 1
		a = randint(0, n - 1)
		b = (q[1] * q[1] - q[0] * q[0] * q[0] - a * q[0]) % n
		g = gcd(4 * a * a * a + 27 * b * b, n)
	if g > 1:
		return g
	for p in primes(limit):
		pp = p
		while pp < limit:
			q = elliptic_mul(p, q, a, b, n)
			if q[2] > 1:
				return gcd(q[2], n)
			pp = p * pp
	return False

def main():
	if len(sys.argv) < 2:
		print("Pass n. Usage: python3 <name> n")
		exit(0)
	print(lenstra(int(sys.argv[1]), 100000000))

if __name__ == '__main__':
	main()
