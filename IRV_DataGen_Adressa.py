
import pandas as pd
import json


def genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS):
    # ************ fname ******************
    file = r"Data\adressaraw\20170101"
    MAX= 10000000
    MAXB = NUM_VOTERS

    count = 0
    allrows = []
    with open(file) as f:
        for line in f:
            row = []
            jsonData = json.loads(line)
            row.append(jsonData['userId'])
            row.append(jsonData['url'])
            if jsonData['url'] == "http://adressa.no":
                continue
            if 'activeTime' not in jsonData:
                continue
            row.append(jsonData['activeTime'])
            if 'region' not in jsonData:
                continue
            row.append(jsonData['region'])
            allrows.append(row)
            count = count + 1
            # if count == MAX:
            #     break




    data = pd.DataFrame(allrows, columns=['userId', 'url','activeTime','region'])

    # ************ fname ******************
    datasetname = r"Data\ADRESSA"
    MIN_COUNT = 0



    dataGrouped = data.groupby('url').agg(["count"])




    dataGrouped = dataGrouped.iloc[:, [1]]



    dataGrouped.columns = ['count']



    dataFiltered = dataGrouped[dataGrouped['count'] > MIN_COUNT]



    dataFiltered = dataFiltered.sort_values(by=['count'],ascending=[False])



    popularMoviesDf = dataFiltered.head(NUM_MOVIES)



    # ************ fname ******************
    popular_movie_file = r"Data\ADRESSA\temp\adressa_candidates_n="+str(NUM_MOVIES)+".csv"



    popularMoviesDf.to_csv(popular_movie_file)


    # In[133]:


    popularMoviesDf = pd.read_csv(popular_movie_file)


    # In[134]:


    popular_movies = popularMoviesDf['url'].tolist()




    selectedRows = data[data['url'].isin(popular_movies)]




    ballotsDic = {}
    for  index, row in selectedRows.iterrows():
        movieId = row['url']
        rating = row['activeTime']
        userId = row['userId']
        if(userId in ballotsDic):
            ballotsDic[userId].append((rating,movieId))
        else:
            ballotsDic[userId] = [(rating,movieId)]




    popular_moviesToId = {}
    ID = 0
    for movieId in popular_movies:
        popular_moviesToId[movieId] = ID
        ID = ID + 1


    # In[142]:


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
        ballotTuple = tuple(set(ballotArr))
        # if len(ballotTuple) < BALLOT_SIZE:
        #     continue
        # if len(ballotTuple) < 30:
        #     continue
        if ballotTuple in BallotProfile:
            BallotProfile[ballotTuple] = BallotProfile[ballotTuple]  + 1
        else:
            BallotProfile[ballotTuple] =  1
        # if BallotProfile[ballotTuple] > 2:
        #     BallotProfile[ballotTuple] = 0
        numBallots = numBallots + 1
        if numBallots >= MAXB:
            break


    print("num voters = ",sum(list(BallotProfile.values())))

    #writeTo
    inputfilename = datasetname + "/adressa=" + str(NUM_MOVIES) + "_ballot=" + str(NUM_VOTERS) + "bs=" + str(
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
        for i in range(0,26):
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




    selectedMovieDes = data[data['url'].isin(popular_movies)]


    modifiedMovies = []


    # In[94]:


    for row in selectedMovieDes.iterrows():
        movieid = row[1]['url']
        movieid = popular_moviesToId[movieid]
        genres = row[1]['region']
        name = "nan"
        row = [movieid,name,genres]
        modifiedMovies.append(row)





    # In[97]:




    # Create the pandas DataFrame
    modifiedmoviedf = pd.DataFrame(modifiedMovies, columns=['MovieId', 'MovieName', 'Genre'])


    # In[99]:


    movieoutfile = r"Data\ADRESSA\adressa="+str(NUM_MOVIES)+"_description.csv"
    modifiedmoviedf.to_csv(movieoutfile)



# NUM_VOTERS = 10000000
# BALLOT_SIZE_LIST = [4,5,6,7,8]
# NUM_MOVIES = 8
# for BALLOT_SIZE in BALLOT_SIZE_LIST:
#     genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS)


#genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS)

NUM_VOTERS = 10000000
BALLOT_SIZE_LIST = [4,5,6,7,8]
BALLOT_SIZE = 4
NUM_MOVIES = 8
NUM_VOTERS_LIST= [1000,5000,10000,30000]
for NUM_VOTERS in NUM_VOTERS_LIST:
    genData(NUM_MOVIES,BALLOT_SIZE,NUM_VOTERS)
