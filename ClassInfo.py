#encoding=utf-8
import os

class ClassInfo:

    @staticmethod
    def informativoPrograma ():
        print ("Universidade de Brasília - 02/2017")
        print ("Projeto Final - Sistemas Operacionais")
        print ("Aguardando inicialização de processos...")

    @staticmethod
    def limparTela ():
        os.system('cls' if os.name=='nt' else 'clear')
