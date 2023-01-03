#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

with open(sys.argv[1]) as f:
    jets = f.read().strip()

def addt(*tuples):
    return tuple(map(sum, zip(*tuples)))

class Shape:
    # width: int, number of columns spanned
    # offsets: frozenset of tuples of (int, int), the set of offsets
    def __init__(self, *offsets):
        self.width = 1 + max(map(lambda t: t[0], offsets))
        self.offsets = frozenset(offsets)

shapes = (
    Shape(
        (0, 0), (1, 0), (2, 0), (3, 0)
    ),
    Shape(
                (1, 2),
        (0, 1), (1, 1), (2, 1),
                (1, 0)
    ),
    Shape(
                        (2, 2),
                        (2, 1),
        (0, 0), (1, 0), (2, 0)
    ),
    Shape(
        (0, 3),
        (0, 2),
        (0, 1),
        (0, 0)
    ),
    Shape(
        (0, 1), (1, 1),
        (0, 0), (1, 0)
    )
)

class BitVector:
    def __init__(self):
        self.n_ = 0

    def __getitem__(self, key):
        return (self.n_ & (2 ** key)) != 0

    def __setitem__(self, key, value):
        if value:
            self.n_ |= 2 ** key
        else:
            self.n_ &= ~(2 ** key)

class Counter:
    def __init__(self, count, top):
        self.seen = 1
        self.count = count
        self.top = top

    def see(self, count, top):
        self.seen += 1
        self.count = count
        self.top = top

def nextid(current, container):
    return (current + 1) % len(container)

WIDTH = 7

def simulate(rocks):
    jetid = 0
    rockid = 0
    maxy = 0
    occupied = list() # list of BitVector
    seen = dict() # dict of (jetid, rockid) to Counter

    def intersects(shapeoccupies):
        for x, y in shapeoccupies:
            if y < len(occupied) and occupied[y][x]:
                return True
        return False

    added_to_top = 0
    dropped = 0
    while dropped < rocks:
        # position of the lower left corner of the new shape
        x = 2
        y = maxy + 3

        shape = shapes[rockid]
        rockid = nextid(rockid, shapes)
        shapeoccupies = {
            addt((x, y), offset)
            for offset in shape.offsets
        }

        while True:
            # attempt sideways movement
            jet = jets[jetid]
            jetid = nextid(jetid, jets)
            if jet == '<':
                if 0 < x:
                    shapewouldoccupy = {
                        addt((-1, 0), position)
                        for position in shapeoccupies
                    }
                    if not intersects(shapewouldoccupy):
                        x -= 1
                        shapeoccupies = shapewouldoccupy
            else: # jet == '>'
                if x + shape.width < WIDTH:
                    shapewouldoccupy = {
                        addt((1, 0), position)
                        for position in shapeoccupies
                    }
                    if not intersects(shapewouldoccupy):
                        x += 1
                        shapeoccupies = shapewouldoccupy

            # attempt downwards movement
            if y == 0:
                break
            shapewouldoccupy = {
                addt((0, -1), position)
                for position in shapeoccupies
            }
            if intersects(shapewouldoccupy):
                break
            y -= 1
            shapeoccupies = shapewouldoccupy

        for ox, oy in shapeoccupies:
            while len(occupied) <= oy:
                occupied.append(BitVector())
            occupied[oy][ox] = True
            if maxy <= oy:
                maxy = oy + 1

        if added_to_top == 0:
            k = jetid, rockid
            if k in seen:
                if 2 <= seen[k].seen:
                    # We have seen this key 3 times already
                    # | ... 1 ... 2 ... 3
                    # ^ start           ^ you are here
                    # 1-2 may not be the same as 2-3 but we can assume there
                    # would be a 4, 5, ... if we were to repeat 2-3
                    dcount = dropped - seen[k].count
                    dtop = maxy - seen[k].top
                    todrop = rocks - dropped
                    repeats = todrop // dcount
                    # simulate dropping `repeats` rocks
                    dropped += repeats * dcount
                    added_to_top += repeats * dtop
                    # do not update maxy or occupied: we only record how much we
                    # *could* add for the same result

                seen[k].see(dropped, maxy)
            else:
                seen[k] = Counter(dropped, maxy)

        dropped += 1

    return maxy + added_to_top

print(simulate(2022)) # part 1
print(simulate(1000000000000)) # part 2
