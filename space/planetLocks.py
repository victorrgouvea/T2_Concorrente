import globals
from threading import Lock, Semaphore



class PlanetLocks():
    '''Classe para armazenar os locks e semaforos dos planetas'''
    
    def __init__(self):
        # Dicionarios com os Locks para os valores de terraform e acesso aos polos de cada planeta
        self.terraform_locks = {}
        self.polo_norte_locks = {}
        self.polo_sul_locks = {}

        # Dicionario com os semaforos para a detecção de nukes em cada planeta
        self.nuke_event = {}
        
        # Criação dos locks e semaforos dos planetas
        for planet in globals.planets:
            self.terraform_locks[planet] = Lock()
            self.polo_norte_locks[planet] = Lock()
            self.polo_sul_locks[planet] = Lock()
            self.nuke_event[planet] = Semaphore(0)
