#encoding=utf-8

# Para executar o programa:
#	python3 teste1.py


from ClassProcesso import *
from ClassInfo import *
from ClassDespachante import *
import sys

def main():

	#Limpeza de terminal e exibição de informações do projeto
	ClasseInformativo = ClassInfo()
	ClasseInformativo.limparTela()

	try:
		if (sys.argv[1] == "processes.txt" and sys.argv[2] == "files.txt"):
			nomeArquivoProcesses = sys.argv[1]
			nomeArquivoFiles = sys.argv[2]
	except IndexError:
		print("Arquivos de entrada não fornecidos. Por favor, digite o nome do arquivo .txt contendo os processos")
		nomeArquivoProcesses = input("Nome do arquivo (inclua a extensão .txt): ")
		print("Por favor, digite o nome do arquivo .txt contendo a execução")
		nomeArquivoFiles = input("Nome do arquivo (inclua a extensão .txt): ")

	ClasseInformativo.limparTela()
	ClasseInformativo.informativoPrograma()

	ProcessoDespachante = ClassDespachante(nomeArquivoProcesses,nomeArquivoFiles)

	ProcessoDespachante.startSO()


if __name__ == "__main__":
	main()
