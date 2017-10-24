#encoding=utf-8

from ClassGerenciadorMemoria import *
from ClassGerenciadorRecurso import *
from ClassGerenciadorArquivo import *
import time
from threading import *

class ClassGerenciadorFilas:

    def __init__(self):
        self.lista_processos = []
        self.fila_global_prontos = []
        self.fila_processosrt_prontos = []
        self.fila_processosusuario_prontos = []
        self.gerenteMemoria = ClassGerenciadorMemoria()
        self.gerenteRecursos = ClassGerenciadorRecurso()
        self.gerenteArquivo = ClassGerenciadorArquivo()
        self.lock = Lock()

    def setListaProcessos(self,vetor_processos):
        self.lista_processos = vetor_processos

    def getListaProcessos(self):
        return self.lista_processos


    #Novo RunProcesses
    def runProcesses(self,processos):
        lista_global = processos
        while (len(lista_global) > 0):
            processo = lista_global.pop(0)
            AVANCAR = True
            tempoAtual = time.time()
            while (AVANCAR):
                #Tempo de diferença está em temp_cpu+temp_inicializacao, ajustar
                if ((time.time() >= tempoAtual + processo.int_TempIniciacao) or processo.getAposTempInicializacao() == 1):
                    if (self.gerenteMemoria.verificaDisponibilidadeMemoria(processo) and self.gerenteRecursos.verificaDisponibilidadeRecursos(processo)):
                        #Mover para uma fila de prontos, ao inves de executar, AJUSTAR
                        t = Thread(target=self.executeProcess,args=(processo,))
                        t.start()
                        AVANCAR = False
                    else:
                        processo.setAposTempInicializacao()
                        lista_global.append(processo)
                        AVANCAR = False

    def executeProcess(self, processo):
        self.lock.acquire()
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
