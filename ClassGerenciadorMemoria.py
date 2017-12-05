#encoding=utf-8

#Universidade de Brasília
#Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

# Declaração de constantes utilizadas na gerência de memória

# Tamanho total da memoria 
TAMANHO_TOTAL_MEMORIA = 1024

# Tamanho da partição voltada aos processos RT
TAMANHO_MEMORIA_PROCESSOS_RT = 64

# Tamanho da partição voltada aos processos de usuário
TAMANHO_MEMORIA_PROCESSOS_USUARIO = 960

# Classe que faz a gerência de memória do SO simulado
class ClassGerenciadorMemoria:

	# Construtor da classe
	def __init__(self):
		self.int_memoria_processos_usuario = TAMANHO_MEMORIA_PROCESSOS_USUARIO
		self.int_memoria_processos_rt = TAMANHO_MEMORIA_PROCESSOS_RT
		self.int_offset_memoria = 0

	# Verifica a disponibilidade de memória para um processo. É levado 
	# em conta o tipo de processo (RT ou usuário).
	# Argumentos: processo que solicita a memória
	def verificaDisponibilidadeMemoria(self, processo):
		if processo.getPrioridade() == 0:
			if processo.getBlocosMemoria() <= self.getMemoriaLivreProcessosRT():
				return True
			else:
				return False
		else:
			if processo.getBlocosMemoria() <= self.getMemoriaLivreProcessosUsuario():
				return True
			else:
				return False

	# Verifica se uma solicitação de memória de um processo é válida.
	# Processos podem requisitar um espaço de memória menor ou igual ao
	# máximo alocado para cada tipo.
	# Argumentos: processo que solicita a memória			
	def verificaRequisicaoMemoria(self, processo):
		if processo.getPrioridade() == 0:
			if processo.getBlocosMemoria() > TAMANHO_MEMORIA_PROCESSOS_RT:
				return False
			else:
				return True
		else:
			if processo.getBlocosMemoria() > TAMANHO_MEMORIA_PROCESSOS_USUARIO:
				return False
			else:
				return True


	# Atualiza o valor de offset atual da memória, somando o valor passado à contagem.
	# Argumentos: valor a ser incrementado
	def atualizaOffsetMemoria(self, valor):
		self.int_offset_memoria += valor

	# Retorna o valor de offset de memória atual
	def getOffsetMemoria (self):
		if self.int_offset_memoria > 0:
			return self.int_offset_memoria+1
		else:
			return self.int_offset_memoria

	# Retorna o valor de memória livre na partição de processos de usuário
	def getMemoriaLivreProcessosUsuario (self):
		return self.int_memoria_processos_usuario

	# Faz operações de adição e subtração na memória da partição de processos de usuário
	# Argumentos: valor a ser somado/subtraído, operacao desejada (ADICAO/SUBTRACAO)
	def atualizaMemoriaProcessosUsuario (self, valor, operacao):
			if operacao == 'ADICAO':
				self.int_memoria_processos_usuario += valor
			elif operacao == 'SUBTRACAO':
				self.int_memoria_processos_usuario -= valor

	# Retorna o valor de memória livre na partição de processos RT
	def getMemoriaLivreProcessosRT (self):
		return self.int_memoria_processos_rt

	# Faz operações de adição e subtração na memória da partição de processos RT
	# Argumentos: valor a ser somado/subtraído, operacao desejada (ADICAO/SUBTRACAO)
	def atualizaMemoriaProcessosRT (self, valor, operacao):
		if operacao == 'ADICAO':
			self.int_memoria_processos_rt += valor
		elif operacao == 'SUBTRACAO':
			self.int_memoria_processos_rt -= valor
