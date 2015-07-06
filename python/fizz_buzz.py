#!/usr/bin/python3

for N in range(1,100+1):
    output = ''
    if N % 3 == 0:
        output += 'Fizz'
    elif N % 5 == 0:
        output += 'Buzz'
    else:
        output = '%s' % N
    print(output)

