#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

def getneighbours(position):
    neighboursd = (
        (1,0,0),
        (-1,0,0),
        (0,1,0),
        (0,-1,0),
        (0,0,1),
        (0,0,-1)
    )
    return {
        tuple(map(sum, zip(position, dt)))
        for dt in neighboursd
    }

cubes = set()
connections = 0
with open(sys.argv[1]) as f:
    for line in f:
        newcube = tuple(
            map(
                int,
                line.strip().split(',')
            )
        )
        neighbours = getneighbours(newcube)
        connections += len(cubes & neighbours)
        cubes.add(newcube)

print(6 * len(cubes) - 2 * connections) # part 1

minx = min(map(lambda t: t[0], cubes))
miny = min(map(lambda t: t[1], cubes))
minz = min(map(lambda t: t[2], cubes))
maxx = max(map(lambda t: t[0], cubes))
maxy = max(map(lambda t: t[1], cubes))
maxz = max(map(lambda t: t[2], cubes))

# We build a cuboid larger on all sides from the droplet and fill it, as if with
# water
cminx = minx - 1
cminy = miny - 1
cminz = minz - 1
cmaxx = maxx + 1
cmaxy = maxy + 1
cmaxz = maxz + 1

waters = set()
faces_exposed_to_water = 0
startwater = (cminx, cminy, cminz)
tofill = { startwater }
while tofill:
    water = tofill.pop()
    waters.add(water)

    neighbours = getneighbours(water)

    incuboidneighbours = {
        n
        for n in neighbours
        if (cminx <= n[0] <= cmaxx
            and cminy <= n[1] <= cmaxy
            and cminz <= n[2] <= cmaxz)
    }
    nonwaterneighbours = incuboidneighbours - waters

    faces_exposed_to_water += len(nonwaterneighbours & cubes)
    airneighbours = nonwaterneighbours - cubes
    tofill.update(airneighbours)

print(faces_exposed_to_water) # part 2
