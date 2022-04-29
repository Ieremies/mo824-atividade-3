import kstsp
import heuristic
from sys import argv
from math import sqrt

# pi = (1 + sqrt(5))/2
pi = 2

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
    return [ {e: x_i[e].getAttr("x") - d[e].getAttr("x") for e in d.keys()} for x_i in x ]

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
        for e in t.values():
            sum_subgradients += e**2
    return pi * ((upper - lower) / sum_subgradients)


if __name__ == "__main__":
    capitals, dist = kstsp.read_coords(int(argv[1]))
    lagrange = [ {e: 0 for e in dist[t].keys()} for t in range(2) ]

    upper = heuristic.heuristic(capitals=capitals, dist=dist, k=int(argv[2]))
    gurobi_model = kstsp.gurobi(capitals, dist, lagrange, upper)

    for i in range(50):
        print(f"Interação {i}, upper {upper}, lower {gurobi_model.objVal}.")
        subg = subgradient(gurobi_model._vars, gurobi_model._dup)
        alpha = passo(pi, upper, gurobi_model.objVal, subg)
        # print(alpha)
        lagrange = [ {e : max(lagrange[t][e] + alpha * subg[t][e], 0.0) for e in subg[t].keys()} for t in range(2) ]
        gurobi_model = kstsp.gurobi(capitals, dist, lagrange, upper)

        pi = pi * 0.9
