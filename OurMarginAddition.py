
import heapq as heap
from  LRMAddition import LRM
from OurUBAddition import upperBoundAddition
from DistanceToPiAddition import distanceToPiAddition,distanceToPiExact
from BlomLBAddition import blomLBv1Addition
from OurLBAddition import OurLB
import timeit
import  graphviz
import random as rnd

class OurMargin:
    def __init__(self,inputName):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        self.branchExplored = 0
        self.timeDistAdd = 0
        self.timeLBCal = 0
        self.timeDistAddSingle = 0
        self.saveGraph = True
        ##################################################################
        # self.fn = "graph\\OurExact_" + inputName
        # self.f = graphviz.Digraph(inputName, filename=self.fn)
        ##################################################################

    def marginOurs(self,C,B,cw):
        Q = []
        U = upperBoundAddition(B,C,cw)
        #print("upper bound = ",U)
        self.nodeExplored = self.nodeExplored + 1
        pi = []
        l = 0
        for cand in cw:
            pi = [cand]
            l,t = blomLBv1Addition(B, C, pi)
            self.timeLBCal = self.timeLBCal + t
            heap.heappush(Q, [l, pi])

            #################################################################
            # if self.saveGraph:
            #     nodeVal = str(pi) + " , lb=" + str(l)
            #     self.f.node(nodeVal)
            ##################################################################
            self.lowerBoundMap[tuple(pi)] = 0

        while (len(Q) != 0):
            l, pi = heap.heappop(Q)
            if l < U:
                U = min(U, self.expandMOurs(l, pi, U, Q, C, B))
        ######################################################################
        # if self.saveGraph:
        #     self.f.render(self.fn, view=False)
        #     self.f.save()
        ######################################################################
        return U

    def expandMOurs(self,l,pi,U,Q,C,B):
        if len(pi) == len(C):
            #self.numLP = self.numLP + 1
            U = min(U, l)
            return U
        else:
            C_pi = set(C) - set(pi)
            for c in C_pi:
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0, c)
                if len(pi_prime) == len(C):
                    #self.numLP = self.numLP + 1
                    self.branchExplored = self.branchExplored + 1

                    l_prime,t,ts = distanceToPiExact(B, pi_prime)
                    U = min(U,l_prime)
                    self.timeDistAdd = self.timeDistAdd + t
                    self.timeDistAddSingle = self.timeDistAddSingle + ts
                else:
                    l_new,t = blomLBv1Addition(B, C, pi_prime)
                    self.blomLBCall = self.blomLBCall + t
                    l_prime = max(l, l_new)
                    if l_prime < U:
                        #self.numLP = self.numLP + 1

                        m,t,ts = distanceToPiExact(B, pi_prime)
                        self.timeDistAdd = self.timeDistAdd + t
                        self.timeDistAddSingle = self.timeDistAddSingle + ts
                        l_prime = max(l_prime, m)

                #######################
                # if self.saveGraph:
                #     nodeVal = str(pi) + " , lb=" + str(l)
                #     nodeVal_prime = str(pi_prime) + " , lb=" + str(l_prime)
                #     self.f.node(nodeVal_prime)
                #     edgeLabel = 'UB='+str(U)
                #     self.f.edge(nodeVal, nodeVal_prime,label=edgeLabel)
                ######################
                if l_prime < U:
                    heap.heappush(Q, [l_prime, pi_prime])

        return U



################################################################## expand all #################################
class OurMarginExpandAll:
    def __init__(self,inputName):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        self.branchExplored = 0
        self.timeDistAdd = 0
        self.timeLBCal = 0
        self.timeDistAddSingle = 0
        self.fn = "graph\\OurExact_" + inputName + "_expandall"
        self.f = graphviz.Digraph(inputName, filename=self.fn)

    def marginOurs(self,C,B,cw):
        Q = []
        U = upperBoundAddition(B,C,cw)
        #print("upper bound = ",U)
        self.nodeExplored = self.nodeExplored + 1
        pi = []
        l = 0
        for cand in cw:
            pi = [cand]
            l,t = blomLBv1Addition(B, C, pi)
            self.timeLBCal = self.timeLBCal + t
            heap.heappush(Q, [l, pi])

            #######################
            nodeVal = str(pi) + " , lb=" + str(l)
            self.f.node(nodeVal)
            ######################
            self.lowerBoundMap[tuple(pi)] = 0

        while (len(Q) != 0):
            l, pi = heap.heappop(Q)
            #if l < U:
            U = min(U, self.expandMOurs(l, pi, U, Q, C, B))
        self.f.render(self.fn, view=False)
        self.f.save()
        return U

    def expandMOurs(self,l,pi,U,Q,C,B):
        if len(pi) == len(C):
            #self.numLP = self.numLP + 1
            U = min(U, l)
            return U
        else:
            C_pi = set(C) - set(pi)
            for c in C_pi:
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0, c)
                if len(pi_prime) == len(C):
                    #self.numLP = self.numLP + 1
                    self.branchExplored = self.branchExplored + 1
                    l_prime,t,ts = distanceToPiExact(B, pi_prime)
                    U = min(U,l_prime)
                    #l_prime1, t1 = distanceToPiAddition(B, pi_prime)
                    #if l_prime != l_prime1:
                    #    print("not equal")
                    self.timeDistAdd = self.timeDistAdd + t
                    self.timeDistAddSingle = self.timeDistAddSingle + ts
                else:
                    l_new,t = blomLBv1Addition(B, C, pi_prime)
                    self.blomLBCall = self.blomLBCall + t
                    l_prime = max(l, l_new)
                    if l_prime < U:
                        #self.numLP = self.numLP + 1
                        m,t,ts = distanceToPiExact(B, pi_prime)
                        #m1,t1 = distanceToPiAddition(B,pi_prime)
                        #if m1 != m:
                        #    print("not equal")
                        self.timeDistAdd = self.timeDistAdd + t
                        self.timeDistAddSingle = self.timeDistAddSingle + ts
                        l_prime = max(l_prime, m)

                #######################
                nodeVal = str(pi) + " , lb=" + str(l)
                nodeVal_prime = str(pi_prime) + " , lb=" + str(l_prime)
                self.f.node(nodeVal_prime)
                edgeLabel = 'UB='+str(U)
                self.f.edge(nodeVal, nodeVal_prime,label=edgeLabel)
                ######################
                #if l_prime < U:
                heap.heappush(Q, [l_prime, pi_prime])

        return U




class OurMarginV2:
    def __init__(self,inputName):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        self.branchExplored = 0
        self.timeDistAdd = 0
        self.timeLBCal = 0
        self.fn = "graph\\OurExact_" + inputName +"v2"
        self.f = graphviz.Digraph(inputName, filename=self.fn)

    def marginOurs(self,C,B,cw):
        Q = []
        U = upperBoundAddition(B,C,cw)
        #print("upper bound = ",U)
        self.nodeExplored = self.nodeExplored + 1
        pi = []
        l = 0
        for cand in cw:
            pi = [cand]
            l,t = blomLBv1Addition(B, C, pi)
            self.timeLBCal = self.timeLBCal + t
            heap.heappush(Q, [l, pi])

            #######################
            nodeVal = str(pi) + " , lb=" + str(l)
            self.f.node(nodeVal)
            ######################
            self.lowerBoundMap[tuple(pi)] = 0

        while (len(Q) != 0):
            l, pi = heap.heappop(Q)
            if l < U:
                U = min(U, self.expandMOurs(l, pi, U, Q, C, B))
        self.f.render(self.fn, view=False)
        self.f.save()
        return U

    def expandMOurs(self,l,pi,U,Q,C,B):
        if len(pi) == len(C):
            #self.numLP = self.numLP + 1
            U = min(U, l)
            return U
        else:
            C_pi = set(C) - set(pi)
            for c in C_pi:
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0, c)
                if len(pi_prime) == len(C):
                    #self.numLP = self.numLP + 1
                    self.branchExplored = self.branchExplored + 1
                    l_prime,t = distanceToPiExact(B, pi_prime)
                    U = min(U,l_prime)
                    #l_prime1, t1 = distanceToPiAddition(B, pi_prime)
                    #if l_prime != l_prime1:
                    #    print("not equal")
                    self.timeDistAdd = self.timeDistAdd + t
                else:
                    l_new,t = blomLBv1Addition(B, C, pi_prime)
                    self.blomLBCall = self.blomLBCall + t
                    l_prime = max(l, l_new)
                    if l_prime < U:
                        #self.numLP = self.numLP + 1
                        m,t = distanceToPiExact(B, pi_prime)
                        #m1,t1 = distanceToPiAddition(B,pi_prime)
                        #if m1 != m:
                        #    print("not equal")
                        self.timeDistAdd = self.timeDistAdd + t
                        l_prime = max(l_prime, m)

                #######################
                nodeVal = str(pi) + " , lb=" + str(l)
                nodeVal_prime = str(pi_prime) + " , lb=" + str(l_prime)
                self.f.node(nodeVal_prime)
                edgeLabel = 'UB='+str(U)
                self.f.edge(nodeVal, nodeVal_prime,label=edgeLabel)
                ######################
                if l_prime < U:
                    heap.heappush(Q, [l_prime, pi_prime])

        return U

