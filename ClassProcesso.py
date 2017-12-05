#encoding=utf-8

#Universidade de Brasília
#Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

#Classe que modelo um Processo no PseudoSO
class ClassProcesso:


	#Construtor da classe
	def __init__(self, int_TempIniciacao, int_prioridade,
					int_tempDeProcessador, int_blocosDeMem,
					int_numReqImpressora,int_numReqScanner,
					int_numReqModem, int_numReqDisco, int_sizeLista):

		self.int_PID = int_sizeLista
		self.int_TempIniciacao = int_TempIniciacao
		self.int_prioridade = int_prioridade
		self.int_tempDeProcessador = int_tempDeProcessador
		self.int_blocosDeMem = int_blocosDeMem
		self.int_numReqImpressora = int_numReqImpressora
		self.int_numReqScanner = int_numReqScanner
		self.int_numReqModem = int_numReqModem
		self.int_numReqDisco = int_numReqDisco
		self.int_aposTempInicializacao = 0
		self.int_tokenCPU = False
		self.int_esperaRecurso = False


	#Método de get e set de atributos
	def getEsperaRecurso(self):
		return self.int_esperaRecurso

	def setEsperaRecurso(self, valor):
		self.int_esperaRecurso = valor

	def activateTokenCPU(self):
		self.int_tokenCPU = True

	def deactivateTokenCPU(self):
		self.int_tokenCPU = False

	def getTokenCPU(self):
		return self.int_tokenCPU

	def getAposTempInicializacao(self):
		return self.int_aposTempInicializacao

	def getTempoProcessador(self):
		return self.int_tempDeProcessador

	def getTempoInicializacao(self):
		return self.int_TempIniciacao

	def setAposTempInicializacao(self):
		self.int_aposTempInicializacao = 1

	def getRequisicaoScanner (self):
		return self.int_numReqScanner

	def getRequisicaoModem (self):
		return self.int_numReqModem

	def getRequisicaoImpressora (self):
		return self.int_numReqImpressora

	def getRequisicaoDisco (self):
		return self.int_numReqDisco

	def getBlocosMemoria (self):
		return self.int_blocosDeMem

	def getPrioridade (self):
		return self.int_prioridade

	def setPrioridade (self, valor):
		self.int_prioridade = valor

	def getPID (self):
		return self.int_PID

	def setPID(self,valor):
		self.int_PID = valor

	#Método para impressão dos atributos do processo
	def imprimirValoresProcesso(self):

		print("PID = ", self.int_PID)
		print("Tempo de inicializacao = ", self.int_TempIniciacao)
		print("Prioridade = ", self.int_prioridade)
		print("Tempo de processador = ", self.int_tempDeProcessador)
		print("Blocos de memoria = ", self.int_blocosDeMem)
		print("Num codigo impressora requisitada = ", self.int_numReqImpressora)
		print("Requisicao do Scanner = ", self.int_numReqScanner)
		print("Requisicao do Modem = ", self.int_numReqModem)
		print("Num codigo disco = ", self.int_numReqDisco)
		print("TokenCPU: ", self.int_tokenCPU)
