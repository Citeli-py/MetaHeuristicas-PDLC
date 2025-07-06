"""
Algoritmo Construtivo Guloso para o Problema de Dimensionamento de Lotes Capacitado (PDLC)
===========================================================================================
  
Descrição:
----------
Implementação de um algoritmo guloso construtivo para o PDLC, utilizando como métrica
de decisão o CUSTO MÉDIO por período. O algoritmo busca minimizar os custos totais
de produção (fixos + estoque) atendendo à demanda em cada período sem exceder a
capacidade máxima de produção.

Autor(es):
----------
- Bernardo Ramos
- Matheus Citeli

Métodos Implementados:
---------------------
- custo(): Calcula o custo total de um lote entre os períodos i e j.
- custo_medio(): Calcula o custo médio por período de um lote.
- algoritmo_construtivo(): Algoritmo guloso principal.
"""

def custo(i: int, j: int, custo_fixo: int, demanda: list[int], custo_estoque: int, capacidade: int) -> float:
    """Calcula o custo total e estoque máximo para um lote do período i ao j"""
    custo_total = custo_fixo  # Custo fixo
    producao = 0
    
    k=i+1
    while k <= j and k < len(demanda):
        producao += demanda[k]
        custo_total += demanda[k] * (custo_estoque**(k-i))  # Custo de estoque

        #print(f"[DEBUG] Período {k}: Produção acumulada = {producao}, Custo total = {custo_total}")

        # Se a produção necessária excede a capacidade, retorna infinito
        if producao > capacidade:
            return float('inf')
        
        k+=1
        
    return custo_total


def custo_medio(i, j, custo_fixo, demanda, custo_estoque, capacidade):
    """Calcula o custo médio por período para um lote do período i ao j"""
    custo_total = custo(i, j, custo_fixo, demanda, custo_estoque, capacidade)
    return custo_total / (j - i + 1)

def custo_plano(plano, custo_fixo, demanda, custo_estoque, capacidade) -> float:
    
    custo_total = 0

    for periodo in plano:
        i,j = periodo
        custo_total += custo(i,j, custo_fixo, demanda, custo_estoque, capacidade)

    return custo_total


def algoritmo_construtivo(plano_atual, demanda, custo_fixo, custo_estoque, capacidade) -> list[tuple]:
    """Implementa o algoritmo construtivo para encontrar o melhor plano de produção utilizando a métrica de custo médio"""
    
    inicio, fim = 0, 0
    if plano_atual != []:
        inicio = plano_atual[-1][1] + 1
        fim=inicio

    # Se o plano atual já cobre toda a demanda, retorna o plano
    if fim >= len(demanda):
        return plano_atual
    
    melhor_custo = float('inf')
    melhor_passo = (-1,-1)

    # Itera sobre os períodos de (inicio,i) até (inicio,j) para encontrar o melhor passo
    while fim < len(demanda):
        # Calcula o custo médio para o período atual
        custo_medio_atual = custo_medio(inicio, fim, custo_fixo, demanda, custo_estoque, capacidade)
        
        if custo_medio_atual < melhor_custo:
            melhor_custo = custo_medio_atual
            melhor_passo = (inicio, fim)

        #print(f"[DEBUG] Período {inicio} a {fim}: Custo médio = {custo_medio_atual}, Melhor custo = {melhor_custo}")
        fim+=1

    plano_atual.append(melhor_passo)
    return plano_atual

# Dados de exemplo
demanda = [22, 35, 18, 42, 27, 31, 25, 38, 29, 33, 
            19, 26, 37, 24, 41, 28, 32, 23, 36, 30,]
capacidade = 80
custo_fixo = 100  # por período
custo_estoque = 2  # por unidade por período

plano_atual = []
while plano_atual == [] or plano_atual[-1][1] < len(demanda)-1:
    plano_atual = algoritmo_construtivo(plano_atual, demanda, custo_fixo, custo_estoque, capacidade)
    #print("Plano atual:", plano_atual)

print("Plano final:", plano_atual)
print("Custo total", custo_plano(plano_atual, custo_fixo, demanda, custo_estoque, capacidade))