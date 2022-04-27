from math import inf

def fechar_tuor(capitals: list[int], dist: dict, atual: int):
    not_visited = capitals[:]
    total_dist = 0

    # While there is a capital to be visited
    while not_visited:
        # Find the closest capital
        closest_capital = not_visited[0]
        closest_capital_dist = inf

        for c in not_visited:
            distancia_atual_c = dist[atual, c] if (atual, c) in dist.keys() else dist[c, atual]
            if (distancia_atual_c < closest_capital_dist):
                closest_capital = c
                closest_capital_dist = distancia_atual_c

        not_visited.remove(closest_capital)
        atual = closest_capital
        total_dist += closest_capital_dist

    total_dist += dist[atual, 0] if (atual, 0) in dist.keys() else dist[0, atual]
    return total_dist

def heuristic(capitals: list[int], dist: list[dict], k: int):

    not_visited = capitals[:]
    atual = 0
    not_visited.remove(0)
    total_dist = 0

    # While there is a capital to be visited
    while len(not_visited) > len(capitals) - k:
        # Find the closest capital
        closest_capital = not_visited[0]
        closest_capital_dist = inf

        for c in not_visited:
            distancia_atual_c = dist[0][atual, c] if (atual, c) in dist[0].keys() else dist[0][c, atual]
            distancia_atual_c += dist[1][atual, c] if (atual, c) in dist[1].keys() else dist[1][c, atual]
            if (distancia_atual_c < closest_capital_dist):
                closest_capital = c
                closest_capital_dist = distancia_atual_c

        not_visited.remove(closest_capital)
        atual = closest_capital
        total_dist += closest_capital_dist

    total_dist += fechar_tuor(not_visited, dist[0], atual)
    total_dist += fechar_tuor(not_visited, dist[1], atual)
    return total_dist
