#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

cubes = set()
connections = 0
neighboursd = {
    (1,0,0),
    (-1,0,0),
    (0,1,0),
    (0,-1,0),
    (0,0,1),
    (0,0,-1)
}
with open(sys.argv[1]) as f:
    for line in f:
        newcube = tuple(
            map(
                int,
                line.strip().split(',')
            )
        )
        neighbours = {
            tuple(map(sum, zip(newcube, dt)))
            for dt in neighboursd
        }
        connections += len(cubes & neighbours)
        cubes.add(newcube)

print(6 * len(cubes) - 2 * connections)
