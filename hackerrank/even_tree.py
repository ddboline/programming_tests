#!/usr/bin/python3

def even_tree(N, edges):
    edge_dict = {n: set() for n in range(1,N+1)}
    for u, v in edges:
        edge_dict[u].add(v)
        edge_dict[v].add(u)
    u, v = edges[0]
    start = u
    visited = set({u})
    for e in [x for x in edge_dict[start] if x != v]:
        visited.add(e)
    print(visited)
    return

N, M = 10, 9
edges = ((2, 1), (3, 1), (4, 3), (5, 2), 
         (6, 1), (7, 2), (8, 6), (9, 8), (10, 8),)

even_tree(N, edges)

print('\n\n')

N, M = 20, 19
edges = ((2, 1), (3, 1), (4, 3), (5, 2), (6, 5), (7, 1), (8, 1), (9, 2),
         (10, 7), (11, 10), (12, 3), (13, 7), (14, 8), (15, 12), (16, 6),
         (17, 6), (18, 10), (19, 1), (20, 8))

even_tree(N, edges)
