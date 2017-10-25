#encoding=utf-8

from ClassProcesso import *
from ClassGerenciadorMemoria import *
from ClassGerenciadorRecurso import *
from ClassGerenciadorArquivo import *
import time
from threading import *

class ClassGerenciadorProcesso:

    def __init__(self):
        self.processos_all = []
        self.processos_RT = []
        self.processos_usuario = []
        self.gerenteMemoria = ClassGerenciadorMemoria()
        self.gerenteRecursos = ClassGerenciadorRecurso()
        self.gerenteArquivo = ClassGerenciadorArquivo()
        self.lock = Lock()

    def montaFilaProcesses (self, linhasArquivoProcesses):
        vetor_auxiliar = []
        for linha in linhasArquivoProcesses:
            atri_Processo = linha.split(",")
            processo_temporario = ClassProcesso(int(atri_Processo[0]),
								int(atri_Processo[1]), int(atri_Processo[2]),
								int(atri_Processo[3]), int(atri_Processo[4]),
								int(atri_Processo[5]), int(atri_Processo[6]),
								int(atri_Processo[7]), len(vetor_auxiliar))
            vetor_auxiliar.append(processo_temporario)
        self.processos_all = vetor_auxiliar

    def separaProcessos(self, vetor_processos):
        processos_usuario = []
        processos_tempoReal = []
        for processo in vetor_processos:
            if(processo.getPrioridade() == 0):
                processos_tempoReal.append(processo)
            else:
                processos_usuario.append(processo)

        self.processos_RT = processos_tempoReal
        self.processos_usuario = processos_usuario

    def runProcesses (self,processos):
        for processo in processos:
            AVANCAR = True
            tempoAtual = time.time()
            while (AVANCAR):
                #Tempo de diferença está em temp_cpu+temp_inicializacao, ajustar
                if (time.time() >= tempoAtual + processo.int_TempIniciacao):
                    t = Thread(target=self.executeProcess,args=(processo,))
                    t.start()
                    AVANCAR = False

    def executeProcess(self, processo):
        if (self.gerenteMemoria.verificaDisponibilidadeMemoria(processo) and self.gerenteRecursos.verificaDisponibilidadeRecursos(processo)):
            self.lock.acquire()
            #self.gerenteArquivo.manipulaArquivo(processo.getPID(), vetor_arquivos_processos, vetor_arquivos_disco, posicoesDisco)
            self.imprimeInicioDeExecucaoProcesso(processo)
            print("process " + str(processo.int_PID))
            print("P" + str(processo.int_PID) + " STARTED")
            contadorInstruc = 1
            contadorCPU = 0
            tempoAtual = time.time()
            while (contadorCPU < processo.int_tempDeProcessador):
                if (time.time() > (tempoAtual+1)):
                    print("P" + str(processo.int_PID) + " instruction " + str(contadorInstruc))
                    contadorCPU += 1
                    contadorInstruc += 1
                    tempoAtual = time.time()
            print("P" + str(processo.int_PID) + " return SIGINT")
            self.lock.release()

    def imprimeInicioDeExecucaoProcesso(self, processo):
        print("dispatcher => ")
        print("\tPID: " + str(processo.int_PID))
        print("\toffset: " + str(self.gerenteMemoria.getOffsetMemoria()))
        print("\tblocks: " + str(processo.int_blocosDeMem))
        print("\tpriority: " + str(processo.int_prioridade))
        print("\ttime: " + str(processo.int_tempDeProcessador))
        print("\tprinters: " + str(processo.int_numReqImpressora))
        print("\tscanners: " + str(processo.int_numReqScanner))
        print("\tmodems: " + str(processo.int_numReqModem))
        print("\tdrives: " + str(processo.int_numReqDisco))
        self.gerenteMemoria.atualizaOffsetMemoria(processo.int_blocosDeMem)

    def getProcessos(self):
        return self.processos_all

    def getProcessosRT(self):
        return self.processos_RT

    def getProcessosUsuario(self):
        return self.processos_usuario