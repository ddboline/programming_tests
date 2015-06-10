def fib_modified(f0, f1):
    def closure_(N):
        if N == 0:
            return f0
        elif N == 1:
            return f1
        else:
            return closure_(N-1)**2 + closure_(N-2)

fib_func = fib_modified(
for N in range(20):
    
    print(fib_modified(N))
