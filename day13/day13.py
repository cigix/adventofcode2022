#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    lines = list(map(str.strip, f))

paircount = (len(lines) + 1) // 3

# Returns:
#  - <0 if l1 < l2
#  - >0 if l1 > l2
#  - 0 if l1 == l2
def complists(l1, l2):
    if isinstance(l1, int) and isinstance(l2, int):
        return l1 - l2
    # at least one is a list
    if isinstance(l1, int):
        return complists([l1], l2)
    if isinstance(l2, int):
        return complists(l1, [l2])
    # both are lists
    for i, (e1, e2) in enumerate(zip(l1, l2)):
        if (r := complists(e1, e2)) != 0:
            return r
    return len(l1) - len(l2)

# Returns:
#  - True if l1 <= l2
#  - False if l1 > l2
def complistsle(l1, l2):
    return complists(l1, l2) <= 0

pairs = [
    (eval(lines[i * 3]), eval(lines[i * 3 + 1]))
    for i in range(paircount)
]

pairsorder = (complistsle(*pair) for pair in pairs)

# part 1
print(
    sum(
        map(lambda x: x[0] + 1,
            filter(lambda x: x[1],
                   enumerate(pairsorder)
            )
        )
    )
)
