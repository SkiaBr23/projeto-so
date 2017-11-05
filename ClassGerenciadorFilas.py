#encoding=utf-8

from ClassGerenciadorMemoria import *
from ClassGerenciadorRecurso import *
from ClassGerenciadorArquivo import *
import time
from threading import *
import operator

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
        self.lockMoveFilaGlobal = Lock()
        self.lockStartProcess = Lock()
        self.USER_STARTED = 0
        self.CONTADOR_RUN_USUARIO = 0
        self.RT_STARTED = 0
        self.USER_PROCESSES_RUNNING = []

    def setListaProcessos(self,vetor_processos):
        self.lista_processos = vetor_processos

    def getListaProcessos(self):
        return self.lista_processos

    def runProcesses(self, processos):
        lista_global = processos[:]
        tempoInicio = time.time()
        AVANCAR = False
        while len(lista_global) > 0:
            processoTemp = lista_global[0]
            #print('Iniciando while do tempo do processo ' + str(processoTemp.getPID()))
            #print("Size lista_global: " + str(len(lista_global)))
            #print("Size processo top: " + str(len(self.getListaProcessos())))
            #print(tempoAtual)
            #@TODO Tempo de diferença está em temp_cpu+temp_inicializacao, ajustar
            while time.time() <= (tempoInicio + processoTemp.getTempoInicializacao()) and processoTemp.getAposTempInicializacao() == 0:
                AVANCAR = True
                break
                #Eu botei isso aqui pro python nao xaropar que tem while sem nd dentro
                # xarope de indent, se alguem souber so arrumar dps
                # Resposta: usar o 'pass' para laços vazios
            #print(time.time())
            if AVANCAR:
                AVANCAR = False
                processo = lista_global.pop(0)
                lista_global.append(processo)
                continue
            processo = lista_global.pop(0)
            #print('Processo poped ' + str(processo.getPID()))
            #tempoAtual = time.time()
            #print('Processo[' + str(processo.getPID()) + '] iniciado no tempo: ' + str(tempoAtual-tempoInicio))
            #print('Passou aqui EIN ------------------------------------------------')
            if self.gerenteMemoria.verificaRequisicaoMemoria(processo):
                processo.setAposTempInicializacao()
                if self.gerenteMemoria.verificaDisponibilidadeMemoria(processo):
                    #print('IF BROADER')
                    self.lockMoveFilaGlobal.acquire()
                    if processo.getPrioridade() == 0:
                        self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'SUBTRACAO')
                    else:
                        self.gerenteMemoria.atualizaMemoriaProcessosUsuario(processo.getBlocosMemoria(),'SUBTRACAO')
                    #print('Valor de memoria livre: ' + str(self.gerenteMemoria.getMemoriaLivreProcessosRT()))
                    self.moverParaFilaGlobal(processo)
                    self.lockMoveFilaGlobal.release()
                else:
                    #print('ELSE BROADER')
                    lista_global.append(processo)

            else:
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
        while self.isAnyThreadUsuarioAlive():
            pass

    def isAnyThreadRTAlive(self):
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
                if self.USER_STARTED == 0:
                    processo.activateTokenCPU()
                    self.USER_STARTED = 1
                self.USER_PROCESSES_RUNNING.append(processo)
                indice = self.USER_PROCESSES_RUNNING.index(processo)
                t = Thread(target=self.executeProcessUsuario,name='ExecuteProcessUsuario'+str(processo.getPID()),args=(self.USER_PROCESSES_RUNNING[indice],))
                t.start()
                self.THREADS_USUARIO.append(t)

    #Nova execute process para RTs
    def executarProcessoFilaRT(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadRTAlive():
            #print('Meu Piru run')
            if len(self.FILA_RT) > 0:
                #print('Passou em executarProcessoFilaRT')
                processo = self.FILA_RT.pop(0)
                self.deactivateUserProcesses()
                processo.activateTokenCPU()
                t = Thread(target=self.executeProcessRT,name='ExecuteProcessRT'+str(processo.getPID()),args=(processo,))
                #t.daemon = True
                t.start()
                self.THREADS_RT.append(t)
            #print('Size lista fdp run: ' + str(len(self.getListaProcessos())))
            #print('Alive run: ' + str(self.isAnyThreadAlive()))
        #print('Saiu piru run')

    def deactivateUserProcesses(self):
        for processo in self.USER_PROCESSES_RUNNING:
            processo.deactivateTokenCPU()

    def isUsuarioProcess (self):
        usuarioProcess = False
        if len(self.FILA_GLOBAL) > 0:
            if self.FILA_GLOBAL[0].getPrioridade() != 0:
                usuarioProcess = True
        return usuarioProcess

    def isRTProcess (self):
        rtProcess = False
        if len(self.FILA_GLOBAL) > 0:
            if self.FILA_GLOBAL[0].getPrioridade() == 0:
                rtProcess = True
        return rtProcess

    def hasProcessWaiting(self, processo, prioridade):
        indice = self.USER_PROCESSES_RUNNING.index(processo)
        if indice < (len(self.USER_PROCESSES_RUNNING)-1):
            for i in range(indice+1, len(self.USER_PROCESSES_RUNNING)):
                if not self.USER_PROCESSES_RUNNING[i].getTokenCPU() and self.USER_PROCESSES_RUNNING[i].getPrioridade() == prioridade:
                    return (True,i)
        for i in range(0,indice):
            if not self.USER_PROCESSES_RUNNING[i].getTokenCPU() and self.USER_PROCESSES_RUNNING[i].getPrioridade() == prioridade:
                return (True,i)
        return (False,None)

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
            if processo.getTokenCPU() and self.RT_STARTED == 0:
                #print("antes do acquire")
                #print("passooou ")
                if time.time() > (tempoAtual+1):
                    self.lockStartProcess.acquire()
                    print("P" + str(processo.getPID()) + " instruction " + str(contadorInstruc))
                    contadorCPU += 1
                    contadorInstruc += 1
                    tempoAtual = time.time()
                    self.CONTADOR_RUN_USUARIO += 1
                    self.lockStartProcess.release()
                    if processo.getPrioridade() == 1:
                        if self.CONTADOR_RUN_USUARIO%3 == 0:
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,2)
                            if boolean:
                                #print("Caiu aqui 1")
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                        if self.CONTADOR_RUN_USUARIO%4 == 0:
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                            if boolean:
                                #print("Caiu aqui 2")
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,1)
                        if boolean:
                            #print("Caiu aqui 3")
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        #Contadores ainda nao bateram, nao ha mais processo 1 esperando,
                        #porem tem de dois ou 3 esperando
                        elif not boolean and contadorCPU == processo.getTempoProcessador():
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,2)
                            if boolean:
                                #print("Caiu aqui 1")
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                            if boolean:
                                #print("Caiu aqui 1")
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                    if processo.getPrioridade() == 2:
                        if self.CONTADOR_RUN_USUARIO%4 == 0:
                            #Verifica processos de prioridade 3 ou mais (menos prioritarios)
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                            if boolean:
                                #print("Caiu aqui 4")
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                        #Verifica se tem algum de nivel 1 esperando
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,1)
                        if boolean:
                            #print("Caiu aqui 5")
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        #Verifica se tem algum de nivel 2 esperando
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,2)
                        if boolean:
                            #print("Caiu aqui 6")
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        #Adicionado este, pq verifica se tem alguem de prioridade 3 esperando,
                        #caso nao haja mais prioridade 1 ou 2 e o contador nao esteja no valor correto
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                        if boolean:
                            #print("Caiu aqui 1")
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                    if processo.getPrioridade() == 3:
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,1)
                        if boolean:
                            #print("Caiu aqui 7")
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,2)
                        if boolean:
                            #print("Caiu aqui 8")
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                        if boolean:
                            #print("Caiu aqui 9")
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue

        print("P" + str(processo.getPID()) + " return SIGINT")
        self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'ADICAO')
        indice = self.getListaProcessos().index(processo)
        self.getListaProcessos().pop(indice)

    def executeProcessRT(self, processo):
        self.RT_STARTED = True
        self.lockStartProcess.acquire()
        self.imprimeInicioDeExecucaoProcesso(processo)
        self.gerenteMemoria.atualizaOffsetMemoria(processo.getBlocosMemoria())
        print("process " + str(processo.getPID()))
        print("P" + str(processo.getPID()) + " STARTED")
        contadorInstruc = 1
        contadorCPU = 0
        tempoAtual = time.time()
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
        self.RT_STARTED = 0
        self.lockStartProcess.release()
        self.activateFirstUserProcess()

    def activateFirstUserProcess(self):
        for processo in self.USER_PROCESSES_RUNNING:
            if processo.getPrioridade() > 0 and processo.getTokenCPU() == False:
                processo.activateTokenCPU()
                return

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
