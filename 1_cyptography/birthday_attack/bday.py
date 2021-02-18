import hashlib 
import string
import random
import sys

def randomString(size):
	chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
	return ''.join(random.choice(chars) for _ in range(size))

def getHash(s):
	encoded_str = s.encode()
	return hashlib.sha3_256(encoded_str).hexdigest()

def charToBits(c):
	n = ord(c)
	if n >= ord('a') and n <= ord('f'):
		n = n - ord('a') + 10
	else:
		n -= ord('0')
	l = []
	while n > 0:
		l.append(n%2)
		n = n//2
	while len(l) < 4:
		l.append(0)
	l.reverse()
	return l

def stringToBits(s, bits):
	l = []
	for x in s:
		l += bits[x]
	return l

def check(l1, l2, d):
	for i in range(d):
		if l1[i] != l2[i]:
			return False
	return True

def hashMatch(s1, s2, bits, d):
	l1 = stringToBits(getHash(s1), bits)
	l2 = stringToBits(getHash(s2), bits)
	return check(l1, l2, d)

def getTuple(d):
	l = "0123456789abcdef"
	bits = {}
	for x in l:
		bits[x] = charToBits(x)
	n = (d+1)//2
	n = 2**n
	msgLength = 0
	while 62**msgLength < n**2:
		msgLength += 1
	attempt = 0
	while True:
		l = []
		while len(l) < n:
			l.append(randomString(msgLength))
		for i in range(len(l)):
			for j in range(i+1, len(l)):
				attempt += 1
				if hashMatch(l[i], l[j], bits, d):
					if l[i] != l[j]:
						return (l[i], l[j], getHash(l[i]), getHash(l[j]), sys.getsizeof(l)*8, attempt)

def main():
	if len(sys.argv) < 2:
		print("Pass d. Usage: python3 <name> d")
		exit(0)
	d = int(sys.argv[1])
	random.seed(0)
	print(d, getTuple(d))

if __name__ == '__main__':
    main()
