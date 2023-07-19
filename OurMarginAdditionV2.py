
import heapq as heap
from  LRMAddition import LRM
from OurUBAddition import upperBoundAdditionV2
from DistanceToPiAddition import distanceToPiAddition,distanceToPiExact
from BlomLBAddition import blomLBv1Addition
from OurLBAddition import OurLB
import timeit

class OurMarginV2:
    def __init__(self,identifier,exploredMap):
        self.nodeExplored = 0
        self.numLP = 0
        self.blomLBCall = 0
        self.lowerBoundMap = {}
        self.branchExplored = 0
        self.timeDistAdd = 0
        self.timeLBCal = 0
        self.identifier = identifier
        self.exploredMap = exploredMap

    def marginOurs(self,C,B,cw):
        Q = []
        U, winner = upperBoundAdditionV2(B,C,cw)
        #print("upper bound = ",U)
        self.nodeExplored = self.nodeExplored + 1
        pi = []
        l = 0
        for cand in cw:
            pi = [cand]
            if tuple(pi) in self.exploredMap:
                l = self.exploredMap[tuple(pi)]
                heap.heappush(Q, [l, pi])
            else:
                l,t = blomLBv1Addition(B, C, pi)
                self.timeLBCal = self.timeLBCal + t
                heap.heappush(Q, [l, pi])
                self.exploredMap[tuple(pi)] = l

            #######################
            nodeVal = str(pi) + " , w=" + str(l)
            # self.f.node(nodeVal)
            ######################
            self.lowerBoundMap[tuple(pi)] = 0

        while (len(Q) != 0):
            l, pi = heap.heappop(Q)
            if l < U:
                m,w = self.expandMOurs(l, pi, U, Q, C, B)
                if m < U:
                    U = m
                    winner = w

        # self.f.render(self.fn, view=False)
        # self.f.save()
        return U,winner

    def expandMOurs(self,l,pi,U,Q,C,B):
        if len(pi) == len(C):
            #self.numLP = self.numLP + 1
            self.exploredMap[tuple(pi)] = l
            return l,pi[-1]
        else:
            C_pi = set(C) - set(pi)
            for c in C_pi:
                pi_prime = list(pi)
                pi_prime.insert(0, c)

                if tuple(pi_prime) in self.exploredMap:
                    l_prime = self.exploredMap[tuple(pi_prime)]
                    if l_prime < U:
                        heap.heappush(Q, [l_prime, pi_prime])
                else:
                    self.nodeExplored = self.nodeExplored + 1
                    if len(pi_prime) == len(C):
                        #self.numLP = self.numLP + 1
                        self.branchExplored = self.branchExplored + 1
                        l_prime,t = distanceToPiExact(B, pi_prime)
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
                    if l_prime < U:
                        heap.heappush(Q, [l_prime, pi_prime])

                    self.exploredMap[tuple(pi_prime)] = l_prime
        return U,-1
