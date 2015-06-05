#!/usr/bin/python3

def get_vdict(edges):
    vdict = {}
    for u, v in edges:
        for x in (u, v):
            if x not in vdict:
                vdict[x] = set()
        vdict[u].add(v)
        vdict[v].add(u)
    return vdict

def walk_tree(vdict, vset, ucurr, vcurr=None):
    if ucurr not in vdict:
        return 0
    vset.add(ucurr)
    if not vdict[ucurr]:
        return 0
    for node in vdict[ucurr]:
        if node == vcurr:
            continue
        if node not in vset:
            vset.add(node)
            walk_tree(vdict, vset, node, ucurr)
    return 1

def split_tree(edges):
    vdict = get_vdict(edges)
    for edge in edges:
        u, v = edge
        vset0 = set()
        walk_tree(vdict, vset0, u, v)
        
        if len(vset0) == 0 or len(vset0) % 2 != 0:
            continue
        
        vset1 = set()
        walk_tree(vdict, vset1, v, u)
        
        if len(vset1) == 0 or len(vset1) % 2 != 0:
            continue
        print('vset0', vset0, 'vset1', vset1)

        edge0 = []
        edge1 = []
        for ed in edges:
            if ed == edge:
                continue
            u, v = ed
            if u in vset0 and v in vset0:
                edge0.append(ed)
            elif u in vset1 and v in vset1:
                edge1.append(ed)
        return split_tree(edge0) + split_tree(edge1)
        
    return edges
        

N, M = 10, 9
edges = ((2, 1), (3, 1), (4, 3), (5, 2), 
         (6, 1), (7, 2), (8, 6), (9, 8), (10, 8),)
print('even_tree', len(edges) - len(split_tree(edges)))

print('\n\n')

N, M = 20, 19
edges = ((2, 1), (3, 1), (4, 3), (5, 2), (6, 5), (7, 1), (8, 1), (9, 2),
         (10, 7), (11, 10), (12, 3), (13, 7), (14, 8), (15, 12), (16, 6),
         (17, 6), (18, 10), (19, 1), (20, 8))

print('even_tree', len(edges) - len(split_tree(edges)))
