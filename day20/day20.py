#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    numbers = tuple(
        map(
            int,
            map(
                str.strip,
                f
            )
        )
    )

def mix(key, times):
    l = len(numbers)
    # numbers can have duplicates, so instead of mixing the numbers, we mix the positions
    message = tuple(range(l))

    for _ in range(times):
        for npos in range(l):
            n = numbers[npos] * key
            mstartpos = message.index(npos)

            # % ensures result is positive
            mendpos = (mstartpos + n) % (l - 1)

            # remove at mstartpos
            message = message[:mstartpos] + message[mstartpos + 1:]

            # insert at mendpos
            message = message[:mendpos] + (npos,) + message[mendpos:]

    zeronpos = numbers.index(0)
    zerompos = message.index(zeronpos)

    return key * (
        numbers[message[(zerompos + 1000) % l]]
        + numbers[message[(zerompos + 2000) % l]]
        + numbers[message[(zerompos + 3000) % l]])

print(mix(1, 1)) # part 1
print(mix(811589153, 10)) # part 2
