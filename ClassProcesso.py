#encoding=utf-8
class ClassProcesso:


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

	def getPID (self):
		return self.int_PID


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


	def envelhecimento(fila_processos):

		for processo in fila_processos:
			processo.int_prioridade = processo.int_prioridade - 1

		return fila_processos
