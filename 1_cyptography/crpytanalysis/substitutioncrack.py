import sys

def decrText(s, key, c):
	ans = ""
	for x in s:
		if x not in c:
			ans += x
			continue
		flag = True
		for y in key:
			if key[y] == x:
				ans += y
				flag = False
				break
		if flag:
			ans += x
	return ans

def frequency_1(s, cipher):
	cipher_cnt = {}
	for x in cipher:
		cipher_cnt[x] = 0
	for x in s:
		if x in cipher:
			cipher_cnt[x] += 1
	cnt = []
	for x in cipher_cnt:
		cnt.append([cipher_cnt[x], x])
	cnt.sort(reverse = True)
	print("Most frequent letters: E, T, A, O, I")
	print(cnt[0:min(10, len(cnt))])
	print("\n")

def getWords(s, cipher, n):
	l = []
	a = ""
	for x in s:
		if x in cipher:
			a += x
		else:
			if len(a) == n:
				l.append(a)
			a = ""
	if len(a) == n:
		l.append(a)
	return l

def frequency_2(s, cipher):
	l = getWords(s, cipher, 2)
	cipher_cnt = {}
	for x in l:
		cipher_cnt[x] = 0
	for x in l:
		cipher_cnt[x] += 1
	cnt = []
	for x in cipher_cnt:
		cnt.append([cipher_cnt[x], x])
	cnt.sort(reverse = True)
	print("Most frequent 2 letter words: OF, TO, IN, IT, IS")
	print(cnt[0:min(10, len(cnt))])
	print("\n")

def frequency_3(s, cipher):
	l = getWords(s, cipher, 3)
	cipher_cnt = {}
	for x in l:
		cipher_cnt[x] = 0
	for x in l:
		cipher_cnt[x] += 1
	cnt = []
	for x in cipher_cnt:
		cnt.append([cipher_cnt[x], x])
	cnt.sort(reverse = True)
	print("Most frequent 3 letter words: THE, AND, FOR, ARE, BUT")
	print(cnt[0:min(10, len(cnt))])
	print("\n")

def frequency_double(sfull):
	cipher_cnt_2 = {}
	for i in range(1, len(sfull)):
		if sfull[i] == sfull[i-1]:
			cipher_cnt_2[sfull[i-1:i+1]] = 0
	for i in range(1, len(sfull)):
		if sfull[i] == sfull[i-1]:
			cipher_cnt_2[sfull[i-1:i+1]] += 1
	cnt = [] 
	for x in cipher_cnt_2:
		cnt.append([cipher_cnt_2[x], x])
	cnt.sort(reverse = True)
	print("Most frequent doubles: SS, EE, TT, FF, LL, MM, OO")
	print(cnt[0:min(10, len(cnt))])
	print("\n")

def frequency_bigram(sfull):
	cipher_cnt_2 = {}
	for i in range(1, len(sfull)):
		cipher_cnt_2[sfull[i-1:i+1]] = 0
	for i in range(1, len(sfull)):
		cipher_cnt_2[sfull[i-1:i+1]] += 1
	cnt = [] 
	for x in cipher_cnt_2:
		cnt.append([cipher_cnt_2[x], x])
	cnt.sort(reverse = True)
	print("Most frequent bigrams: TH, ER, ON, AN, RE")
	print(cnt[0:min(10, len(cnt))])
	print("\n")

def frequency_trigram(sfull):
	cipher_cnt_2 = {}
	for i in range(2, len(sfull)):
		cipher_cnt_2[sfull[i-2:i+1]] = 0
	for i in range(2, len(sfull)):
		cipher_cnt_2[sfull[i-2:i+1]] += 1
	cnt = [] 
	for x in cipher_cnt_2:
		cnt.append([cipher_cnt_2[x], x])
	cnt.sort(reverse = True)
	print("Most frequent trigrams: THE, AND, THA, ENT, ION")
	print(cnt[0:min(10, len(cnt))])
	print("\n")

def without_space(s, cipher):
	sfull = ""
	for x in s:
		if x in cipher:
			sfull += x
	return sfull

def decrypt(s):
	p = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	c = "0123456789@#$nopqrstuvwxyz"
	plain = []
	cipher = []
	for x in p:
		plain.append(x)
	for x in c:
		cipher.append(x)
	key = {}
	for x in plain:
		key[x] = None
	
	frequency_1(s, cipher)
	frequency_2(s, cipher)
	frequency_3(s, cipher)
	sFull = without_space(s, cipher)
	frequency_bigram(sFull)
	frequency_trigram(sFull)
	frequency_double(sFull)
	
	count = 26
	print("Current text:", decrText(s, key, cipher))
	while count > 0:
		# print("\nCurrent text:", decrText(s, key, cipher))
		inp = input("Next mapping: ")
		if inp == "break":
			break
		if inp == "show":
			print("\nCurrent text:", decrText(s, key, cipher))
			continue
		inp = inp.split(" ")
		if len(inp) != 2:
			print("Incorrect format. Expected: show OR break OR <plainKey> <cipherKey>")
			continue
		if inp[0] in plain and inp[1] in cipher:
			key[inp[0]] = inp[1]
			count -= 1
		else:
			print("Incorrect format. Expected: show OR break OR <plainKey> <cipherKey>")
	print("\n\n--------------  FINISHED EXECUTION  --------------")
	print("Current text:", decrText(s, key, cipher))
	print("Mappings found:", 26 - count)
	print(key)
	
	s = ""
	se = {""}
	for x in cipher:
		se.add(x)
	se.discard("")
	for x in key:
		if key[x] == None:
			s = s + x + " "
		else:
			se.discard(key[x])
	if len(se) > 0:
		s1 = ""
		for x in se:
			s1 += x + " "
		s = "{ " + s + "}"
		s1 = "{ " + s1 + "}"
		print("Cant find mapping from", s, "to", s1)

def main():
	if len(sys.argv) < 2:
		print("Pass file name. Usage: python3 <name> fileName")
		exit(0)
	fileName = str(sys.argv[1])
	# assumption: the entire cipher text is in first line
	with open(fileName) as f:
		s = f.readlines()[0]
	decrypt(s)
	

if __name__ == '__main__':
	main()