
import os
import timeit
from ProcessInput import readInput,createDummyInput
from Utils import IRV
from BlomMarginAddition import BlomMargin
from OurMarginAddition import OurMargin,OurMarginExpandAll
from LRM import LRM
from OurUBAddition import upperBoundAddition
from OurHeuristicV1 import heuristic, heuristicFaster
from OurHeuristicV2 import OurHeuristicV2
import itertools
import pandas as pd
import math




def runAddition(path,resultPath,despath):
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
            "Blom_Leaf_node_explored," \
            "Our_Time_distanceTo," \
            "Blom_Time_distanceTo," \
            "Our_Time_lbcall," \
            "Blom_Time_lbcall\n"


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
            genresAll = row['Genre'].split("|")
            for g in genresAll:
                # if g in movieGenre:
                #     movieGenre[g].add(int(row['MovieId']))
                # else:
                movieGenre[g] = {int(row['MovieId'])}

        for genre, cw_all in movieGenre.items():

            cw = []
            for can in cw_all:
                if can < n:
                    cw.append(can)

            # if genre != 'Sci-Fi':
            #     continue

            numVoters = sum(B.values())
            ub = upperBoundAddition(B,C,cw)

            start = timeit.default_timer()
            heuristicV1_margin, elimOrder = heuristicFaster(B,C,cw) #heuristic(B,C,cw)
            end = timeit.default_timer()
            heuristicV1_time = end - start

            identifier = inputfile + "_" + genre
            print("################# Election ########################")
            print("Dataset Name = ",datasetName)
            print("Number of candidates = ",n)
            print("Number of voters = ",numVoters)
            print("Max ballot length = ",maxBLen)
            print("Preferred winner = ", genre,str(cw))
            print("Upper bound = ",ub)
            print("heuristic margin = ",heuristicV1_margin)
            print("heuristic time = ",heuristicV1_time)
            print("elim order = ",elimOrder)

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
            print("time distance sr call = ", ourMargin.timeDistAddSingle)
            print("time lb call = ", ourMargin.timeLBCal)




            ###################################################### OURS ################################################

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
            # ##################################################################################
            blomMargin = BlomMargin()
            start = timeit.default_timer()
            marginBlom = 0#blomMargin.marginBlom(C, B, cw)
            end = timeit.default_timer()
            runtimeBlom = end - start
            print("################# Blom Result ########################")
            print("margin  = ", marginBlom)
            print("run time = ", runtimeBlom)
            print("number of nodes explored = ", blomMargin.nodeExplored)
            print("number of ILPs = ", blomMargin.numLP)
            print("time distnace call = ", blomMargin.timeDistAdd)
            print("time lb call = ", blomMargin.timeLBCal)



            ############################################################
            # blomMargin = OurMarginExpandAll(identifier)
            # start = timeit.default_timer()
            # marginBlom = blomMargin.marginOurs(C, B, cw)
            # end = timeit.default_timer()
            # runtimeBlom = end - start
            # print("################# Blom Result ########################")
            # print("margin  = ", marginBlom)
            # print("run time = ", runtimeBlom)
            # print("number of nodes explored = ", blomMargin.nodeExplored)
            # print("number of ILPs = ", blomMargin.numLP)
            # print("time distnace call = ", blomMargin.timeDistAdd)
            # print("time lb call = ", blomMargin.timeLBCal)
            ##################################################################################
            # blomMargin = BlomMargin()
            # start = timeit.default_timer()
            # marginBlom = blomMargin.marginBlom(C, B, cw)
            # end = timeit.default_timer()
            # runtimeBlom = end - start
            # print("################# Blom Result ########################")
            # print("margin  = ", marginBlom)
            # print("run time = ", runtimeBlom)
            # print("number of nodes explored = ", blomMargin.nodeExplored)
            # print("number of ILPs = ", blomMargin.numLP)
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
            if marginOurs != marginBlom:
                print("error in margin calculation")
                marginCorrect = 0

            upperBoundCorrect = 1
            if marginBlom > ub:
                print("error in ub calculation")
                upperBoundCorrect = 0

            heuristicV1_equal = 0
            heuristicV2_equal = 0
            if marginBlom == heuristicV1_margin:
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
            result = result + str(marginBlom) + ","
            #result = result + str(ourMarginHeuristic.approxRatio) + ","
            #result = result + str(heuristicV2_approx_actual) + ","
            #runtimes
            result = result + str(heuristicV1_time) + ","
            #result = result + str(heuristicV2_time) + ","
            result = result + str(runtimeOurs) + ","
            result = result + str(runtimeBlom) + ","
            #correctness
            result =  result + str(marginCorrect) + ","
            result = result + str(upperBoundCorrect) + ","
            result = result + str(heuristicV1_equal) + ","
            #debug
            result =  result + str(ourMargin.numLP) + ","
            result =  result + str(blomMargin.numLP) + ","
            result =  result + str(ourMargin.nodeExplored) + ","
            result = result + str(blomMargin.nodeExplored) + ","
            result = result + str(ourMargin.blomLBCall) + ","
            result =  result + str(blomMargin.branchExplored) + ","
            result = result + str(ourMargin.timeDistAdd) + ","
            result = result + str(blomMargin.timeDistAdd) + ","
            result = result + str(ourMargin.timeLBCal) + ","
            result = result + str(blomMargin.timeLBCal) + "\n"
            f = open(resultPath, "a")
            f.write(result)
            f.close()
 # To test dummy dataset specify following parameters.
# numIt,numCand,numSig,bsize,fixed,bPerSig
# runDummyData(100,10,500,10,1,10)