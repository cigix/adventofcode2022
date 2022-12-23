#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

elves = set()
with open(sys.argv[1]) as f:
    for y, line in enumerate(map(str.strip, f)):
        for x, c in enumerate(line):
            if c == '#':
                elves.add((x, y))

def addt(*tuples):
    return tuple(map(sum, zip(*tuples)))

moves = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}
moves["NE"] = addt(moves['N'], moves['E'])
moves["NW"] = addt(moves['N'], moves['W'])
moves["SE"] = addt(moves['S'], moves['E'])
moves["SW"] = addt(moves['S'], moves['W'])

directions = ['N', 'S', 'W', 'E']
# the first element is the key, this is important
directionkeys = {
    'N': ["N", "NE", "NW"],
    'S': ["S", "SE", "SW"],
    'W': ["W", "NW", "SW"],
    'E': ["E", "NE", "SE"]
}

for _ in range(10):
    # dict of position to set of elves
    destinations = dict()
    for elf in elves:
        adjacent = {
            addt(elf, move)
            for move in moves.values()
        }
        # if no intersection
        if not adjacent & elves:
            # register this elf's destination as itself
            destinations.setdefault(elf, set()).add(elf)
            continue

        for direction in directions:
            candidates = [
                addt(elf, moves[key])
                for key in directionkeys[direction]
            ]
            # if no intersection
            if not set(candidates) & elves:
                # pick that direction to move to
                destinations.setdefault(candidates[0], set()).add(elf)
                break
        else: # not executed if we break'd
            # register this elf's destination as itself
            destinations.setdefault(elf, set()).add(elf)

    elves = set()
    for destination, elfset in destinations.items():
        if len(elfset) == 1:
            # 1 elf set for that destination, it moves to it => 1 elf at the destination
            elves.add(destination)
        else:
            # multiple elves for 1 destination => they stay as is
            elves.update(elfset)
    directions = directions[1:] + [directions[0]]

minx = min(map(lambda t: t[0], elves))
maxx = max(map(lambda t: t[0], elves))
miny = min(map(lambda t: t[1], elves))
maxy = max(map(lambda t: t[1], elves))
print((maxx - minx + 1) * (maxy - miny + 1) - len(elves)) # part 1
