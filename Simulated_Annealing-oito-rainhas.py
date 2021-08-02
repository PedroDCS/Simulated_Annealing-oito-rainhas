# Codigo baseado no seguinte repositorios
#https://github.com/tolgahanakgun/School-Projects/blob/master/Computatinal%20Intelligence/8Queens_Simulated_Annealing/eightqueens.py

# Bibliotca usada para gerar copias
import copy

# Bibliotca usada para gerar numeros aleatórios
import random

# Bibliotca usada para operações matemáticas
import math

# Para contar o tempo de execução
from timeit import default_timer as timer

# Quantidade de rainhas
qtdRainhas = 3

# Classe usada para gerar o tabuleiro
class board:
    # Gera um tabuleiro de dimensão relativa a quantidade de rainhas
    def __init__(self, list=None):
        if list == None:
            self.board = [random.randint(0, qtdRainhas-1) for i in range(0, qtdRainhas)]

    # Função usada para preencher o tabuleiro
    def __str__(self):
        # Gera N linhas e N colunas
        b = [[0 for i in range(0, qtdRainhas)] for j in range(0, qtdRainhas)]

        # Insere N rainhas ao longo da diagonal
        for i in range(0, qtdRainhas):
            b[self.board[i]][i] = 'X'

        
        mstr = ""
        for i in range(0, qtdRainhas):
            for j in range(0, qtdRainhas):
                mstr = mstr + str(b[i][j]) + " "
            mstr += '\n'
        return (mstr)  # Retorna o tabuleiro

# Classe principal
class rainhas():
    def __init__(self):

        # Armazena a quantidade de vezes que uma rainha foi movimentada
        self.num_total_passos = 0

        # Parametros do Simulated Annealing        
        self.temp_atual_sistema = int(40) # Temperatura inicial
        self.temp_parada = 0 # Critério de parada
        self.fator_resfriamento = float(0.005) # Fator de resfriamento


    # Função objetiva
    def calc_custo(self, tabuleiro):
        # Calcula o numero total de rainhas que estão se atacando
        custo = 0
        for i in range(0, qtdRainhas):
            for j in range(i+1, qtdRainhas):
                # Verifica vertical
                if tabuleiro.board[i] == tabuleiro.board[j]:
                    custo += 1
                # Verifica nas outras direções
                offset = j - i
                if tabuleiro.board[i] == tabuleiro.board[j] - offset or tabuleiro.board[i] == tabuleiro.board[j] + offset:
                    custo += 1
        return custo

    # Metaheuristica
    def simulated_anneling(self):
        # Cria o tabuleiro
        self.tabuleito_t = board()

        # Solução inicial
        self.custo_atual_sistema = self.calc_custo(self.tabuleito_t)

        # Executa enquanto a temperatura for maior que 0 ou ele conseguir distribuir todas as rainhas sem nenhuma se atacar
        while self.temp_atual_sistema > self.temp_parada and self.custo_atual_sistema != 0:

            # Executa N vezes em cada temperatura
            for i in range(int(100)):
                
                # Calcula o novo custo apos gerar uma nova sulucao
                novo_custo = self.gera_nova_solucao()

                # Verifica a diferença entre as soluções
                custo_delta = novo_custo - self.custo_atual_sistema

                # Verifica se deve ou nao aceitar a nova solução
                if self.funcao_probabilidade(self.temp_atual_sistema, custo_delta):
                    
                    self.tabuleito_t = copy.deepcopy(self.possivel_tabuleiro)
                    self.custo_atual_sistema = novo_custo
                    self.num_total_passos += 1
                    if novo_custo == 0:  # Se nenhuma rainha se ataca, sai do loop
                        print(self.tabuleito_t)
                        print("Temperatura: ", self.temp_atual_sistema)
                        return

            # Realiza o resfriamento
            self.temp_atual_sistema = self.temp_atual_sistema - self.fator_resfriamento

        # Se nao encontrou, arredonda a temperatura para 0
        self.temp_atual_sistema = self.temp_parada

    # Diferença entre a solução
    def funcao_probabilidade(self, temperature, delta):
        if delta < 0:  # Se for melhor aceita
            return True

        # Calcula a probabilidade de aceitar a solução ruim
        c = math.exp(-delta/temperature)
        r = random.random()

        if r < c:
            return True

        return False

    def gera_nova_solucao(self):
        # Pega uma rainha aleatoria e a coloca em uma posicao aleatoria

        # Variavel que verifica para nao colocar duas rainhas no mesmo lugar
        repeticoes = True
        while repeticoes == True:
            # Escolhe a rainha
            rainha_aleatoria = random.randint(0, qtdRainhas-1)
            # Coloca a rainha
            posicao_aleatoria = random.randint(0, qtdRainhas-1)

            # Verifica se colocou no mesmo lugar
            if self.tabuleito_t.board[rainha_aleatoria] == posicao_aleatoria:
                repeticoes = True
            else:
                repeticoes = False
            
            if repeticoes == False:
                self.possivel_tabuleiro = copy.deepcopy(self.tabuleito_t)
                self.possivel_tabuleiro.board[rainha_aleatoria] = posicao_aleatoria

        # Retorna o valor da nova solucao
        return self.calc_custo(self.possivel_tabuleiro)


if __name__ == "__main__":

    # Gera o tabuleiro
    tabuleito_t = rainhas()

    # Tempo de inicio
    start = timer()

    # Inicia o algoritmo
    tabuleito_t.simulated_anneling()

    # Tempo de fim
    end = timer()

    print("Simulated Anneling:")
    print("Tempo de execução: {0:5f}".format(end-start))
    print("Número total de movimentos: ", tabuleito_t.num_total_passos)