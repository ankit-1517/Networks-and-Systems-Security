import sys
import math
import time
import random
from fractions import gcd
from sympy.ntheory import factorint

def publicKey(phi):
	while True:
		e = random.randint(0, phi-1)
		if gcd(e, phi) == 1:
			return e
	return -1

def inverse(a, b):
	if a == 0:
		return 0
	if b%a == 0:
		return 1
	return b - inverse(b%a, a)*b//a

def privateKey(phi, e):
	return inverse(e, phi)

def fastExp(a, po, n):
    if po == 0:
      return 1
    x = fastExp(a, po//2, n)
    x = (x*x)%n
    if po%2 == 1:
      x = x*a
    return x%n

def encrypt(M, e, n):
	return fastExp(M, e, n)

def decrypt(C, d, n):
	return fastExp(C, d, n)

def textToNum(text, n):
	nums = []
	for i in range(len(text)):
		nums.append(str(ord(text[i])))
	
	for i in range(len(nums)):
		while len(nums[i]) < 3:
			nums[i] = "0" + nums[i]

	l = []
	s = ""
	for i in range(len(nums)):
		if int(s + nums[i]) >= n:
			l.append(int(s))
			s = nums[i]
		else:
			s += nums[i]
	l.append(int(s))
	return l

def numToText(ls):
	l = [str(x) for x in ls]
	text = ""
	for i in range(len(l)):
		while len(l[i])%3 != 0:
			l[i] = "0" + l[i]
	for x in l:
		for i in range(0, len(x), 3):
			asc = int(x[i:i+3])
			text += chr(asc)
	return text

def rsa(n, factors):
	s = 0
	fac = []
	for x in factors:
		s += factors[x]
		for i in range(factors[x]):
			fac.append(x)
	if s != 2:
		print("Input not valid as it has {} factors".format(s))
		return
	p, q = fac[0], fac[1]
	if p == q:
		print("Input invalid as it is a square: {}*{}".format(p, p))
		return
	phi = (p-1)*(q-1)
	e = publicKey(phi)
	d = privateKey(phi, e)

	plainText = "haha, I can encode stuff that you cannot decode"
	numbers = textToNum(plainText, n)
	encryptedNums = [encrypt(x, e, n) for x in numbers]
	decryptedNums = [decrypt(x, d, n) for x in encryptedNums]
	text = numToText(decryptedNums)
	print("p =", p)
	print("q =", q)
	print("e =", e)
	print("d =", d)
	print("\nM (as list of concatenated integers) =", encryptedNums)
	print("\nC (as list of concatenated integers) =", decryptedNums)

def main():
	if len(sys.argv) != 2:
		print("Invalid usage. Pass n. Usage: python3 <name> n")
		exit(0)
	random.seed(0)
	n = int(sys.argv[1])
	
	# factorization step
	t1 = time.perf_counter()
	factors = factorint(n)
	t2 = time.perf_counter()
	print("Time taken:", t2-t1)

	rsa(n, factors)

if __name__ == '__main__':
	main()
