#N, M = [int(_) for _ in input().split()]
#C = [int(_) for _ in input().split()]

def coin_change_problem(N, M, C):
    coin_counts = [[0 for _ in range(M)]]
    totals = [0]
    for i in range(M):
        print(i, C[i], len(coin_counts))
        for j in range(len(coin_counts)):
            current_count = coin_counts[j]
            tot = totals[j]
            if tot == N:
                continue
            for k in range(1, ((N-tot)//C[i])+1):
                new_tot = tot + C[i] * k
                if new_tot <= N:
                    new_count = [_ for _ in current_count]
                    new_count[i] += k
                    coin_counts.append(new_count)
                    totals.append(new_tot)
        print(i, C[i], len(coin_counts))
    number_good = 0
    for i in range(len(totals)):
        if totals[i] == N:
            number_good += 1
    return number_good

print(coin_change_problem(4, 3, (1, 2, 3)))
print(coin_change_problem(10, 4, (2, 5, 3, 6)))
print(coin_change_problem(166, 23, (5, 37, 8, 39, 33, 17, 22, 32, 13, 7, 10,
                                    35, 40, 2, 43, 49, 46, 19, 41, 1, 12, 11,
                                    28)))
