


import os
import timeit
from ProcessInput import readInput,createDummyInput
from Utils import IRV
from BlomMargin import BlomMargin
from OurMargin import OurMargin
from LRM import LRM
from OurUB import upperBound
from OurHeuristicV1 import heuristic
from OurHeuristicV2 import OurHeuristicV2
import itertools
import pandas as pd




def runRealData(path):



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
            "HeuristicV2_equl_margin," \
            "HeuristicV2_approximation_correct," \
            "Our_number_LPS," \
            "Blom_number_LPS," \
            "Our_number_node_explored," \
            "Blom_number_node_explored," \
            "Our_blom_lb_calls," \
            "Blom_Leaf_node_explored\n"


    f = open("result/result_set_candidate_movie_lens.csv", "w")
    f.write(result)

    dir_list = os.listdir(path)
    print(dir_list)

    #dir_list = ['Data_NA_Auburn.txt_ballots.txt']#, 'Data_NA_Ballina.txt_ballots.txt', 'Data_NA_Balmain.txt_ballots.txt']#, 'Data_NA_Bankstown.txt_ballots.txt', 'Data_NA_Barwon.txt_ballots.txt']#['Data_NA_Murray.txt_ballots.txt']

    #dir_list = ['Aspen_2009_CityCouncil.txt']
    for inputfile in dir_list:

        if inputfile.__contains__(".txt") == False:
            continue
        datasetName = inputfile.split(".")[0]
        fileName = path +"/"+ inputfile
        B,C,n,maxBLen = readInput(fileName)

        for cw in itertools.combinations(C, 2):
        #for cw in C:
            identifier = datasetName+"_w="+str(cw)
            numVoters = sum(B.values())
            ub = upperBound(B,C,cw)

            start = timeit.default_timer()
            heuristicV1_margin = heuristic(B,C,cw)
            end = timeit.default_timer()
            heuristicV1_time = end - start


            print("################# Election ########################")
            print("Dataset Name = ",datasetName)
            print("Number of candidates = ",n)
            print("Number of voters = ",numVoters)
            print("Max ballot length = ",maxBLen)
            print("Preferred winner = ", cw)
            print("Upper bound = ",ub)
            print("heuristic margin = ",heuristicV1_margin)

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



            ###################################################### OURS ################################################

            blomMargin = BlomMargin()
            start = timeit.default_timer()
            marginBlom = blomMargin.marginBlom(C,B,cw)
            end = timeit.default_timer()
            runtimeBlom = end - start
            print("################# Blom Result ########################")
            print("margin  = ", marginBlom)
            print("run time = ", runtimeBlom)
            print("number of nodes explored = ",blomMargin.nodeExplored)
            print("number of ILPs = ",blomMargin.numLP)

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
            result = result + str(cw[0])+"_"+ str(cw[1]) + ","
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
            result = result + str(heuristicV2_equal) + ","
            result = result + str(heuristicV2_approx_correct) + ","
            #debug
            result =  result + str(ourMargin.numLP) + ","
            result =  result + str(blomMargin.numLP) + ","
            result =  result + str(ourMargin.nodeExplored) + ","
            result = result + str(blomMargin.nodeExplored) + ","
            result = result + str(ourMargin.blomLBCall) + ","
            result =  result + str(blomMargin.branchExplored) + "\n"
            f.write(result)
            break
    f.close()


def runDummyData(numIt,numCand,numSig,bsize,fixed,bPerSig):
    result = "Dataset," \
             "Number_Of_Candidates," \
             "Number_of_voters," \
             "Max_Ballot_length," \
             "Upper_Bound," \
             "Our_margin," \
             "Blom_margin," \
             "Correct," \
             "Our_runtime," \
             "Blom_runtime," \
             "Our_number_LPS," \
             "Blom_number_LPS," \
             "Our_number_node_explored," \
             "Blom_number_node_explored\n"

    f = open("result_dummy.csv", "w")
    f.write(result)

    for it in range(0,numIt):

        bsize = it%10 + 1
        #numCand = 3 + it

        B,C = createDummyInput(numCand,numSig,bsize,fixed,bPerSig,it)

        datasetName = "Dummy_"+str(it)
        pi = IRV(B, C)
        n = len(C)
        maxBLen = bsize
        cw = pi[n - 1]
        numVoters = sum(B.values())
        ub = LRM(B, C)

        result = ""
        result = result + datasetName + ","
        result = result + str(n) + ","
        result = result + str(numVoters) + ","
        result = result + str(maxBLen) + ","
        result = result + str(ub) + ","

        print("################# Election ########################")
        print("Dataset Name = ", datasetName)
        print("Number of candidates = ", n)
        print("Number of voters = ", numVoters)
        print("Max ballot length = ", maxBLen)
        print("Upper bound = ", ub)


        ################################################# Ours #########################################################

        ourMargin = OurMargin()
        start = timeit.default_timer()
        marginOurs = ourMargin.marginOurs(C, B, cw)
        end = timeit.default_timer()
        runtimeOurs = end - start
        print("################# Our Result ########################")
        print("margin  = ", marginOurs)
        print("run time = ", runtimeOurs)
        print("number of nodes explored = ", ourMargin.nodeExplored)
        print("number of nodes explored = ", ourMargin.numLP)

        ###################################################### Bloms ####################################################

        blomMargin = BlomMargin()
        start = timeit.default_timer()
        marginBlom = blomMargin.marginBlom(C, B, cw)
        end = timeit.default_timer()
        runtimeBlom = end - start
        print("################# Blom Result ########################")
        print("margin  = ", marginBlom)
        print("run time = ", runtimeBlom)
        print("number of nodes explored = ", blomMargin.nodeExplored)
        print("number of nodes explored = ", blomMargin.numLP)

        ##########################################################################################################

        ourMarginHeuristic = OurHeuristic()
        start = timeit.default_timer()
        marginOurHeuristic = ourMarginHeuristic.marginOurs(C, B, cw)
        end = timeit.default_timer()
        runtimeOurHeuristic = end - start
        print("################# Our Result ########################")
        print("margin  = ", marginOurHeuristic)
        print("run time = ", runtimeOurHeuristic)
        print("number of nodes explored = ", ourMarginHeuristic.nodeExplored)
        print("number of nodes explored = ", ourMarginHeuristic.numLP)


        ##########################################################################################################
        correct = 1
        if marginOurs != marginBlom:
            print("error in calculation")
            correct = 0

        result = result + str(marginOurs) + ","
        result = result + str(marginBlom) + ","
        result = result + str(correct) + ","
        result = result + str(runtimeOurs) + ","
        result = result + str(runtimeBlom) + ","
        result = result + str(ourMargin.numLP) + ","
        result = result + str(blomMargin.numLP) + ","
        result = result + str(ourMargin.nodeExplored) + ","
        result = result + str(blomMargin.nodeExplored) + "\n"

        f.write(result)

    f.close()







def runMovieData(path):



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
            "HeuristicV2_equl_margin," \
            "HeuristicV2_approximation_correct," \
            "Our_number_LPS," \
            "Blom_number_LPS," \
            "Our_number_node_explored," \
            "Blom_number_node_explored," \
            "Our_blom_lb_calls," \
            "Blom_Leaf_node_explored\n"


    f = open("result/movieLens_b=4_vary_n.csv", "a")
    f.write(result)

    dir_list = os.listdir(path)
    print(dir_list)





    for inputfile in dir_list:

        if inputfile.__contains__(".txt") == False:
            continue
        datasetName = inputfile.split(".")[0]
        fileName = path +"/"+ inputfile
        B,C,n,maxBLen = readInput(fileName)




        movieDesPath = path+"/"+ "movieLens_movie=_30_description.csv"
        movieGnere = pd.read_csv(movieDesPath, names=['MovieId', 'MovieName', 'Genre'])
        movieGenre = {}
        for ind, row in movieGnere.iterrows():
            if row['Genre'] in movieGenre:
                movieGenre[row['Genre']].append(row['MovieId'])
            else:
                movieGenre[row['Genre']] = [row['MovieId']]

        for genre, cw_all in movieGenre.items():

            cw = []
            for can in cw_all:
                if can < n:
                    cw.append(can)

        #for cw in itertools.combinations(C, 2):
        #for cw in C:
            identifier = genre
            numVoters = sum(B.values())
            ub = upperBound(B,C,cw)

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



            ###################################################### OURS ################################################

            blomMargin = BlomMargin()
            start = timeit.default_timer()
            marginBlom = blomMargin.marginBlom(C,B,cw)
            end = timeit.default_timer()
            runtimeBlom = end - start
            print("################# Blom Result ########################")
            print("margin  = ", marginBlom)
            print("run time = ", runtimeBlom)
            print("number of nodes explored = ",blomMargin.nodeExplored)
            print("number of ILPs = ",blomMargin.numLP)

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
            result = result + str(heuristicV2_equal) + ","
            result = result + str(heuristicV2_approx_correct) + ","
            #debug
            result =  result + str(ourMargin.numLP) + ","
            result =  result + str(blomMargin.numLP) + ","
            result =  result + str(ourMargin.nodeExplored) + ","
            result = result + str(blomMargin.nodeExplored) + ","
            result = result + str(ourMargin.blomLBCall) + ","
            result =  result + str(blomMargin.branchExplored) + "\n"
            f.write(result)
            #break
    f.close()
 # To test dummy dataset specify following parameters.
# numIt,numCand,numSig,bsize,fixed,bPerSig
# runDummyData(100,10,500,10,1,10)