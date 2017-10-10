from ClassProcesso import *

class ClassDespachante:

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

		with open ("processes.txt") as arquivo:

			for line in arquivo:
				line = line.rstrip("\n")	# Remocao do "\n" no final de linha
				if line:
					linhasArquivo.append(line)

		arquivo.close()

		return(linhasArquivo)


	def montaProcesses (self, linhasArquivoProcesses):

		vetor_auxiliar = []

		for linha in linhasArquivoProcesses:
			atri_Processo = linha.split(",")

			processo_temporario = ClassProcesso(int(atri_Processo[0]),
								int(atri_Processo[1]), int(atri_Processo[2]),
								int(atri_Processo[3]), int(atri_Processo[4]),
								int(atri_Processo[5]), int(atri_Processo[6]),
								int(atri_Processo[7]))


			vetor_auxiliar.append(processo_temporario)

		return vetor_auxiliar


	def imprimeProcessos(self, vetorProcessos):
		for processo in vetorProcessos:
			processo.imprimirValoresProcesso()
			print("-----------------------------------------------")


	def startSO (self):
		#Criação das listas de processos e linhas do arquivo .txt de entrada
		linhasArquivo = []
		vetor_processos = []

		#Leitura das linhas do arquivo .txt de entrada com os processos
		linhasArquivo = self.lendoArquivoProcesses()

		vetor_processos = self.montaProcesses(linhasArquivo)

		self.imprimeProcessos(vetor_processos)