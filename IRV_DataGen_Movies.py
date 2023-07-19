#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
# from utils import plot
import numpy as np

import random as rnd
# In[2]:






def genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS):

    datasetname = "Data\MOVIE_LENS"
    MIN_COUNT = 2
    inputratingfile = r'Data\movielensraw\ratings.csv'
    inputmoviefile = r'Data\movielensraw\movies.csv'

    data = pd.read_csv(inputratingfile)



    dataGrouped = data.groupby('movieId').agg(["count"])



    dataGrouped = dataGrouped.iloc[:, [1]]



    dataGrouped.columns = ['count']



    dataFiltered = dataGrouped[dataGrouped['count'] > MIN_COUNT]

    #
    dataFiltered = dataFiltered.sort_values(by=['count'], ascending=[False])

    # In[14]:


    popularMoviesDf = dataFiltered.head(NUM_MOVIES)



    popular_movie_file = "Data\movie_lens_candidates_n=" + str(NUM_MOVIES) + ".csv"



    popularMoviesDf.to_csv(popular_movie_file)


    popularMoviesDf = pd.read_csv(popular_movie_file)




    popular_movies = popularMoviesDf['movieId'].tolist()





    selectedRows = data[data['movieId'].isin(popular_movies)]



    ballotsDic = {}
    for index, row in selectedRows.iterrows():
        movieId = row['movieId']
        rating = row['rating']
        userId = row['userId']
        if (userId in ballotsDic):
            ballotsDic[userId].append((rating, movieId))
        else:
            ballotsDic[userId] = [(rating, movieId)]




    popular_moviesToId = {}
    ID = 0
    for movieId in popular_movies:
        popular_moviesToId[movieId] = ID
        ID = ID + 1

    # In[27]:


    BallotProfile = {}
    numBallots = 0
    for userId, movieArr in ballotsDic.items():
        movieArr = sorted(movieArr)
        ballotArr = []
        ballotSize = 0
        for rating, movieId in movieArr:
            ballotArr.append(popular_moviesToId[movieId])
            ballotSize = ballotSize + 1
            if (ballotSize == BALLOT_SIZE):
                break
        ballotTuple = tuple(ballotArr)
        #################################
        # lth = len(ballotTuple)
        # dbt = []
        # numMov = len(popular_movies)
        # for i in range(0,lth):
        #     dbt.append(rnd.randint(0,numMov-1))
        # ballotTuple = tuple(dbt)
        #################################
        # if len(ballotTuple) < 45:
        #     continue
        if ballotTuple in BallotProfile:
            BallotProfile[ballotTuple] = BallotProfile[ballotTuple] + 1
        else:
            BallotProfile[ballotTuple] = 1 #rnd.randint(5,50)

        numBallots = numBallots + 1
        if numBallots >= NUM_VOTERS:
            break

    print("num voters = ",sum(list(BallotProfile.values())))
    # writeTo
    inputfilename = datasetname + "/movieLens_movie=" + str(NUM_MOVIES) + "_ballot=" + str(NUM_VOTERS)+"bs="+str(BALLOT_SIZE) + ".txt"
    with open(inputfilename, 'w') as movieLensText:
        # movie id
        textWrite = ""
        for i in range(0, NUM_MOVIES):
            textWrite = textWrite + str(i)
            if i != NUM_MOVIES - 1:
                textWrite = textWrite + ", "
            else:
                textWrite = textWrite + "\n"

        movieLensText.write(textWrite)

        # movie names
        textWrite = ""
        for i in range(0, min(NUM_MOVIES,26)):
            textWrite = textWrite + chr(65 + i)
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
                if (count != len(signature)):
                    textWrite = textWrite + ","
            textWrite = textWrite + ")"
            textWrite = textWrite + " : "
            textWrite = textWrite + str(value)
            textWrite = textWrite + "\n"

            movieLensText.write(textWrite)



    # *********************************************************************************************************************************


    dataMovies = pd.read_csv(inputmoviefile)



    selectedMovieDes = dataMovies[dataMovies['movieId'].isin(popular_movies)]


    modifiedMovies = []


    for row in selectedMovieDes.iterrows():
        movieid = row[1]['movieId']
        movieid = popular_moviesToId[movieid]
        genres = row[1]['genres']
        title = row[1]['title']
        row = [movieid, title, genres]
        modifiedMovies.append(row)

    # In[39]:


    # Create the pandas DataFrame
    modifiedmoviedf = pd.DataFrame(modifiedMovies, columns=['movieId', 'title', 'genres'])



    movieoutfile = "Data\MOVIE_LENS\movieLens_movie=" + str(NUM_MOVIES) + "_description.csv"
    modifiedmoviedf.to_csv(movieoutfile)




NUM_VOTERS = 10000000
#BALLOT_SIZE_LIST = [4,5,6,7,8]
BALLOT_SIZE = 4
#NUM_MOVIES = 10
#NUM_VOTERS_LIST= [100]
NUM_MOVIESList = [4,5,6,7,8,9,10]
for NUM_MOVIES in NUM_MOVIESList:
    genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS)





