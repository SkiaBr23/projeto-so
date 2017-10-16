from ClassProcesso import *
from ClassGerenciadorMemoria import *
from ClassArquivo import *
import time
from threading import *

class ClassDespachante:

	def __init__ (self, arquivoProcesses, arquivoFiles):
		self.arquivoProcesses = arquivoProcesses
		self.arquivoFiles = arquivoFiles
		self.gerenteMemoria = ClassGerenciadorMemoria()
		self.lock = Lock()

#
# Funcao lendoArquivoProcesses()
# Descricao: Realiza a leitura do arquivo txt chamado processes
# O padrao do arquivo deve ser:
# TempIniciacao, prioridade, tempDeProcessador, blocosDeMem, numReqImpressora, numReqScanner, numReqModem, numReqDisco
# A leitura ocorre por linha, ou seja, em cada linha, esses valores serao
# obtidos em uma string.
#
# Retorno: Um vetor de strings(cada string eh uma linha do arquivo).
#
	def lendoArquivoProcesses(self):

		linhasArquivo = []

		try:

			with open (self.arquivoProcesses) as arquivo:

				for line in arquivo:
					line = line.rstrip("\n")	# Remocao do "\n" no final de linha
					if line:
						linhasArquivo.append(line)

			arquivo.close()

			return(linhasArquivo)

		except FileNotFoundError:
			print("Arquivo contendo os processos não encontrado, encerrando")
			exit()


	def montaFilaProcesses (self, linhasArquivoProcesses):

		vetor_auxiliar = []

		for linha in linhasArquivoProcesses:
			atri_Processo = linha.split(",")

			processo_temporario = ClassProcesso(int(atri_Processo[0]),
								int(atri_Processo[1]), int(atri_Processo[2]),
								int(atri_Processo[3]), int(atri_Processo[4]),
								int(atri_Processo[5]), int(atri_Processo[6]),
								int(atri_Processo[7]), len(vetor_auxiliar))

			vetor_auxiliar.append(processo_temporario)

		return vetor_auxiliar

	def lendoArquivoFiles(self):

		linhasArquivo = []

		try:

			with open (self.arquivoFiles) as arquivo:

				for line in arquivo:
					line = line.rstrip("\n")	# Remocao do "\n" no final de linha
					if line:
						linhasArquivo.append(line)

			arquivo.close()

			return(linhasArquivo)

		except FileNotFoundError:
			print("Arquivo contendo os processos não encontrado, encerrando")
			exit()

	def runFiles(self, linhasArquivoFiles):

		contador = 0 
		quantSegmenOcupadosDisco = 0
		vetor_arquivos_auxiliar = []

		for linhaTemp in linhasArquivoFiles:
			#print(linhaTemp)
		
			if(contador == 0): # estamos lendo a primeira linha
				quantBlocosDisco = int(linhaTemp)
			if(contador == 1):
				quantSegmenOcupadosDisco = int(linhaTemp)
			if(contador > 1 and contador <= (quantSegmenOcupadosDisco + 1)):
				# Nesse momento, criar os arquivos que ja estao salvos no
				# disco. Criar uma classe arquivo!
				# ATENCAO: Esses caras nao sao de nenhum processo
				# ID_processo = -1

				atri_Arquivo = linhaTemp.split(",")
				#print(atri_Arquivo)

				arquivo_temporario = ClassArquivo((-1), atri_Arquivo[0],
													int(atri_Arquivo[1]),
													int(atri_Arquivo[2]))

				vetor_arquivos_auxiliar.append(arquivo_temporario)


			if(contador > (quantSegmenOcupadosDisco + 1)):
				# Nesse momento, colocamos os arquivos que sao criados
				# por processos no vetor de arquivos.
				# ATENCAO: Esses arquivos nao possuem int_Bloco_Inicial.
				# logo, sera colocado -1.
				
				atri_Arquivo = linhaTemp.split(",")
				#print(atri_Arquivo)

				if(atri_Arquivo[1] == "0"):
					arquivo_temporario = ClassArquivo(int(atri_Arquivo[0]),
														atri_Arquivo[2],
														(-1),	# Bloco inicial
														int(atri_Arquivo[3]))
			
					vetor_arquivos_auxiliar.append(arquivo_temporario)

				else: # Nesse caso, temos os arquivos que devem ser deletados 
					  # do disco.
					pass
					print("Comando para deletar arquivo")

			#print("------------------------------------")
			contador = contador + 1

		self.imprimeFiles(vetor_arquivos_auxiliar)


		return(vetor_arquivos_auxiliar)

	def runProcesses (self,processos):
		for processo in processos:
			AVANCAR = True
			tempoAtual = time.time()
			while (AVANCAR):
				#Tempo de diferença está em temp_cpu+temp_inicializacao, ajustar
				if (time.time() >= tempoAtual + processo.int_TempIniciacao):
					t = Thread(target=self.executeProcess,args=(processo,))
					t.start()
					AVANCAR = False

	def executeProcess(self, processo):
		if (self.gerenteMemoria.verificaDisponibilidadeMemoria(processo)):
			self.lock.acquire()
			self.imprimeInicioDeExecucaoProcesso(processo)
			print("process " + str(processo.int_PID))
			print("P" + str(processo.int_PID) + " STARTED")
			contadorInstruc = 1
			contadorCPU = 0
			tempoAtual = time.time()
			while (contadorCPU < processo.int_tempDeProcessador):
				if (time.time() > (tempoAtual+1)):
					print("P" + str(processo.int_PID) + " instruction " + str(contadorInstruc))
					contadorCPU += 1
					contadorInstruc += 1
					tempoAtual = time.time()

			print("P" + str(processo.int_PID) + " return SIGINT")
			self.lock.release()

	def imprimeProcessos(self, vetorProcessos):
		for processo in vetorProcessos:
			processo.imprimirValoresProcesso()
			print("-----------------------------------------------")

	def imprimeInicioDeExecucaoProcesso(self, processo):
		print("dispatcher => ")
		print("\tPID: " + str(processo.int_PID))
		print("\toffset: " + str(self.gerenteMemoria.getOffsetMemoria()))
		print("\tblocks: " + str(processo.int_blocosDeMem))
		print("\tpriority: " + str(processo.int_prioridade))
		print("\ttime: " + str(processo.int_tempDeProcessador))
		print("\tprinters: " + str(processo.int_numReqImpressora))
		print("\tscanners: " + str(processo.int_numReqScanner))
		print("\tmodems: " + str(processo.int_numReqModem))
		print("\tdrives: " + str(processo.int_numReqDisco))
		self.gerenteMemoria.atualizaOffsetMemoria(processo.int_blocosDeMem)


	def imprimeFiles(self, vetorFiles):
		for files in vetorFiles:
			files.imprimirValoresArquivo()
			print("-----------------------------------------------")			


	def startSO (self):
		#Criação das listas de processos e linhas do arquivo .txt de entrada
		linhasArquivoProcesses = []
		linhasArquivoFiles = []
		vetor_processos = []
		vetor_arquivos = []

		#Leitura das linhas do arquivo .txt de entrada com os processos
		linhasArquivoProcesses = self.lendoArquivoProcesses()

		linhasArquivoFiles = self.lendoArquivoFiles()

		vetor_processos = self.montaFilaProcesses(linhasArquivoProcesses)

		#self.runProcesses(vetor_processos)

		vetor_arquivos = self.runFiles(linhasArquivoFiles)


		#self.imprimeProcessos(vetor_processos)

		#self.imprimeFiles(vetor_arquivos)


