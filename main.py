# Para executar o programa:
#	python3 teste1.py


from ClassProcesso import *
from ClassInfo import *
from ClassDespachante import *

def main():

	#Limpeza de terminal e exibição de informações do projeto
	ClasseInformativo = ClassInfo()
	ClasseInformativo.limparTela()
	ClasseInformativo.informativoPrograma()

	ProcessoDespachante = ClassDespachante()

	ProcessoDespachante.startSO()


if __name__ == "__main__":
	main()