import os
import timeit
from ProcessInput import readInput, createDummyInput
from Utils import IRV
from BlomMarginAddition import BlomMargin
#from OurMarginAddition import OurMargin
from LRM import LRM
from OurUBAddition import upperBoundAddition
from OurHeuristicV1 import heuristic, heuristicFaster,heuristicV3,heuristicV4
from DistanceToPiAddition import distanceToPiExact
from OurHeuristicV2 import OurHeuristicV2
import itertools
import pandas as pd
import math
import random as rnd
from OurMargin import OurMargin
import numpy as np
from Utils import changeBallotsAddition,IRV,delBallots


def runAdditionHeuristic(path, resultPath, despath):
    result = "Dataset," \
             "Number_Of_Candidates," \
             "Number_of_voters," \
             "Max_Ballot_length," \
             "Initial winner," \
             "Preferred winner," \
             "Number Ballots add," \
             "Heuristic v2 margin," \
             "our margin," \
             "Upper limit margin," \
             "heuristic v2 runtime," \
             "our runtime," \
             "baseline runtime," \
             "avg heap modify \n"


            # "heuristicV1_margin optimise," \
             #"heuristicV1_runtime optimise \n"

    f = open(resultPath, "w")
    f.write(result)
    f.close()
    dir_list = os.listdir(path)
    print(dir_list)
    dir_list = sorted(dir_list, reverse=True)

    for inputfile in dir_list:
        if inputfile.__contains__(".txt") == False:
            continue
        datasetName = inputfile.split(".")[0]
        fileName = path + "/" + inputfile
        B, C, n, maxBLen = readInput(fileName)

        # if n != 10000:
        #     continue

        # if n >1000:
        #     continue


        #movieDesPath = path + "/" + despath + "=" + str(n) + "_description.csv"
        # movieGnere = pd.read_csv(movieDesPath, names=['MovieId', 'MovieName', 'Genre'])
        # movieGenre = {}
        # for ind, row in movieGnere.iterrows():
        #     if math.isnan(ind):
        #         continue
        #     if isinstance(row['Genre'], str) == False:
        #         continue
        #     genresAll = row['Genre'].split("|")
        #     for g in genresAll:
        #         # if g in movieGenre:
        #         #     movieGenre[g].add(int(row['MovieId']))
        #         # else:
        #         movieGenre[g] = {int(row['MovieId'])}
        #
        # for genre, cw_all in movieGenre.items():

            # cw = []
            # for can in cw_all:
            #     if can < n:
            #         cw.append(can)
            # for cw in itertools.combinations(C, 2):
            # for cw in C:
            #identifier = genre

        # if n !=500000:
        #     continue
        numVoters = sum(B.values())


        #irvRes = IRV(B, C)[0]
        irvRes = IRV(B,C)

        # if irvRes != ireRes1:
        #     print("wrong irv")



        winner_init =  [irvRes[-1]]
        winner_new = winner_init

        # test = IRV(B, C)[0][-1]
        # if test != winner_init[0]:
        #     print("error")

        # tryCount = 100
        # while (winner_new[0] == winner_init[0] and tryCount > 0):
        #     B_New = delBallots(B,percent)
        #     irvRes = IRV_Eff(B_New, C)
        #     winner_new = [irvRes[-1]]
        #     tryCount = tryCount - 1
        #
        # numVotersNew = sum(B_New.values())
        # numBallotAdd = numVoters - numVotersNew


        # topCand = irvRes[1][0:10]
        # if winner_init[0] in topCand:
        #     topCand.remove(winner_init[0])
        # tryCount = 500
        # start = timeit.default_timer()
        # while(winner_new[0] == winner_init[0] and tryCount >0 ):
        #     B_New = changeBallotsAddition(B, numBallotAdd, maxBLen, topCand)
        #     irvRes = IRV_Eff(B_New, C)
        #     winner_new = [irvRes[0][-1]]
        #     tryCount = tryCount - 1
        #     print("trycount = ",tryCount)
        # end = timeit.default_timer()
        # baselineRuntime = end - start

        topCand = irvRes[0:4]
        numBallotAdd = 1
        # percent = 0.00001
        start = timeit.default_timer()
        while numBallotAdd < 1000000000:
            # percent = percent * 2
            numBallotAdd = int(numBallotAdd * 2)
            numWinner = 4
            winnerSet = list(np.random.choice(topCand,numWinner ,replace = False))
            if winner_init[0] in winnerSet:
                winnerSet.remove(winner_init[0])
            #try with different trycount
            tryCount = 100
            while (winner_new[0] not in winnerSet and tryCount > 0):
                B_New = changeBallotsAddition(B, numBallotAdd, maxBLen, winnerSet)
                try:
                    irvRes = IRV(B_New, C)
                except:
                    irvRes = [-1]
                winner_new = [irvRes[-1]]
                tryCount = tryCount - 1
                print("trycount = ", tryCount)

            if winner_new[0]  in winnerSet:
                break
        end = timeit.default_timer()
        baselineRuntime = end - start
        print("################# Election ########################")
        print("Dataset Name = ", datasetName)
        print("Number of candidates = ", n)
        print("Number of voters = ", numVoters)
        print("Max ballot length = ", maxBLen)
        # print("Preferred winner = ", genre)
        #print("Percent of ballots to add",percent)
        print("Number of ballots to add",numBallotAdd)
        print("New winner is ",winner_new[0])
        print("Winner of original election",winner_init[0])


        ourMargin = OurMargin(datasetName)
        start = timeit.default_timer()
        marginOurs = ourMargin.marginOurs(C, B, winnerSet)
        end = timeit.default_timer()
        runtimeOurs = end - start

        # ub = upperBoundAddition(B,C,winner_new)
        # print(ub)
        ######### modified heuristic ##############################

        start = timeit.default_timer()
        heuristicV3_margin = 9999999999
        elimOrderv3 = []
        modcand = -1
        for w in winnerSet:
            h, e, m = (0,0,0) #heuristicV4(B, C, w)
            if h < heuristicV3_margin:
                heuristicV3_margin = h
                elimOrderv3 = e
                modcand = m
        end = timeit.default_timer()
        heuristicV3_time = end - start

        # start = timeit.default_timer()
        # heuristicV4_margin, elimOrderv4 = heuristicV4(B, C, winner_new[0])
        # end = timeit.default_timer()
        # heuristicV4_time = end - start
        #
        # if heuristicV3margin != heuristicV1_margin:
        #     print("wrong")
        ################### our margin ############################
       #  ourMargin = OurMargin(datasetName)
       #  start = timeit.default_timer()
       #  marginOurs = 0#ourMargin.marginOurs(C, B, winner_new)
       #  end = timeit.default_timer()
       #  runtimeOurs = end - start
       # # print("################# Our Result ########################")
       #  print("our margin  = ", marginOurs)
       #  print("run time = ", runtimeOurs)
       #  print("number of nodes explored = ", ourMargin.nodeExplored)
       #  print("number of ILPs = ", ourMargin.numLP)
       #  print("time distnace call = ", ourMargin.timeDistAdd)
       #  print("time distance sr call = ", ourMargin.timeDistAddSingle)
       #  print("time lb call = ", ourMargin.timeLBCal)

        # start = timeit.default_timer()
        # distanceToValue , t,t1 = 0 #distanceToPiExact(B,elimOrder)
        # end = timeit.default_timer()
        # distanceToValue_time = end - start
        #
        #
        # if distanceToValue != heuristicV1_margin:
        #     print("not equal")


        ###################################
        #change x%  ballot



       # print("Upper bound = ", ub)
        #print("heuristic margin = ", heuristicV1_margin)
        #print("heuristic time = ", heuristicV1_time)

        # print("heuristic margin optimise = ", heuristicV1_margin)
        # print("heuristic time optimise = ", heuristicV1_time)
        # print("maximum possible margin = ",numBallotAdd)


        result = ""
        result = result + datasetName + ","
        result = result + str(n) + ","
        result = result + str(numVoters) + ","
        result = result + str(maxBLen) + ","
        result = result + str(winner_init[0]) + ","
        result = result + str(winner_new[0]) + ","
        #result = result + str(percent) + ","
        result = result + str(numBallotAdd) + ","
        # # margins
        # result = result + str(ub) + ","
        result = result + str(heuristicV3_margin) + ","
        result = result + str(marginOurs) + ","
        result = result + str(numBallotAdd) + ","
        result = result + str(heuristicV3_time) + ","
        result = result + str(runtimeOurs) + ","
        result = result + str(baselineRuntime)+ ","
        result = result + str(modcand)
        result = result + "\n"
        f = open(resultPath, "a")
        f.write(result)
        f.close()



