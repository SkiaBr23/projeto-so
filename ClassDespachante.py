#encoding=utf-8
from ClassProcesso import *
from ClassGerenciadorMemoria import *
from ClassArquivo import *
from ClassGerenciadorArquivo import *
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
		posicoesDisco = self.inserirInicioDisco(vetor_arquivos_disco, posicoesDisco)

		print(posicoesDisco)

		# Retorna 3 vetores.
		# vetor_arquivos_disco = Vetor de classeArquivo com os dados dos arquivos
		#						ja salvos no disco.
		# posicoesDisco = Posicoes dos arquivos no disco.
		# vetor_arquivos_processos = Vetor de classeArquivo com os dados dos arquivos
		#						que devem ser salvos no disco.
		return(vetor_arquivos_disco, posicoesDisco, vetor_arquivos_processos)


	# Funcao criada para inserir os arquivos que ja estao no
	# disco no momento de iniciacao do programa.
	def inserirInicioDisco(self, vetor_arquivos_disco, posicoesDisco):

		for arquivo in vetor_arquivos_disco:
			for posicoesArquivo in range(arquivo.getBlocoInicial(), (arquivo.getBlocoInicial() + arquivo.getNumBlocos())):
				posicoesDisco[posicoesArquivo] = arquivo.getNomeArquivo();
		
		return (posicoesDisco)


	def runProcesses (self,processos, vetor_arquivos_processos,
						vetor_arquivos_disco, posicoesDisco):
		for processo in processos:
			AVANCAR = True
			tempoAtual = time.time()
			while (AVANCAR):
				#Tempo de diferença está em temp_cpu+temp_inicializacao, ajustar
				if (time.time() >= tempoAtual + processo.int_TempIniciacao):
					t = Thread(target=self.executeProcess,args=(processo, vetor_arquivos_processos,vetor_arquivos_disco, posicoesDisco,))
					t.start()
					AVANCAR = False

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
	def executeProcess(self, processo, vetor_arquivos_processos,
						vetor_arquivos_disco, posicoesDisco):
		if (self.gerenteMemoria.verificaDisponibilidadeMemoria(processo)):
			self.lock.acquire()
			self.manipulaArquivo(processo.getPID(), vetor_arquivos_processos,			# Linha nova!
								vetor_arquivos_disco, posicoesDisco)					# Linha nova!
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


	# Nessa funcao, buscamos o primeiro arquivo no array(que foram inseridos na ordem do arquivo)
	# que esteja relacionado ao processo em execucao. Nesse caso, verificamos se eh um processo de
	# criacao ou remocao de arquivo.
	def manipulaArquivo(self, idProcesso, vetor_arquivos_processos,
						vetor_arquivos_disco, posicoesDisco):

		for arquivo in vetor_arquivos_processos:
			if(idProcesso == arquivo.getIDProcesso()):
				break

		print("Processo manipula arquivo!")
		print("------------------------------------------")
		arquivo.imprimirValoresArquivo()
		print("------------------------------------------")

		if(arquivo.getBlocoInicial() == (-1)):
			print("Instrucao para criacao de arquivo...")

			self.inserirArquivoDisco(arquivo, vetor_arquivos_disco, posicoesDisco)

		else:
			print("Instrucao para deletar arquivo...")

			self.deletarArquivoDisco(arquivo, vetor_arquivos_disco, posicoesDisco)

	# Funcao para inserir um arquivo no disco. Essa funcao eh diferente da inserirInicioDisco
	# pois nesse caso essa funcao realiza uma verificacao no disco.
	# verifica se o arquivo ja foi inserido e verifica se possui espaco. ---------------------------> DONE
	# Quando inserir um arquivo no disco, devemos remover esse mesmo 
	# arquivo em vetor_arquivos_processos.----------------------------------------------------------> NOT DONE
	#
	def inserirArquivoDisco(self, arquivo, vetor_arquivos_disco, posicoesDisco):
		
		flagInserir = 0
		tamanhoArquivo = arquivo.getNumBlocos()

		for arquivo_temporario in vetor_arquivos_disco:
			if(arquivo.getNomeArquivo() == arquivo_temporario.getNomeArquivo()):
				print("Arquivo ja existe no disco!")
				return (-1)

		for posicoesArquivo in range(len(posicoesDisco)):
			if(posicoesDisco[posicoesArquivo] == "0"):
				tamanhoArquivo = tamanhoArquivo - 1
			else:
				tamanhoArquivo = arquivo.getNumBlocos()

			if(tamanhoArquivo == 0):
				print("o arquivo cabe entre as posicoes: ", (posicoesArquivo - arquivo.getNumBlocos() + 1), "a", posicoesArquivo)
				break

		if(tamanhoArquivo != 0):
			print("Nao existe espaco para o arquivo...")
		else:
			for posicoesArquivo in range((posicoesArquivo - arquivo.getNumBlocos() + 1), (posicoesArquivo + 1)):
				posicoesDisco[posicoesArquivo] = arquivo.getNomeArquivo();


		print(posicoesDisco)

		return (vetor_arquivos_disco, posicoesDisco)


	# Funcao nao testada! Verificar funcionamento.
	# Como temos dois arrays relacionados com os arquivos em disco,
	# temos que nos preocupar em remover o arquivo de ambas referencias.
	def deletarArquivoDisco(self, arquivo, vetor_arquivos_disco, posicoesDisco):
		
		for index in range(len(vetor_arquivos_disco)):
			if(vetor_arquivos_disco[index].getNomeArquivo() == arquivo.getNomeArquivo()):
				break

		del vetor_arquivos_disco[index]


		for posicoesArquivo in range(len(posicoesDisco)):
			if(posicoesDisco[posicoesArquivo] == arquivo.getNomeArquivo()):
				posicoesDisco[posicoesArquivo] = "0"


		return (vetor_arquivos_disco, posicoesDisco)



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
		if not vetorFiles:
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
		posicoesDisco = []

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
		vetor_arquivos_disco, posicoesDisco, vetor_arquivos_processos = self.runFiles(linhasArquivoFiles)




		self.runProcesses(vetor_processos_tempoReal, vetor_arquivos_processos,
							vetor_arquivos_disco, posicoesDisco)


		# vetor_arquivos_disco = arquivos ja em disco
		# vetor_arquivos_processos = arquivos que serao executados por processos
		# pode ser tanto para instrucoes de deletar como criar. Salvos na ordem
		# do arquivo.
		



		#self.imprimeFiles(vetor_arquivos_disco)
		#self.imprimeFiles(vetor_arquivos_processos)
		


