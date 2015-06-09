import math
for _ in range(int(input())):
    N, K = [int(x) for x in input().split()]
    mval = int(K * math.log(10)/math.log(2))
    if N-1 <= mval:
        lowest_k = 2**(N-1) % 10**K
    else:
        pow2_mval = 2**mval
        lowest_k = pow2_mval % 10**K
        pow2 = N-1-mval
        while pow2 > mval:
            lowest_k *= pow2_mval
            lowest_k %= 10**K
            pow2 -= mval
        lowest_k *= 2**pow2
        lowest_k %= 10**K
        
    n1log102 = (N-1) * math.log10(2)
    power = n1log102 - int(n1log102) + K - 1
    highest_k = int(10**power)
    print(highest_k+lowest_k)
