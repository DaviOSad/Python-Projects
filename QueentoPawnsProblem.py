# Autor: Davi Oliveira Sad
# Última Atualização: 22/06/2025
# Descrição: Este código resolve o problema de uma rainha no xadrez, onde a rainha deve visitar todos os peões no tabuleiro.
# Fila dupla para o BFS
from collections import deque
import time

#Função para tratamento de entrada
def ler_entrada():
    N,M,K = map(int, input().split())
    tabuleiro = []
    for _ in range(N):
        linha = input().strip()
        tabuleiro.append(linha)
    return N, M, K, tabuleiro

#BFS adaptado para criar um grafo que representa os menores números de movimentos para que a rainha chegue a cada ponto de interesse (peões e a própria rainha)
def bfs(tabuleiro, inicio, N, M):
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    fila = deque([inicio])
    visitados = [[False] * M for _ in range(N)]
    distancias = [[float('inf')] * M for _ in range(N)]
    visitados[inicio[0]][inicio[1]] = True
    distancias[inicio[0]][inicio[1]] = 0

    while fila:
        x, y = fila.popleft()
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            while 0 <= nx < N and 0 <= ny < M and tabuleiro[nx][ny] != '-':
                if not visitados[nx][ny]:
                    visitados[nx][ny] = True
                    distancias[nx][ny] = distancias[x][y] + 1
                    fila.append((nx, ny))
                nx += dx
                ny += dy
    
    return distancias

#Construção do grafo de distâncias entre a rainha e os peões
def construir_grafo(N, M, K, tabuleiro):
    vertices = []

    for i in range(N):
        for j in range(M):
            if tabuleiro[i][j] == 'R':
                vertices.insert(0, (i, j))  # A rainha é o primeiro vértice
            elif tabuleiro[i][j] == 'P':
                vertices.append((i, j))
    
    distancias = [[float('inf')] * (K+1) for _ in range(K+1)]

    for i in range (K+1):
        dmap = bfs(tabuleiro, vertices[i], N, M)
        for j in range(K+1):
            x, y = vertices[j]
            distancias[i][j] = dmap[x][y]
    
    return distancias, vertices

#Função com a solução exata, que usa DFS com cache.
def solucao_exata(grafo, K):
    # Cache para armazenar resultados já calculados
    cache = {}
    # Função DFS para encontrar o caminho mínimo visitando todos os peões
    def dfs(atual, visitados):
        if visitados ==  (1 << (K + 1)) - 1: 
            return 0
        if (atual, visitados) in cache:
            return cache[(atual, visitados)]
        
        min_mov = float('inf')
        for proximo in range(1, K + 1):
            if not (visitados & (1 << proximo)):
                mov = grafo[atual][proximo]
                if mov != float('inf'):
                    mov_total = mov + dfs(proximo, visitados | (1 << proximo))
                    min_mov = min(min_mov, mov_total)
        
        # Armazena o resultado no cache
        cache[(atual, visitados)] = min_mov
        # Retorna a distância mínima encontrada
        return min_mov
    
    resultado = dfs(0, 1 << 0)  # Começa na rainha (índice 0) com a rainha visitada
    return resultado if resultado != float('inf') else -1 #Retorna -1 se não for possível visitar todos os peões

#Função que implementa a heurística, usando algoritmo guloso
def heuristica(grafo, K):
    visitados = [False] * (K + 1)
    visitados[0] = True  
    total_movimentos = 0
    atual = 0 

    for _ in range(K):
        proximo = -1
        menor_mov = float('inf')
        
        for i in range(1, K + 1):
            if not visitados[i] and grafo[atual][i] < menor_mov:
                menor_mov = grafo[atual][i]
                proximo = i
        
        if menor_mov == float('inf'):  # Não há mais peões para visitar
            return -1
        
        total_movimentos += menor_mov
        visitados[proximo] = True
        atual = proximo
    
    return total_movimentos
   


#Leitura da entrada
N,M,K,tabuleiro = ler_entrada()

# Construção do grafo
grafo, vertices = construir_grafo(N, M, K, tabuleiro)

# Chamada da função para encontrar a solução exata
start = time.perf_counter()
resultado_exato = solucao_exata(grafo, K)
end = time.perf_counter()

# Chamada da função heurística
start_heuristica = time.perf_counter()
resultado_heuristica = heuristica(grafo, K)
end_heuristica = time.perf_counter()
# Impressão do tempo de execução
print(f"Tempo de execução da solução exata: {end - start:.6f} segundos")
print(f"Tempo de execução da heurística: {end_heuristica - start_heuristica:.6f} segundos")

# Impressão do resultado
print(resultado_exato)

# Impressão do resultado da heurística
print(resultado_heuristica)


