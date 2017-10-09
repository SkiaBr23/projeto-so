




class ClassProcesso:


	def __init__(self, int_TempIniciacao, int_prioridade,
					int_tempDeProcessador, int_blocosDeMem,
					int_numReqImpressora,int_numReqScanner,
					int_numReqModem, int_numReqDisco):

		self.int_TempIniciacao = int_TempIniciacao
		self.int_prioridade = int_prioridade
		self.int_tempDeProcessador = int_tempDeProcessador
		self.int_blocosDeMem = int_blocosDeMem
		self.int_numReqImpressora = int_numReqImpressora
		self.int_numReqScanner = int_numReqScanner
		self.int_numReqModem = int_numReqModem
		self.int_numReqDisco = int_numReqDisco



	def imprimirValoresProcesso(self):

		print("Tempo de inicializacao = ", self.int_TempIniciacao)
		print("Prioridade = ", self.int_prioridade)
		print("Tempo de processador = ", self.int_tempDeProcessador)
		print("Blocos de memoria = ", self.int_blocosDeMem)
		print("Num codigo impressora requisitada = ", self.int_numReqImpressora)
		print("Requisicao do Scanner = ", self.int_numReqScanner)
		print("Requisicao do Modem = ", self.int_numReqModem)
		print("Num codigo disco = ", self.int_numReqDisco)






