#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    exit(1)

scores = {
    'A': { # Rock
          'X': 1 + 3, # rock => draw
          'Y': 2 + 6, # paper => win
          'Z': 3 + 0}, # scissors => lose
    'B': { # Paper
          'X': 1 + 0, # rock => lose
          'Y': 2 + 3, # paper => draw
          'Z': 3 + 6}, # scissors => win
    'C': { # Scissors
          'X': 1 + 6, # rock => win
          'Y': 2 + 0, # paper => lose
          'Z': 3 + 3}} # scissors => draw

score = 0
with open(sys.argv[1]) as f:
    for line in f:
        opponent, you = line.strip().split()
        score += scores[opponent][you]

print(score)
