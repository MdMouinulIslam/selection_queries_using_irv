
from run import runRealData, runDummyData,runMovieData
from runAddition import runAddition
from runAdditionV2 import runAdditionV2
#from runHeuristic import runAdditionHeuristic
from runV2 import runV2
from  runAntiplurality import runAnti
from runHeuristic import  runAdditionHeuristic

def main():
    # To test on real dataset specify input file directory
    #path = "Data/USIRV"
    # path = "Data/BOOKS/"
    # resultPath = "result/Addition_books_test5.csv"
    # despath = "imdb_books"
    #runBooksDataAddition(path,resultPath,despath)
    #runMovieDataAddition(path,resultPath)
    #runMovieData(path)

    # path = "Data/FOODS"
    # resultPath = "result/TestEx5.csv"
    # despath = "foods" #movieLens_movie=4_ballot=4
    # runAddition(path,resultPath,despath)

    # path = "Data/ADRESSA"
    # resultPath = "result/TestEx12.csv"
    # despath = "adressa"  # movieLens_movie=4_ballot=4

    # runAdditionHeuristic(path, resultPath, despath)

    # path = "Data/EXAMPLE"
    # resultPath = "result/exampleV3.csv"
    # despath = "movieLens_movie"  # movieLens_movie=4_ballot=4
    # runV2(path, resultPath, despath)

    # path = "Data/MOVIE_LENS"
    # resultPath = "result/food_vary_m_V1.csv"
    # despath = "movieLens_movie"  # movieLens_movie=4_ballot=4
    # runV2(path, resultPath, despath)

    #Anti-plurality
    # path = "Data/MOVIE_LENS/anti"
    # resultPath = "result/res.csv"
    # despath = "movieLens_movie"  # movieLens_movie=4_ballot=4
    # runAnti(path, resultPath, despath)

    path = "Data/ADRESSA"
    resultPath = "result/heuristicApproxMovie.csv"
    despath = "movieLens_movie"
    runAdditionHeuristic(path,resultPath,despath)


if __name__ == '__main__':
    main()
