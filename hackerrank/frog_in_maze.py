#!/bin/python3

import sys

n, m, k = input().strip().split(' ')
n, m, k = [int(n), int(m), int(k)]
list_of_nodes = {}
alephs_node = None
for idx in range(n):
    row = input().strip()
    # Write Your Code Here
    for jdx, node in enumerate(row):
        if node == '#':
            continue
        key = (idx+1, jdx+1)
        list_of_nodes[key] = {'type': node}
        if node == 'A':
            alephs_node = key

for idx in range(k):
    i1, j1, i2, j2 = input().strip().split(' ')
    i1, j1, i2, j2 = [int(i1), int(j1), int(i2), int(j2)]
    # Write Your Code Here
    list_of_nodes[(i1, j1)]['tunnel'] = (i2, j2)
    list_of_nodes[(i2, j2)]['tunnel'] = (i1, j1)

visited_nodes = set()
nodes_being_considered = {alephs_node: list_of_nodes[alephs_node]}
number_of_successes = 0
number_of_failures = 0

while len(nodes_being_considered) > 0:
    key, val = nodes_being_considered.popitem()
    visited_nodes.add(key)
    if val['type'] == '*':
        number_of_failures += 1
        continue
    if val['type'] == '%':
        number_of_successes += 1
        continue
    i, j = key
    adjacent_nodes = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]
    number_of_adjacent_nodes = 0
    for node in adjacent_nodes:
        if node in list_of_nodes:
            if node not in visited_nodes:
                nodes_being_considered[node] = list_of_nodes[node]
            number_of_adjacent_nodes += 1
    if 'tunnel' in val:
        if number_of_adjacent_nodes == 0:
            number_of_failures += 1
            continue
        node = val['tunnel']
        if node in list_of_nodes:
            if node not in visited_nodes:
                nodes_being_considered[node] = list_of_nodes[node]

if number_of_successes + number_of_failures == 0:
    print(0)
else:
    print(number_of_successes / float(number_of_successes + number_of_failures))
