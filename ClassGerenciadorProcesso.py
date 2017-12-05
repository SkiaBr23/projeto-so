#encoding=utf-8

#Universidade de Brasília
#Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

#Importação de classes e bibliotecas
from ClassProcesso import *
from ClassGerenciadorMemoria import *
from ClassGerenciadorRecurso import *
from ClassGerenciadorArquivo import *
from threading import *
import operator

#Classe responsável pela manipualação de objetos do tipo Processo
class ClassGerenciadorProcesso:

    #Construtor da classe
    def __init__(self):
        self.processos_RT = []
        self.processos_usuario = []
        self.gerenteMemoria = ClassGerenciadorMemoria()
        self.gerenteRecursos = ClassGerenciadorRecurso()
        self.gerenteArquivo = ClassGerenciadorArquivo()
        self.lock = Lock()

    #Método para elaborar processos oriundos da leitura do arquivo .txt
    def montaListaProcesses (self, linhasArquivoProcesses):
        vetor_auxiliar = []
        for linha in linhasArquivoProcesses:
            atri_Processo = linha.split(",")
            processo_temporario = ClassProcesso(int(atri_Processo[0]),
								int(atri_Processo[1]), int(atri_Processo[2]),
								int(atri_Processo[3]), int(atri_Processo[4]),
								int(atri_Processo[5]), int(atri_Processo[6]),
								int(atri_Processo[7]), len(vetor_auxiliar))
            if processo_temporario.getPrioridade() > 3:
                processo_temporario.setPrioridade(3)
            vetor_auxiliar.append(processo_temporario)
        return self.organizaViaTempInicializacao(vetor_auxiliar)

    #Método para organizar lista de processos com base
    #no tempo de inicialização de cada processo, em ordem crescente
    @staticmethod
    def organizaViaTempInicializacao(vetor_processos):
        vetor_processos.sort(key = operator.attrgetter('int_TempIniciacao'))
        return vetor_processos

    #Método para separar os processos da lista geral em duas listas,
    #lista de processos de usuário e lista de processos de tempo real
    def separaProcessos(self, vetor_processos):
        processos_usuario = []
        processos_tempoReal = []
        for processo in vetor_processos:
            if processo.getPrioridade() == 0:
                processos_tempoReal.append(processo)
            else:
                processos_usuario.append(processo)

        self.processos_RT = processos_tempoReal
        self.processos_usuario = processos_usuario

    #Método para obter a lista de processos de tempo real
    def getProcessosRT(self):
        return self.processos_RT

    #Método para obter a lista de processos de usuário
    def getProcessosUsuario(self):
        return self.processos_usuario
