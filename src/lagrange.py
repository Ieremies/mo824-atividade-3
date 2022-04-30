import time
from math import sqrt
from sys import argv

import heuristic
import kstsp

pi = (1 + sqrt(5))/2

def subgradient(x, d):
    """Função responsável por calcular o subgradiente.

    Parameters
    ----------
    x : list[dict]
        x[i][e] indica o uso da aresta no tuor i.
    d : dict
        d[e] força a duplicidade da aresta e em ambos os ciclos.

    Return
    ------
    list[dict]
        Para cada tuor i, um dicionário contendo o subgradiente para cada aresta.
    """
    return [ {e: d[e].getAttr("x") - x_i[e].getAttr("x") for e in d} for x_i in x ]

def passo(pi, upper, lower, subg):
    """Calcula o tamanho escalar do passo alpha.

    Segue a fórmula \pi \frac{upper - lower}{\sum subgrad^2}.

    Parameters
    ----------
    pi : float
        0 < pi <= 2. Utilizando a dica do professor da razão áurea.
    upper : int
        Limite superior encontrado por uma heurística.
    lower : int
        Melhor solução encontrada até então.
    subgradient : list[dict]
        Vetor de gradientes para cada tuor.

    Returns
    -------
    float
        Passo a ser usado para a próxima interação de lambda.
    """

    sum_subgradients = 0
    for t in subg:
        sum_subgradients += sum([e**2 for e in t.values()])
    return pi * ((upper - lower) / sum_subgradients)


if __name__ == "__main__":
    capitals, dist = kstsp.read_coords(int(argv[1]))
    lagrange = [ {e: 0 for e in dist[t]} for t in range(2) ]

    upper = heuristic.heuristic(capitals, dist, int(argv[2]))
    print(f"Upper bound heuristic:{upper}")
    gurobi_model = kstsp.gurobi(capitals, dist, lagrange, upper)

    start = time.time()
    elapsed = 0

    i = 0
    while elapsed < 30*60:
        print(f"Interação {i}, time {elapsed}, lower {gurobi_model.objVal}")

        i += 1

        subg = subgradient(gurobi_model._vars, gurobi_model._dup)
        alpha = passo(pi, upper, gurobi_model.objVal, subg)

        lagrange = [ {e : max(lagrange[t][e] + alpha * subg[t][e], 0.0) for e in subg[t]} for t in range(2) ]
        gurobi_model = kstsp.gurobi(capitals, dist, lagrange, upper)

        elapsed = time.time() - start
