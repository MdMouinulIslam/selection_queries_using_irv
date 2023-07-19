#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
#from utils import plot
import numpy as np


#https://data.world/sumitrock/rating/workspace/file?filename=rating_final.csv



def genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS):

    datasetname =  r"Data\FOODS"
    MIN_COUNT = 2
    inputratingfile= r'Data\foodrevewraw\food.csv'
    inputmoviefile=r'Data\foodrevewraw\food.csv'



    data = pd.read_csv(inputratingfile,",")


    dataGrouped = data.groupby('placeID').agg(["count"])


    dataGrouped = dataGrouped.iloc[:, [1]]



    dataGrouped.columns = ['count']



    dataFiltered = dataGrouped[dataGrouped['count'] > MIN_COUNT]


    dataFiltered = dataFiltered.sort_values(by=['count'],ascending=[False])


    popularMoviesDf = dataFiltered.head(NUM_MOVIES)

    popular_movie_file = datasetname +r'\foods_candidates_n='+str(NUM_MOVIES)+'.csv'

    popularMoviesDf.to_csv(popular_movie_file)


    popularMoviesDf = pd.read_csv(popular_movie_file)

    popular_movies = popularMoviesDf['placeID'].tolist()


    selectedRows = data[data['placeID'].isin(popular_movies)]


    ballotsDic = {}
    for  index, row in selectedRows.iterrows():
        movieId = row['placeID']
        rating = row['rating']
        userId = row['userID']
        if(userId in ballotsDic):
            ballotsDic[userId].append((rating,movieId))
        else:
            ballotsDic[userId] = [(rating,movieId)]



    popular_moviesToId = {}
    ID = 0
    for movieId in popular_movies:
        popular_moviesToId[movieId] = ID
        ID = ID + 1


    BallotProfile = {}
    numBallots = 0
    for userId, movieArr in ballotsDic.items():
        movieArr = sorted(movieArr)
        ballotArr = []
        ballotSize = 0
        for rating,movieId in movieArr:
            ballotArr.append(popular_moviesToId[movieId])
            ballotSize = ballotSize + 1
            if(ballotSize == BALLOT_SIZE):
                break
        ballotTuple = tuple(ballotArr)
        if ballotTuple in BallotProfile:
            BallotProfile[ballotTuple] = BallotProfile[ballotTuple]  + 1
        else:
            BallotProfile[ballotTuple] =  1
        # if BallotProfile[ballotTuple] > 3:
        #     BallotProfile[ballotTuple] = 0
        numBallots = numBallots + 1
        if numBallots >= NUM_VOTERS:
            break

    print("num voters = ", sum(list(BallotProfile.values())))
    #writeTo
    inputfilename = datasetname + "/food=" + str(NUM_MOVIES) + "_ballot=" + str(NUM_VOTERS) + "bs=" + str(
        BALLOT_SIZE) + ".txt"

    with open(inputfilename, 'w') as movieLensText:
        #movie id
        textWrite = ""
        for i in range(0,NUM_MOVIES):
            textWrite = textWrite + str(i)
            if i != NUM_MOVIES - 1:
                textWrite = textWrite + ", "
            else:
                textWrite = textWrite + "\n"

        movieLensText.write(textWrite)

        #movie names
        textWrite = ""
        for i in range(0,NUM_MOVIES):
            textWrite = textWrite + chr(65+i)
            if i != NUM_MOVIES - 1:
                textWrite = textWrite + ","
            else:
                textWrite = textWrite + "\n"

        movieLensText.write(textWrite)
        movieLensText.write("-+-+-+-+-\n")
        for signature, value in BallotProfile.items():
            textWrite = "("
            count = 0
            for mid in signature:
                textWrite = textWrite + str(mid)
                count = count + 1
                if(count != len(signature)):
                    textWrite = textWrite + ","
            textWrite = textWrite + ")"
            textWrite = textWrite + " : "
            textWrite = textWrite + str(value)
            textWrite = textWrite + "\n"

            movieLensText.write(textWrite)



    #*********************************************************************************************************************************



    dataMovies = pd.read_csv(inputmoviefile,",")



    selectedMovieDes = dataMovies[dataMovies['placeID'].isin(popular_movies)]


    modifiedMovies = []


    for row in selectedMovieDes.iterrows():
        movieid = row[1]['placeID']
        movieid = popular_moviesToId[movieid]
        serviceRating = row[1]['service_rating']
        foodRating = row[1]['food_rating']
        row = [movieid,serviceRating,foodRating]
        modifiedMovies.append(row)



    # Create the pandas DataFrame
    modifiedmoviedf = pd.DataFrame(modifiedMovies, columns=['movieId','title','genres'])

    movieoutfile = datasetname+r'\foods='+str(NUM_MOVIES)+"_description.csv"
    modifiedmoviedf.to_csv(movieoutfile)




# NUM_VOTERS = 10000000
# BALLOT_SIZE_LIST = [4,5,6,7,8]
# NUM_MOVIES = 8
# for BALLOT_SIZE in BALLOT_SIZE_LIST:
#     genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS)



NUM_VOTERS = 10000000
BALLOT_SIZE_LIST = [4,5,6,7,8]
BALLOT_SIZE = 4
NUM_MOVIES = 8
NUM_VOTERS_LIST= [10,20,30,50]
for NUM_VOTERS in NUM_VOTERS_LIST:
    genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS)