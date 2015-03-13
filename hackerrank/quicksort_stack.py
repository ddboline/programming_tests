import random

def quicksort(ar):
    n = len(ar)
    stack = [(0, n-1)]
    while stack:
        lower_idx, upper_idx = stack.pop()
        if upper_idx-lower_idx<2:
            if ar[upper_idx] < ar[lower_idx]:
                temp = ar[upper_idx]
                ar[upper_idx] = ar[lower_idx]
                ar[lower_idx] = temp
                print ' '.join(str(x) for x in ar)
            continue
        new_lower_idx = lower_idx
        pivot = ar[upper_idx]
        for N in range(lower_idx, upper_idx):
            if ar[N] > pivot:
                if ar[new_lower_idx] < pivot:
                    new_lower_idx = N
            elif N > new_lower_idx and ar[new_lower_idx] > ar[N]:
                temp = ar[N]
                ar[N] = ar[new_lower_idx]
                ar[new_lower_idx] = temp
                new_lower_idx += 1
        temp = ar[upper_idx]
        ar[upper_idx] = ar[new_lower_idx]
        ar[new_lower_idx] = temp
        print ' '.join(str(x) for x in ar)
        stack.append((new_lower_idx+1, upper_idx))
        stack.append((lower_idx, new_lower_idx-1))

ar = [1, 3, 9, 8, 2, 7, 5]
print ' '.join(str(x) for x in ar)
quicksort(ar)
ar = [9, 8, 6, 7, 3, 5, 4, 1, 2]
print ' '.join(str(x) for x in ar)
quicksort(ar)
#ar = [random.randint(-10000,10000) for n in range(20)]
#newar = []
#for n in range(len(ar)):
    #if ar[n] not in ar[:n]:
        #newar.append(ar[n])
#ar = newar
#print ' '.join(str(x) for x in ar)
#quicksort(ar)
#quicksort([random.randint(-10000,10000) for n in range(random.randint(1,5000))])
