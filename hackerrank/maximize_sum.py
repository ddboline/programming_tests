def find_max_sum_mod(array, number_to_select, current_max_sum, M):
    if number_to_select == 1: ### if 1, we only need to find max mod M
        current_max = current_max_sum
        max_possible = M - current_max - 1
        if max_possible == 0:
            return current_max_sum
        for a in array:
            val = (current_max + a) % M
            if val > current_max:
                current_max = val
            if current_max == max_possible:
                return max_possible
        return current_max
    else:
        for idx in range(len(array)):
            new_number_to_select = number_to_select - 1
            new_current_max_sum = (current_max_sum + array[idx]) % M
            if new_current_max_sum < current_max_sum:
                continue
            new_array = []
            for jdx in range(len(array)):
                if idx == jdx:
                    continue
                new_array.append(array[jdx])
            new_max = find_max_sum_mod(new_array, new_number_to_select, new_current_max_sum, M)
            if new_max > current_max_sum:
                return new_max
    return current_max_sum

def maximize_sum(N, M, arr):
    current_max = 0
    max_possible = M-1
    for nsel in range(1, N):
        new_max = find_max_sum_mod(arr, nsel, current_max, M)
        if new_max == max_possible:
            return new_max
        if new_max > current_max:
            current_max = new_max
    return current_max
    
for _ in range(int(input())):
    N, M = [int(_) for _ in input().split()]
    arr = [int(_) % M for _ in input().split()]
    print(maximize_sum(N, M, arr))
#N, M = 5, 7
#arr = [3, 3, 9, 9, 5]
#print(maximize_sum(N, M, arr))
