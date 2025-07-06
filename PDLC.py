
class PDLC:
    
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