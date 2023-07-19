import heapq

def IRV(B, C):
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

    elimOrder.extend(S)
    return elimOrder



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

class UpdateableQueue:
   def __init__(self, iterable=None):
       self._heap = []
       self._entry_finder = {}
       if iterable:
           for item in iterable:
               self._entry_finder[item[0]] = item[1]
               heapq.heappush(self._heap, (item[1], item[0]))

   def __getitem__(self, key):
       if key in self._entry_finder:
           return self._entry_finder[key]
       else:
           raise KeyError('Item not found in the priority queue')

   def __len__(self):
       return len(self._entry_finder)

   def __contains__(self, key):
       return key in self._entry_finder

   def push(self, key, priority):
       self._entry_finder[key] = priority
       heapq.heappush(self._heap, (priority, key))

   def pop(self):
       if not self._heap:
           raise IndexError("The heap is empty")

       value, key = self._heap[0]
       while key not in self or self._entry_finder[key] != value:
           heapq.heappop(self._heap)
           if not self._heap:
               raise IndexError("The heap is empty")
           value, key = self._heap[0]

       value, key = heapq.heappop(self._heap)
       del self._entry_finder[key]
       return key, value


C = {'a','b','c','d'}
B = {('a','b','c'):2,
    ('b','d','c'):3,
     ('d','b'):4}
elimination_order = IRV(B,C)
print("winner is : ",elimination_order[-1])
