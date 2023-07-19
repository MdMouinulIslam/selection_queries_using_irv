
import gurobipy as gp
from gurobipy import GRB
#from Utils import projectedBallots,projectedBallotsAndTally
from  Utils import createEquivalenceClasses
from Utils import finAllSignature
import timeit
import math


def distanceToPiAddition(B,pi):

    start = timeit.default_timer()
    B = projectedBallots(B, pi)
    B = createEquivalenceClasses(B,pi)
    signature = finAllSignature(pi)
    ns ={}
    for s in signature:
        if s in B.keys():
            ns[s] = B[s]
        else:
            ns[s] = 0

    m = gp.Model('RAP')
        # Create decision variables for the RAP model
    ps = m.addVars(signature,vtype=GRB.INTEGER,name='ps')
    #ms = m.addVars(signature,vtype=GRB.INTEGER,name='ms')
    ys = m.addVars(signature,vtype=GRB.INTEGER,name='ys')
    sumPs = m.addVar(name="sumPs")
    #sumMs = m.addVar(name="sumMs")


    for s in signature:
        m.addConstr(ps[s] >=0 )

    # for s in signature:
    #     m.addConstr(ms[s] >=0)


    # for s in signature:
    #     m.addConstr(ms[s] <= ns[s])

    for s in signature:
        m.addConstr(ys[s] <= sum(B.values()))

    for s in signature:
        m.addConstr(ys[s] >=0)

    # for s in signature:
    #     m.addConstr(ns[s]+ps[s]-ms[s] == ys[s] )

    for s in signature:
        m.addConstr(ns[s]+ps[s] == ys[s] )



    def findTallyAtr(signature,pi,r):
        pi = pi[r:]
        F = {}
        for i in pi:
            F[i] = set()
        for s in signature:
            u = [x for x in s if x  in pi]
            if len(u)>0:
                w = u[0]
                #print(u,w)
                F[w].add(tuple(s))
        return F




    for r in range(0,len(pi)-1):
        #Tally = findTallyAtr(signature,pi,r)
        Tally = findTallyAtr(signature, pi, r)
        l = pi[r]
        winners = pi[r+1:]

        #print("winners = ",winners)
        #print("losers = ",l)
        for w in winners:
            m.addConstr(gp.quicksum(ys[s] for s in  Tally[w]) - gp.quicksum(ys[s] for s in  Tally[l]) >=0)


    m.addConstr(sumPs == gp.quicksum(ps[s] for s in  signature))

    #m.addConstr(sumMs == gp.quicksum(ms[s] for s in  signature))

    #m.addConstr(sumPs - sumMs == 0)


    m.setObjective(sumPs,GRB.MINIMIZE)


    m.optimize()

    print("distance = ", m.objVal)

    end = timeit.default_timer()
    return math.ceil(m.objVal),end-start





from Utils import projectedBallots, findTally

B_start = {}

def findTallyOptimise(B,S):
    ts = timeit.default_timer()
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
    te = timeit.default_timer()
    return Tally,te - ts



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
            # if candidate == e:
            #     break
    return T

def getAllTallys(B,pi):
    lenpi = len(pi)
    allTallys = []

    tallydic = {}
    # for i in range(0,lenpi):
    #     tallydic[i] = 0

    for i in range(0, lenpi):
        allTallys.append(tallydic.copy())


    for s, count in B.items():
        sl = list(s)
        sl.reverse()
        w = sl[-1]

        for i in range(0,lenpi):
            pi_slice = pi[i:lenpi]
            if i != 0 and w != pi[i-1]:
                if w != -1:
                    if w  in allTallys[i]:
                        allTallys[i][w] = allTallys[i][w] + count
                    else:
                        allTallys[i][w] = count
            else:
                if i != 0:
                    sl.pop()
                    if len(sl) == 0:
                        break
                    w = sl[-1]
                while(w not in pi_slice):
                    sl.pop()
                    if len(sl) == 0:
                        w = -1
                        break
                    w = sl[-1]
                if w != -1:
                    if w in allTallys[i]:
                        allTallys[i][w] = allTallys[i][w] + count
                    else:
                        allTallys[i][w] = count

    return allTallys

def distanceToPiExact(B,pi):
    global B_start
    B_start = {}

    addTally = {}
    for c in pi:
        addTally[c] = 0
    pi_prime = pi
    r = 1
    tSingleRound = 0
    start = timeit.default_timer()
    allTally = getAllTallys(B, pi)
    end = timeit.default_timer()


    while len(pi_prime) > 1:
        if r == 1:
            prevElm = {}
        else:
            prevElm = pi[0:r-1]

        pi_prime = pi[r-1:]
        #B_prime = projectedBallots(B,pi_prime)
        #TotalAdd,AddTally = distanceSingleRound(B_prime,pi_prime,addTally)
        # if r==10:
        #     print("debug")
        tsSr = timeit.default_timer()

        thistall = allTally[r-1]
        TotalAdd, AddTally,t = distanceSingleRound(B, pi_prime, addTally,thistall)
        teSr = timeit.default_timer()
        tSingleRound = tSingleRound + t
        #print(r,TotalAdd)
        while TotalAdd > 0 and len(prevElm) > 0:
            e = prevElm.pop()
            if TotalAdd >= addTally[e]:
                TotalAdd = TotalAdd - addTally[e]
                addTally[e] = 0
            else:
                addTally[e] = addTally[e] - TotalAdd
                TotalAdd = 0
        r = r + 1
    res = sum(addTally.values())
    if res == TotalAdd:
        print("correct")
    return res , end-start,tSingleRound




def distanceSingleRound(B,pi,addTally,Tally):
    global B_start
    TotalAdd = 0
    #Tally = findTally(B,pi)
    c1 = pi[0]
    #Tally = projectedBallotsAndTally(B, pi, c1)
    #Tally,t = findTallyOptimise(B,pi)
    # if Tally != thistall:
    #     print("wrong")
    if c1 not in Tally:
        Tally[c1] = 0
    for c in pi[1:]:
        if c not in Tally:
            Tally[c] = 0
        if Tally[c1] + addTally[c1] > Tally[c] + addTally[c]:
            diff = Tally[c1] + addTally[c1] - Tally[c] - addTally[c]
            TotalAdd = TotalAdd + diff
            addTally[c] = addTally[c] + diff
    return TotalAdd,addTally,0