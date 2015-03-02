#!/bin/python

def even_tree(N, edges):
    list_of_trees = [edges]
    new_list_of_trees = []
    
    verticies = {n: [] for n in range(1,N+1)}
    for n in range(len(edges)):
        e0 = edges[n][0]
        e1 = edges[n][1]
        if e1 not in verticies[e0]:
            verticies[e0].append(e1)
        if e0 not in verticies[e1]:
            verticies[e1].append(e0)
    
    print verticies
        
    for n in range(len(edges)):
        e0 = edges[n][0]
        e1 = edges[n][1]
        
        if len(verticies[e0]) == 1 or len(verticies[e1]) == 1:
            continue
        
        test_trees = []
        
        print e0, verticies[e0] , [verticies[e] for e in verticies[e0] if e0 not in verticies[e] ]
        
        print e1, verticies[e1]
    
    return list_of_trees

#def even_tree(N, edges):
    #edge_count = {n: 0 for n in range(1,N+1)}
    #vertex_list = {n: [] for n in range(1,N+1)}
    #for n in range(1,N+1):
        #for e0, e1 in edges:
            #if e0 == n:
                #edge_count[n] += 1
                #vertex_list[n].append(e1)
            #elif e1 == n:
                #edge_count[n] += 1
                #vertex_list[n].append(e0)
    #count = {n: 0 for n in edge_count.values()}
    #for n in range(1,N+1):
        #count[edge_count[n]] += 1
    #print count
    
    #in_trees = []
    #for n in range(1,N+1):
        ##if len(vertex_list[n]) == 1:
        #print n, len(vertex_list[n]), edge_count[vertex_list[n][0]]
    
N, M = 10, 9
edges = [(2, 1), (3, 1), (4, 3), (5, 2), 
         (6, 1), (7, 2), (8, 6), (9, 8), (10, 8),]

even_tree(N, edges)

print '\n\n'

N, M = 12, 11
edges = [(2, 1), (3, 1), (4, 3), (5, 2), 
         (6, 1), (7, 2), (8, 6), (9, 8), (10, 8), (1, 11), (6,12)]

even_tree(N, edges)
