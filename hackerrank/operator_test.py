#!/usr/bin/python

def pos(a, b):
    return a + b

def neg(a, b):
    return a - b

def join(a, b):
    return a*10 + b

ops = {'+': pos, '-': neg, '': join}
opskeys = sorted(ops.keys())

def reduce_arr(arr, opsarr):
    arr_ = [x for x in arr]
    opsarr_ = [x for x in opsarr]
    idx = 0
    while idx < len(opsarr_):
        if opsarr_[idx] == '':
            arr_[idx] = join(arr_[idx], arr_[idx+1])
            arr_.pop(idx+1)
            opsarr_.pop(idx)
        idx += 1
    result = arr_[0]
    for idx in range(len(opsarr_)):
        result = ops[opsarr_[idx]](result, arr_[idx+1])
    return result

def pretty_print(arr, opsarr):
    arr_ = [x for x in arr]
    opsarr_ = [x for x in opsarr]
    idx = 0
    while idx < len(opsarr_):
        if opsarr_[idx] == '':
            arr_[idx] = join(arr_[idx], arr_[idx+1])
            arr_.pop(idx+1)
            opsarr_.pop(idx)
        idx += 1
    output = ['%s' % arr_[0]]
    for idx in range(len(opsarr_)):
        output.extend([opsarr_[idx], '%s' % arr_[idx+1]])
    return ''.join(output)


arr = range(1, 10)

print reduce_arr(arr, ['+', '+', '', '-', '+', '', '-', '+'])

opsarr = 3**8 * [8*[None]]

good_ops = []

for jdx in range(3**8):
    for idx in range(8):
        if idx == 0:
            opsarr[jdx][idx] = opskeys[jdx % 3]
        else:
            opsarr[jdx][idx] = opskeys[jdx//(3*idx) % 3]
    if reduce_arr(arr, opsarr[jdx]) == 100:
        _out = [x for x in opsarr[jdx]]
        if _out not in good_ops:
            good_ops.append(_out)
#print '\n'.join(['%s' % x for x in good_ops])
for good_op in good_ops:
    print pretty_print(arr, good_op)
