from ClassProcesso import *
from ClassGerenciadorMemoria import *

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

	def executeProcess(self, processo):
		if (self.gerenteMemoria.verificaDisponibilidadeMemoria(processo)):
			print("dispatcher => ")


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

		vetor_processos = self.runProcesses(linhasArquivo)

		self.imprimeProcessos(vetor_processos)