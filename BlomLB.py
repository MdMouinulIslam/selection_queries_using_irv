
import math
from Utils import findTally
from Utils import projectedBallots,projectedBallotsAndTally


def blomLB(B,C,pi):
    LB = 0
    if type(pi) is  int:
        pi = [pi]
    C_Pi = tuple(set(C) - set(pi))
    F = findTally(B,C)
    for e in C_Pi:
        S = set(pi).union({e})
        B_prime = projectedBallots(B,S)
        delta_S = findTally(B_prime,C)
        delta_S_prime = projectedBallotsAndTally(B,pi,e)

        for c in pi:
            lb2 = (F[e] - delta_S[c])/2
            LB = max(LB,lb2)
    return math.ceil(LB)


def blomLBv1(B, C, pi):
    LB = 0
    if type(pi) is int:
        pi = [pi]
    C_Pi = tuple(set(C) - set(pi))
    F = findTally(B, C)
    for e in C_Pi:
        #S = set(pi).union({e})
        # B_prime = projectedBallots(B, S)
        # delta_S = findTally(B_prime, C)
        delta_S_prime = projectedBallotsAndTally(B, pi, e)

        for c in pi:
            lb2 = (F[e] - delta_S_prime[c]) / 2
            LB = max(LB, lb2)
    return math.ceil(LB)