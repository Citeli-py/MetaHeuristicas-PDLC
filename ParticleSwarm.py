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
        if i > j or i < 0 or j >= len(self.demanda):
            return float('inf')

        custo_total = self.custo_fixo
        producao = 0
        for k in range(i, j + 1):
            producao += self.demanda[k]
            if producao > self.capacidade:
                return float('inf')
            if k > i:
                custo_total += self.demanda[k] * self.custo_estoque * (k - i)
        return custo_total

    def custo_total_plano(self, plano: list[tuple[int, int]]) -> float:
        return sum(self.custo(i, j) for i, j in plano)

    def custo_medio(self, i: int, j: int) -> float:
        custo = self.custo(i, j)
        if custo == float('inf'):
            return float('inf')
        return custo / (j - i + 1)

class ConstrutorPlano:
    def __init__(self, problema: ProblemaLote):
        self.problema = problema

    def algoritmo_construtivo(self, plano_atual: list[tuple[int, int]]) -> list[tuple[int, int]]:
        inicio = plano_atual[-1][1] + 1 if plano_atual else 0
        fim = inicio
        if fim >= len(self.problema.demanda):
            return plano_atual
        
        melhor_custo = float('inf')
        melhor_passo = (inicio, fim)
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
        while not plano_atual or plano_atual[-1][1] < len(self.problema.demanda) - 1:
            plano_atual = self.algoritmo_construtivo(plano_atual)
        return plano_atual

class Particula:
    def __init__(self, problema: ProblemaLote, plano: list[tuple[int, int]]):
        self.problema = problema
        self.T = len(problema.demanda) - 1
        self.vetor = self.plano_p_vetor(plano)
        self.vel = [random.uniform(-1, 1) for _ in range(len(self.vetor))]
        
        # Limites para evitar overflow
        self.max_vel = 5.0
        self.min_pos = 0
        self.max_pos = self.T
        
        self.custo_melhor_local = self.calcular_custo()
        self.melhor_local = self.vetor.copy()

    def plano_p_vetor(self, plano: list[tuple[int, int]]) -> list[int]:
        vetor = []
        for periodo in plano[:-1]:
            vetor.append(periodo[1])
        return vetor
    
    def get_plano(self) -> list[tuple[int, int]]:
        i = 0
        plano = []
        for variavel in self.vetor:
            # Limita o valor entre 0 e T
            valor_limitado = max(self.min_pos, min(self.max_pos, variavel))
            j = int(round(valor_limitado))
            j = max(i, min(j, self.T))
            plano.append((i, j))
            i = j + 1

        if i <= self.T:
            plano.append((i, self.T))
        return plano

    def calcular_custo(self) -> float:
        plano = self.get_plano()
        if not plano or plano[-1][1] != self.T:
            return float('inf')
        return self.problema.custo_total_plano(plano)
    
    def atualizar(self, w: float, c1: float, c2: float, melhor_global_pos: list[float], melhor_global_custo: float):
        for i in range(len(self.vetor)):
            r1, r2 = random.random(), random.random()
            inercia = w * self.vel[i]
            cognitivo = c1 * r1 * (self.melhor_local[i] - self.vetor[i])
            social = c2 * r2 * (melhor_global_pos[i] - self.vetor[i])
            
            # Atualiza velocidade com limite
            self.vel[i] = max(-self.max_vel, min(self.max_vel, inercia + cognitivo + social))
            
            # Atualiza posição com limite
            self.vetor[i] = max(self.min_pos, min(self.max_pos, self.vetor[i] + self.vel[i]))
        
        custo_atual = self.calcular_custo()
        if custo_atual < self.custo_melhor_local:
            self.custo_melhor_local = custo_atual
            self.melhor_local = self.vetor.copy()
            
        return custo_atual



class OtimizadorPlano:
    def __init__(self, problema: ProblemaLote, num_particulas: int):
        self.problema = problema
        self.construtor = ConstrutorPlano(problema)
        self.num_particulas = num_particulas
        
        # Gera plano inicial guloso
        plano_guloso = self.construtor.construcao_gulosa()
        
        # Inicializa partículas
        self.particulas = []
        for _ in range(num_particulas):
            # Cria pequenas variações do plano guloso para diversidade
            plano_perturbado = self.perturbar_plano(plano_guloso.copy())
            self.particulas.append(Particula(problema, plano_perturbado))
        
        # Inicializa melhor global
        self.melhor_global_pos = None
        self.melhor_global_custo = float('inf')
        self.atualizar_melhor_global()

    def perturbar_plano(self, plano: list[tuple[int, int]]) -> list[tuple[int, int]]:
        if len(plano) <= 1:
            return plano
            
        index = random.randint(0, len(plano)-2)
        p1, p2 = plano[index], plano[index+1]

        minimo, maximo = p1[0], p2[1]-1
        i = random.randint(minimo, maximo)

        return plano[:index] + [(p1[0], i), (i + 1, p2[1])]  + plano[index+2:]

    def atualizar_melhor_global(self):
        for particula in self.particulas:
            custo = particula.custo_melhor_local
            if custo < self.melhor_global_custo:
                self.melhor_global_custo = custo
                self.melhor_global_pos = particula.melhor_local.copy()
                self.melhor_global = particula.get_plano()

    def PSO(self, temp_exec: int, w: float, c1: float, c2: float) -> tuple[list[tuple[int, int]], float]:

        print("Melhor Custo Global Semi-guloso:", self.melhor_global_custo)

        temp_final = time.time() + temp_exec
        while time.time() < temp_final:
            # Atualiza cada partícula
            for particula in self.particulas:
                particula.atualizar(w, c1, c2, self.melhor_global_pos, self.melhor_global_custo)
                print("Melhor Custo:", particula.custo_melhor_local, "       ", end='\r')
            
            # Atualiza melhor global
            self.atualizar_melhor_global()
            print("Melhor Custo:", self.melhor_global_custo, "       ", end='\r')
        


        return self.melhor_global, self.melhor_global_custo


# Exemplo de uso
if __name__ == "__main__":
    random.seed(42)
    demanda = [random.randint(1, 50) for _ in range(100)]
    
    problema = ProblemaLote(demanda, custo_fixo=200, custo_estoque=5, capacidade=500)
    otimizador = OtimizadorPlano(problema, num_particulas=100)

    t0 = time.time()
    melhor_plano, custo_total = otimizador.PSO(
        temp_exec=60,
        w=0.8,
        c1=1.7,
        c2=1.2
    )

    print("Melhor plano:", melhor_plano)
    print("Custo total:", custo_total)
    print("Tempo de execução:", round(time.time() - t0, 4), "segundos")