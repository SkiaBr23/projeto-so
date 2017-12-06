#encoding=utf-8

#Universidade de Brasília
#Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

from ClassArquivo import *
from ClassProcesso import *

class ClassGerenciadorArquivo:



	# Descricao: Funcao criada para inserir os arquivos que ja estao no
	# disco no momento de iniciacao do programa.
	# Argumentos: vetor de posicoes do disco(que devem estar zerados) e o vetor de arquivos que ja
	# devem estar salvos no disco quando o SO iniciar.
	def inserirInicioDisco(self, vetor_arquivos_disco, posicoesDisco):

		for arquivo in vetor_arquivos_disco:
			for posicoesArquivo in range(arquivo.getBlocoInicial(), (arquivo.getBlocoInicial() + arquivo.getNumBlocos())):
				posicoesDisco[posicoesArquivo] = arquivo.getNomeArquivo();

		return (posicoesDisco)


	# Descricao: Verifica se o processo existe.
	# Argumentos: recebe o arquivo a ser gravado e a lista de processos do SO.
	# Retorno:
	# caso o processo nao exista = retorna 0.
	# caso o processo nao exista = retorna 1.
	#
	def verificaProcessoExiste(self, arquivo, lista_processos):

		idExiste = 0

		idProcessoNoArquivo = arquivo.getIDProcesso()

		for processo in lista_processos:
			idProcesso = processo.getPID()
			if(idProcessoNoArquivo == idProcesso):
				idExiste = 1 # Existe processo

		return idExiste


	# Descricao: Nessa funcao, buscamos o primeiro arquivo no array(que foram inseridos na ordem do arquivo)
	# que esteja relacionado ao processo em execucao. Nesse caso, verificamos se eh um processo de
	# criacao ou remocao de arquivo.
	# Argumentos: Lista de processos do SO, Os arquivos ja salvos no disco, as posicoes que eles ocupam
	# e os arquivos que serao manipulados pelos processos do SO.
	def executeArquivos(self, vetor_arquivos_processos,
						vetor_arquivos_disco, posicoesDisco, lista_processos):

		print("")
		print("Sistema de arquivos =>\n")

		contador = 0
		idExiste = 0

		for arquivo in vetor_arquivos_processos:

			idExiste = self.verificaProcessoExiste(arquivo, lista_processos)

			if(idExiste == 1):

				if(arquivo.getBlocoInicial() == (-1)):
					self.inserirArquivoDisco(arquivo, vetor_arquivos_disco, posicoesDisco, contador)

				else:
					self.deletarArquivoDisco(arquivo, vetor_arquivos_disco, posicoesDisco, contador, lista_processos)

			else:
				print("Operacao ", contador, " => Falha\n")
				print("Nao existe o processo.")

			self.imprimeMapaPosicoesDisco(posicoesDisco)
			contador +=1
			print("")

	# descricao: Funcao para inserir um arquivo no disco. Essa funcao eh diferente da inserirInicioDisco
	# pois nesse caso essa funcao realiza uma verificacao no disco.
	# Argumentos: recebe o arquivo que vai ser salvo no disco, o vetor de arquivos que estao no disco, as posicoes
	# dos arquivos no disco e um contador para mostrar o numero da operacao.
	def inserirArquivoDisco(self, arquivo, vetor_arquivos_disco, posicoesDisco, contador):

		flagInserir = 0
		tamanhoArquivo = arquivo.getNumBlocos()

		for arquivo_temporario in vetor_arquivos_disco:
			if(arquivo.getNomeArquivo() == arquivo_temporario.getNomeArquivo()):
				print("Operacao ", contador, " => Falha")
				print("Processo ", arquivo.getIDProcesso(), " nao pode criar o arquivo " + arquivo.getNomeArquivo() + " (ja existe)")
				return (-1)

		for posicoesArquivo in range(len(posicoesDisco)):
			if(posicoesDisco[posicoesArquivo] == "0"):
				tamanhoArquivo = tamanhoArquivo - 1
			else:
				tamanhoArquivo = arquivo.getNumBlocos()

			if(tamanhoArquivo == 0):
				print("Operacao ", contador, " => Sucesso")
				print("O processo ", arquivo.getIDProcesso(), " criou o arquivo "+ arquivo.getNomeArquivo() +" (Blocos de: ", (posicoesArquivo - arquivo.getNumBlocos() + 1), " a ", posicoesArquivo, ")")
				break

		if(tamanhoArquivo != 0):
			print("Operacao ", contador, " => Falha")
			print("O processo ", arquivo.getIDProcesso(), " nao pode criar o arquivo " + arquivo.getNomeArquivo() + " (falta espaco)")
		else:

			for posicoesArquivo in range((posicoesArquivo - arquivo.getNumBlocos() + 1), (posicoesArquivo + 1)):
				posicoesDisco[posicoesArquivo] = arquivo.getNomeArquivo();


		return (vetor_arquivos_disco, posicoesDisco)

	# Descricao: Deleta arquivo no disco. Funcao chamada quando deseja deletar arquivo.
	# Argumentos: recebe o arquivo que vai ser salvo no disco, o vetor de arquivos que estao no disco, as posicoes
	# dos arquivos no disco e um contador para mostrar o numero da operacao.
	# Retorno: Retorna o vetor de posicoes no disco e o vetor de arquivos que estao salvos no disco.
	def deletarArquivoDisco(self, arquivo, vetor_arquivos_disco, posicoesDisco, contador, lista_processos):

		#processoArquivo eh o processo que quer deletar o arquivo.
		processoArquivo = arquivo.getIDProcesso()

		#nomeArquivo eh o nome do arquivo que queremos deletar.
		nomeArquivoDeletar = arquivo.getNomeArquivo()

		for file in vetor_arquivos_disco:
			if(file.getNomeArquivo() == nomeArquivoDeletar):
				break;

		for processo in lista_processos:
			if(processo.getPID() == processoArquivo):
				#processo.imprimirValoresProcesso()
				prioridadeProcesso = processo.getPrioridade()
				break

		if((file.getIDProcesso() == processoArquivo) or (prioridadeProcesso == 0)):

			for index in range(len(vetor_arquivos_disco)):
				if(vetor_arquivos_disco[index].getNomeArquivo() == arquivo.getNomeArquivo()):
					break

			del vetor_arquivos_disco[index]


			for posicoesArquivo in range(len(posicoesDisco)):
				if(posicoesDisco[posicoesArquivo] == arquivo.getNomeArquivo()):
					posicoesDisco[posicoesArquivo] = "0"

			print("Operacao ", contador, " => Sucesso")
			print("O processo ", arquivo.getIDProcesso(), " deletou o arquivo " + arquivo.getNomeArquivo())

		else:
			print("Operacao", contador, "=> falha")
			print("O processo ", arquivo.getIDProcesso(), " nao deletou o arquivo " + arquivo.getNomeArquivo() + " e o processo nao e de tempo real.");

		return (vetor_arquivos_disco, posicoesDisco)

	def imprimeMapaPosicoesDisco(self, posicoesDisco):

		print("Mapa de ocupação do disco:\n")
		print("---------------------------------------------------------------")
		print( "[|",end="")
		for posicao in posicoesDisco:
			print("  " + posicao + "  |",end="")

		print("]")
		print("---------------------------------------------------------------")
