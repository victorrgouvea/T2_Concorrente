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
lock_uranio = Lock()
lock_oil = Lock()
simulation_time = None
planet_locks = None

# Abastecimento da lua
# Importante que quando o código for
# inicializado, dar um aquire no reabastecer refuel
# pra que seja inicializado adquirido
abastecer_lua = False

def get_abastecer_lua():
    global abastecer_lua
    return abastecer_lua

def set_abastecer_lua(valor):
    global abastecer_lua
    abastecer_lua = valor

# mutex localizado nas funções reabastecer_lua
# e refuels, utilizado na lógica.
mutex_reabastecer_refuel_uranium = Lock()

def acquire_reabastecer_refuel_uranium():
    global mutex_reabastecer_refuel_uranium
    mutex_reabastecer_refuel_uranium.acquire()

def release_reabastecer_refuel_uranium():
    global mutex_reabastecer_refuel_uranium
    mutex_reabastecer_refuel_uranium.release()

mutex_reabastecer_refuel_oil = Lock()

def acquire_reabastecer_refuel_oil():
    global mutex_reabastecer_refuel_oil
    mutex_reabastecer_refuel_oil.acquire()

def release_reabastecer_refuel_oil():
    global mutex_reabastecer_refuel_oil
    mutex_reabastecer_refuel_oil.release()

# mutex localizado na verificação de abastecimento da lua
mutex_verifica_abastecer_lua = Semaphore(value = 0)

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
