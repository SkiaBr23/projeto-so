

class ClassArquivo:


	#Obs. Arquivos que ja estao em disco, nao pertencem e nenhum
	# dos processos que estao sendo criados. Dessa forma, esses
	# arquivos possuem int_ID_Processo = -1.


	def __init__(self, int_ID_Processo,char_Nome_Arquivo,
				int_Bloco_Inicial, int_Num_Blocos):

		self.int_ID_Processo = int_ID_Processo
		self.char_Nome_Arquivo = char_Nome_Arquivo
		self.int_Num_Blocos = int_Num_Blocos
		self.int_Bloco_Inicial = int_Bloco_Inicial





	def imprimirValoresArquivo(self):
		
		print("ID do processo: ", self.int_ID_Processo)
		print("Nome do processo: " + self.char_Nome_Arquivo)
		print("Bloco Inicial: ", self.int_Bloco_Inicial)
		print("Quantidade de Blocos: ", self.int_Num_Blocos)















