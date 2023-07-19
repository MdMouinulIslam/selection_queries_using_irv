import random
import pickle


def findCandidateSet(line):
    #print(line)
    C = line.split(',')
    C = [int(c)  for c in C if c !=' ']
    return C


def convertBallots(line, B,maxBLen):
    # print("line = ",line)
    line = line.replace('(', '')
    line = line.replace(')', '')
    split = line.split(':')
    # print(split)
    if len(split) == 2 and split[0] != ' ':
        pi = findCandidateSet(split[0])
        b = int(split[1])
        B[tuple(pi)] = b
        if len(pi)> maxBLen[0]:
            maxBLen[0] = len(pi)
        # print("B ",B)

#'Data_NA_Albury.txt_ballots.txt'

def readInput(file):
    numCand = 0
    C = []
    B={}


    file1 = open(file, 'r')
    Lines = file1.readlines()

    count = 0.0
    maxBLen = [0]
    # Strips the newline character
    for line in Lines:
        line = line.strip()
        #print(line)
        if count == 0:
            C = findCandidateSet(line)
            numCand = len(C)
        elif count == 1 or count == 2:
            count = count + 1
            continue  # skip
        else:
            # print(line)
            convertBallots(line, B,maxBLen)
        count = count + 1

    return B,C,numCand,maxBLen[0]


def createDummyInput(numCand,numSig,bsize,fixed,bPerSig,it):


    C = [i + 1 for i in range(numCand)]

    B = {}
    load = False
    fname = "Data/test1.pickle"
    if load:
        print(fname)
        bpkl = open(fname, 'rb')
        B = pickle.load(bpkl)
        return B,C
    else:
        for i in range(numSig):
            if fixed:
                bs = bsize
            else:
                bs = random.randint(1,bsize)

            b = random.sample(range(1, numCand + 1), bs)
            B[tuple(b)] = random.randint(0, bPerSig)


        print(fname)
        bpkl = open(fname, 'wb')
        pickle.dump(B,bpkl)

    return B,C