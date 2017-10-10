import os

class ClassInfo:

	def informativoPrograma (self):
		print ("Universidade de Brasília - 02/2017")
		print ("Projeto Final - Sistemas Operacionais")


	def limparTela (self):
		os.system('cls' if os.name=='nt' else 'clear')
