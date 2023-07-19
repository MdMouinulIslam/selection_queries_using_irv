
import gurobipy as gp
from gurobipy import GRB
from Utils import projectedBallots
from  Utils import createEquivalenceClasses
from Utils import finAllSignature



def distanceToPi(B,pi):

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
    ms = m.addVars(signature,vtype=GRB.INTEGER,name='ms')
    ys = m.addVars(signature,vtype=GRB.INTEGER,name='ys')
    sumPs = m.addVar(name="sumPs")
    sumMs = m.addVar(name="sumMs")


    for s in signature:
        m.addConstr(ps[s] >=0 )

    for s in signature:
        m.addConstr(ms[s] >=0)


    for s in signature:
        m.addConstr(ms[s] <= ns[s])

    for s in signature:
        m.addConstr(ys[s] <= sum(B.values()))

    for s in signature:
        m.addConstr(ys[s] >=0)

    for s in signature:
        m.addConstr(ns[s]+ps[s]-ms[s] == ys[s] )



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

    m.addConstr(sumMs == gp.quicksum(ms[s] for s in  signature))

    m.addConstr(sumPs - sumMs == 0)


    m.setObjective(sumPs,GRB.MINIMIZE)


    m.optimize()

    print("distance = ", m.objVal)

    return m.objVal