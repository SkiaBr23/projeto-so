#encoding=utf-8
from ClassArquivo import *

class ClassGerenciadorArquivo:



	# Funcao criada para inserir os arquivos que ja estao no
	# disco no momento de iniciacao do programa.
	def inserirInicioDisco(self, vetor_arquivos_disco, posicoesDisco):

		for arquivo in vetor_arquivos_disco:
			for posicoesArquivo in range(arquivo.getBlocoInicial(), (arquivo.getBlocoInicial() + arquivo.getNumBlocos())):
				posicoesDisco[posicoesArquivo] = arquivo.getNomeArquivo();
		
		return (posicoesDisco)
	
	# Nessa funcao, buscamos o primeiro arquivo no array(que foram inseridos na ordem do arquivo)
	# que esteja relacionado ao processo em execucao. Nesse caso, verificamos se eh um processo de
	# criacao ou remocao de arquivo.
	def executeArquivos(self, vetor_arquivos_processos,
						vetor_arquivos_disco, posicoesDisco):

		print("")
		print("Sistema de arquivos =>\n")

		contador = 0

		for arquivo in vetor_arquivos_processos:
			#print("------------------------------------------")
			#arquivo.imprimirValoresArquivo()
			#print("------------------------------------------")

			if(arquivo.getBlocoInicial() == (-1)):
				#print("Instrucao para criacao de arquivo...")

				self.inserirArquivoDisco(arquivo, vetor_arquivos_disco, posicoesDisco, contador)

			else:
				#print("Instrucao para deletar arquivo...")

				self.deletarArquivoDisco(arquivo, vetor_arquivos_disco, posicoesDisco, contador)

			self.imprimeMapaPosicoesDisco(posicoesDisco)
			print("")

	# Funcao para inserir um arquivo no disco. Essa funcao eh diferente da inserirInicioDisco
	# pois nesse caso essa funcao realiza uma verificacao no disco.
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

	# Funcao nao testada! Verificar funcionamento.
	# Como temos dois arrays relacionados com os arquivos em disco,
	# temos que nos preocupar em remover o arquivo de ambas referencias.
	def deletarArquivoDisco(self, arquivo, vetor_arquivos_disco, posicoesDisco, contador):
		
		for index in range(len(vetor_arquivos_disco)):
			if(vetor_arquivos_disco[index].getNomeArquivo() == arquivo.getNomeArquivo()):
				break

		del vetor_arquivos_disco[index]


		for posicoesArquivo in range(len(posicoesDisco)):
			if(posicoesDisco[posicoesArquivo] == arquivo.getNomeArquivo()):
				posicoesDisco[posicoesArquivo] = "0"

		print("Operacao ", contador, " => Sucesso")
		print("O processo ", arquivo.getIDProcesso(), " deletou o arquivo " + arquivo.getNomeArquivo())

		return (vetor_arquivos_disco, posicoesDisco)

	def imprimeMapaPosicoesDisco(self, posicoesDisco):

		print("Mapa de ocupação do disco:\n")
		print("---------------------------------------------------------------")
		print( "[|",end="")
		for posicao in posicoesDisco:
			print("  " + posicao + "  |",end="")

		print("]")
		print("---------------------------------------------------------------")