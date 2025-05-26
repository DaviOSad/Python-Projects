# Autor: Davi Oliveira Sad
# Última Alteração: 17/04/2025


# Funções auxiliares


def input_valido():
    while True:
        linha = input()
        if linha.strip():  # se não está vazia ou só espaços
            return linha

# Função para adicionar aresta
def adicionar_aresta(GrafoAbrigos, u, v):
    GrafoAbrigos[u].append(v)
    GrafoAbrigos[v].append(u)

# Função para criar o grafo
def criar_grafo(numAbrigos):
    GrafoAbrigos = {}
    for i in range(1, numAbrigos + 1):
        GrafoAbrigos[i] = []
    return GrafoAbrigos

# Função para calcular a distância entre dois pontos
def calcular_distancia(ponto1, ponto2):
    return ((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2) ** 0.5

# BFS
def BFS(GrafoAbrigos, inicio, destino):
    fila = [inicio]
    visitados = {inicio}
    pais = {inicio: None}

    while fila:
        vertice = fila.pop(0)

        if vertice == destino:
            caminho = []
            while vertice is not None:
                caminho.append(vertice)
                vertice = pais[vertice]
            return caminho[::-1]

        for vizinho in GrafoAbrigos[vertice]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                pais[vizinho] = vertice
                fila.append(vizinho)

    return None


#Função para definir maior caminho a partir de um abrigo
def maior_caminho(GrafoAbrigos, inicio):
    visitados = set()
    fila = [(inicio, 0)]
    maior_distancia = 0

    while fila:
        vertice, distancia = fila.pop(0)
        visitados.add(vertice)

        for vizinho in GrafoAbrigos[vertice]:
            if vizinho not in visitados:
                fila.append((vizinho, distancia + 1))
                maior_distancia = max(maior_distancia, distancia + 1)

    return maior_distancia


# Leitura e tratamento dos parâmetros


# Coordenadas Ana
cordA = list(map(int, input_valido().split()))

# Coordenadas Bernardo
cordB = list(map(int, input_valido().split()))

# Tratamento dos abrigos
numAbrigos = int(input_valido())

VetorAbrigos = []

for i in range(numAbrigos):
    abrigos = input().split()
    abrigos = list(map(int, abrigos))
    indice = i + 1
    VetorAbrigos.append((indice, abrigos[0], abrigos[1], abrigos[2]))

# Criar o grafo
GrafoAbrigos = criar_grafo(numAbrigos)

# Adicionar arestas ao grafo
for i in range(numAbrigos):
    for j in range(i + 1, numAbrigos):
        distancia = calcular_distancia((VetorAbrigos[i][2], VetorAbrigos[i][3]), (VetorAbrigos[j][2], VetorAbrigos[j][3]))
        if distancia <= VetorAbrigos[i][1] + VetorAbrigos[j][1]:
            adicionar_aresta(GrafoAbrigos, VetorAbrigos[i][0], VetorAbrigos[j][0])

# Definir em que abrigo estão Ana e Bernardo
for i in range (numAbrigos):
    if calcular_distancia((cordA[0], cordA[1]), (VetorAbrigos[i][2], VetorAbrigos[i][3])) <= VetorAbrigos[i][1]:
        abrigoAna = VetorAbrigos[i][0]
    if calcular_distancia((cordB[0], cordB[1]), (VetorAbrigos[i][2], VetorAbrigos[i][3])) <= VetorAbrigos[i][1]:
        abrigoBernardo = VetorAbrigos[i][0]


# Parte 1


# Encontrar o caminho mais curto entre os abrigos de Ana e Bernardo
caminho = BFS(GrafoAbrigos, abrigoAna, abrigoBernardo)

# Imprime o resultado da parte 1
if caminho is not None:
    print("Parte 1:", len(caminho) - 1)
else:
    print("Parte 1: -1")


# Parte 2


# BFS para encontrar o vértice mais distante 
def bfs_mais_distante(GrafoAbrigos, inicio):
    visitados = set([inicio])
    fila = [(inicio, 0)]
    mais_distante = (inicio, 0)

    while fila:
        vertice, distancia = fila.pop(0)
        if distancia > mais_distante[1]:
            mais_distante = (vertice, distancia)

        for vizinho in GrafoAbrigos[vertice]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, distancia + 1))

    return mais_distante

# Encontra o maior caminho dentro do grafo
def encontrar_maior_caminho(GrafoAbrigos):
    visitados_geral = set()
    maior_distancia = 0

    for vertice in GrafoAbrigos:
        if vertice not in visitados_geral:
            # Primeira BFS
            u, _ = bfs_mais_distante(GrafoAbrigos, vertice)
            # Segunda BFS para encontrar o real mais distante
            v, distancia = bfs_mais_distante(GrafoAbrigos, u)
            maior_distancia = max(maior_distancia, distancia)

            # Marca todos os vértices dessa componente como visitados
            fila = [vertice]
            visitados_geral.add(vertice)
            while fila:
                atual = fila.pop()
                for vizinho in GrafoAbrigos[atual]:
                    if vizinho not in visitados_geral:
                        visitados_geral.add(vizinho)
                        fila.append(vizinho)

    return maior_distancia

#Imprime o resultado da parte 2
maiorCaminho = encontrar_maior_caminho(GrafoAbrigos)
print("Parte 2:", maiorCaminho)


# Parte 3


# Encontra pontos críticos (articulação) no grafo
def pontos_criticos(GrafoAbrigos):
    tempo = [0]
    visitado = {v: False for v in GrafoAbrigos}
    descoberta = {}
    low = {}
    pai = {v: None for v in GrafoAbrigos}
    pontosCriticos = set()

    # Função DFS adaptada para encontrar pontos críticos
    def DFS(u):
        visitado[u] = True
        descoberta[u] = low[u] = tempo[0]
        tempo[0] += 1
        filhos = 0

        for v in GrafoAbrigos[u]:
            if not visitado[v]:
                pai[v] = u
                filhos += 1
                DFS(v)

                low[u] = min(low[u], low[v])

                if pai[u] is None and filhos > 1:
                    pontosCriticos.add(u)
                if pai[u] is not None and low[v] >= descoberta[u]:
                    pontosCriticos.add(u)
            elif v != pai[u]:
                low[u] = min(low[u], descoberta[v])

    # Iniciar DFS em cada vértice não visitado, para caso o grafo não seja conexo
    for u in GrafoAbrigos:
        if not visitado[u]:
            DFS(u)

    return pontosCriticos

# Imprime o resultado da parte 3
pontos_criticos = pontos_criticos(GrafoAbrigos)

if pontos_criticos:
    print("Parte 3:", len(pontos_criticos), " ".join(map(str, sorted(pontos_criticos))))
else:
    print("Parte 3: 0")





   




    

