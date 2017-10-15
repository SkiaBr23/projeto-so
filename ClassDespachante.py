from ClassProcesso import *
from ClassGerenciadorMemoria import *
from ClassArquivo import *

class ClassDespachante:

	def __init__ (self, arquivoProcesses, arquivoFiles):
		self.arquivoProcesses = arquivoProcesses
		self.arquivoFiles = arquivoFiles
		self.gerenteMemoria = ClassGerenciadorMemoria()

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


	def runProcesses (self, linhasArquivoProcesses):

		vetor_auxiliar = []

		for linha in linhasArquivoProcesses:
			atri_Processo = linha.split(",")

			processo_temporario = ClassProcesso(int(atri_Processo[0]),
								int(atri_Processo[1]), int(atri_Processo[2]),
								int(atri_Processo[3]), int(atri_Processo[4]),
								int(atri_Processo[5]), int(atri_Processo[6]),
								int(atri_Processo[7]), len(vetor_auxiliar))

			self.executeProcess(processo_temporario)


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
			print(linhaTemp)
		
			if(contador == 0): # estamos lendo a primeira linha
				quantBlocosDisco = int(linhaTemp)
			if(contador == 1):
				quantSegmenOcupadosDisco = int(linhaTemp)
			if(contador > 1 and contador <= (quantSegmenOcupadosDisco + 1)):
				# Nesse momento, criar os arquivos que ja estao salvos no
				# disco. Criar uma classe arquivo!
				# ATENCAO: Esses caras nao sao de nenhum processo
				# ID_processo = -1
				#arquivo_temporario = ClassArquivo()

				atri_Arquivo = linhaTemp.split(",")
				print(atri_Arquivo)

				arquivo_temporario = ClassArquivo((-1), atri_Arquivo[0],
													int(atri_Arquivo[1]),
													int(atri_Arquivo[2]))

				vetor_arquivos_auxiliar.append(arquivo_temporario)


			if(contador > (quantSegmenOcupadosDisco + 1)):
				print("AQUIIIIII 2")
				# Aqui, temos que verificar se eh para criacar o arquivo
				# ou se eh para deletar o arquivo.
				# Nesse caso, temos os arquivos que sao criados ao
				# longo da execucao dos processos.
				# Verificar a logica de execucao do trabalho para
				# saber quando que o arquivo vai ser criado.


			print("------------------------------------")
			contador = contador + 1


		return(vetor_arquivos_auxiliar)


	def executeProcess(self, processo):
		if (self.gerenteMemoria.verificaDisponibilidadeMemoria(processo)):
			self.imprimeInicioDeExecucaoProcesso(processo)


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

		vetor_processos = self.runProcesses(linhasArquivoProcesses)

		vetor_arquivos = self.runFiles(linhasArquivoFiles)


		self.imprimeProcessos(vetor_processos)

		self.imprimeFiles(vetor_arquivos)


