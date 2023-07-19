import heapq as heap
from  LRM import LRM
from DistanceToPi import distanceToPi
from BlomLB import blomLB,blomLBv1
from OurUB import upperBound
import graphviz

class BlomMargin:
    def __init__(self,inputName):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        self.U = -1
        self.branchExplored = 0
        self.fn = "graph\\Blom_" + inputName
        self.f = graphviz.Digraph(inputName, filename=self.fn)
        self.saveGraph = False

    def marginBlom(self, C, B, cw):
        Q = []
        self.U = 1000000000 #upperBound(B, C, cw)
        # print("upper bound = ",U)

        self.nodeExplored = self.nodeExplored + 1
        pi = []
        l = 0
        for cand in cw:
            pi = [cand]
            l = blomLB(B, C, pi)
            heap.heappush(Q, [l, pi])
        ################################################################
        if self.saveGraph:
            nodeVal = str(pi) + " , lb=" + str(l)
            self.f.node(nodeVal)
        #################################################################
        self.lowerBoundMap[tuple(pi)] = 0

        while (len(Q) != 0):
            l, pi = heap.heappop(Q)
            if l < self.U:
                self.U = min(self.U, self.expandBlom(l, pi, Q, C, B))
        #####################################################################
        if self.saveGraph:
            self.f.render(self.fn, view=False)
            self.f.save()
        #####################################################################
        return self.U


    def expandBlom(self,l,pi,Q,C,B):

        if len(pi) == len(C):
            self.numLP = self.numLP + 1
            return l  # max(l,distanceToPi(B,pi))
        else:
            C_pi = set(C) - set(pi)
            ipcalled = False
            for c in C_pi:
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0, c)
                if len(pi_prime) == len(C):
                    self.numLP = self.numLP + 1
                    self.branchExplored = self.branchExplored + 1
                    l_prime = distanceToPi(B, pi_prime)
                    if l_prime < self.U:
                        self.U = l_prime
                else:
                    l_new = blomLBv1(B, C, pi_prime)
                    l_prime = max(l, l_new)
                    if l_prime < self.U:
                        self.numLP = self.numLP + 1
                        m = distanceToPi(B, pi_prime)
                        ipcalled = True
                        l_prime = max(l_prime, m)
                if l_prime < self.U:
                    heap.heappush(Q, [l_prime, pi_prime])

                ######################
                if self.saveGraph:
                    nodeVal = str(pi) + " , lb=" + str(l)
                    nodeVal_prime = str(pi_prime) + " , lb=" + str(l_prime)
                    self.f.node(nodeVal_prime)
                    if self.U > 100000:
                        edgeLabel = 'UB=' + "Inf"
                    else:
                        edgeLabel = 'UB=' + str(self.U)
                    edgeLabel = edgeLabel + "_"+str(ipcalled)
                    self.f.edge(nodeVal, nodeVal_prime, label=edgeLabel)
                #####################
        return self.U

