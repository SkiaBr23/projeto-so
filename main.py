# Para executar o programa:
#	python3 teste1.py


from ClassProcesso import *
from ClassInfo import *

def main():

	ClasseInformativo = ClassInfo()
	ClasseInformativo.limparTela()
	ClasseInformativo.informativoPrograma()

	linhasArquivo = []
	vetor_processos = []

	linhasArquivo = lendoArquivoProcesses()


	for linha in linhasArquivo:
		atri_Processo = linha.split(",")
		print(atri_Processo)

		processo_temporario = ClassProcesso(int(atri_Processo[0]),
							int(atri_Processo[1]), int(atri_Processo[2]),
							int(atri_Processo[3]), int(atri_Processo[4]),
							int(atri_Processo[5]), int(atri_Processo[6]),
							int(atri_Processo[7]))


		vetor_processos.append(processo_temporario)

	vetor_processos[0].imprimirValoresProcesso()
	print("-----------------------------------------------")
	vetor_processos[1].imprimirValoresProcesso()




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



if __name__ == "__main__":
	main()



