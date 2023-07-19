import heapq as heap
from  LRM import LRM
from DistanceToPi import distanceToPi

def marginMagrino(C,B,cw):
    Q = []
    U = LRM(B,C)
    C_w = set(C)-{cw}
    for c in C_w:
        pi = [c]
        l = 0
        heap.heappush(Q, [l,pi])

    while(len(Q) != 0 ):
        l,pi = heap.heappop(Q)
        if l < U:
            U = expandMagrino(l,pi,U,Q,C,B)

    return U

def expandMagrino(l,pi,U,Q,C,B):
    if len(pi) == len(C):
        return distanceToPi(B,pi)
    else:
        C_pi = set(C) - set(pi)
        for c in C_pi:
            pi_prime = list(pi)
            pi_prime.insert(0,c)
            l_prime =  distanceToPi(B,pi_prime)
            if l_prime < U:
                heap.heappush(Q,[l_prime,pi_prime])
    return U