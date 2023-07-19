import heapq as heap
from  LRM import LRM
from DistanceToPiAddition import distanceToPiAddition
from BlomLBAddition import blomLBv1Addition
from OurUBAddition import upperBoundAddition
import timeit


class BlomMargin:
    def __init__(self):
        self.nodeExplored = 0
        self.numLP = 0
        self.branchExplored = 0
        self.start = timeit.default_timer()
        self.TIMELIMIT = 60*30
        self.timeDistAdd = 0
        self.timeLBCal = 0

    def marginBlom(self,C,B,cw):


        Q = []
        #U = 9999999999999
        U = upperBoundAddition(B, C, cw)
        self.nodeExplored = self.nodeExplored + 1
        for cand in cw:
            pi = [cand]
            l ,t= blomLBv1Addition(B, C, pi)
            self.timeLBCal = self.timeLBCal + t
            heap.heappush(Q, [l, pi])

        while(len(Q) != 0 ):
            nowTime = timeit.default_timer()
            if nowTime-self.start > self.TIMELIMIT:
                print("time limit excedded")
                break
            l,pi = heap.heappop(Q)
            if l < U:
                U = min(U,self.expandBlom(l,pi,U,Q,C,B))

        return U


    def expandBlom(self,l,pi,U,Q,C,B):

        if len(pi) == len(C):
            U = min(U, l)
            return U
        else:
            C_pi = set(C) - set(pi)
            for c in C_pi:
                self.nodeExplored = self.nodeExplored + 1
                pi_prime = list(pi)
                pi_prime.insert(0,c)
                if len(pi_prime) == len(C):
                    self.numLP = self.numLP + 1
                    self.branchExplored = self.branchExplored + 1
                    l_prime,t = distanceToPiAddition(B, pi_prime)
                    self.timeDistAdd = self.timeDistAdd + t
                    U = min(U, l_prime)
                else:
                    l_new,t = blomLBv1Addition(B,C,pi_prime)
                    self.timeLBCal = self.timeLBCal + t
                    l_prime = max(l,l_new)
                    if l_prime < U:
                        self.numLP = self.numLP + 1
                        m,t =  distanceToPiAddition(B,pi_prime)
                        self.timeDistAdd = self.timeDistAdd + t
                        l_prime = max(l_prime,m)
                if l_prime < U:
                    heap.heappush(Q,[l_prime,pi_prime])
        return U

