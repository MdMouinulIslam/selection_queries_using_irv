

from Utils import projectedBallots
from Utils import findTally
import math


def LRM(B, C):
    n = len(C)
    pi = []
    C_pi = set(C) - set(pi)
    while (len(C_pi) != 1):
        B = projectedBallots(B, C_pi)
        T = findTally(B, C_pi)
        e = min(T, key=T.get)
        pi.append(e)
        C_pi = set(C) - set(pi)
    pi.extend(C_pi)
    S = [pi[n-2],pi[n-1]]
    B = projectedBallots(B, S)
    T = findTally(B,S)
    UB = math.ceil((T[pi[n-1]] - T[pi[n-2]])/2)

    return UB
