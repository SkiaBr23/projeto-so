#encoding=utf-8

class ClassGerenciadorRecurso:

    def __init__(self):
        self.scannerLivre = 1
        self.impressorasLivres = [1,2]
        self.modemLivre = 1
        self.dispSataLivres = [1,2]

    def liberaRecursos(self,processo):

        if processo.getRequisicaoScanner() == 1 and self.scannerLivre == 0:
            self.scannerLivre = 1;
        if processo.getRequisicaoModem() == 1 and self.modemLivre == 0:
            self.modemLivre = 1;
        if processo.getRequisicaoImpressora() != 0 and processo.getRequisicaoImpressora() not in self.impressorasLivres:
            self.impressorasLivres.append(processo.getRequisicaoImpressora())
        if processo.getRequisicaoDisco() != 0 and processo.getRequisicaoDisco() not in self.dispSataLivres:
            self.dispSataLivres.append(processo.getRequisicaoDisco())

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

    def verificaDisponibilidadeScanner (self, processo):
        if processo.getRequisicaoScanner() == 0:
            return True
        elif (processo.getRequisicaoScanner() == 1) and self.scannerLivre == 1:
            self.scannerLivre = 0
            return True
        else:
            return False

    def verificaDisponibilidadeModem (self, processo):
        if processo.getRequisicaoModem() == 0:
            return True
        elif (processo.getRequisicaoModem() == 1) and self.modemLivre == 1:
            self.modemLivre = 0
            return True
        else:
            return False

    def verificaDisponibilidadeImpressoras (self, processo):
        if processo.getRequisicaoImpressora() == 0:
            return True
        elif processo.getRequisicaoImpressora() in self.impressorasLivres:
            self.impressorasLivres.remove(processo.getRequisicaoImpressora())
            return True
        else:
            return False

    def verificaDisponibilidadeDispSatas (self, processo):
        if processo.getRequisicaoDisco() == 0:
            return True
        elif processo.getRequisicaoDisco() in self.dispSataLivres:
            self.dispSataLivres.remove(processo.getRequisicaoDisco())
            return True
        else:
            return False
