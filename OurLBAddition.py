from Utils import projectedBallots
import math

def  OurLB(B,pi):
    LB = 0
    B = projectedBallots(B, pi)
    pi = list(pi)
    while len(pi) != 0:
        Tally = {}
        for c in pi:
            Tally[c] = 0
        for s, count in B.items():
            if len(s) == 0:
                continue
            u = [x for x in s if x in pi]
            if len(u) > 0:
                w = u[0]
                Tally[w] = Tally[w] + count
        e = pi[0]
        pi.remove(e)

        allci = []
        for c in pi:
            #LB = math.ceil(max(LB, (Tally[e] - Tally[c]) / 2))
            if Tally[e] > Tally[c]:
                allci.append(Tally[c])

        allci.sort()

        if len(allci) != 0:
            minCi = min(allci)

            LB_t = 999999999999
            lo = minCi
            hi = Tally[e]

            while lo<hi:
                t = math.floor((hi + lo)/2)
                lb_t1 = Tally[e] - t
                lb_t2 = sum([t - x for x in allci if x < t])
                LB_t = max(lb_t1, lb_t2)

                t = t + 1
                lb_t1 = Tally[e] - t
                lb_t2 = sum([t - x for x in allci if x < t])
                LB_t_1 = max(lb_t1, lb_t2)

                if LB_t < LB_t_1:
                    hi = t - 1
                else:
                    lo = t

            LB = max(LB,min(LB_t,LB_t_1))
    return LB