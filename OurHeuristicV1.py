import sys
from Utils import  UpdateableQueue

import math

B_start = {}

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


def findTallyOptimise(B,S):
    Tally = {}
    for s, count in B.items():
        start = 0
        if s in B_start:
            start = B_start[s]
        else:
            B_start[s] = 0

        for i in range(start,len(s)):
            w = s[i]
            if w in S:
                if w in Tally:
                    Tally[w] = Tally[w] + count
                else:
                    Tally[w] = count

                break
            else:
                B_start[s] = B_start[s] + 1
    return Tally


def boundTree1(B,S,c_w,UB):
    if len(S) != len(c_w):
        Tally = findTally(B, S)

        temp = {};
        for c in c_w :
            temp[c] = Tally[c]
            Tally[c] = sys.maxsize

        # temp = Tally[c_w]
        # Tally[c_w] = sys.maxsize

        minval = min(Tally.values())
        allMin = [k for k, v in Tally.items() if v == minval]

        for loser in allMin:
            S_copy = S.copy()
            S_copy.remove(loser)


            for c in c_w:
                Tally[c] = temp[c]
                UB = UB + max(UB, (Tally[loser] - Tally[c]))
            UB = max(UB,boundTree1(B,S_copy,c_w,UB))
    return UB


def boundTree2(B,S,c_w,UB):
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
            UB = max(UB,boundTree2(B,S_copy,c_w,UB))
    return UB


def heuristic(B,C,c_w):
    for s in B:
        B_start[s] = 0
    S = list(C)
    UB = 0
    minUB = sys.maxsize
    for c in c_w:
        UB = boundTree2(B, S, c, UB)
        minUB = min(UB, minUB)
    return minUB








def heuristicFaster(B,C,c_w):
    global B_start
    elimOrder = []
    c_w = c_w[0]
    S = set(C)
    UB = 0
    count = len(S)
    B_start = {}



    while count > 1:
        Tally = findTallyOptimise(B,S)
        #
        #Tally = findTally(B,S)

        if c_w in Tally:
            temp = Tally[c_w]
        else:
            temp  = 0

        Tally[c_w] = sys.maxsize
        minVal = sys.maxsize
        lastCand = -1
        for c in S:
            if c not in Tally:
                Tally[c] = 0
                lastCand = c
                break
            else:
                if Tally[c] < minVal:
                    minVal = Tally[c]
                    lastCand = c

        # minval = min(Tally.values())
        # allMin = [k for k, v in Tally.items() if v == minval]
        # lastCand = allMin[0]

        S.remove(lastCand)
        elimOrder.append(lastCand)
        Tally[c_w] = temp
        UB = max(UB,Tally[lastCand] - Tally[c_w])
        count = count - 1
    elimOrder.append(c_w)
    return UB,elimOrder


class Ballot:
   def __init__(self, signature=None,signatureCount = None):
      signature = list(signature)
      signature.reverse()
      self.signature = signature
      self.signatureCount = signatureCount
   def getFirstChoiceCandidate(self):
        if len(self.signature) > 0:
            return self.signature[-1]
        else:
            return -1
   def removeFirstChoiceCandidate(self):
       if len(self.signature) > 0:
           self.signature.pop()

   def getBallotLength(self):
        return len(self.signature)


def heuristicV3(B,C,cw):
    tallyDict = {}
    tallyCount = {}
    for signature,count in B.items():
        b = Ballot(signature,count)
        firstChoice = b.getFirstChoiceCandidate()
        # b.removeFirstChoiceCandidate()

        if firstChoice not in tallyDict:
            tallyDict[firstChoice] = {b}
            tallyCount[firstChoice] = count
        else:
            tallyDict[firstChoice].add(b)
            tallyCount[firstChoice] = tallyCount[firstChoice] + count



    remainCand = len(C)
    elimOrder = []
    S = set(C)
    UB = 0

    while remainCand > 1:
        if cw in tallyCount:
            temp = tallyCount[cw]
        else:
            temp = 0
        tallyCount[cw] = sys.maxsize
        minVal = sys.maxsize
        lastCand = -1
        for c in S:
            if c in tallyCount:
                if tallyCount[c] < minVal:
                    minVal = tallyCount[c]
                    lastCand = c
            else:
                lastCand = c
                minVal = 0
                tallyCount[c] = 0
        #heap
        #runtime for baseline
        #plot irv varying candidates, ballot size.

        S.remove(lastCand)
        elimOrder.append(lastCand)
        tallyCount[cw] = temp
        UB = max(UB, tallyCount[lastCand] - tallyCount[cw])
        remainCand = remainCand - 1

        #########################
        # calculate new tally
        tallyCount[lastCand] = 0

        if lastCand not in tallyDict:
            continue
        if len(tallyDict[lastCand]) == 0:
            continue

        for b in tallyDict[lastCand]:
            count = b.signatureCount
            b.removeFirstChoiceCandidate()
            if b.getBallotLength() < 1:
                continue
            firstChoice = b.getFirstChoiceCandidate()
            while(firstChoice not in S):
                b.removeFirstChoiceCandidate()
                firstChoice = b.getFirstChoiceCandidate()
                if b.getBallotLength() < 1:
                    break
            if b.getBallotLength() < 1:
                continue

            if firstChoice not in tallyDict:
                tallyDict[firstChoice] = {b}
                tallyCount[firstChoice] = count
            else:
                tallyDict[firstChoice].add(b)
                tallyCount[firstChoice] = tallyCount[firstChoice] + count



    elimOrder.append(cw)
    return UB, elimOrder


def heuristicV4(B, C, cw):
    tallyDict = {}
    tallyCount = {}
    totalModCand = 0

    heap = UpdateableQueue()

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




    remainCand = len(C)
    elimOrder = []
    S = set(C)
    UB = 0

    for candidate in S:
        count = 0
        if candidate in tallyCount:
            count = tallyCount[candidate]
        if candidate != cw:
            heap.push(candidate,count)
        # heappush(heap, (count, candidate))





    while remainCand > 1:
        if cw in tallyCount:
            temp = tallyCount[cw]
        else:
            temp = 0
        tallyCount[cw] = sys.maxsize

        lastCand, minVal = heap.pop()  #heappush(heap)

        S.remove(lastCand)
        elimOrder.append(lastCand)
        tallyCount[cw] = temp
        UB = max(UB, minVal - tallyCount[cw])
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
            if candidate != cw:
                heap.push(candidate,count)
        totalModCand = totalModCand + len(modifiedCand)

    elimOrder.append(cw)
    return UB, elimOrder,totalModCand



def heuristicSingleWinner(B, C, cw):
    tallyDict = {}
    tallyCount = {}
    totalModCand = 0

    heap = UpdateableQueue()

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




    remainCand = len(C)
    elimOrder = []
    S = set(C)
    UB = 0

    for candidate in S:
        count = 0
        if candidate in tallyCount:
            count = tallyCount[candidate]
        if candidate != cw:
            heap.push(candidate,count)
        # heappush(heap, (count, candidate))





    while remainCand > 1:
        if cw in tallyCount:
            temp = tallyCount[cw]
        else:
            temp = 0
        tallyCount[cw] = sys.maxsize
        minVal = sys.maxsize
        lastCand = -1
        # for c in S:
        #     if c in tallyCount:
        #         if tallyCount[c] < minVal:
        #             minVal = tallyCount[c]
        #             lastCand = c
        #     else:
        #         lastCand = c
        #         minVal = 0
        #         tallyCount[c] = 0
        # heap
        # runtime for baseline
        # plot irv varying candidates, ballot size.

        lastCand, minVal = heap.pop()  #heappush(heap)

        S.remove(lastCand)
        elimOrder.append(lastCand)
        tallyCount[cw] = temp
        UB = max(UB, minVal - tallyCount[cw])
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
            if candidate != cw:
                heap.push(candidate,count)
        totalModCand = totalModCand + len(modifiedCand)

    elimOrder.append(cw)
    return UB, elimOrder,totalModCand