import gurobipy as gp
from gurobipy import GRB
from itertools import combinations
import math
from sys import argv

# Read
def read_coords(qtd):
    coordinates = [ [], [] ]
    capitals = []
    with open("coord", "r", encoding="utf-8") as f:
        for i in range(qtd):
            linha = f.readline().split()
            capitals.append(i)
            coordinates[0].append((int(linha[0]), int(linha[1])))
            coordinates[1].append((int(linha[2]), int(linha[3])))

    def distance(city1, city2, tuor):
        c1 = coordinates[tuor][city1]
        c2 = coordinates[tuor][city2]
        diff = (c1[0]-c2[0], c1[1]-c2[1])
        return math.ceil(math.sqrt(diff[0]*diff[0]+diff[1]*diff[1]))

    dist = []
    dist.append({(c1,c2): distance(c1,c2,0) for c1, c2 in combinations(capitals,2)})
    dist.append({(c1,c2): distance(c1,c2,1) for c1, c2 in combinations(capitals,2)})

    return (capitals,dist)

def gurobi(capitals, dist, lagrange, upper_bound):
    m = gp.Model()
    m.modelSense = GRB.MINIMIZE
    m.setParam('OutputFlag', False) # turns off solver chatter

    # Variables: is city 'i' adjacent to city 'j' on the tour?
    vars = [m.addVars(dist[i].keys(), vtype=GRB.BINARY, name=f'x_{i}') for i in range(2)]
    dup = m.addVars(dist[0].keys(), vtype=GRB.BINARY, name="D")

    m.update()

    # Set the objective function
    obj = gp.LinExpr()
    for i in range(2):
        for k in dist[i].keys():
            obj.add(vars[i][k]*dist[i][k])
            obj.add(lagrange[i][k]*(vars[i][k] - dup[k]))
    m.setObjective(obj, GRB.MINIMIZE)

    # Symmetric direction: Copy the object
    for k in range(2):
        for i, j in vars[k].keys():
            vars[k][j, i] = vars[k][i, j]  # edge in opposite direction

    # Constraints: two edges incident to each city
    m.addConstrs(vars[i].sum(c, '*') == 2 for c in capitals for i in range(2))

    # Edge duplication restrains
    # m.addConstrs(vars[i][k] >= dup[k] for k in dist[0].keys() for i in range(2))
    m.addConstr(dup.sum("*") >= int(argv[2]))

    # Callback - use lazy constraints to eliminate sub-tours
    def subtourelim(model, where):
        if where == GRB.Callback.MIPSOL:
            for t in range(2):
                # make a list of edges selected in the solution
                vals = model.cbGetSolution(model._vars[t])
                selected = gp.tuplelist((i, j) for i, j in model._vars[t].keys() if vals[i, j] > 0.5)
                # find the shortest cycle in the selected edge list
                tour = subtour(selected)
                if len(tour) < len(capitals):
                    # add subtour elimination constr. for every pair of cities in subtour
                    model.cbLazy(gp.quicksum(model._vars[t][i, j] for i, j in combinations(tour, 2)) <= len(tour)-1)

    # Given a tuplelist of edges, find the shortest subtour
    def subtour(edges):
        unvisited = capitals[:]
        cycle = capitals[:] # Dummy - guaranteed to be replaced
        while unvisited:  # true if list is non-empty
            thiscycle = []
            neighbors = unvisited
            while neighbors:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, '*') if j in unvisited]
            if len(thiscycle) <= len(cycle):
                cycle = thiscycle # New shortest subtour
        return cycle


    m._vars = vars
    m._dup = dup
    m.Params.lazyConstraints = 1
    m.optimize(subtourelim)

    return m

