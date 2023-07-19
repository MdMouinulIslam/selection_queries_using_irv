
import os
import timeit
from ProcessInput import readInput,createDummyInput
from Utils import IRV
from BlomMarginAddition import BlomMargin
from OurMarginAddition import OurMargin
from OurMarginAdditionV2 import OurMarginV2
from LRM import LRM
from OurUBAddition import upperBoundAddition
from OurHeuristicV1 import heuristic, heuristicFaster
from OurHeuristicV2 import OurHeuristicV2
import itertools
import pandas as pd
import math




def runAdditionV2(path,resultPath,despath):
    result = "Dataset," \
             "Number_Of_Candidates," \
             "Number_of_voters," \
             "Max_Ballot_length," \
             "Preferred_winner," \
             "Upper_Bound," \
             "heuristicV1_margin," \
            "Our_margin," \
            "OurV2_margin," \
            "heuristicV1_runtime," \
            "Our_runtime," \
            "OurV2_runtime," \
            "Margin_OurV2=Ours," \
            "Upper_bound_correct," \
            "HeuristicV1_equl_margin," \
            "Our_number_LPS," \
            "OurV2_number_LPS," \
            "Our_number_node_explored," \
            "OurV2_number_node_explored," \
            "Our_blom_lb_calls," \
            "OurV2_Leaf_node_explored," \
            "Our_Time_distanceTo," \
            "OurV2_Time_distanceTo," \
            "Our_Time_lbcall," \
            "OurV2_Time_lbcall\n"


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
        fileName = path +"/"+ inputfile
        B,C,n,maxBLen = readInput(fileName)

        movieDesPath = path+"/"+ despath+"="+str(n)+"_description.csv"
        movieGnere = pd.read_csv(movieDesPath, names=['MovieId', 'MovieName', 'Genre'])
        movieGenre = {}
        for ind, row in movieGnere.iterrows():
            if math.isnan(ind):
                continue
            if isinstance(row['Genre'], str) == False:
                continue
            genresAll = row['Genre'].split("|")[:1]
            for g in genresAll:
                # if g in movieGenre:
                #     movieGenre[g].add(int(row['MovieId']))
                # else:
                #     movieGenre[g] = {int(row['MovieId'])}
                movieGenre[g] = int(row['MovieId'])


        allPossibleWinner = []
        for genre, cw in movieGenre.items():
            allPossibleWinner.append(cw)

        exploredMap = {}

        while(len(allPossibleWinner) != 0):
            cw = allPossibleWinner
            identifier = str(cw)
            numVoters = sum(B.values())
            ub = upperBoundAddition(B,C,cw)

            start = timeit.default_timer()
            heuristicV1_margin = heuristic(B,C,cw)
            end = timeit.default_timer()
            heuristicV1_time = end - start



            print("################# Election ########################")
            print("Dataset Name = ",datasetName)
            print("Number of candidates = ",n)
            print("Number of voters = ",numVoters)
            print("Max ballot length = ",maxBLen)
            print("Preferred winner = ", genre)
            print("Upper bound = ",ub)
            print("heuristic margin = ",heuristicV1_margin)
            print("heuristic time = ",heuristicV1_time)
            print("possible winners = ",allPossibleWinner)

            ################################################# ours #####################################################

            ourMargin = OurMargin(identifier)
            start = timeit.default_timer()
            marginOurs = ourMargin.marginOurs(C,B,cw)
            end = timeit.default_timer()
            runtimeOurs = end - start
            print("################# Our Result ########################")
            print("margin  = ", marginOurs)
            print("run time = ", runtimeOurs)
            print("number of nodes explored = ",ourMargin.nodeExplored)
            print("number of ILPs = ",ourMargin.numLP)
            print("time distnace call = ",ourMargin.timeDistAdd)
            print("time lb call = ", ourMargin.timeLBCal)


            ##################################################################################################

            ourMarginV2 = OurMarginV2(identifier,exploredMap)
            start = timeit.default_timer()
            marginOursV2,winner = ourMarginV2.marginOurs(C, B, cw)
            end = timeit.default_timer()
            runtimeOursV2 = end - start
            exploredNodesV2 = ourMarginV2.exploredMap
            print("################# Our Result ########################")
            print("margin  = ", marginOursV2)
            print("run time = ", runtimeOursV2)
            print("number of nodes explored = ", ourMarginV2.nodeExplored)
            print("number of ILPs = ", ourMarginV2.numLP)
            print("time distnace call = ", ourMarginV2.timeDistAdd)
            print("time lb call = ", ourMarginV2.timeLBCal)
            print("winner of this round is = ",winner)


            # ###################################################### blom ################################################
            #
            # blomMargin = BlomMargin()
            # start = timeit.default_timer()
            # marginBlom = blomMargin.marginBlom(C,B,cw)
            # end = timeit.default_timer()
            # runtimeBlom = end - start
            # print("################# Blom Result ########################")
            # print("margin  = ", marginBlom)
            # print("run time = ", runtimeBlom)
            # print("number of nodes explored = ",blomMargin.nodeExplored)
            # print("number of ILPs = ",blomMargin.numLP)
            # print("time distnace call = ", blomMargin.timeDistAdd)
            # print("time lb call = ", blomMargin.timeLBCal)

            ################################################## our heuristic v2 ########################################
            # ourMarginHeuristic = OurHeuristicV2(identifier)
            # start = timeit.default_timer()
            # heuristicV2_margin = 0#ourMarginHeuristic.marginOurs(C, B, cw)
            # end = timeit.default_timer()
            # heuristicV2_time = end - start
            # print("################# Our Result ########################")
            # print("margin heuristic v2 = ", heuristicV2_margin)
            # print("run time heuristic v2  = ", heuristicV2_time)
            # print("number of nodes explored heuristic v2  = ", ourMarginHeuristic.nodeExplored)
            # print("number of ilp calls heuristic v2  = ", ourMarginHeuristic.numLP)

            ##########################################################################################################
            marginCorrect = 1
            if marginOurs != marginOursV2:
                print("error in margin calculation")
                marginCorrect = 0

            upperBoundCorrect = 1
            if marginOurs > ub:
                print("error in ub calculation")
                upperBoundCorrect = 0

            heuristicV1_equal = 0
            heuristicV2_equal = 0
            if marginOurs == heuristicV1_margin:
                heuristicV1_equal = 1
            if marginOurs == 0:
                heuristicV2_equal = 1

            heuristicV2_approx_actual = float('inf')
            if marginOurs != 0:
                heuristicV2_approx_actual = float(0) / marginOurs

                heuristicV2_approx_correct = 0

                # if ourMarginHeuristic.approxRatio >= heuristicV2_approx_actual:
                #     heuristicV2_approx_correct = 1
            else:
                heuristicV2_approx_correct = 1
            #election param
            result = ""
            result = result + datasetName + ","
            result = result + str(n) + ","
            result = result + str(numVoters) + ","
            result = result + str(maxBLen) + ","
            result = result + genre + ","
            # margins
            result = result + str(ub) + ","
            result = result + str(heuristicV1_margin) + ","
            #result = result + str(heuristicV2_margin) + ","
            result = result + str(marginOurs) + ","
            result = result + str(marginOursV2) + ","
            #result = result + str(ourMarginHeuristic.approxRatio) + ","
            #result = result + str(heuristicV2_approx_actual) + ","
            #runtimes
            result = result + str(heuristicV1_time) + ","
            #result = result + str(heuristicV2_time) + ","
            result = result + str(runtimeOurs) + ","
            result = result + str(runtimeOursV2) + ","
            #correctness
            result =  result + str(marginCorrect) + ","
            result = result + str(upperBoundCorrect) + ","
            result = result + str(heuristicV1_equal) + ","
            #debug
            result =  result + str(ourMargin.numLP) + ","
            result =  result + str(ourMarginV2.numLP) + ","
            result =  result + str(ourMargin.nodeExplored) + ","
            result = result + str(ourMarginV2.nodeExplored) + ","
            result = result + str(ourMargin.blomLBCall) + ","
            result =  result + str(ourMarginV2.branchExplored) + ","
            result = result + str(ourMargin.timeDistAdd) + ","
            result = result + str(ourMarginV2.timeDistAdd) + ","
            result = result + str(ourMargin.timeLBCal) + ","
            result = result + str(ourMarginV2.timeLBCal) + "\n"
            f = open(resultPath, "a")
            f.write(result)
            f.close()
            allPossibleWinner.remove(winner)
 # To test dummy dataset specify following parameters.
# numIt,numCand,numSig,bsize,fixed,bPerSig
# runDummyData(100,10,500,10,1,10)