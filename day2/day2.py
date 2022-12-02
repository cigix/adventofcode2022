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

outcomes = {
    'A': { # Rock
          'X': 0 + 3, # lose => scissors
          'Y': 3 + 1, # draw => rock
          'Z': 6 + 2}, # win => paper
    'B': { # Paper
          'X': 0 + 1, # lose => rock
          'Y': 3 + 2, # draw => paper
          'Z': 6 + 3}, # win => scissors
    'C': { # Scissors
          'X': 0 + 2, # lose => paper
          'Y': 3 + 3, # draw => scissors
          'Z': 6 + 1}} # win => rock


score = 0
outcome = 0
with open(sys.argv[1]) as f:
    for line in f:
        opponent, you = line.strip().split()
        score += scores[opponent][you]
        outcome += outcomes[opponent][you]

#print(score) # part 1
print(outcome)
