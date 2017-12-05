#encoding=utf-8

#Universidade de Brasília
#Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

#Importação de classes
from ClassGerenciadorProcesso import *
from ClassGerenciadorFilas import *
from ClassGerenciadorArquivo import *

#Classe Despachante para organizar e inicializar a operação do PseudoSO
class ClassDespachante:

	#Construtor da classe
	def __init__ (self, arquivoProcesses, arquivoFiles):
		self.arquivoProcesses = arquivoProcesses
		self.arquivoFiles = arquivoFiles
		self.gerenteMemoria = ClassGerenciadorMemoria()
		self.gerenteArquivo = ClassGerenciadorArquivo()
		self.gerenteRecursos = ClassGerenciadorRecurso()
		self.gerenteProcessos = ClassGerenciadorProcesso()
		self.gerenteFilas = ClassGerenciadorFilas()

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

			return linhasArquivo

		except FileNotFoundError:
			print("Arquivo contendo os processos não encontrado, encerrando")
			exit()


# Descricao: realiza a leitura de arquivos no arquivo.txt . A leitura eh realizada linha a linha
# Retorno: Um vetor das linhas do arquivo.txt
	def lendoArquivoFiles(self):

		linhasArquivo = []

		try:

			with open (self.arquivoFiles) as arquivo:

				for line in arquivo:
					line = line.rstrip("\n")	# Remocao do "\n" no final de linha
					if line:
						linhasArquivo.append(line)

			arquivo.close()

			return linhasArquivo

		except FileNotFoundError:
			print("Arquivo contendo os processos não encontrado, encerrando")
			exit()

# Descricao: Nessa funcao os objetos arquivos sao criados a partir das linhas
# lidas do arquivo.txt
# Argumento: As linhas do txt
# Retorno: 3 vetores
# vetor_arquivos_disco = Vetor de classeArquivo com os dados dos arquivos
#						ja salvos no disco.
# posicoesDisco = Posicoes dos arquivos no disco.
# vetor_arquivos_processos = Vetor de classeArquivo com os dados dos arquivos
#						que devem ser salvos no disco.
	def runFiles(self, linhasArquivoFiles):

		contador = 0
		quantBlocosDisco = 0
		quantSegmenOcupadosDisco = 0
		vetor_arquivos_disco = []
		vetor_arquivos_processos = []

		for linhaTemp in linhasArquivoFiles:
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

				arquivo_temporario = ClassArquivo((-1), atri_Arquivo[0],
													int(atri_Arquivo[1]),
													int(atri_Arquivo[2]))

				vetor_arquivos_disco.append(arquivo_temporario)

			if(contador > (quantSegmenOcupadosDisco + 1)):
				# Nesse momento, colocamos os arquivos que sao criados
				# por processos no vetor de arquivos.
				# ATENCAO: Esses arquivos nao possuem int_Bloco_Inicial.
				# logo, sera colocado -1.

				atri_Arquivo = linhaTemp.split(",")


				if(atri_Arquivo[1] == "0"):
					arquivo_temporario = ClassArquivo(int(atri_Arquivo[0]),
														atri_Arquivo[2],
														(-1),	# Bloco inicial
														int(atri_Arquivo[3]))

					vetor_arquivos_processos.append(arquivo_temporario)

				else: # Nesse caso, temos os arquivos que devem ser deletados
					  # do disco.
					arquivo_temporario = ClassArquivo(int(atri_Arquivo[0]),
														atri_Arquivo[2],
														(-2),	# BlocoInicial
														(-1))	# TamanhoBlobo
					vetor_arquivos_processos.append(arquivo_temporario)

			contador = contador + 1

		posicoesDisco = []						# Nessa parte, temos que posicoesDisco seria a simulacao do disco
		for posicao in range(quantBlocosDisco):	# eh um vetor de char que possui as posicoes relativas de onde os
			posicoesDisco.append("0")			# arquivos estao salvos.

		# Inserir os arquivos que estao no vetor_arquivos_disco (salvos no disco)
		# nas posicoes do vetor posicoesDisco.
		posicoesDisco = self.gerenteArquivo.inserirInicioDisco(vetor_arquivos_disco, posicoesDisco)

		#print(posicoesDisco)

		# Retorna 3 vetores.
		# vetor_arquivos_disco = Vetor de classeArquivo com os dados dos arquivos
		#						ja salvos no disco.
		# posicoesDisco = Posicoes dos arquivos no disco.
		# vetor_arquivos_processos = Vetor de classeArquivo com os dados dos arquivos
		#						que devem ser salvos no disco.
		return(vetor_arquivos_disco, posicoesDisco, vetor_arquivos_processos)

	#Método para impressão de lista de processos
	def imprimeProcessos(self, vetorProcessos):
		if not vetorProcessos:
			print("Vetor de processos vazio")
		else:
			for processo in vetorProcessos:
				processo.imprimirValoresProcesso()
				print("-----------------------------------------------")

	#Método para remover processos que apresentam tempo de inicialização
	#igual, mantendo somente um deles
	def removeProcessosTempoInicializacaoIgual (self, lista_processos):
		lista_processos_final = []
		for processo in lista_processos:
			if self.listWithoutEqualsInicializationTime(processo.getTempoInicializacao(), lista_processos_final):
				lista_processos_final.append(processo)
		return lista_processos_final

	#Método para avaliar se um processo com tempo de inicialização X já se
	#encontra na lista de processos
	def listWithoutEqualsInicializationTime(self, tempoInicializa, lista_processos_final):
		for processo in lista_processos_final:
			if processo.getTempoInicializacao() == tempoInicializa:
				return False
		return True

	#Método para atualizar os IDs dos processos, após remover
	#prováveis processos repetidos
	def updatePIDs(self,lista_processos):
		contador = 0
		for processo in lista_processos:
			processo.setPID(contador)
			contador += 1
		return lista_processos

	#Método de inicialização do PseudoSO
	def startSO (self):
		#Criação das listas de processos e linhas do arquivo .txt de entrada
		linhasArquivoProcesses = []
		linhasArquivoFiles = []
		vetor_processos = []
		vetor_arquivos_disco = []
		vetor_arquivos_processos = []
		vetor_processos_tempoReal = []
		vetor_processos_usuario = []
		posicoesDisco = []

		#Leitura das linhas do arquivo .txt de entrada com os processos
		linhasArquivoProcesses = self.lendoArquivoProcesses()

		#Leitura das linhas do arquivo .txt de entrada com os files
		linhasArquivoFiles = self.lendoArquivoFiles()

		#Montagem da lista de processos geral
		lista_processos = self.gerenteProcessos.montaListaProcesses(linhasArquivoProcesses)

		#Cópia da lista de processos
		todos_os_processos = lista_processos

		#Remoção de processos com tempo de inicialização iguais
		lista_processos = self.removeProcessosTempoInicializacaoIgual(lista_processos)

		#Atualização de IDs dos processos após remoção de processos com
		#tempo de inicialização iguais
		lista_processos = self.updatePIDs(lista_processos)

		#Set da lista de processos no gerenciador de filas
		self.gerenteFilas.setListaProcessos(lista_processos)

		#Inicialização da thread que move os processos da fila global para a
		#fila de processos de tempo real
		moveFilaRT = Thread(target=self.gerenteFilas.moverParaFilaRT,name='MoveFilaRT',args=())
		moveFilaRT.start()

		#Inicialização da thread que realiza a chamada para execução dos
		#processos de tempo real
		runFilaRT = Thread(target=self.gerenteFilas.executarProcessoFilaRT,name='RunFilaRT',args=())
		runFilaRT.start()

		#Inicialização da thread que move os processos da fila global para a
		#fila de processos de usuario
		moveFilaUsuario = Thread(target=self.gerenteFilas.moverParaFilaUsuario,name='MoveFilaUsuario',args=())
		moveFilaUsuario.start()

		#Inicialização da thread que realiza a chamada para execução dos
		#processos de usuario
		runFilaUsuario = Thread(target=self.gerenteFilas.executarProcessosFilaUsuario,name='RunFilaUsuario',args=())
		runFilaUsuario.start()

		#Chamada do método que executa os processos
		self.gerenteFilas.runProcesses(self.gerenteFilas.getListaProcessos())

		#Obtenção dos valores do .txt de files para execução dos files
		vetor_arquivos_disco, posicoesDisco, vetor_arquivos_processos = self.runFiles(linhasArquivoFiles)

		#Chamada do método que executa os files
		self.gerenteArquivo.executeArquivos(vetor_arquivos_processos, vetor_arquivos_disco, posicoesDisco, todos_os_processos)
