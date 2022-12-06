#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    message = f.read().strip()

def marker(length, message):
    i = length
    while len(set(message[i - length:i])) != length:
        i += 1
    return i

#print(marker(4, message)) # part 1
print(marker(14, message)) # part 2
