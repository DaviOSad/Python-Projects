# Autor: Davi Oliveira Sad
# Última Alteração: 26/05/2025

# Fila dupla para o BFS
from collections import deque

#Tratamento de entrada
linhas, colunas = map(int, input().split())
matriz = [list(map(int, input().split())) for _ in range(linhas)]
posCapital = list(map(int, input().split()))
posCapital[0] -= 1  # Ajusta para índice 0
posCapital[1] -= 1  # Ajusta para índice 0

# Função que gera o grafo a partir da matriz
def geraGrafo(matriz):
    grafo = {}
    INF = 10**10

    # Direções: cima, baixo, esquerda, direita
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(linhas):
        for j in range(colunas):
            valor = matriz[i][j]

            AijIn = (i, j, 'in')
            AijOut = (i, j, 'out')

            # 1. Aresta interna com peso da célula
            grafo.setdefault(AijIn, []).append((AijOut, valor))

            # 2. Arestas para vizinhos com peso infinito
            for di, dj in direcoes:
                ni, nj = i + di, j + dj
                if 0 <= ni < linhas and 0 <= nj < colunas:
                    vizinho_in = (ni, nj, 'in')
                    grafo.setdefault(AijOut, []).append((vizinho_in, INF))

    grafo["source"] = []
    for i in range(linhas):
        for j in range(colunas):
            # Verifica se está na borda
            na_borda = (i == 0 or j == 0 or i == linhas - 1 or j == colunas - 1)
            if na_borda:
                grafo['source'].append(((i, j, 'in'), INF))

    grafo["sink"] = []
    grafo.setdefault((posCapital[0], posCapital[1], 'out'), []).append(("sink", INF))

    return grafo

# Cria o grafo a partir da matriz
grafo = geraGrafo(matriz)

#Implementação do BFS adaptada para o algoritmo de Ford-Fulkerson
def bfs(residual_grafo, source, sink, v_pai):
    visitados = set()
    fila = deque([source])
    visitados.add(source)

    while fila:
        u = fila.popleft()
        for v, capacidade in residual_grafo.get(u, []):
            if v not in visitados and capacidade > 0:
                visitados.add(v)
                v_pai[v] = u
                if v == sink:
                    return True
                fila.append(v)
    return False

# Implementação do algoritmo de Ford-Fulkerson
def fordFulkerson(grafo, source, sink):
    INF = 10**10
    # Inicializa grafo residual
    residual_grafo = {}
    for u in grafo:
        for v, capacidade in grafo[u]:
            residual_grafo.setdefault(u, []).append([v, capacidade])
            residual_grafo.setdefault(v, [])

    v_pai = {}
    fluxo_maximo = 0

    while bfs(residual_grafo, source, sink, v_pai):
        # Encontra o fluxo mínimo ao longo do caminho encontrado pelo BFS
        caminho_fluxo = INF
        s = sink
        while s != source:
            p = v_pai[s]
            # Acha a capacidade da aresta p->s
            for i, (v, capacidade) in enumerate(residual_grafo[p]):
                if v == s:
                    caminho_fluxo = min(caminho_fluxo, capacidade)
                    break
            s = p

        # Atualiza as capacidade residuais
        v = sink
        while v != source:
            u = v_pai[v]
            # Diminui a capacidade na aresta u->v
            for i, (vertice, capacidade) in enumerate(residual_grafo[u]):
                if vertice == v:
                    residual_grafo[u][i][1] -= caminho_fluxo
                    break
            # Aumenta capacidade na aresta v->u (aresta reversa)
            reversa_encontrada = False
            for i, (vertice, capacidade) in enumerate(residual_grafo[v]):
                if vertice == u:
                    residual_grafo[v][i][1] += caminho_fluxo
                    reversa_encontrada = True
                    break
            if not reversa_encontrada:
                residual_grafo[v].append([u, caminho_fluxo])
            v = u

        fluxo_maximo += caminho_fluxo
        v_pai = {}

    return fluxo_maximo

# Executa o algoritmo de Ford-Fulkerson
fluxo_maximo = fordFulkerson(grafo, "source", "sink")

# Exibe o resultado
print(fluxo_maximo) 











