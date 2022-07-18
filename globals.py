from threading import Lock, Semaphore
from space.planetLocks import PlanetLocks

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las. 
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.



release_system = False
mutex_print = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None

# Mutex para o acesso das quantidades de 
# uranio e combustível nas minas
lock_uranio = Lock()
lock_oil = Lock()

# Instancia do objeto da classe PlanetLocks que
# Contém os semaforos e locks necessários para cada planeta
# (Ele é instanciado na função set_release_system())
planet_locks = None

# Lista de planetas que ainda não são habitaveis
planets_to_terraform = []

def set_planets_terraform(planets):
    global planets_to_terraform
    planets_to_terraform = planets

def get_planets_terraform():
    global planets_to_terraform
    return planets_to_terraform

# Variável que armazena uma tupla com as quantidades 
# de recursos que a lua necessita na forma (uranio, combustivel)
moon_needs = None

def set_moon_needs(resources):
    global moon_needs
    moon_needs = resources

def get_moon_needs():
    global moon_needs
    return moon_needs

# Varíavel que diz se a lua precisa
# ou não ser reabastecida
abastecer_lua = False

def get_abastecer_lua():
    global abastecer_lua
    return abastecer_lua

def set_abastecer_lua(valor):
    global abastecer_lua
    abastecer_lua = valor

# semaforo localizado nas funções reabastecer_lua
# e refuels, utilizado na lógica.
sem_refuel = Semaphore(0)

def acquire_sem_refuel():
    global sem_refuel
    sem_refuel.acquire()

def release_sem_refuel():
    global sem_refuel
    sem_refuel.release()


# mutex localizado na verificação de abastecimento da lua
# para garantir que só uma base faça essa verificação e
# o reabastecimento por vez
mutex_verifica_abastecer_lua = Lock()

def acquire_verifica_abastecer_lua():
    global mutex_verifica_abastecer_lua
    mutex_verifica_abastecer_lua.acquire()

def release_verifica_abastecer_lua():
    global mutex_verifica_abastecer_lua
    mutex_verifica_abastecer_lua.release()

# ===========================
def acquire_print():
    global mutex_print
    mutex_print.acquire()

def release_print():
    global mutex_print
    mutex_print.release()

def set_planets_ref(all_planets):
    global planets
    planets = all_planets

def get_planets_ref():
    global planets
    return planets

def set_bases_ref(all_bases):
    global bases
    bases = all_bases

def get_bases_ref():
    global bases
    return bases

def set_mines_ref(all_mines):
    global mines
    mines = all_mines

def get_mines_ref():
    global mines
    return mines

def set_release_system():
    global release_system
    global planet_locks
    release_system = True
    # Inicializo esse objeto aqui para que
    # ele esteja ativo desde o inicio da execução
    planet_locks = PlanetLocks()

def get_release_system():
    global release_system
    return release_system

def set_simulation_time(time):
    global simulation_time
    simulation_time = time

def get_simulation_time():
    global simulation_time
    return simulation_time
