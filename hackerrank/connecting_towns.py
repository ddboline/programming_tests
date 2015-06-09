for _ in range(int(input())):
    N = int(input())
    arr = [int(x) for x in input().split()]
    prodmod = 1
    for a in arr:
        prodmod *= a
        prodmod %= 1234567
    print(prodmod)
