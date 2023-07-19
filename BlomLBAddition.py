
import math
from Utils import findTally
from Utils import projectedBallots,projectedBallotsAndTally
import timeit


def blomLBv1Addition(B, C, pi):
    start = timeit.default_timer()
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
            lb2 = (F[e] - delta_S_prime[c])
            LB = max(LB, lb2)
    end = timeit.default_timer()
    return math.ceil(LB),end-start