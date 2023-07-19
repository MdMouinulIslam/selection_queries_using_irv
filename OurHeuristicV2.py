
import heapq as heap
from  LRM import LRM
from DistanceToPi import distanceToPi
from BlomLB import blomLB,blomLBv1
from OurLB import OurLB,OurLBdp,OurLBdpV1
from OurUB import upperBound
import matplotlib.pyplot as plt
import networkx as nx
import  graphviz







class OurHeuristicV2:
    def __init__(self,inputName):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        #self.roundCount = {}
        self.fn = "graph\\heuristic_"+ inputName
        self.f = graphviz.Digraph(inputName, filename=self.fn)
        self.approxRatio = 1.0

    def marginOurs(self,C,B,cw):
        Q = []
        U = upperBound(B,C,cw)

        #print("upper bound = ",U)

        # for i in C:
        #     self.roundCount[i] = 0
        self.nodeExplored = self.nodeExplored + 1
        pi = [cw]
        l = blomLB(B,C,pi)
        heap.heappush(Q, [l,pi])
        #######################
        nodeVal = str(pi) + " , w=" + str(l)
        self.f.node(nodeVal)
        ######################
        self.lowerBoundMap[tuple(pi)] = 0

        while(len(Q) != 0 ):
            l,pi = heap.heappop(Q)
            if l < U:
                #self.roundCount[len(pi)-1] = self.roundCount[len(pi)-1] + 1
                #if self.roundCount[len(pi)-1] < 2:
                U = min(U,self.expandMOurs(l,pi,U,Q,C,B))

        self.f.render(self.fn, view=False)
        #self.f.save()
        return U

    def expandMOurs(self,l,pi,U,Q,C,B):
        C_pi = set(C) - set(pi)
        for c in C_pi:
            self.nodeExplored = self.nodeExplored + 1
            pi_prime = list(pi)
            pi_prime.insert(0,c)
            l_prime = OurLBdpV1(B,pi_prime,l)

            ##############################
            if len(pi_prime) == len(C):
                self.numLP = self.numLP + 1
                d = distanceToPi(B, pi_prime)

                # d = OurLBdpV1(B, pi, l)
                #######################
                nodeVal = str(pi) + " , w=" + str(l)
                nodeVal_prime = str(pi_prime) + " , w=" + str(d)
                self.f.node(nodeVal_prime)
                self.f.edge(nodeVal, nodeVal_prime)
                ######################
                if len(Q) != 0:
                    l, pi_pre = heap.heappop(Q)
                    self.approxRatio = float('inf')
                    if l != 0:
                        self.approxRatio = d / l
                    Q.clear()
                return d
            ###############################
            if l_prime < U:
                self.blomLBCall = self.blomLBCall + 1
                l_new_prime = blomLBv1(B, C, pi_prime)
                l_prime = max(l_new_prime,l_prime)
            if l_prime < U:
                heap.heappush(Q,[l_prime,pi_prime])
            #######################
            nodeVal = str(pi) + " , w=" + str(l)
            nodeVal_prime = str(pi_prime)+" , w="+str(l_prime)
            self.f.node(nodeVal_prime)
            self.f.edge(nodeVal,nodeVal_prime)
            ######################

        return U




class OurHeuristicV3:
    def __init__(self,inputName):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        #self.roundCount = {}
        fn = "graph\\heuristic_"+ inputName
        self.f = graphviz.Digraph(inputName, filename=fn)

    def marginOurs(self,C,B,cw):
        Q = []
        U = upperBound(B,C,cw)

        #print("upper bound = ",U)

        # for i in C:
        #     self.roundCount[i] = 0


        self.nodeExplored = self.nodeExplored + 1
        pi = [cw]
        l = blomLB(B,C,pi)
        heap.heappush(Q, [l,pi])
        #######################
        nodeVal = str(pi) + " w=" + str(l)
        self.f.node(nodeVal)
        ######################
        self.lowerBoundMap[tuple(pi)] = 0

        while(len(Q) != 0 ):
            l,pi = heap.heappop(Q)
            if l < U:
                #self.roundCount[len(pi)-1] = self.roundCount[len(pi)-1] + 1
                #if self.roundCount[len(pi)-1] < 2:
                U = min(U,self.expandMOurs(l,pi,U,Q,C,B))

        self.f.view()
        return U

    def expandMOurs(self,l,pi,U,Q,C,B):
        if len(pi) == len(C):
            self.numLP = self.numLP + 1
            d = distanceToPi(B, pi)
            return d
        else:
            C_pi = set(C) - set(pi)
            for c in C_pi:
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0,c)
                l_prime = OurLBdpV1(B,pi_prime,l)
                if l_prime < U:
                    self.blomLBCall = self.blomLBCall + 1
                    l_new_prime = blomLBv1(B, C, pi_prime)
                    l_prime = max(l_new_prime,l_prime)
                if l_prime < U:
                    heap.heappush(Q,[l_prime,pi_prime])
                    #######################
                    nodeVal = str(pi) + " w=" + str(l)
                    nodeVal_prime = str(pi_prime)+" w="+str(l_prime)
                    self.f.node(nodeVal_prime)
                    self.f.edge(nodeVal,nodeVal_prime)
                    ######################

        return U



class OurHeuristic:
    def __init__(self):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        self.U = 0

    def marginOurs(self,C,B,cw):
        Q = []
        self.U  = upperBound(B,C,cw)
        #print("upper bound = ",U)


        self.nodeExplored = self.nodeExplored + 1
        pi = [cw]
        l = blomLB(B,C,pi)
        heap.heappush(Q, [l,pi])
        self.lowerBoundMap[tuple(pi)] = 0

        while(len(Q) != 0 ):
            l,pi = heap.heappop(Q)
            if l < self.U:
                self.U = min(self.U,self.expandMOurs(l,pi,C,B))

        return self.U

    def expandMOurs(self,l,pi,C,B):
        if len(pi) == len(C):
            self.numLP = self.numLP + 1
            self.U = min(self.U, distanceToPi(B,pi))
            return self.U
            #return max(l,distanceToPi(B,pi))
        else:
            C_pi = set(C) - set(pi)
            newQ = []
            for c in C_pi:
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0,c)
                l_prime = OurLBdpV1(B,pi_prime,l)
                if l_prime < self.U:
                    self.blomLBCall = self.blomLBCall + 1
                    l_new_prime = blomLBv1(B, C, pi_prime)
                    l_prime = max(l_new_prime,l_prime)
                if l_prime < self.U:
                    #heap.heappush(Q,[l_prime,pi_prime])
                    heap.heappush(newQ, [l_prime, pi_prime])


            for i in range(0,1):
                if len(newQ) == 0:
                    return self.U
                l, pi = heap.heappop(newQ)
                self.U = min(self.U,self.expandMOurs(l,pi,C,B))


        return self.U




class OurMarginPrev:
    def __init__(self):
        self.nodeExplored = 0
        self.numLP = 0

    def marginOurs(self,C,B,cw):
        Q = []
        U = upperBound(B,C,cw)
        #print("upper bound = ",U)


        self.nodeExplored = self.nodeExplored + 1
        pi = [cw]
        l = blomLB(B,C,pi)
        heap.heappush(Q, [l,pi])

        while(len(Q) != 0 ):
            l,pi = heap.heappop(Q)
            if l < U:
                U = min(U,self.expandMOurs(l,pi,U,Q,C,B))

        return U

    def expandMOurs(self,l,pi,U,Q,C,B):
        if len(pi) == len(C):
            m = OurLB(B, pi)
            if m >= U:
                return U
            self.numLP = self.numLP + 1
            return distanceToPi(B,pi)
        else:
            C_pi = set(C) - set(pi)
            for c in C_pi:
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0,c)
                l_new = blomLB(B,C,pi_prime)
                l_prime = max(l,l_new)
                if l_prime < U:
                    m = OurLB(B,pi_prime)
                    l_prime = max(l_prime,m)
                if l_prime < U:
                    heap.heappush(Q,[l_prime,pi_prime])
        return U