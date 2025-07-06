def custo(s, demanda, h, i, j):
    """Calcula o custo total e estoque máximo para um lote do período i ao j"""
    custo_total = s  # Custo fixo
    producao = sum(demanda[i-1:j])  # Produção necessária para cobrir i até j
    estoque_max = 0
    estoque_atual = producao
    
    for k in range(i, j+1):
        if k > len(demanda):
            break
        estoque_atual -= demanda[k-1]  # Consome a demanda do período
        custo_total += estoque_atual * h  # Custo de estoque
        estoque_max = max(estoque_max, estoque_atual)
    
    return custo_total, estoque_max

def custo_medio(s, demanda, h, i, j):
    """Calcula o custo médio por período para um lote do período i ao j"""
    custo_total, estoque = custo(s, demanda, h, i, j)
    return custo_total / (j - i + 1), estoque

def calcular_custo_total(plano, demanda, custo_fixo, custo_estoque, capacidade):
    """Calcula o custo total de um plano de produção"""
    custo_total = 0
    for inicio, fim in plano:
        custo_lote, estoque = custo(custo_fixo, demanda, custo_estoque, inicio, fim)
        if estoque > capacidade:
            return float('inf')  # Plano inviável
        custo_total += custo_lote
    return custo_total

def backtracking(demanda, capacidade, custo_fixo, custo_estoque):
    menor_custo = float('inf')
    melhor_combinacao = None
    n_periodos = len(demanda)

    def recursao(inicio, combinacao_atual):
        nonlocal menor_custo, melhor_combinacao
        
        if inicio > n_periodos:
            custo_total = calcular_custo_total(combinacao_atual, demanda, custo_fixo, custo_estoque, capacidade)
            if custo_total < menor_custo:
                menor_custo = custo_total
                melhor_combinacao = combinacao_atual.copy()
            return
        
        for fim in range(inicio, n_periodos + 1):
            combinacao_atual.append((inicio, fim))
            recursao(fim + 1, combinacao_atual)
            combinacao_atual.pop()

    recursao(1, [])
    return melhor_combinacao, menor_custo

def silver_meal(demanda, capacidade, custo_fixo, custo_estoque):
    n_periodos = len(demanda)
    plano = []
    i = 1
    
    while i <= n_periodos:
        melhor_custo_medio = float('inf')
        melhor_j = i
        
        for j in range(i, n_periodos + 1):
            custo_medio_atual, estoque = custo_medio(custo_fixo, demanda, custo_estoque, i, j)
            
            if estoque > capacidade:
                break
                
            if custo_medio_atual < melhor_custo_medio:
                melhor_custo_medio = custo_medio_atual
                melhor_j = j
            else:
                break
        
        plano.append((i, melhor_j))
        i = melhor_j + 1
    
    custo_total = calcular_custo_total(plano, demanda, custo_fixo, custo_estoque, capacidade)
    return plano, custo_total


# Dados de exemplo
demanda = [22, 35, 18, 42, 27, 31, 25, 38, 29, 33, 
            19, 26, 37, 24, 41, 28, 32, 23, 36, 30, 18, 42, 27, 31,]

capacidade = 80
custo_fixo = 100  # por período
custo_estoque = 2  # por unidade por período

import time

t0 = time.time()
solucao, custo_total = silver_meal(demanda, capacidade, custo_fixo, custo_estoque)
print(f"Silver Meal ({round(time.time()-t0, 6)}):", solucao, custo_total)

# Execução do Backtracking
t0 = time.time()
solucao, custo_total = backtracking(demanda, capacidade, custo_fixo, custo_estoque)
print(f"Backtracking ({round(time.time()-t0, 6)}):", solucao, custo_total)