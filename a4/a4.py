import random
import math
# import time

# To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

# pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return n**x mod q(keeping space complexity to O(logq) bits), avoiding if any limit is there on power calculating
def power(n,x,q):
    ans=1
    for i in range(x):
        ans = ans*n % q
    return ans


# return Hash Value of a string
def getHash(s,n,q):
	hashVal=0
	fac = 1
	for i in range(n-1, -1, -1):
		'''hashVal will be our final value of f(s) mod q, f(s) as mentioned in a4.pdf, starting from least significant i.e. s[n-1]'''
		# time complexity: O(len(s))
		hashVal = (hashVal+fac*(ord(s[i])-65))%q
		fac=fac*26 % q
	return hashVal


# return appropriate N that satisfies the error bounds, I have named it findN2 as if O(1) is required, but returned N will not be minimum
def findN2(eps,m):
	'''let we have two substring s and s' of length m, so clearly we know (f(s)-f(s'))<26**m.
 		Now, Using "Claim 1. The number of prime factors of a positive integer d is at most log2(d)."
 		So no. of prime divisors of (f(s)-f(s')) will be less than mlog2(26).
   		Now, suppose N is our output, Let π(N) denote the number of primes that are less than or equal to N. Then for all N > 1,
		π(N) ≥ N/(2log2(N)) .
		Error will occur at values if f(s)/q==f(s')/q , no. of possible q are less than mlog2(26)
  		Hence, error probability(eps) >= 2*mlog2(26)*log2(N)/N 
    	Suppose x=(2*m/eps)*(log2(26))  => x<N/log2(N)'''
     
	'''Solving for upper and lower limit of N
  		So N/log2(N) < N as N >=2(prime) => so log2(N)>=1 
    	lower limit is going to be x itself for N
      	Now, let N= 4(x**2)(for upper limit), => N/log2(N) = 4(x**2)/(log2(4(x**2)) > x (so satisfied)'''
    
	''' Using Desmos it is clear that no linear value of x satisfy as N so I have taken x square which satisfy the inequation well'''
	return int(((2*m/eps)*(math.log2(26))**2))

# return N in O(log(m/eps)) and N will be minimum possible by using binary search
def findN(eps,m):
    x=(2*m/eps)*(math.log2(26))
    high = 4*(x**2)
    low = x
    found = False
    ans=high
    while (low<=high):
        # print("ebwfv")
        mid=(low+high)//2
        # if mid satisfy the inequation then search to left of it and update ans to mid(as it is possible answer)
        if (x<=(mid/(math.log2(mid)))):
            ans = mid
            high = mid-1
        # if mid don't satisfy the inequation then search to right of it
        else:
            low=mid+1
    return int(ans)    # return ans
        
# print(findN(0.5,5))
        
# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
	'''patternHash is the modified hash value of pattern p and textHash is the modified hash value of substring 's' of x upto m length
	then by window sliding I have updated the value of textHash'''
	# space complexity analysis
	'''patternHash, textHash and g will be taking logq bits of space, will be stored in working memory and The logn to store at least a constant number of indices'''
	# Time complexity analysis
	'''n-m times loop with constant calculation inside so O(n-m) and O(m) outside, gives O(n+m) total '''
	l=[]
	n=len(x)
	m=len(p)
	patternHash=getHash(p,m,q)
	textHash=getHash(x[0:m],m,q)
	g=power(26,(m-1),q)
	for i in range(0,n-m+1):
		if(patternHash==textHash):
			l.append(i)
		if(i!=n-m):
			textHash=(26*(textHash-g*(ord(x[i])-65))+(ord(x[m+i])-65))%q
	return l


# Return hash value for a string with a character '?', in function I pass an argument which stores '?' index position
def getWildHash2(s,n,w,q):
	hashVal=0
	fac = 1
	for i in range(n-1, -1, -1):
		'''hashVal will be our final value of f(s) mod q, f(s) as mentioned in a4.pdf, starting from least significant i.e. s[n-1]
  		with handling '?' character'''
		# time complexity: O(len(s))
		if (i==w):
			fac=fac*26%q
			continue
		hashVal = (hashVal + fac*(ord(s[i])-65)) % q
		fac=fac*26 % q
	return hashVal


# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
	l=[]
	n=len(x)
	m=len(p)
	w=-1
	'''finding position of '?' in O(m) time'''
	for i in range(len(p)):
		if (p[i]=='?'):
			w=i
			break
	# space and time complexity analysis is same as in modePatternMatch
	# here h is to remove the value of char at corresponding position to '?' in pattern
	patternHash=getWildHash2(p,m,w,q)
	textHash=getHash(x[0:m],m,q)
	h=power(26,(m-w-1),q)
	g=power(26, (m-1), q)
	for i in range(0,n-m+1):
		'''If pattern doesn't containing character '?', otherwise no worry'''
		if w!=-1:				
			t = (textHash-h*(ord(x[w+i])-65)+q)%q
		else:
			t=textHash
		if(patternHash==t):
			l.append(i)
		if(i!=n-m):
			textHash=(26*(textHash-g*(ord(x[i])-65))+(ord(x[m+i])-65))%q
	return l



# print(getWildHash('AB?',3,'C'))
# print(modPatternMatch(1000000007, 'CD', 'ABCDE'))
# print(modPatternMatch(1000000007, 'AA', 'AAAAA'))
# print(modPatternMatchWildcard(1000000007, 'D?', 'ABCDE'))
# print(modPatternMatch(2, 'AA', 'ACEGI'))
# print(modPatternMatchWildcard(1000000007, '?A', 'ABCDE'))
# st = time.time()
# print(randPatternMatch(0.5, 'AAEGI', 'AAEGIYUFFAAEGI'))
# print('time taken:', time.time()-st)
