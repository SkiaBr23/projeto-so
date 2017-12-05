#encoding=utf-8

# Universidade de Brasília
# Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
#
# Projeto Final
# Para executar o programa:
#
#	python3 main.py  (Para execução com arquivos padrão)
#
# 	ou
#   
# 	python3 main.py -p processes.txt -f files.txt  (Para execução com arquivos customizados)
#
# Obs: É obrigatório o uso de Python3 para o funcionamento
# correto do programa.
#

from ClassInfo import *
from ClassDespachante import *
import sys
import argparse

# Função principal do programa
# Declara as classes de alto nível de Despachante e Informativo,
# recebe os argumentos do usuário e executa o simulador de SO.
def main():

	# Declaração da classe utilitária de informação
	ClasseInformativo = ClassInfo()

	# Limpa a tela do terminal
	ClasseInformativo.limparTela()


	# Utiliza a lib argparse para receber argumentos do usuário.
	parser = argparse.ArgumentParser(description="Os arquivos que definem os processos " +
		 							 " devem ser informados pela linha de comando. Caso contrário" +
		 							 " os valores padrão serão utilizados."	)

	# Recebe argumento do nome do arquivo que define os atributos de processo.
	# Valor padrão caso não passado: processes.txt na pasta raiz
	parser.add_argument('-p', action='store',
                    dest='processes_input',
                    default='processes.txt',
                    help="Arquivo com atributos dos processos (Default: processes.txt)")

	# Recebe argumento do nome do arquivo que define os atributos de processo.
	# Valor padrão caso não passado: files.txt na pasta raiz
	parser.add_argument('-f', action='store',
                    dest='files_input',
                    default='files.txt',
                    help="Arquivo com atributos dos arquivos (Default: files.txt)")

	# Executa o parse de argumentos
	args = parser.parse_args()

	# Limpa a tela e exibe as informações de cabeçalho do 
	ClasseInformativo.limparTela()
	ClasseInformativo.informativoPrograma()

	# Cria uma instância da classe despachante. Essa classe declara internamente
	# todas as classes de gerenciamento do modelo
	ProcessoDespachante = ClassDespachante(args.processes_input,args.files_input)

	# Inicia o processo de simulação de SO
	ProcessoDespachante.startSO()


if __name__ == "__main__":
	main()
