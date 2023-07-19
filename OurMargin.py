
import heapq as heap
from  LRM import LRM
from DistanceToPi import distanceToPi
from BlomLB import blomLB,blomLBv1
from OurLB import OurLB,OurLBdp,OurLBdpV1,OurLBdpV2,OurLBdp
from OurUB import upperBound
import  graphviz

FAST_IP_LEN = 0
class OurMargin:
    def __init__(self,inputName):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        self.U =  -1
        self.branchExplored = 0
        self.fn = "graph\\OurExact_" + inputName
        self.f = graphviz.Digraph(inputName, filename=self.fn)
        self.saveGraph = False

    def marginOurs(self,C,B,cw):
        Q = []
        self.U = upperBound(B,C,cw)
        #print("upper bound = ",U)


        self.nodeExplored = self.nodeExplored + 1
        pi = []
        l = 0
        for cand in cw:
            pi = [cand]
            l = blomLB(B,C,pi)
            heap.heappush(Q, [l,pi])
        ################################################################
        if self.saveGraph:
            nodeVal = str(pi) + " , lb=" + str(l)
            self.f.node(nodeVal)
        #################################################################
        self.lowerBoundMap[tuple(pi)] = 0

        while(len(Q) != 0 ):
            l,pi = heap.heappop(Q)
            if l < self.U:
                self.U = min(self.U,self.expandMOurs(l,pi,Q,C,B))
            #self.U = min(self.U, self.expandMOurs(l, pi, Q, C, B))
        #####################################################################
        if self.saveGraph:
            self.f.render(self.fn, view=False)
            self.f.save()
        #####################################################################
        return self.U

    def expandMOurs(self,l,pi,Q,C,B):
        if len(pi) == len(C):
            self.numLP = self.numLP + 1
            self.U = l #distanceToPi(B,pi)
            return self.U #max(l,distanceToPi(B,pi))
        else:
            C_pi = set(C) - set(pi)
            for c in C_pi:
                ipcalled = False
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0,c)
                #l_prime = OurLBdpV1(B,pi,l)
                #l_prime = OurLBdp(B,pi,l)
                #l_prime = OurLBdpV2(B,pi,l)
                # if l_prime !=l_primetest:
                #     print("not equal")
                l_prime = OurLBdpV2(B, pi_prime, l)
                if len(pi_prime) == len(C) and l_prime < self.U:
                    self.numLP = self.numLP + 1
                    self.branchExplored = self.branchExplored + 1
                    l_prime = distanceToPi(B, pi_prime)
                    ipcalled = True
                    if l_prime < self.U :
                        self.U = l_prime

                else:
                    #l_prime = OurLBdpV2(B, pi_prime, l)
                    if l_prime < self.U:
                        self.blomLBCall = self.blomLBCall + 1
                        l_new_prime = blomLBv1(B, C, pi_prime)
                        l_prime = max(l_new_prime,l_prime)
                    if l_prime < self.U and len(pi_prime) < FAST_IP_LEN:
                        self.numLP = self.numLP + 1
                        m = distanceToPi(B, pi_prime)
                        l_prime = max(l_prime, m)
                if l_prime < self.U:
                    heap.heappush(Q,[l_prime,pi_prime])

                #heap.heappush(Q, [l_prime, pi_prime])

                ######################
                if self.saveGraph:
                    nodeVal = str(pi) + " , lb=" + str(l)
                    nodeVal_prime = str(pi_prime) + " , lb=" + str(l_prime)
                    self.f.node(nodeVal_prime)
                    edgeLabel = 'UB='+str(self.U)
                    edgeLabel = edgeLabel + "_" + str(ipcalled)
                    self.f.edge(nodeVal, nodeVal_prime,label=edgeLabel)
                #####################
        return self.U




# class OurMarginPrev:
#     def __init__(self):
#         self.nodeExplored = 0
#         self.numLP = 0
#
#     def marginOurs(self,C,B,cw):
#         Q = []
#         U = upperBound(B,C,cw)
#         #print("upper bound = ",U)
#
#
#         self.nodeExplored = self.nodeExplored + 1
#         pi = [cw]
#         l = blomLB(B,C,pi)
#         heap.heappush(Q, [l,pi])
#
#         while(len(Q) != 0 ):
#             l,pi = heap.heappop(Q)
#             if l < U:
#                 U = min(U,self.expandMOurs(l,pi,U,Q,C,B))
#
#         return U
#
#     def expandMOurs(self,l,pi,U,Q,C,B):
#         if len(pi) == len(C):
#             m = OurLB(B, pi)
#             if m >= U:
#                 return U
#             self.numLP = self.numLP + 1
#             return distanceToPi(B,pi)
#         else:
#             C_pi = set(C) - set(pi)
#             for c in C_pi:
#                 self.nodeExplored = self.nodeExplored + 1
#                 pi_prime = list(pi)
#                 pi_prime.insert(0,c)
#                 l_new = blomLB(B,C,pi_prime)
#                 l_prime = max(l,l_new)
#                 if l_prime < U:
#                     m = OurLB(B,pi_prime)
#                     l_prime = max(l_prime,m)
#                 if l_prime < U:
#                     heap.heappush(Q,[l_prime,pi_prime])
#         return U