import kstsp
import heuristic
from sys import argv
from math import sqrt

pi = (1 + sqrt(5))/2

if __name__ == "__main__":
    capitals, dist = kstsp.read_coords(int(argv[1]))
    print(heuristic.heuristic(capitals=capitals, dist=dist, k=int(argv[2])))
    #gurobi_sol = kstsp.gurobi(capitals=capitals, dist=dist, lagrange=None)
