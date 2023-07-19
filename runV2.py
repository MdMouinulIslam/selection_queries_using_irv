
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




def runV2(path,resultPath,despath):
    result = "Dataset," \
             "Number_Of_Candidates," \
             "Number_of_voters," \
             "Max_Ballot_length," \
             "Preferred_winner," \
             "Upper_Bound," \
             "heuristicV1_margin," \
            "Our_margin," \
            "Blom_margin," \
            "heuristicV1_runtime," \
            "Our_runtime," \
            "Blom_runtime," \
            "Margin_Blom=Ours," \
            "Upper_bound_correct," \
            "HeuristicV1_equl_margin," \
            "Our_number_LPS," \
            "Blom_number_LPS," \
            "Our_number_node_explored," \
            "Blom_number_node_explored," \
            "Our_blom_lb_calls," \
            "Blom_Leaf_node_explored\n"


    f = open(resultPath, "w")
    f.write(result)
    f.close()
    dir_list = os.listdir(path)
    print(dir_list)
    dir_list = sorted(dir_list,reverse=False)

    for inputfile in dir_list:
        if inputfile.__contains__(".txt") == False:
            continue
        datasetName = inputfile.split(".")[0]
        fileName = path + "/" + inputfile
        B, C, n, maxBLen = readInput(fileName)
        # if n != 10:
        #     continue

        movieDesPath = path + "/" + despath + "=" + str(n) + "_description.csv"
        movieGnere = pd.read_csv(movieDesPath, names=['MovieId', 'MovieName', 'Genre'])
        movieGenre = {}
        for ind, row in movieGnere.iterrows():
            if math.isnan(ind):
                continue
            if isinstance(row['Genre'], str) == False:
                continue
            genresAll = row['Genre'].split("|")
            for g in genresAll:
                if g in movieGenre:
                    movieGenre[g].add(int(row['MovieId']))
                else:
                    movieGenre[g] = {int(row['MovieId'])}

        for genre, winnerSetAll in movieGenre.items():

            # if genre != "Sci-Fi":
            #     continue
            winnerSet = []
            for can in winnerSetAll:
                if can < n:
                    winnerSet.append(can)

            # if genre != 'Sci-Fi':
            #     continue

            numVoters = sum(B.values())

            ########################################################################################
            #ub = upperBoundAddition(B, C, winnerSet)

            start = timeit.default_timer()
            heuristicMargin = 9999999999
            heuristicElimationOrder = []
            heapModify = -1
            for w in winnerSet:
                h, e, m = heuristicSingleWinner(B, C, w)
                if h < heuristicMargin:
                    heuristicMargin = h
                    heuristicElimationOrder = e
                    heapModify = m
            end = timeit.default_timer()
            heuristicRuntime = end - start

            ############################################# upper bound ##############################################
            ub = heuristicMargin
            ####################################### print heuristic #################################################


            identifier = inputfile + "_" + genre
            print("################# Election ########################")
            print("Dataset Name = ", datasetName)
            print("Number of candidates = ", n)
            print("Number of voters = ", numVoters)
            print("Max ballot length = ", maxBLen)
            print("Preferred winner = ", genre)
            print("Upper bound = ", ub)
            print("heuristic margin = ", heuristicMargin)
            print("heuristic time = ", heuristicRuntime)
            print("heuristic order = ", heuristicElimationOrder)
            print("heuristic total heap modify ",heapModify)

            ################################################# ours #####################################################

            ourMargin = OurMargin(identifier)
            start = timeit.default_timer()
            marginOurs = ourMargin.marginOurs(C, B, winnerSet)
            end = timeit.default_timer()
            runtimeOurs = end - start
            print("################# Our Result ########################")
            print("margin  = ", marginOurs)
            print("run time = ", runtimeOurs)
            print("number of nodes explored = ", ourMargin.nodeExplored)
            print("number of ILPs = ", ourMargin.numLP)
            #print("time distnace call = ", ourMargin.timeDistAdd)
            #print("time distance sr call = ", ourMargin.timeDistAddSingle)
            #print("time lb call = ", ourMargin.timeLBCal)

            ################################################# bloms #####################################################

            blomMargin = BlomMargin(identifier)
            start = timeit.default_timer()
            marginBlom = blomMargin.marginBlom(C,B,winnerSet)
            end = timeit.default_timer()
            runtimeBlom = end - start
            print("################# Blom Result ########################")
            print("margin  = ", marginBlom)
            print("run time = ", runtimeBlom)
            print("number of nodes explored = ",blomMargin.nodeExplored)
            print("number of ILPs = ",blomMargin.numLP)
            #print("time distnace call = ", blomMargin.timeDistAdd)
            #print("time lb call = ", blomMargin.timeLBCal)

            ################################################# debug result #########################################################
            marginCorrect = 1
            if marginOurs != marginBlom:
                print("error in margin calculation")
                marginCorrect = 0

            upperBoundCorrect = 1
            if marginBlom > ub:
                print("error in ub calculation")
                upperBoundCorrect = 0

            heuristicV1_equal = 0
            heuristicV2_equal = 0
            if marginBlom == heuristicMargin:
                heuristicV1_equal = 1
            if marginBlom == 0:
                heuristicV2_equal = 1

            heuristicV2_approx_actual = float('inf')
            if marginBlom != 0:
                heuristicV2_approx_actual = float(0) / marginBlom

                heuristicV2_approx_correct = 0

                # if ourMarginHeuristic.approxRatio >= heuristicV2_approx_actual:
                #     heuristicV2_approx_correct = 1
            else:
                heuristicV2_approx_correct = 1


            ################################################# write result #####################################################
            result = ""
            result = result + datasetName + ","
            result = result + str(n) + ","
            result = result + str(numVoters) + ","
            result = result + str(maxBLen) + ","
            result = result + genre + ","
            # margins
            result = result + str(ub) + ","
            result = result + str(heuristicMargin) + ","
            # result = result + str(heuristicV2_margin) + ","
            result = result + str(marginOurs) + ","
            result = result + str(marginBlom) + ","
            # result = result + str(ourMarginHeuristic.approxRatio) + ","
            # result = result + str(heuristicV2_approx_actual) + ","
            # runtimes
            result = result + str(heuristicRuntime) + ","
            # result = result + str(heuristicV2_time) + ","
            result = result + str(runtimeOurs) + ","
            result = result + str(runtimeBlom) + ","
            # correctness
            result = result + str(marginCorrect) + ","
            result = result + str(upperBoundCorrect) + ","
            result = result + str(heuristicV1_equal) + ","
            # debug
            result = result + str(ourMargin.numLP) + ","
            result = result + str(blomMargin.numLP) + ","
            result = result + str(ourMargin.nodeExplored) + ","
            result = result + str(blomMargin.nodeExplored) + ","
            result = result + str(ourMargin.blomLBCall) + ","
            result = result + str(blomMargin.branchExplored) #+ ","
            #result = result + str(ourMargin.timeDistAdd) + ","
            #result = result + str(blomMargin.timeDistAdd) + ","
            #result = result + str(ourMargin.timeLBCal) + ","
            #result = result + str(blomMargin.timeLBCal) + "\n"
            result = result + "\n"
            f = open(resultPath, "a")
            f.write(result)
            f.close()

