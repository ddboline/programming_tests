#!/usr/bin/python3
from math import sqrt


def lambda_func(lambda_sm1):
    return (1 + sqrt(1 + 4 * lambda_sm1**2)) / 2.


def gamma_func(lambda_s, lambda_sp1):
    return (1 - lambda_s) / lambda_sp1


lambda_vec = [0]
gamma_vec = []
for n in range(1, 11):
    lambda_vec.append(lambda_func(lambda_vec[n - 1]))
    gamma_vec.append(gamma_func(lambda_vec[n - 1], lambda_vec[n]))

for n in range(10):
    print(n, lambda_vec[n], gamma_vec[n])
