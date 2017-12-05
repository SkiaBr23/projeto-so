#encoding=utf-8
import os

#Universidade de Brasília
#Sistemas Operacionais - 02/2017
# Alunos: 	Maximillian Xavier
#			Rafael Costa
#			Eduardo Schuabb
# Projeto Final

#Classe para exibir informações do projeto
class ClassInfo:

    #Método para exibir informações do projeto
    @staticmethod
    def informativoPrograma ():
        print ("Universidade de Brasília - 02/2017")
        print ("Projeto Final - Sistemas Operacionais")
        print ("Aguardando inicialização de processos...")

    #Método para limpar a tela do terminal
    @staticmethod
    def limparTela ():
        os.system('cls' if os.name=='nt' else 'clear')
