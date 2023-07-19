
import os
import timeit
from ProcessInput import readInput,createDummyInput
from Utils import IRV
from BlomMargin import BlomMargin
from OurMargin import OurMargin
from LRM import LRM

from OurHeuristicV1 import heuristic, heuristicFaster,heuristicSingleWinner
from OurHeuristicV2 import OurHeuristicV2
import itertools
import pandas as pd
import math

import random




def runAnti(path,resultPath,despath):
    dir_list = os.listdir(path)
    print(dir_list)
    dir_list = sorted(dir_list,reverse=False)

    antiPluralityIRV = 0
    antiPluralityPlu = 0
    testCase = 0
    for inputfile in dir_list:
        if inputfile.__contains__(".txt") == False:
            continue
        datasetName = inputfile.split(".")[0]
        fileName = path + "/" + inputfile
        B, C, n, maxBLen = readInput(fileName)
        numVoters = sum(B.values())

        hatedMap = {}
        hs = 10
        for s,c in B.items():
            for i in range(hs):
                if i<len(s):
                    e = s[-i]
                    if e not in hatedMap:
                        hatedMap[e] = c
                    else:
                        hatedMap[e] = hatedMap[e] + c

        sorted_hatedList= sorted(hatedMap.items(), key=lambda x: x[1], reverse=True)
        sorted_hatedMap = dict(sorted_hatedList)
        hatedList = list(sorted_hatedMap.keys())


        prefferedMap = {}
        for s, c in B.items():
            e = s[0]
            if e not in prefferedMap:
                prefferedMap[e] = c
            else:
                prefferedMap[e] = prefferedMap[e] + c

        sorted_preferredList = sorted(prefferedMap.items(), key=lambda x: x[1], reverse=True)
        sorted_preferredMap = dict(sorted_preferredList)
        preferredList = list(sorted_preferredMap.keys())

        preferredMap = {}
        for i in range(0,len(preferredList)):
            preferredMap[preferredList[i]] = i

        winnerSetAll = []
        sizeOfWinnerSet = 10
        for i in range(10):
            winnerSet = []
            for i in range(sizeOfWinnerSet/2):
                r1 = random.randint(0, 15)
                winnerSet.append(hatedList[r1])

            w = random.choices(preferredList,k=sizeOfWinnerSet/2)
            winnerSet.extend(w)
            winnerSetAll.append(winnerSet)

        for  winnerSet in winnerSetAll:

            start = timeit.default_timer()
            heuristicMargin = 9999999999
            heuristicElimationOrder = []
            for w in winnerSet:
                h, e, m = heuristicSingleWinner(B, C, w)
                if h < heuristicMargin:
                    heuristicMargin = h
                    heuristicElimationOrder = e

            end = timeit.default_timer()
            heuristicRuntime = end - start
            heuristicWinner = heuristicElimationOrder[-1]

            pos = 999999999
            for c in winnerSet:
                if c in prefferedMap:
                    p = preferredMap[c]
                    if p < pos:
                        pos = p
                        pluralityWinner = c
                else:
                    p = 0
                    if p < pos:
                        pos = p
                        pluralityWinner = c


            antiPluralityIRV = antiPluralityIRV + hatedMap[heuristicWinner]/numVoters
            antiPluralityPlu = antiPluralityPlu + hatedMap[pluralityWinner]/numVoters

            print("IRV: ", hatedMap[heuristicWinner]/numVoters)
            print("PLU:", hatedMap[pluralityWinner]/numVoters)

            testCase = testCase  + 1

        print("n = ",n)
        print("antipluraility in IRV = ", antiPluralityIRV/testCase)
        print("antipluraility in Plurality = ", antiPluralityPlu / testCase)
        testCase = 0
        antiPluralityIRV = 0
        antiPluralityPlu = 0