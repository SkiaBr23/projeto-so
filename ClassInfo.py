#encoding=utf-8
import os

#Universidade de Brasília
#Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

class ClassInfo:

    @staticmethod
    def informativoPrograma ():
        print ("Universidade de Brasília - 02/2017")
        print ("Projeto Final - Sistemas Operacionais")
        print ("Aguardando inicialização de processos...")

    @staticmethod
    def limparTela ():
        os.system('cls' if os.name=='nt' else 'clear')
