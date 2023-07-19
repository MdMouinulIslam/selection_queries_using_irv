
import sys
import math


def findTally(B,S):
    Tally = {}
    for c in S:
        Tally[c] = 0
    for s, count in B.items():
        u = [x for x in s if x in S]
        if len(u) > 0:
            w = u[0]
            Tally[w] = Tally[w] + count
    return Tally

def boundTree1(B,S,c_w,UB):
    if len(S) != len(c_w):
        Tally = findTally(B, S)

        temp = {}
        for c in c_w :
            temp[c] = Tally[c]
            Tally[c] = sys.maxsize

        #temp = Tally[c_w]
        #Tally[c_w] = sys.maxsize

        minval = min(Tally.values())
        allMin = [k for k, v in Tally.items() if v == minval]

        for loser in allMin:
            S_copy = S.copy()
            S_copy.remove(loser)
            # Tally[c_w] = temp
            # UB = max(UB, (Tally[loser] - Tally[c_w]))
            for c in c_w:
                Tally[c] = temp[c]
                UB = UB + max(UB, (Tally[loser] - Tally[c]))
            UB = max(UB,boundTree1(B,S_copy,c_w,UB))
    return UB


def boundTree(B,S,c_w,UB):
    if len(S) != 1:
        Tally = findTally(B, S)

        temp = Tally[c_w]
        Tally[c_w] = sys.maxsize

        minval = min(Tally.values())
        allMin = [k for k, v in Tally.items() if v == minval]

        for loser in allMin:
            S_copy = S.copy()
            S_copy.remove(loser)
            Tally[c_w] = temp
            UB = max(UB, (Tally[loser] - Tally[c_w]))
            UB = max(UB,boundTree(B,S_copy,c_w,UB))
    return UB


def upperBound(B,C,c_w):

    S = list(C)
    UB = 0
    minUB = sys.maxsize
    for c in c_w:
        UB = boundTree(B, S, c, UB)
        minUB = min(UB, minUB)

    return math.ceil(minUB)

# magrino example 1
# a = 1
# b = 2
# c = 3
# d = 4
#
# B_in = {(a,c,b,d): 40,
#     (b,c,d,a): 21,
#     (c,a,b,d):10,
#     (c,a,d):10,
#     (d,b,c,a):5}
#
# C = (a,b,c,d)
#
#
# #given
# B = B_in.copy()
# c_w = d


#ub = upperBound(B,C,c_w)
