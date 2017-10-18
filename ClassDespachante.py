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

				vetor_arquivos_processos.append(arquivo_temporario)


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

		# Retorna 3 vetores de arquivos.
		# os que ja estao em disco, os que 
		return(vetor_arquivos_disco, vetor_arquivos_processos)

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

	# Em executeProcess a gente verifica se o processo faz referencia a
	# manipulacao de arquivos (por meio do PID) e tambem se faz referencia
	# a algum recurso (modem, impressora...). Caso faca referencia
	# a algum recurso, travamos ele.
	# No caso de processos de tempo real, isso eh tranquilo pq eh FIFO sem ser
	# preemptivo. Entao ele comeca e termina.
	# No caso de processos de usuario, quando o recurso for alocado, ele so eh
	# desalocado quando temrinar o processo. (Ainda tem que pensar um pouco mais...)

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
		if not vetorProcessos:
			print("Vetor de processos vazio")
		else:
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
		if not vetorProcessos:
			print("Vetor de arquivos vazio")
		else:
			for files in vetorFiles:
				files.imprimirValoresArquivo()
				print("-----------------------------------------------")			


	def separaProcessos(self, vetor_processos):
		processos_usuario = []
		processos_tempoReal = []

		for processo in vetor_processos:
			if(processo.getPrioridade == 0):
				processos_tempoReal.append(processo)
			else:
				processos_usuario.append(processo)

		return(processos_usuario, processos_tempoReal)



	def startSO (self):
		#Criação das listas de processos e linhas do arquivo .txt de entrada
		linhasArquivoProcesses = []
		linhasArquivoFiles = []
		vetor_processos = []
		vetor_arquivos_disco = []
		vetor_arquivos_processos = []
		vetor_processos_tempoReal = []
		vetor_processos_usuario = []

		#Leitura das linhas do arquivo .txt de entrada com os processos
		linhasArquivoProcesses = self.lendoArquivoProcesses()

		linhasArquivoFiles = self.lendoArquivoFiles()

		vetor_processos = self.montaFilaProcesses(linhasArquivoProcesses)

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

		vetor_processos_tempoReal, vetor_processos_usuario = self.separaProcessos(vetor_processos)
		#self.imprimeProcessos(vetor_processos_tempoReal)


		self.runProcesses(vetor_processos_tempoReal)


		# vetor_arquivos_disco = arquivos ja em disco
		# vetor_arquivos_processos = arquivos que serao executados por processos
		# pode ser tanto para instrucoes de deletar como criar. Salvos na ordem
		# do arquivo.
		vetor_arquivos_disco, vetor_arquivos_processos = self.runFiles(linhasArquivoFiles)



		#self.imprimeFiles(vetor_arquivos_disco)
		#self.imprimeFiles(vetor_arquivos_processos)
		


