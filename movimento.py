from random import randint

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

def deslocamento(p1: tuple[int, int], p2: tuple[int, int]) -> list[list[tuple[int, int]]]:
    
    deslocamentos =[]
    # (1,a)(a+1,5) 1<=a<5
    for i in range(p1[0], p2[1]):
        #print(f"({p1[0]}, {i}), ({i+1}, {p2[1]})")
        deslocamentos.append([(p1[0], i), (i+1, p2[1])])
    
    return deslocamentos

def vizinhos(plano: list[tuple[int, int]], iteracoes=10) -> list[list[tuple[int, int]]]:
    
    if len(plano) < 2:
        return plano
    
    ns = []

    for i in range(iteracoes):
        index = randint(1, len(plano)-1)
        ds = deslocamento(plano[index-1], plano[index])
        for d in ds:
            n = plano[:index-1] + d + plano[index+1:]
            ns.append(n)
            print(n)
            
    return ns



def buscalocal(plano: list[tuple[int, int]]) -> list[tuple[int, int]]:
    pass

deslocamento((1,1), (2,5))
vizinhos( [(0, 2), (3, 4), (5, 6)])