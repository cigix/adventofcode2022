#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

digits = "=-012"

s = 0
with open(sys.argv[1]) as f:
    for line in f:
        n = 0
        for c in line.strip():
            n = n * 5 + digits.find(c) - 2
        s += n

base5 = list()
while s:
    d, m = divmod(s, 5)
    base5.insert(0, m)
    s = d

baseS = list(base5) # deep copy
for i in range(len(baseS) - 1, 0, -1):
    if 2 < baseS[i]: # can't represent that base5 digit in base SNAFU
        baseS[i] -= 5 # lower that digit by 5
        baseS[i - 1] += 1 # add 5 through the higher power

sumS = ""
for digit in baseS:
    sumS += digits[digit + 2]

print(sumS) # part 1
