import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distancia = 0
        for indice, peca in enumerate(state.tiles):
            if peca == 0:
                continue
            alvo = peca - 1
            distancia += abs(indice // 3 - alvo // 3) + abs(indice % 3 - alvo % 3)
        return distancia

    def search(self, initial: State) -> SearchResult:
        contador = 0
        fronteira = [(self.heuristic(initial), contador, initial)]
        melhor_g = {initial.tiles: 0}
        expandidos_set = set()

        expandidos = 0
        gerados = 1
        max_fronteira = 1

        while fronteira:
            _, _, atual = heapq.heappop(fronteira)

            if atual.tiles in expandidos_set:
                continue

            if atual.is_goal:
                return SearchResult(atual, expandidos, gerados, max_fronteira, atual.cost)

            expandidos_set.add(atual.tiles)
            expandidos += 1

            for filho in atual.neighbors():
                if filho.tiles in expandidos_set:
                    continue
                if filho.cost >= melhor_g.get(filho.tiles, float("inf")):
                    continue
                melhor_g[filho.tiles] = filho.cost
                contador += 1
                f = filho.cost + self.heuristic(filho)
                heapq.heappush(fronteira, (f, contador, filho))
                gerados += 1

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(None, expandidos, gerados, max_fronteira, 0)
