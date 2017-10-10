TAMANHO_TOTAL_MEMORIA = 1024
TAMANHO_MEMORIA_PROCESSOS_RT = 64
TAMANHO_MEMORIA_PROCESSOS_USUARIO = 960

class ClassGerenciadorMemoria:

	def __init__(self):
		self.int_memoria_processos_usuario = TAMANHO_MEMORIA_PROCESSOS_USUARIO
		self.int_memoria_processos_rt = TAMANHO_MEMORIA_PROCESSOS_RT

	def verificaDisponibilidadeMemoria(self, processo):
		return True


