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


def  OurLBdp(B,pi,prevLB):
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
        LB = max(LB,prevLB)
        break
    return LB



def  OurLBdpV2(B,pi,prevLB):
    LB = 0
    #B = projectedBallots(B, pi)
    pi = list(pi)
    while len(pi) != 0:
        Tally = {}
        for c in pi:
            Tally[c] = 0
        for s, count in B.items():
            if len(s) == 0:
                continue
            for x in s:
                if x in pi:
                    Tally[x] = Tally[x] + count
                    break
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
        LB = max(LB,prevLB)
        break
    return LB

from Utils import Ballot,UpdateableQueue




def  OurLBdpV1(B,pi,prevLB):
    LB = 0
    #B = projectedBallots(B, pi)
    C = list(pi)
    totalModCand = 0
    tallyDict = {}
    tallyCount = {}
    for signature, count in B.items():
        b = Ballot(signature, count)
        firstChoice = b.getFirstChoiceCandidate()
        # b.removeFirstChoiceCandidate()

        if firstChoice not in tallyDict:
            tallyDict[firstChoice] = {b}
            tallyCount[firstChoice] = count
        else:
            tallyDict[firstChoice].add(b)
            tallyCount[firstChoice] = tallyCount[firstChoice] + count

    TopCand = []
    sortedT = sorted(tallyCount.items(), key=lambda x: x[1], reverse=True)
    for cand, votes in sortedT:
        TopCand.append(cand)

    remainCand = len(C)
    elimOrder = []
    S = set(C)
    # UB = 0

    heap = UpdateableQueue()
    for candidate in S:
        count = 0
        if candidate in tallyCount:
            count = tallyCount[candidate]
        heap.push(candidate, count)
        # heappush(heap, (count, candidate))

    while remainCand > 1:
        lastCand, minVal = heap.pop()  # heappush(heap)
        S.remove(lastCand)
        elimOrder.append(lastCand)
        # tallyCount[cw] = temp
        # UB = max(UB, tallyCount[lastCand] - tallyCount[cw])
        remainCand = remainCand - 1

        #########################
        # calculate new tally
        tallyCount[lastCand] = 0

        if lastCand not in tallyDict:
            continue
        if len(tallyDict[lastCand]) == 0:
            continue

        modifiedCand = []
        for b in tallyDict[lastCand]:
            count = b.signatureCount
            b.removeFirstChoiceCandidate()
            if b.getBallotLength() < 1:
                continue
            firstChoice = b.getFirstChoiceCandidate()
            while (firstChoice not in S):
                b.removeFirstChoiceCandidate()
                firstChoice = b.getFirstChoiceCandidate()
                if b.getBallotLength() < 1:
                    break
            if b.getBallotLength() < 1:
                continue
            modifiedCand.append(firstChoice)

            if firstChoice not in tallyDict:
                tallyDict[firstChoice] = {b}
                tallyCount[firstChoice] = count
            else:
                tallyDict[firstChoice].add(b)
                tallyCount[firstChoice] = tallyCount[firstChoice] + count

        for candidate in modifiedCand:
            count = 0
            if candidate in tallyCount:
                count = tallyCount[candidate]
            heap.push(candidate, count)
        totalModCand = totalModCand + len(modifiedCand)

        allci = []
        for c in S:
            # LB = math.ceil(max(LB, (Tally[e] - Tally[c]) / 2))
            if tallyCount[lastCand] > tallyCount[c]:
                allci.append(tallyCount[c])

        allci.sort()

        if len(allci) != 0:
            minCi = min(allci)

            LB_t = 999999999999
            lo = minCi
            hi = tallyCount[lastCand]

            while lo < hi:
                t = math.floor((hi + lo) / 2)
                lb_t1 = tallyCount[lastCand] - t
                lb_t2 = sum([t - x for x in allci if x < t])
                LB_t = max(lb_t1, lb_t2)

                t = t + 1
                lb_t1 = tallyCount[lastCand] - t
                lb_t2 = sum([t - x for x in allci if x < t])
                LB_t_1 = max(lb_t1, lb_t2)

                if LB_t < LB_t_1:
                    hi = t - 1
                else:
                    lo = t

            LB = max(LB, min(LB_t, LB_t_1))
        LB = max(LB, prevLB)
    return LB







    # pi = list(pi)
    # while len(pi) != 0:
    #     Tally = {}
    #     for c in pi:
    #         Tally[c] = 0
    #     for s, count in B.items():
    #         if len(s) == 0:
    #             continue
    #         for x in s:
    #             if x in pi:
    #                 Tally[x] = Tally[x] + count
    #                 break
    #     e = pi[0]
    #     pi.remove(e)
    #
    #     allci = []
    #     for c in pi:
    #         #LB = math.ceil(max(LB, (Tally[e] - Tally[c]) / 2))
    #         if Tally[e] > Tally[c]:
    #             allci.append(Tally[c])
    #
    #     allci.sort()
    #
    #     if len(allci) != 0:
    #         minCi = min(allci)
    #
    #         LB_t = 999999999999
    #         lo = minCi
    #         hi = Tally[e]
    #
    #         while lo<hi:
    #             t = math.floor((hi + lo)/2)
    #             lb_t1 = Tally[e] - t
    #             lb_t2 = sum([t - x for x in allci if x < t])
    #             LB_t = max(lb_t1, lb_t2)
    #
    #             t = t + 1
    #             lb_t1 = Tally[e] - t
    #             lb_t2 = sum([t - x for x in allci if x < t])
    #             LB_t_1 = max(lb_t1, lb_t2)
    #
    #             if LB_t < LB_t_1:
    #                 hi = t - 1
    #             else:
    #                 lo = t
    #
    #         LB = max(LB,min(LB_t,LB_t_1))
    #     LB = max(LB,prevLB)
    #     break
    # return LB