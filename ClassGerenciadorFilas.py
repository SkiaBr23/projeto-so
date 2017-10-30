#encoding=utf-8

from ClassGerenciadorMemoria import *
from ClassGerenciadorRecurso import *
from ClassGerenciadorArquivo import *
import time
from threading import *
import operator

CONTADOR_RUN_USUARIO = 0
RT_STARTED = 0

class ClassGerenciadorFilas:

    def __init__(self):
        self.lista_processos = []
        self.gerenteMemoria = ClassGerenciadorMemoria()
        self.gerenteRecursos = ClassGerenciadorRecurso()
        self.gerenteArquivo = ClassGerenciadorArquivo()
        self.FILA_GLOBAL = []
        self.FILA_RT = []
        self.THREADS_RT = []
        self.FILA_USUARIO = []
        self.THREADS_USUARIO = []
        self.lockMoveFilaGlobal = RLock()
        self.lockStartProcess = RLock()

    def setListaProcessos(self,vetor_processos):
        self.lista_processos = vetor_processos

    def getListaProcessos(self):
        return self.lista_processos

    def runProcesses(self, processos):
        lista_global = processos[:]
        tempoInicio = time.time()
        while len(lista_global) > 0:
            processoTemp = lista_global[0]
            #print('Iniciando while do tempo do processo ' + str(processoTemp.getPID()))
            #print("Size lista_global: " + str(len(lista_global)))
            #print("Size processo top: " + str(len(self.getListaProcessos())))
            #print(tempoAtual)
            #@TODO Tempo de diferença está em temp_cpu+temp_inicializacao, ajustar
            while time.time() <= (tempoInicio + processoTemp.getTempoInicializacao()):
                pass
                #Eu botei isso aqui pro python nao xaropar que tem while sem nd dentro
                # xarope de indent, se alguem souber so arrumar dps
                # Resposta: usar o 'pass' para laços vazios
            #print(time.time())
            processo = lista_global.pop(0)
            #print('Processo poped ' + str(processo.getPID()))
            tempoAtual = time.time()
            #print('Processo[' + str(processo.getPID()) + '] iniciado no tempo: ' + str(tempoAtual-tempoInicio))
            #print('Passou aqui EIN ------------------------------------------------')
            if self.gerenteMemoria.verificaDisponibilidadeMemoria(processo):
                #print('IF BROADER')
                self.lockMoveFilaGlobal.acquire()
                self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'SUBTRACAO')
                #print('Valor de memoria livre: ' + str(self.gerenteMemoria.getMemoriaLivreProcessosRT()))
                self.moverParaFilaGlobal(processo)
                self.lockMoveFilaGlobal.release()
            else:
                #print('ELSE BROADER')
                print('Processo ' + str(processo.getPID()) + ' descartado por falta de memória!')
                indice = self.getListaProcessos().index(processo)
                self.getListaProcessos().pop(indice)
        #print('oloco')

        while self.isAnyThreadRTAlive():
            pass
            #Eu botei isso aqui pro python nao xaropar que tem while sem nd dentro
            # xarope de indent, se alguem souber so arrumar dps
            # Resposta: usar o 'pass' para laços vazios
        #print('Saiu na loca')

    def isAnyThreaRTdAlive(self):
        threadsAlive = False
        for threadRT in self.THREADS_RT:
            if threadRT.isAlive():
                threadsAlive = True

        return threadsAlive

    def isAnyThreadUsuarioAlive(self):
        threadsAlive = False
        for threadUsuario in self.THREADS_USUARIO:
            if threadUsuario.isAlive():
                threadsAlive = True

        return threadsAlive

    def moverParaFilaGlobal(self,processo):
        #print('Passou no append fdp')
        self.FILA_GLOBAL.append(processo)
        #print('Size fila global: ' + str(len(self.FILA_GLOBAL)))

    def moverParaFilaRT(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadRTAlive():
            #print('Lista processos maior que zero: ' + str(len(self.lista_processos) > 0))
            #print('Any Thread Alive: ' + str(self.isAnyThreadAlive()))
            #print('Meu Piru fila')
            if (len(self.FILA_GLOBAL) > 0 and self.isRTProcess()):
                #print('Passou em moverParaFilaRT')
                #GARANTIR QUE O PRIMEIRO PROCESSO NA FILA GLOBAL É RT!
                processo = self.FILA_GLOBAL.pop(0)
                #print('processo obtido tmp de inicializacao: ' + str(processo.getTempoInicializacao()))
                self.FILA_RT.append(processo)
                #print('Size fila RT apos apend fdp: ' + str(len(self.FILA_RT)))
        #print('Size lista fdp: ' + str(len(self.getListaProcessos())))
        #print('Alive: ' + str(self.isAnyThreadAlive()))
        #print('Saiu piru fila')

    def moverParaFilaUsuario(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadUsuarioAlive():
            if (len(self.FILA_GLOBAL) > 0 and self.isUsuarioProcess()):
                processo = self.FILA_GLOBAL.pop(0)
                self.FILA_USUARIO.append(processo)

    def executarProcessosFilaUsuario(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadUsuarioAlive():
            if len(self.FILA_USUARIO) > 0:
                processo = self.FILA_USUARIO.pop(0)
                processo.activateTokenCPU()
                t = Thread(target=self.executeProcessUsuario,name='ExecuteProcessUsuario'+str(processo.getPID()),args=(processo,))
                t.start()
                self.THREADS_USUARIO.appen(t)

    #Nova execute process para RTs
    def executarProcessoFilaRT(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadRTAlive():
            #print('Meu Piru run')
            if len(self.FILA_RT) > 0:
                #print('Passou em executarProcessoFilaRT')
                processo = self.FILA_RT.pop(0)
                processo.activateTokenCPU()
                RT_STARTED = True
                t = Thread(target=self.ExecuteProcessRT,name='ExecuteProcessRT'+str(processo.getPID()),args=(processo,))
                #t.daemon = True
                t.start()
                self.THREADS_RT.append(t)
            #print('Size lista fdp run: ' + str(len(self.getListaProcessos())))
            #print('Alive run: ' + str(self.isAnyThreadAlive()))
        #print('Saiu piru run')

    def isUsuarioProcess (self):
        usuarioProcess = False
        for processo in self.FILA_GLOBAL:
            if processo.getPrioridade() != 0:
                usuarioProcess = True
        return usuarioProcess

    def isRTProcess (self):
        rtProcess = False
        for processo in self.FILA_GLOBAL:
            if processo.getPrioridade() == 0:
                rtProcess = True
        return rtProcess

    def executeProcessUsuario(self, processo):
        while not processo.getTokenCPU():
            pass
        self.imprimeInicioDeExecucaoProcesso(processo)
        self.gerenteMemoria.atualizaOffsetMemoria(processo.getBlocosMemoria())
        print("process " + str(processo.getPID()))
        print("P" + str(processo.getPID()) + " STARTED")
        contadorInstruc = 1
        contadorCPU = 0
        tempoAtual = time.time()
        while contadorCPU < processo.getTempoProcessador():
            if processo.getTokenCPU() and RT_STARTED == 0:
                self.lockStartProcess.acquire()
                if time.time() > (tempoAtual+1):
                    print("P" + str(processo.getPID()) + " instruction " + str(contadorInstruc))
                    contadorCPU += 1
                    contadorInstruc += 1
                    tempoAtual = time.time()
                    CONTADOR_RUN_USUARIO += 1
                    if processo.getPrioridade() == 1:
                        if CONTADOR_RUN_USUARIO%2 == 0:
                            if hasProcessLevelTwoWaiting():
                                processo.deactivateTokenCPU()
                                updateTokenProcessesLevelTwo()
                        if CONTADOR_RUN_USUARIO%4 == 0:
                            if hasProcessLevelThreeWaiting():
                                processo.deactivateTokenCPU()
                                updateTokenProcessesLevelThree()
                        if hasProcessLevelOneWaiting():
                            processo.deactivateTokenCPU()
                            updateTokenProcessesLevelOne()
                    if processo.getPrioridade() == 2:
                        if CONTADOR_RUN_USUARIO%4 == 0:
                            if hasProcessLevelThreeWaiting():
                                processo.deactivateTokenCPU()
                        elif hasProcessLevelOneWaiting():
                            processo.deactivateTokenCPU()
                            updateTokenProcessesLevelOne()
                        elif hasProcessLevelTwoWaiting():
                            processo.deactivateTokenCPU()
                            updateTokenProcessesLevelTwo()
                    if processo.getPrioridade() > 2:
                        if hasProcessLevelOneWaiting():
                            processo.deactivateTokenCPU()
                            updateTokenProcessesLevelOne()
                        elif hasProcessLevelTwoWaiting():
                            processo.deactivateTokenCPU()
                            updateTokenProcessesLevelTwo()
                        elif hasProcessLevelThreeWaiting():
                            processo.deactivateTokenCPU()
                            updateTokenProcessesLevelThree()
                self.lockStartProcess.release()

        print("P" + str(processo.getPID()) + " return SIGINT")
        self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'ADICAO')
        indice = self.getListaProcessos().index(processo)
        self.getListaProcessos().pop(indice)

    def executeProcessRT(self, processo):
        self.imprimeInicioDeExecucaoProcesso(processo)
        self.gerenteMemoria.atualizaOffsetMemoria(processo.getBlocosMemoria())
        print("process " + str(processo.getPID()))
        print("P" + str(processo.getPID()) + " STARTED")
        contadorInstruc = 1
        contadorCPU = 0
        tempoAtual = time.time()
        self.lockStartProcess.acquire()
        while contadorCPU < processo.getTempoProcessador():
            if processo.getTokenCPU():
                if time.time() > (tempoAtual+1):
                    print("P" + str(processo.getPID()) + " instruction " + str(contadorInstruc))
                    contadorCPU += 1
                    contadorInstruc += 1
                    tempoAtual = time.time()
        print("P" + str(processo.getPID()) + " return SIGINT")
        self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'ADICAO')
        indice = self.getListaProcessos().index(processo)
        self.getListaProcessos().pop(indice)
        RT_STARTED = 0
        self.lockStartProcess.release()

    #BACKUP DE EXECUCAO
    #def executeProcess(self, processo):
        #self.lockStartProcess.acquire()
        #self.imprimeInicioDeExecucaoProcesso(processo)
        #self.gerenteMemoria.atualizaOffsetMemoria(processo.getBlocosMemoria())
        #print("process " + str(processo.getPID()))
        #print("P" + str(processo.getPID()) + " STARTED")
        #contadorInstruc = 1
        #contadorCPU = 0
        #tempoAtual = time.time()
        #while contadorCPU < processo.getTempoProcessador():
            #if time.time() > (tempoAtual+1):
                #print("P" + str(processo.getPID()) + " instruction " + str(contadorInstruc))
                #contadorCPU += 1
                #contadorInstruc += 1
                #tempoAtual = time.time()
        #print("P" + str(processo.getPID()) + " return SIGINT")
        #self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'ADICAO')
        #indice = self.getListaProcessos().index(processo)
        #self.getListaProcessos().pop(indice)
        #self.lockStartProcess.release()

    def imprimeInicioDeExecucaoProcesso(self, processo):
        print("dispatcher => ")
        print("\tPID: " + str(processo.getPID()))
        print("\toffset: " + str(self.gerenteMemoria.getOffsetMemoria()))
        print("\tblocks: " + str(processo.int_blocosDeMem))
        print("\tpriority: " + str(processo.int_prioridade))
        print("\ttime: " + str(processo.int_tempDeProcessador))
        print("\tprinters: " + str(processo.int_numReqImpressora))
        print("\tscanners: " + str(processo.int_numReqScanner))
        print("\tmodems: " + str(processo.int_numReqModem))
        print("\tdrives: " + str(processo.int_numReqDisco))
