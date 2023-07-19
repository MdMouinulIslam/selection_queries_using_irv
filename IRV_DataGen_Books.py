#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
#from utils import plot
import numpy as np


# In[2]:


#https://www.kaggle.com/datasets/kayscrapes/movie-dataset?resource=download
#http://www2.informatik.uni-freiburg.de/~cziegler/BX/

def genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS):

    datasetname = r'Data\BOOKS'
    MIN_COUNT = 1

    inputratingfile= r'Data\imdbraw\BX-Book-Ratings.csv'
    inputmoviefile=r'Data\imdbraw\books.csv'


    data = pd.read_csv(inputratingfile,";")


    dataGrouped = data.groupby('ISBN').agg(["count"])



    dataGrouped = dataGrouped.iloc[:, [1]]



    dataGrouped.columns = ['count']



    # In[11]:


    dataFiltered = dataGrouped[dataGrouped['count'] > MIN_COUNT]


    dataFiltered = dataFiltered.sort_values(by=['count'],ascending=[False])



    popularMoviesDf = dataFiltered.head(NUM_MOVIES+10)


    print(NUM_MOVIES)
    popular_movie_file = datasetname + "/books_candidates_n="+str(NUM_MOVIES)+".csv"


    popularMoviesDf.to_csv(popular_movie_file)


    popularMoviesDf = pd.read_csv(popular_movie_file)



    popular_movies = popularMoviesDf['ISBN'].tolist()[10:NUM_MOVIES+10]


    selectedRows = data[data['ISBN'].isin(popular_movies)]



    ballotsDic = {}
    for  index, row in selectedRows.iterrows():
        movieId = row['ISBN']
        rating = row['Book-Rating']
        userId = row['User-ID']
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
        # if BallotProfile[ballotTuple] > 1:
        #     BallotProfile[ballotTuple] = 1

        numBallots = numBallots + 1
        if numBallots >= NUM_VOTERS:
            break

    print("num voters = ", sum(list(BallotProfile.values())))

    #writeTo
    inputfilename = datasetname + "/book=" + str(NUM_MOVIES) + "_ballot=" + str(NUM_VOTERS) + "bs=" + str(
        BALLOT_SIZE) + ".txt"
    # writeTo
    #inputfilename = datasetname + "/movieLens_movie=" + str(NUM_MOVIES) + "_ballot=" + str(BALLOT_SIZE) + ".txt"
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
        for i in range(0, min(NUM_MOVIES, 26)):
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


    #*********************************************************************************************************************************




    # df = pd.read_csv(inputmoviefile, header=None, sep='\n')
    # df = df[0].str.split(';', expand=True)
    #df.to_csv(r"imdbraw\books.csv",sep=",",header=False,index=False)



    dataMovies = pd.read_csv(inputmoviefile,",")




    # selectedMovieDes = dataMovies[dataMovies['ISBN'].isin(popular_movies)]
    #
    # selectedMovieDes = []
    # for c,row in dataMovies.iterrows():
    #     for m in popular_movies:
    #         if row['ISBN'] == m:
    #             selectedMovieDes.append(m)

    movieid = 0
    modifiedMovies = []
    for row in dataMovies.iterrows():
        #movieid = row[1]['ISBN']
        movieid = movieid + 1
        year = row[1]['Year-Of-Publication']
        title = row[1]['Book-Title']
        row = [movieid,title,year]
        modifiedMovies.append(row)
        if movieid == len(popular_movies):
            break




    # Create the pandas DataFrame
    modifiedmoviedf = pd.DataFrame(modifiedMovies, columns=['movieId','title','genres'])

    movieoutfile = datasetname+"/book_crossing="+str(NUM_MOVIES)+"_description.csv"
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
NUM_VOTERS_LIST= [100,1000,1500,3000]
for NUM_VOTERS in NUM_VOTERS_LIST:
    genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS)