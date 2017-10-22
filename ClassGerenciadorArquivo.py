#encoding=utf-8

class ClassGerenciadorArquivo:

	def __init__(self):
		self.int_memoria_processos_usuario = TAMANHO_MEMORIA_PROCESSOS_USUARIO
		self.int_memoria_processos_rt = TAMANHO_MEMORIA_PROCESSOS_RT
		self.int_offset_memoria = 0

	
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

