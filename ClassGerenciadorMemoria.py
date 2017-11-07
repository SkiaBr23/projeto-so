#encoding=utf-8

import operator

TAMANHO_TOTAL_MEMORIA = 1024
TAMANHO_MEMORIA_PROCESSOS_RT = 64
TAMANHO_MEMORIA_PROCESSOS_USUARIO = 960
SUBTRACAO = operator.isub
ADICAO = operator.iadd

class ClassGerenciadorMemoria:

	def __init__(self):
		self.int_memoria_processos_usuario = TAMANHO_MEMORIA_PROCESSOS_USUARIO
		self.int_memoria_processos_rt = TAMANHO_MEMORIA_PROCESSOS_RT
		self.int_offset_memoria = 0

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

	def verificaRequisicaoMemoria(self, processo):
		if processo.getPrioridade() == 0:
			if processo.getBlocosMemoria() > 64:
				return False
			else:
				return True
		else:
			if processo.getBlocosMemoria() > 960:
				return False
			else:
				return True

	def atualizaOffsetMemoria(self, valor):
		self.int_offset_memoria += valor

	def getOffsetMemoria (self):
		if self.int_offset_memoria > 0:
			return self.int_offset_memoria+1
		else:
			return self.int_offset_memoria

	def getMemoriaLivreProcessosUsuario (self):
		return self.int_memoria_processos_usuario

	def atualizaMemoriaProcessosUsuario (self, valor, operacao):
			if operacao == 'ADICAO':
				self.int_memoria_processos_usuario += valor
			elif operacao == 'SUBTRACAO':
				self.int_memoria_processos_usuario -= valor

	def getMemoriaLivreProcessosRT (self):
		return self.int_memoria_processos_rt

	def atualizaMemoriaProcessosRT (self, valor, operacao):
		if operacao == 'ADICAO':
			self.int_memoria_processos_rt += valor
		elif operacao == 'SUBTRACAO':
			self.int_memoria_processos_rt -= valor
