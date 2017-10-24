#encoding=utf-8
import time
from threading import *
from ClassGerenciadorProcesso import *
from ClassGerenciadorMemoria import *
from ClassGerenciadorArquivo import *
from ClassGerenciadorRecurso import *
from ClassGerenciadorFilas import *

class ClassDespachante:

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

			return(linhasArquivo)

		except FileNotFoundError:
			print("Arquivo contendo os processos não encontrado, encerrando")
			exit()

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
		quantBlocosDisco = 0
		quantSegmenOcupadosDisco = 0
		vetor_arquivos_disco = []
		vetor_arquivos_processos = []



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
														(-1),	# BlocoInicial
														(-1))	# TamanhoBlobo
					vetor_arquivos_processos.append(arquivo_temporario)

			#print("------------------------------------")
			contador = contador + 1

		posicoesDisco = []						# Nessa parte, temos que posicoesDisco seria a simulacao do disco
		for posicao in range(quantBlocosDisco):	# eh um vetor de char que possui as posicoes relativas de onde os
			posicoesDisco.append("0")			# arquivos estao salvos.

		# Inserir os arquivos que estao no vetor_arquivos_disco (salvos no disco)
		# nas posicoes do vetor posicoesDisco.
		posicoesDisco = self.gerenteArquivo.inserirInicioDisco(vetor_arquivos_disco, posicoesDisco)

		print(posicoesDisco)

		# Retorna 3 vetores.
		# vetor_arquivos_disco = Vetor de classeArquivo com os dados dos arquivos
		#						ja salvos no disco.
		# posicoesDisco = Posicoes dos arquivos no disco.
		# vetor_arquivos_processos = Vetor de classeArquivo com os dados dos arquivos
		#						que devem ser salvos no disco.
		return(vetor_arquivos_disco, posicoesDisco, vetor_arquivos_processos)


	# Em executeProcess a gente verifica se o processo faz referencia a
	# manipulacao de arquivos (por meio do PID) ------------------------------------------> DONE

	# e tambem se faz referencia a algum recurso (modem, impressora...). Caso faca referencia
	# a algum recurso, travamos ele. -----------------------------------------------------> NOT DONE

	# No caso de processos de tempo real, isso eh tranquilo pq eh FIFO sem ser
	# preemptivo. Entao ele comeca e termina.
	# No caso de processos de usuario, quando o recurso for alocado, ele so eh
	# desalocado quando temrinar o processo. (Ainda tem que pensar um pouco mais...)
	#-------------------------------------------------------------------------------------------------------

		# Um grande problema eh que no roteiro da professora, a manipulacao dos arquivos nao esta seguindo a ordem
		# de execucao dos processos e sim a ordem de execucao do arquivo. Nao faz sentido essa ordem do roteiro.
		# Eu estou seguindo a ordem de execucao dos processos. Na funcao executeProcess, eu faco a busca dos arquivos
		# que sao referenciados pelo processo que esta sendo executado. Ou seja, a primeira operacao de arquivo seria
		# com o processo 0, ja no exemplo dela, a primeira eh com o processo 1. O que eu meu entendimento esta errado.

	#--------------------------------------------------------------------------------------------------------

	# O que falta: Fazer a verificacao de outras operacoes que manipulam arquivos de um mesmo processo.
	# Com essa logica que eu pensei tempos, por enquanto: Uma manupulacao de arquivo por processo.


	def imprimeProcessos(self, vetorProcessos):
		if not vetorProcessos:
			print("Vetor de processos vazio")
		else:
			for processo in vetorProcessos:
				processo.imprimirValoresProcesso()
				print("-----------------------------------------------")

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

		linhasArquivoFiles = self.lendoArquivoFiles()

		lista_processos = self.gerenteProcessos.montaListaProcesses(linhasArquivoProcesses)

		# Comentarios de progresso:
		# Separei os processos. Agora temos que pensar em como executa-los.
		# Processos de tempo real eh FIFO
		# Processos de usuario eh sao minimo 3 filas de prioridades.
		# Minha ideia:
		# Definimos 3 vetores para esses processos.
		#
		# Primeiro: Organizamos por prioridade de processos e executa por meio
		# 			do RoundRobin(preemptivo com quantum 1).
		# Segundo: RoundRobin sem definicao por prioridade (quantum 3).
		# Terceiro: FIFO (nao preemptivo). POSSO ESTAR SENDO RADICAL. ANALISAR
		#									COM CUIDADO -> Quero evitar Starvation
		# A execucao dos processos de usuario serao semelhantes as de tempo real
		# usando o lock e etc.

		#Comentei esse separaProcessos pq nao faz sentido ja manter eles separados sem saber se tem os recursos
		#self.gerenteProcessos.separaProcessos(self.gerenteProcessos.getProcessos())
		#self.imprimeProcessos(vetor_processos_tempoReal)
		#Comentei o runFiles pq nao preciso disso agora
		vetor_arquivos_disco, posicoesDisco, vetor_arquivos_processos = self.runFiles(linhasArquivoFiles)
		self.gerenteFilas.setListaProcessos(lista_processos)
		self.gerenteFilas.runProcesses(self.gerenteFilas.getListaProcessos())
		#self.gerenteProcessos.runProcesses(self.gerenteProcessos.getProcessosRT(), vetor_arquivos_processos,vetor_arquivos_disco, posicoesDisco)


		# vetor_arquivos_disco = arquivos ja em disco
		# vetor_arquivos_processos = arquivos que serao executados por processos
		# pode ser tanto para instrucoes de deletar como criar. Salvos na ordem
		# do arquivo.




		#self.imprimeFiles(vetor_arquivos_disco)
		#self.imprimeFiles(vetor_arquivos_processos)
