#encoding=utf-8

# Universidade de Brasília
# Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

# Classe que faz a gerência de recursos requisitados por um processo 
class ClassGerenciadorRecurso:

    # Notação de disponibilidade de recursos. 0 para indisponível, 1 para disponível
    # Obs: As impressoras e dispositivos SATA possuem 2 unidades.
    def __init__(self):
        self.scannerLivre = 1
        self.impressorasLivres = [1,2]
        self.modemLivre = 1
        self.dispSataLivres = [1,2]


    # Libera todos os recursos alocados por um processo.
    # É executado ao fim do processo e toma como premissa que o processo
    # alocou todos os recursos solicitados com sucesso.
    # Argumentos: processo que utilizou os recursos
    def liberaRecursos(self,processo):
        if processo.getRequisicaoScanner() == 1 and self.scannerLivre == 0:
            self.scannerLivre = 1;
        if processo.getRequisicaoModem() == 1 and self.modemLivre == 0:
            self.modemLivre = 1;
        if processo.getRequisicaoImpressora() != 0 and processo.getRequisicaoImpressora() not in self.impressorasLivres:
            self.impressorasLivres.append(processo.getRequisicaoImpressora())
        if processo.getRequisicaoDisco() != 0 and processo.getRequisicaoDisco() not in self.dispSataLivres:
            self.dispSataLivres.append(processo.getRequisicaoDisco())

    # Executa a verificação de disponibilidade de todos os recursos em cascata.
    # Argumentos: processo que solicita o recurso
    def verificaDisponibilidadeRecursos(self, processo):
        #Verificação de scanner
        if self.verificaDisponibilidadeScanner(processo):
            #Verificação de modem
            if self.verificaDisponibilidadeModem(processo):
                #Verificação de impressoras
                if self.verificaDisponibilidadeImpressoras(processo):
                    #Verificação de dispositivos satas
                    if self.verificaDisponibilidadeDispSatas(processo):
                        return True
        return False

    # Verifica se o scanner está disponível.
    # A função retorna a disponibilidade atual do recurso, e 
    # caso o processo o requisite, já executa a alocação.
    # Argumentos: processo que solicita o recurso
    def verificaDisponibilidadeScanner (self, processo):
        if processo.getRequisicaoScanner() == 0:
            return True
        elif (processo.getRequisicaoScanner() == 1) and self.scannerLivre == 1:
            self.scannerLivre = 0
            return True
        else:
            return False

    # Verifica se o modem está disponível.
    # A função retorna a disponibilidade atual do recurso, e 
    # caso o processo o requisite, já executa a alocação.
    # Argumentos: processo que solicita o recurso
    def verificaDisponibilidadeModem (self, processo):
        if processo.getRequisicaoModem() == 0:
            return True
        elif (processo.getRequisicaoModem() == 1) and self.modemLivre == 1:
            self.modemLivre = 0
            return True
        else:
            return False

    # Verifica se alguma impressora está disponível.
    # A função retorna a disponibilidade atual do recurso, e 
    # caso o processo o requisite, já executa a alocação.
    # Argumentos: processo que solicita o recurso
    def verificaDisponibilidadeImpressoras (self, processo):
        if processo.getRequisicaoImpressora() == 0:
            return True
        elif processo.getRequisicaoImpressora() in self.impressorasLivres:
            self.impressorasLivres.remove(processo.getRequisicaoImpressora())
            return True
        else:
            return False


    # Verifica se o dispositivo SATA está disponível.
    # A função retorna a disponibilidade atual do recurso, e 
    # caso o processo o requisite, já executa a alocação.
    # Argumentos: processo que solicita o recurso
    def verificaDisponibilidadeDispSatas (self, processo):
        if processo.getRequisicaoDisco() == 0:
            return True
        elif processo.getRequisicaoDisco() in self.dispSataLivres:
            self.dispSataLivres.remove(processo.getRequisicaoDisco())
            return True
        else:
            return False
