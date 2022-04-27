import kstsp
import heuristic
from sys import argv


if __name__ == "__main__":
    capitals, dist = kstsp.read_coords(int(argv[1]))
    print(heuristic.heuristic(capitals=capitals, dist=dist, k=int(argv[2])))
    #kstsp.gurobi(capitals=capitals, dist=dist, lagrange=None)
