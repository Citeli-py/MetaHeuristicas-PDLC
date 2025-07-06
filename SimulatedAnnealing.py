"""
Busca Local com Simulated Annealing para o Problema de Dimensionamento de Lotes Capacitado (PDLC)
===================================================================================================

Descrição:
----------
Implementação de uma heurística de busca local baseada no método de *Simulated Annealing* para o
Problema de Dimensionamento de Lotes Capacitado (PDLC). O algoritmo parte de uma solução inicial
gerada por um algoritmo guloso construtivo e realiza perturbações na solução buscando escapar de
mínimos locais, com o objetivo de encontrar planos de produção com menor custo total (custos fixos
de produção + custos de estocagem), respeitando a capacidade máxima de produção.

Autor(es):
----------
- Bernardo Ramos
- Matheus Citeli
"""



import math
import random
import time

class ProblemaLote:
    def __init__(self, demanda: list[int], custo_fixo: int, custo_estoque: int, capacidade: int):
        self.demanda = demanda
        self.custo_fixo = custo_fixo
        self.custo_estoque = custo_estoque
        self.capacidade = capacidade

    def custo(self, i: int, j: int) -> float:
        custo_total = self.custo_fixo
        producao = 0
        for k in range(i + 1, j + 1):
            if k >= len(self.demanda):
                break
            producao += self.demanda[k]
            custo_total += self.demanda[k] * (self.custo_estoque ** (k - i))
            if producao > self.capacidade:
                return float('inf')
        return custo_total

    def custo_total_plano(self, plano: list[tuple[int, int]]) -> float:
        return sum(self.custo(i, j) for i, j in plano)

    def custo_medio(self, i: int, j: int) -> float:
        return self.custo(i, j) / (j - i + 1)

class ConstrutorPlano:
    def __init__(self, problema: ProblemaLote):
        self.problema = problema

    def algoritmo_construtivo(self, plano_atual: list[tuple[int, int]]) -> list[tuple[int, int]]:
        inicio = plano_atual[-1][1] + 1 if plano_atual else 0
        fim = inicio
        if fim >= len(self.problema.demanda):
            return plano_atual
        
        melhor_custo = float('inf')
        melhor_passo = (-1, -1)
        while fim < len(self.problema.demanda):
            custo_medio_atual = self.problema.custo_medio(inicio, fim)
            if custo_medio_atual < melhor_custo:
                melhor_custo = custo_medio_atual
                melhor_passo = (inicio, fim)
            fim += 1

        plano_atual.append(melhor_passo)
        return plano_atual

    def construcao_gulosa(self) -> list[tuple[int, int]]:
        plano_atual = []
        while plano_atual == [] or plano_atual[-1][1] < len(self.problema.demanda) - 1:
            plano_atual = self.algoritmo_construtivo(plano_atual)
        return plano_atual

class OtimizadorPlano:
    def __init__(self, problema: ProblemaLote):
        self.problema = problema

    def deslocamento(self, plano: list[tuple[int, int]]) -> list[tuple[int, int]]:

        index = random.randint(0, len(plano)-2)
        p1, p2 = plano[index], plano[index+1]

        minimo, maximo = p1[0], p2[1]-1
        i = random.randint(minimo, maximo)

        return plano[:index] + [(p1[0], i), (i + 1, p2[1])]  + plano[index+2:]
    

    def simulated_annealing(self, T_inicial=10000, T_min=1e-6, alpha=0.99, iter_por_temp=500, temp_exec=60):
        construtor = ConstrutorPlano(self.problema)
        plano_atual = construtor.construcao_gulosa()
        print("Solução gulosa:", plano_atual)

        melhor_plano = plano_atual[:]
        custo_atual = self.problema.custo_total_plano(plano_atual)
        print("Custo:", custo_atual)

        melhor_custo = custo_atual
        T = T_inicial

        num_iter = 0

        #while T > T_min:
        temp_final = time.time() + temp_exec
        while (time.time() < temp_final) and T > T_min:
            for _ in range(iter_por_temp):

                num_iter += 1
                
                plano_vizinho = self.deslocamento(plano_atual)
                custo_vizinho = self.problema.custo_total_plano(plano_vizinho)

                delta = custo_vizinho - custo_atual
                if delta < 0 or random.random() < math.exp(-delta / T):
                    plano_atual = plano_vizinho
                    custo_atual = custo_vizinho
                
                if custo_atual < melhor_custo:
                    melhor_plano = plano_atual
                    melhor_custo = custo_atual
                
                print("Melhor Custo:", custo_atual, "       ", "Temperatura:", T, end='\r')

            T *= alpha

        print("Temperatura Final:", T)
        print("Numero de iterações:", num_iter)
        return melhor_plano, melhor_custo

# Exemplo de uso
if __name__ == "__main__":
    random.seed(42)
    demanda = [ random.randint(1, 50) for _ in range(100) ]

    
    problema = ProblemaLote(demanda, custo_fixo=200, custo_estoque=5, capacidade=500)
    otimizador = OtimizadorPlano(problema)

    t0 = time.time()
    melhor_plano, custo_total = otimizador.simulated_annealing(
        T_inicial=10000,
        T_min=1e-6, 
        alpha=0.999, 
        iter_por_temp=100, 
        temp_exec=60
    )

    print("Melhor plano:", melhor_plano)
    print("Custo total:", custo_total)
    print("Tempo de execução:", round(time.time() - t0, 6))
