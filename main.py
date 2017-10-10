# Para executar o programa:
#	python3 teste1.py


from ClassProcesso import *
from ClassInfo import *

def main():

	#Limpeza de terminal e exibição de informações do projeto
	ClasseInformativo = ClassInfo()
	ClasseInformativo.limparTela()
	ClasseInformativo.informativoPrograma()

	#Criação das listas de processos e linhas do arquivo .txt de entrada
	linhasArquivo = []
	vetor_processos = []

	#Leitura das linhas do arquivo .txt de entrada com os processos
	linhasArquivo = lendoArquivoProcesses()

	vetor_processos = montaProcesses(linhasArquivo)

	imprimeProcessos(vetor_processos)




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
def lendoArquivoProcesses():

	linhasArquivo = []

	with open ("processes.txt") as arquivo:

		for line in arquivo:
			line = line.rstrip("\n")	# Remocao do "\n" no final de linha
			if line:
				linhasArquivo.append(line)

	arquivo.close()

	return(linhasArquivo)


def envelhecimento(fila_processos):

	for processo in fila_processos:
		processo.int_prioridade = processo.int_prioridade - 1

	return fila_processos


def montaProcesses (linhasArquivoProcesses):

	vetor_auxiliar = []

	for linha in linhasArquivoProcesses:
		atri_Processo = linha.split(",")

		processo_temporario = ClassProcesso(int(atri_Processo[0]),
							int(atri_Processo[1]), int(atri_Processo[2]),
							int(atri_Processo[3]), int(atri_Processo[4]),
							int(atri_Processo[5]), int(atri_Processo[6]),
							int(atri_Processo[7]))


		vetor_auxiliar.append(processo_temporario)

	return vetor_auxiliar


def imprimeProcessos(vetorProcessos):
	for processo in vetorProcessos:
		processo.imprimirValoresProcesso()
		print("-----------------------------------------------")


if __name__ == "__main__":
	main()