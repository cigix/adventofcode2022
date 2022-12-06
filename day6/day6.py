#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    message = f.read().strip()

i = 4
while len(set(message[i - 4:i])) != 4:
    i += 1

print(i) # part 1
