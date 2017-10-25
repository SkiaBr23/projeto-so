#encoding=utf-8

from ClassGerenciadorMemoria import *
from ClassGerenciadorRecurso import *
from ClassGerenciadorArquivo import *
import time
from threading import *

THREADS_RT = []

class ClassGerenciadorFilas:

    def __init__(self):
        self.lista_processos = []
        self.gerenteMemoria = ClassGerenciadorMemoria()
        self.gerenteRecursos = ClassGerenciadorRecurso()
        self.gerenteArquivo = ClassGerenciadorArquivo()
        self.FILA_GLOBAL = []
        self.FILA_RT = []
        self.THREADS_RT = []
        self.lockMoveFilaGlobal = Lock()
        self.lockStartProcess = Lock()

    def setListaProcessos(self,vetor_processos):
        self.lista_processos = vetor_processos

    def getListaProcessos(self):
        return self.lista_processos

    def runProcesses(self, processos):
        lista_global = processos[:]
        while len(lista_global) > 0:
            processoTemp = lista_global[0]
            #print('DEU O POP DO CARALHO ------------------------------------------------')
            tempoAtual = time.time()
            #print("Size lista_global: " + str(len(lista_global)))
            #print("Size processo top: " + str(len(self.getListaProcessos())))
            #print(tempoAtual)
            #@TODO Tempo de diferença está em temp_cpu+temp_inicializacao, ajustar
            while time.time() <= (tempoAtual + processoTemp.getTempoInicializacao()):
                pass
                #Eu botei isso aqui pro python nao xaropar que tem while sem nd dentro
                # xarope de indent, se alguem souber so arrumar dps
                # Resposta: usar o 'pass' para laços vazios
            #print(time.time())
            processo = lista_global.pop(0)
            #print('Passou aqui EIN ------------------------------------------------')
            if self.gerenteMemoria.verificaDisponibilidadeMemoria(processo):
                #print('IF BROADER')
                self.lockMoveFilaGlobal.acquire()
                self.moverParaFilaGlobal(processo)
                self.lockMoveFilaGlobal.release()
            else:
                #print('ELSE BROADER')
                print('Processo ' + str(processo.getPID()) + ' descartado por falta de memória!')

        while self.isAnyThreadAlive():
            pass
            #Eu botei isso aqui pro python nao xaropar que tem while sem nd dentro
            # xarope de indent, se alguem souber so arrumar dps
            # Resposta: usar o 'pass' para laços vazios


    @staticmethod
    def isAnyThreadAlive():
        threadsAlive = False
        for threadRT in THREADS_RT:
            if threadRT.isAlive():
                threadsAlive = True

        return threadsAlive

    def moverParaFilaGlobal(self,processo):
        #print('Passou no append fdp')
        self.FILA_GLOBAL.append(processo)
        #print('Size fila global: ' + str(len(self.FILA_GLOBAL)))

    def moverParaFilaRT(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadAlive():
            #print('Lista processos maior que zero: ' + str(len(self.lista_processos) > 0))
            #print('Any Thread Alive: ' + str(self.isAnyThreadAlive()))
            #print('Meu Piru fila')
            if len(self.FILA_GLOBAL) > 0:
                #print('Passou em moverParaFilaRT')
                processo = self.FILA_GLOBAL.pop(0)
                #print('processo obtido tmp de inicializacao: ' + str(processo.getTempoInicializacao()))
                self.FILA_RT.append(processo)
                #print('Size fila RT apos apend fdp: ' + str(len(self.FILA_RT)))
        #print('Size lista fdp: ' + str(len(self.getListaProcessos())))
        #print('Alive: ' + str(self.isAnyThreadAlive()))
        #print('Saiu piru fila')

    #Nova execute process para RTs
    def executarProcessoFilaRT(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadAlive():
            #print('Meu Piru run')
            if len(self.FILA_RT) > 0:
                #print('Passou em executarProcessoFilaRT')
                self.lockStartProcess.acquire()
                processo = self.FILA_RT.pop(0)
                t = Thread(target=self.executeProcess,args=(processo,))
                t.start()
                self.THREADS_RT.append(t)
        #print('Size lista fdp run: ' + str(len(self.getListaProcessos())))
        #print('Alive run: ' + str(self.isAnyThreadAlive()))
        #print('Saiu piru run')

    #Novo RunProcesses
    def runProcesses_OLD(self,processos):
        lista_global = processos
        while len(lista_global) > 0:
            processo = lista_global.pop(0)
            AVANCAR = True
            tempoAtual = time.time()
            while AVANCAR:
                #Tempo de diferença está em temp_cpu+temp_inicializacao, ajustar
                if (time.time() >= tempoAtual + processo.int_TempIniciacao) or processo.getAposTempInicializacao() == 1:
                    if self.gerenteMemoria.verificaDisponibilidadeMemoria(processo) and self.gerenteRecursos.verificaDisponibilidadeRecursos(processo):
                        #Mover para uma fila de prontos, ao inves de executar, AJUSTAR
                        t = Thread(target=self.executeProcess,args=(processo,))
                        t.start()
                        AVANCAR = False
                    else:
                        processo.setAposTempInicializacao()
                        lista_global.append(processo)
                        AVANCAR = False

    def executeProcess(self, processo):
        self.imprimeInicioDeExecucaoProcesso(processo)
        self.gerenteMemoria.atualizaOffsetMemoria(processo.getBlocosMemoria())
        print("process " + str(processo.getPID()))
        print("P" + str(processo.getPID()) + " STARTED")
        contadorInstruc = 1
        contadorCPU = 0
        tempoAtual = time.time()
        while contadorCPU < processo.getTempoProcessador():
            if time.time() > (tempoAtual+1):
                print("P" + str(processo.getPID()) + " instruction " + str(contadorInstruc))
                contadorCPU += 1
                contadorInstruc += 1
                tempoAtual = time.time()
        print("P" + str(processo.getPID()) + " return SIGINT")
        indice = self.getListaProcessos().index(processo)
        self.getListaProcessos().pop(indice)
        self.lockStartProcess.release()

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
