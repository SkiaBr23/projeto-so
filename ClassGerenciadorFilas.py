#encoding=utf-8

#Universidade de Brasília
#Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

#Importação de classes e bibliotecas
from ClassGerenciadorMemoria import *
from ClassGerenciadorRecurso import *
from ClassGerenciadorArquivo import *
import time
from threading import *
import operator

#Classe para gerenciar as filas de processos e sua execução
class ClassGerenciadorFilas:

    #Construtor da classe
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
        self.RT_PROCESSES_RUNNING = []

    #Método para setar a lista de processos global
    def setListaProcessos(self,vetor_processos):
        self.lista_processos = vetor_processos

    #Método para obter a lista de processos global
    def getListaProcessos(self):
        return self.lista_processos

    #Método que realiza a montagem das filas, analisando recursos e memória
    def runProcesses(self, processos):
        lista_global = processos[:]
        tempoInicio = time.time()
        AVANCAR = False
        #Laço de repetição que executa enquanto houverem processos a serem
        #processados
        while len(lista_global) > 0:
            #Obtenção do primeiro processo da lista global
            processoTemp = lista_global[0]
            #Aguarda chegada do tempo de inicialização deste processo,verificando
            #se o tempo dele já passou e ele só foi escalonado pro fim da fila
            while time.time() <= (tempoInicio + processoTemp.getTempoInicializacao()) and processoTemp.getAposTempInicializacao() == 0:
                #Flag para sinalizar que o tempo de inicialização do processo
                #ja passou, e ele já foi escalonado pro fim da lista
                AVANCAR = True
                break
            #Movimentação do processo para o fim da lista
            if AVANCAR:
                AVANCAR = False
                processo = lista_global.pop(0)
                lista_global.append(processo)
                continue
            #Obtenção do processo
            processo = lista_global.pop(0)
            #Estrutura condicional que verifica se há memória suficiente
            #para esse processo ser executado
            if self.gerenteMemoria.verificaRequisicaoMemoria(processo):
                processo.setAposTempInicializacao()
                #Verifica se existem recursos para esse processo, caso seja
                #um processo de usuario
                if self.gerenteMemoria.verificaDisponibilidadeMemoria(processo):
                    #Estrutura condicional que verifica se o processo é um
                    #processo de tempo real
                    if processo.getPrioridade() == 0:
                        #Se for, ativa o objeto Lock, atualiza a memória livre,
                        #e move o processo para a fila global
                        self.lockMoveFilaGlobal.acquire()
                        self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'SUBTRACAO')
                        self.moverParaFilaGlobal(processo)
                        self.lockMoveFilaGlobal.release()

                    elif self.gerenteRecursos.verificaDisponibilidadeRecursos(processo):
                        #Se for de usuario, ativa o objeto Lock, atualiza a
                        #memória livre e move o processo para a fila global
                        self.lockMoveFilaGlobal.acquire()
                        self.gerenteMemoria.atualizaMemoriaProcessosUsuario(processo.getBlocosMemoria(),'SUBTRACAO')
                        self.moverParaFilaGlobal(processo)
                        self.lockMoveFilaGlobal.release()

                    else:
                        #Caso não haja o recurso, o processo irá aguardar
                        if not processo.getEsperaRecurso():
                            processo.setEsperaRecurso(True);
                            print('Processo ' + str(processo.getPID()) + ' em espera por falta de recurso')
                        lista_global.append(processo)

                else:
                    #Caso nao haja memoria no momento, processo irá aguardar
                    lista_global.append(processo)

            else:
                #Caso a requisição de memória seja maior do que o possivel,
                #descarta o processo e informa em tela
                self.descartaProcesso(processo,'falta de memória')

        #Laço de repetição que aguarda o fim das threads de tempo real,
        #e o esvaziamento da lista global de processos
        while self.isAnyThreadRTAlive() or len(self.getListaProcessos()) > 0:
            pass

        #Laço de repetição que aguarda o fim das threads de usuario,
        #e o esvaziamento da lista global de processos
        while self.isAnyThreadUsuarioAlive() or len(self.getListaProcessos()) > 0:
            pass

    #Método para informar que um processo está sendo descartado da execução
    #por falta de memória, recurso ou outra exceção
    def descartaProcesso(self,processo,mensagem):
        print('Processo ' + str(processo.getPID()) + ' descartado por: '+ mensagem + '!')
        indice = self.getListaProcessos().index(processo)
        self.getListaProcessos().pop(indice)

    #Método para verificar se existe alguma thread com processo de tempo real
    #em execução
    def isAnyThreadRTAlive(self):
        threadsAlive = False
        for threadRT in self.THREADS_RT:
            if threadRT.isAlive():
                threadsAlive = True

        return threadsAlive

    #Método para verificar se existe alguma thread com processo de usuário
    #em execução
    def isAnyThreadUsuarioAlive(self):
        threadsAlive = False
        for threadUsuario in self.THREADS_USUARIO:
            if threadUsuario.isAlive():
                threadsAlive = True

        return threadsAlive

    #Método para mover um processo da lista inicial para a fila global
    def moverParaFilaGlobal(self,processo):
        self.FILA_GLOBAL.append(processo)

    #Método para mover um processo de tempo real da fila global para
    #a fila de processos de tempo real
    #Esse método é executado em uma thread, que permanece ativa enquanto
    #houver processo na lista global ou caso existam threads de tempo real
    #ativas
    #O objeto Lock foi utilizado para impedir acessos concorrentes na fila
    #global, impedindo condições de corrida
    def moverParaFilaRT(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadRTAlive():
            self.lockMoveFilaGlobal.acquire()
            if (len(self.FILA_GLOBAL) > 0 and self.isRTProcess()):
                processo = self.FILA_GLOBAL.pop(0)
                self.FILA_RT.append(processo)
            self.lockMoveFilaGlobal.release()

    #Método para mover um processo de usuario da fila global para
    #a fila de processos de usuario
    #Esse método é executado em uma thread, que permanece ativa enquanto
    #houver processo na lista global ou caso existam threads de usuario
    #ativas
    #O objeto Lock foi utilizado para impedir acessos concorrentes na fila
    #global, impedindo condições de corrida
    def moverParaFilaUsuario(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadUsuarioAlive():
            self.lockMoveFilaGlobal.acquire()
            if (len(self.FILA_GLOBAL) > 0 and self.isUsuarioProcess()):
                processo = self.FILA_GLOBAL.pop(0)
                self.FILA_USUARIO.append(processo)
            self.lockMoveFilaGlobal.release()

    #Método para realizar a inicialização de uma thread que irá executar
    #um processo de usuário
    #Esse método é executado por uma thread enquanto houver processos na lista
    #global ou caso exista alguma thread de usuario ativa
    def executarProcessosFilaUsuario(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadUsuarioAlive():
            if len(self.FILA_USUARIO) > 0:
                processo = self.FILA_USUARIO.pop(0)
                #Estrutura condicional que seta o token de 'utilização da CPU'
                #para o processo quando não há nenhum outro em execução
                if not self.isAnyThreadUsuarioAlive() and not self.isAnyThreadRTAlive():
                    processo.activateTokenCPU()

                #Adição do processo a ser executado na lista de processos de
                #usuario em execução
                self.USER_PROCESSES_RUNNING.append(processo)
                indice = self.USER_PROCESSES_RUNNING.index(processo)
                #Chamada da thread
                t = Thread(target=self.executeProcessUsuario,name='ExecuteProcessUsuario'+str(processo.getPID()),args=(self.USER_PROCESSES_RUNNING[indice],))
                t.start()
                #Adição da thread na lista de threads de usuario
                self.THREADS_USUARIO.append(t)

    #Método para realizar a inicialização de uma thread que irá executar
    #um processo de tempo real
    #Esse método é executado por uma thread enquanto houver processos na lista
    #global ou caso exista alguma thread de tempo real ativa
    def executarProcessoFilaRT(self):
        while len(self.lista_processos) > 0 or self.isAnyThreadRTAlive():
            if len(self.FILA_RT) > 0:
                processo = self.FILA_RT.pop(0)
                #Desativação do token de 'utilização de CPU' para os processos
                #de usuário, pois os processos de tempo real tem prioridade
                #máxima e não são preemptiveis
                self.deactivateUserProcesses()
                #Ativação do token de 'utilização' para esse processo de tempo real
                processo.activateTokenCPU()
                self.RT_PROCESSES_RUNNING.append(processo)
                #Chamada da thread
                t = Thread(target=self.executeProcessRT,name='ExecuteProcessRT'+str(processo.getPID()),args=(processo,))
                t.start()
                #Adição da thread na lista de threads de usuario
                self.THREADS_RT.append(t)

    #Método para desativar o token de 'utilização de CPU' para todos os
    #processos de usuario
    def deactivateUserProcesses(self):
        for processo in self.USER_PROCESSES_RUNNING:
            processo.deactivateTokenCPU()

    #Método que verifica se o processo no inicio da fila global é um processo
    #de usuario
    def isUsuarioProcess (self):
        usuarioProcess = False
        if len(self.FILA_GLOBAL) > 0:
            if self.FILA_GLOBAL[0].getPrioridade() != 0:
                usuarioProcess = True
        return usuarioProcess

    #Método que verifica se o processo no inicio da fila global é um processo
    #de tempo real
    def isRTProcess (self):
        rtProcess = False
        if len(self.FILA_GLOBAL) > 0:
            if self.FILA_GLOBAL[0].getPrioridade() == 0:
                rtProcess = True
        return rtProcess

    #Método que verifica se existe algum processo de usuário de prioridade X
    #aguardando para ser executado (escalonado)
    def hasProcessWaiting(self, processo, prioridade):
        #Obtenção do índice do processo na lista de processos de usuario
        #em execução
        indice = self.USER_PROCESSES_RUNNING.index(processo)
        if indice < (len(self.USER_PROCESSES_RUNNING)-1):
            #Laço de repetição para varrer a lista, da posição desse processo
            #até o fim da lista, buscando processos que não estejam executando
            #e que tenham a prioridade em analise
            for i in range(indice+1, len(self.USER_PROCESSES_RUNNING)):
                if not self.USER_PROCESSES_RUNNING[i].getTokenCPU() and self.USER_PROCESSES_RUNNING[i].getPrioridade() == prioridade:
                    #Se encontrar, retorna o indice desse processo na lista
                    #bem como o proprio processo
                    return (True,i)
        #Laço de repetição para varrer a lista, do inicio até a posição desse
        #processo, buscando processos que não estejam executando
        #e que tenham a prioridade em analise
        for i in range(0,indice):
            if not self.USER_PROCESSES_RUNNING[i].getTokenCPU() and self.USER_PROCESSES_RUNNING[i].getPrioridade() == prioridade:
                #Se encontrar, retorna o indice desse processo na lista
                #bem como o proprio processo
                return (True,i)
        return (False,None)

    #Método que realiza a execução propriamente dita do processo de usuario
    def executeProcessUsuario(self, processo):
        #Laço de repetição que bloqueia a execução do processo de usuário
        #enquanto o token de 'utilização de CPU' estiver bloqueado
        while not processo.getTokenCPU():
            pass
        #Impressao de informações do processo
        self.imprimeInicioDeExecucaoProcesso(processo)
        #Atualização do offset de memória a ser impresso
        self.gerenteMemoria.atualizaOffsetMemoria(processo.getBlocosMemoria())
        print("process " + str(processo.getPID()))
        print("P" + str(processo.getPID()) + " STARTED")
        contadorInstruc = 1
        contadorCPU = 0
        tempoAtual = time.time()
        #Laço de repetição para executar o processo de tempo real durante o
        #tempo de execução do mesmo
        while contadorCPU < processo.getTempoProcessador():
            #Estrutura condicional que verifica se o processo de usuário está
            #com o token de 'utilização da CPU' e se não existem processos de
            #tempo real em execução
            if processo.getTokenCPU() and self.RT_STARTED == 0:
                if time.time() > (tempoAtual+1):
                    #Ativação do objeto Lock para impedir outro processo de
                    #usuário a executar
                    self.lockStartProcess.acquire()
                    #Impressão de 'instrução' do processo
                    print("P" + str(processo.getPID()) + " instruction " + str(contadorInstruc))
                    contadorCPU += 1
                    contadorInstruc += 1
                    tempoAtual = time.time()
                    #Incremento do contador de instruções de processos de usuario
                    self.CONTADOR_RUN_USUARIO += 1
                    #Liberação do objeto Lock
                    self.lockStartProcess.release()
                    #Estrutura condicional que avalia se o processo em execução
                    #é um processo de prioridade 1
                    if processo.getPrioridade() == 1:
                        #Se for, verifica se o contador de instruções global de
                        #processos de usuário é divisível por 3
                        if self.CONTADOR_RUN_USUARIO%3 == 0:
                            #Se for, verifica se existe algum processo de
                            #prioridade nível 2 aguardando por executar
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,2)
                            if boolean:
                                #Se houver, desativa o token de 'utilização da CPU'
                                #para o processo atual e passa esse token para
                                #o processo de prioridade 2 verificado
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                        #Estrutura condicional que verifica se o contador de
                        #instruções global de processos de usuário é divisível por 4
                        if self.CONTADOR_RUN_USUARIO%4 == 0:
                            #Se for, verifica se existe algum processo de
                            #prioridade nível 3 aguardando por executar
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                            if boolean:
                                #Se houver, desativa o token de 'utilização da CPU'
                                #para o processo atual e passa esse token para
                                #o processo de prioridade 3 verificado
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                        #Caso não haja nenhum processo de prioridade 2 ou 3
                        #aguardando, busca-se por outro processo de prioridade 1
                        #que esteja aguardando
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,1)
                        if boolean:
                            #Se houver, desativa o token de 'utilização da CPU'
                            #para o processo atual e passa esse token para
                            #o processo de prioridade 1 verificado
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        #Contadores ainda nao bateram, nao ha mais processo 1 esperando,
                        #porem tem de dois ou 3 esperando
                        elif not boolean and contadorCPU == processo.getTempoProcessador():
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,2)
                            if boolean:
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                            if boolean:
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                    #Estrutura condicional que avalia se o processo em execução
                    #é um processo de prioridade 2
                    if processo.getPrioridade() == 2:
                        #Estrutura condicional que verifica se o contador de
                        #instruções global de processos de usuário é divisível por 4
                        if self.CONTADOR_RUN_USUARIO%4 == 0:
                            #Verifica se existem processos de prioridade 3
                            #aguardando por execução
                            boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                            if boolean:
                                #Se houver, desativa o token de 'utilização da CPU'
                                #para o processo atual e passa esse token para
                                #o processo de prioridade 3 verificado
                                if (contadorCPU != processo.getTempoProcessador()):
                                    processo.deactivateTokenCPU()
                                self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                                continue
                        #Verifica se tem algum de nivel 1 esperando
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,1)
                        if boolean:
                            #Se houver, desativa o token de 'utilização da CPU'
                            #para o processo atual e passa esse token para
                            #o processo de prioridade 1 verificado
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        #Verifica se tem algum de nivel 2 esperando
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,2)
                        if boolean:
                            #Se houver, desativa o token de 'utilização da CPU'
                            #para o processo atual e passa esse token para
                            #o processo de prioridade 2 verificado
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        #Estrutura condicional que verifica se tem algum processo
                        #de prioridade 3 esperando, caso nao haja mais prioridade 1
                        #ou 2 e o contador nao esteja no valor correto
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                        if boolean:
                            #Se houver, desativa o token de 'utilização da CPU'
                            #para o processo atual e passa esse token para
                            #o processo de prioridade 3 verificado
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                    #Estrutura condicional que avalia se o processo em execução
                    #é um processo de prioridade 3
                    if processo.getPrioridade() == 3:
                        #Verifica-se se existe algum processo de prioridade 1
                        #aguardando para executar
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,1)
                        if boolean:
                            #Se houver, desativa o token de 'utilização da CPU'
                            #para o processo atual e passa esse token para
                            #o processo de prioridade 1 verificado
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        #Verifica-se se existe algum processo de prioridade 2
                        #aguardando para executar
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,2)
                        if boolean:
                            #Se houver, desativa o token de 'utilização da CPU'
                            #para o processo atual e passa esse token para
                            #o processo de prioridade 2 verificado
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue
                        #Verifica-se se existe algum processo de prioridade 3
                        #aguardando para executar
                        boolean, indiceProcesso = self.hasProcessWaiting(processo,3)
                        if boolean:
                            #Se houver, desativa o token de 'utilização da CPU'
                            #para o processo atual e passa esse token para
                            #o processo de prioridade 3 verificado
                            if (contadorCPU != processo.getTempoProcessador()):
                                processo.deactivateTokenCPU()
                            self.USER_PROCESSES_RUNNING[indiceProcesso].activateTokenCPU()
                            continue

        print("P" + str(processo.getPID()) + " return SIGINT")
        #Liberação de recursos que o processo estava utilizando
        self.gerenteRecursos.liberaRecursos(processo)
        #Atualização da memória livre
        self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'ADICAO')
        #Remoção do processo com execução completa
        indice = self.getListaProcessos().index(processo)
        self.getListaProcessos().pop(indice)

    #Método que realiza a execução propriamente dita do processo de tempo real
    def executeProcessRT(self, processo):
        #Flag indicando que um processo de tempo real está em execução,
        #impedindo processos de usuário de executarem
        self.RT_STARTED = True
        #Ativação do Lock para impedir que novos processos de tempo real executem
        self.lockStartProcess.acquire()
        #Impressao de informações do processo
        self.imprimeInicioDeExecucaoProcesso(processo)
        #Atualização do offset de memória a ser impresso
        self.gerenteMemoria.atualizaOffsetMemoria(processo.getBlocosMemoria())
        print("process " + str(processo.getPID()))
        print("P" + str(processo.getPID()) + " STARTED")
        contadorInstruc = 1
        contadorCPU = 0
        tempoAtual = time.time()
        #Laço de repetição para executar o processo de tempo real durante o
        #tempo de execução do mesmo
        while contadorCPU < processo.getTempoProcessador():
            if processo.getTokenCPU():
                if time.time() > (tempoAtual+1):
                    #Impressao de execução de instrução
                    print("P" + str(processo.getPID()) + " instruction " + str(contadorInstruc))
                    contadorCPU += 1
                    contadorInstruc += 1
                    tempoAtual = time.time()
        print("P" + str(processo.getPID()) + " return SIGINT")
        processo.setHasExecuted()
        #Atualização da memória livre
        self.gerenteMemoria.atualizaMemoriaProcessosRT(processo.getBlocosMemoria(),'ADICAO')
        #Remoção do processo com execução completa
        indice = self.getListaProcessos().index(processo)
        self.getListaProcessos().pop(indice)
        #Liberação da condição de processo de tempo real em execução
        self.RT_STARTED = 0
        #Liberação do objeto Lock
        self.lockStartProcess.release()
        #Verificação de processo de usuário aguarando para ser escalonado
        #caso não haja threads de tempo real bloqueadas pelo Lock
        if not self.hasAnyThreadRTWaiting():
            self.activateFirstUserProcess()

    #Método que avalia se existem threads de tempo real bloqueadas,
    #aguardando por execução
    def hasAnyThreadRTWaiting(self):
        for processo in self.RT_PROCESSES_RUNNING:
            if processo.getHasExecuted() == False:
                return True
        return False

    #Método que realiza a ativação do token de 'utilização de CPU' para o
    #processo na primeira posição da lista de processos de usuario em execução,
    #esse método é chamado após a execução de um processo de tempo real
    def activateFirstUserProcess(self):
        for processo in self.USER_PROCESSES_RUNNING:
            if processo.getPrioridade() > 0 and processo.getTokenCPU() == False:
                processo.activateTokenCPU()
                return

    #Método para impressão de dados do processo
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
