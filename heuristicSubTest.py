from HeuristicSub import heuristic


import os
import timeit
from ProcessInput import readInput,createDummyInput
from Utils import IRV
from BlomMargin import BlomMargin
from OurMargin import OurMargin
from LRM import LRM
from OurUB import upperBound
#from OurHeuristicV1 import heuristic
from OurHeuristicV2 import OurHeuristicV2
import itertools
import pandas as pd




fileName = r"Data/MOVIE_LENS/movieLens_movie=8_ballot=10.txt"
B, C, n, maxBLen = readInput(fileName)
winner = 0
margin, elimOrder = heuristic(B,C,winner)
print(elimOrder)
print(margin)

