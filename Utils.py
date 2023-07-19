

import  random as rnd
import numpy as np
import sys

import heapq
from heapq import heapify, heappush, heappop

class UpdateableQueue:
    def __init__(self,iterable=None):
        self._heap = []
        self._entry_finder = {}
        if iterable:
            for item in iterable:
                self._entry_finder[item[0]] = item[1]
                heapq.heappush(self._heap,(item[1],item[0]))

    def __getitem__(self, key):
        if key in self._entry_finder:
            return self._entry_finder[key]
        else:
            raise KeyError('Item not found in the priority queue')

    def __len__(self):
        return len(self._entry_finder)

    def __contains__(self, key):
        return key in self._entry_finder

    def push(self, key,priority):
        self._entry_finder[key] = priority
        heapq.heappush(self._heap, (priority, key))

    def pop(self):
        if not self._heap:
            raise IndexError("The heap is empty")

        value,key = self._heap[0]
        while key not in self or self._entry_finder[key] != value:
            heapq.heappop(self._heap)
            if not self._heap:
                raise IndexError("The heap is empty")
            value,key = self._heap[0]

        value, key = heapq.heappop(self._heap)
        del self._entry_finder[key]
        return key,value



# queue = UpdateableQueue()
# # Inserting key=1,priority=4 element to the queue the heap is now of size 1, and the dict size 1
# queue.push(1,4)
#
# queue.push(2,5)
#
# queue.push(1,1)
#
#
# # assert len(queue) == 2
# # We "clean" the remaining (1,4) element from the heap and return pop (2,5) as expected.
# key, value = queue.pop()




def IRVV1(B, C):
    n = len(C)
    pi = []
    C_pi = set(C) - set(pi)
    round = 0
    once = True
    TopCand = []
    while (len(C_pi) != 1):
        round = round + 1
        #print("round = ",round)

        # B_prime = projectedBallots(B, C_pi)
        # T = findTally(B_prime, C_pi)
        T = findTallyOnProjectedBallots(B,C_pi)
        #print("Tally = ",T)
        # if T != T1:
        #     print("wrong")
        if once:
            sortedT = sorted(T.items(), key=lambda x:x[1],reverse=True)
            for cand,votes in sortedT:
                TopCand.append(cand)
            once = False

        # print(TopCand)
        e = min(T, key=T.get)
        pi.append(e)
        C_pi = set(C) - set(pi)
    pi.extend(C_pi)
    return pi,TopCand



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

def IRV(B,C):
    totalModCand = 0
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

    TopCand = []
    sortedT = sorted(tallyCount.items(), key=lambda x: x[1], reverse=True)
    for cand, votes in sortedT:
        TopCand.append(cand)

    remainCand = len(C)
    elimOrder = []
    S = set(C)
    #UB = 0

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
            while(firstChoice not in S):
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

    elimOrder.extend(S)
    return  elimOrder

def findTallyOnProjectedBallots(B,S):
    Tally = {}
    for c in S:
        Tally[c] = 0
    for s, count in B.items():
        u = [x for x in s if x in S]
        if len(u) > 0:
            w = u[0]
            Tally[w] = Tally[w] + count
    return Tally


def delBallots(B,percentToDel):
    Bnew = {}
    for b,c in B.items():
        r = rnd.random()
        if r > percentToDel:
            Bnew[b] = c
    return Bnew

def changeBallotsAddition(B,numBallotAdd,maxBLen,topCand):

    B_New = B.copy()
    br = int(sum(B.values())/len(B))

    while numBallotAdd > 0:
        bs = 4#rnd.randint(2,maxBLen)
        signew = tuple(np.random.choice(topCand, bs,replace = False))
        bc = rnd.randint(1,br)
        if bc > numBallotAdd:
            bc = numBallotAdd
        if signew in B_New:
            B_New[signew] = B_New[signew] + bc
        else:
            B_New[signew] = bc
        numBallotAdd = numBallotAdd - bc
    return B_New


def projectedBallots(ballots,pi):
    newBallots = {}
    for signature,count in ballots.items():
        newSignature = []
        for candidate in signature:
            if candidate in pi:
                newSignature.append(candidate)
        if tuple(newSignature) in newBallots:
            newBallots[tuple(newSignature)] = newBallots[tuple(newSignature)]  + count
        else:
            newBallots[tuple(newSignature)] = count
    return newBallots








def projectedBallotsAndTally(ballots,pi,e):
    newBallots = {}
    T = {}
    for i in pi:
        T[i] = 0
    for signature,count in ballots.items():
        newSignature = []
        for candidate in signature:
            if candidate in pi:
                T[candidate] = T[candidate] + count
                break
            if candidate == e:
                break
    return T

def findTally(B,C):
    T = {}
    for i in C:
        T[i] = 0
    for s,c in B.items():
        if len(s) == 0:
            continue
        w = s[0]
        T[w] = T[w] + c
    return T


def finAllSignature(pi):
    pi = list(pi)
    pi.reverse()
    allSig = []
    for i in range(0,len(pi)):
        c = pi[i]
        newSig = []
        for s in allSig:
            sl = list(s)
            sl.insert(0,c)
            newSig.append(tuple(sl))
        allSig.extend(newSig)
        allSig.append(tuple([c]))
    return allSig

def createEquivalenceClasses(B,pi):
    pi = list(pi)
    pi.reverse()
    B_new = {}
    for b in B.keys():
        b_new = []
        if len(b) == 0:
            continue
        c = b[0]
        b_new.append(c)
        i = pi.index(c)
        for c in b:
            j = pi.index(c)
            if j < i:
                i = j
                b_new.append(c)
        b_new = tuple(b_new)
        if b_new in B_new:
            B_new[b_new] = B_new[b_new] + B[b]
        else:
            B_new[b_new] = B[b]

    return B_new