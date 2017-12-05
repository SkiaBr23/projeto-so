#encoding=utf-8

# Para executar o programa:
#	python3 main.py processes.txt files.txt
#
# Obs: É obrigatório o uso de Python3 para o funcionamento
# correto do programa.
#

from ClassInfo import *
from ClassDespachante import *
import sys

# Função principal do programa
# Declara as classes de alto nível de Despachante e Informativo,
# recebe os argumentos do usuário e executa o simulador de SO.
def main():

	# Declaração da classe utilitária de informação
	ClasseInformativo = ClassInfo()

	# Limpa a tela do terminal
	ClasseInformativo.limparTela()

	# Recebe os argumentos enviados via linha de comando
	try:
		if sys.argv[1] == "processes.txt" and sys.argv[2] == "files.txt":
			nomeArquivoProcesses = sys.argv[1]
			nomeArquivoFiles = sys.argv[2]
	# Caso argumentos não tenham sido passados, solicita ao usuário para entrar
	# com os valores automaticamente.
	except IndexError:
		print("Arquivos de entrada não fornecidos. Por favor, digite o nome do arquivo .txt contendo os processos")
		nomeArquivoProcesses = input("Nome do arquivo (inclua a extensão .txt): ")
		print("Por favor, digite o nome do arquivo .txt contendo a execução")
		nomeArquivoFiles = input("Nome do arquivo (inclua a extensão .txt): ")

	# Limpa a tela e exibe as informações de cabeçalho do 
	ClasseInformativo.limparTela()
	ClasseInformativo.informativoPrograma()

	# Cria uma instância da classe despachante. Essa classe declara internamente
	# todas as classes de gerenciamento do modelo
	ProcessoDespachante = ClassDespachante(nomeArquivoProcesses,nomeArquivoFiles)

	# Inicia o processo de simulação de SO
	ProcessoDespachante.startSO()


if __name__ == "__main__":
	main()
