import globals
from threading import Thread
from space.rocket import Rocket
from random import choice

'''
- Caso a lua precise se recursos, manda um foguete Lion para ela
  se não, ataca um planeta com outro foguete criado aleatoriamente
- Checa se tem recursos suficientes para lançar um foguete (utilizar mutex aqui para checar essas variáveis)
'''

class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")
    
    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35 and self.fuel > 50:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
            case _:
                print("Invalid rocket name")


    def refuel_oil(self):

        oil = globals.mines['oil_earth']
        
        # Vemos qual quantidade tem que ser verificada dependendo da base
        if self.name == 'CANAVERAL CAPE' or self.name == 'MOSCOW':
            unidades_oil = 120
        elif self.name == 'ALCANTARA':
            unidades_oil = 100
        
        # Verificamos se precisa repor o combustivel
        if self.oil < unidades_oil:
            # Mutex para o acesso a mina de combustivel
            with globals.lock_oil:
                oil_atual = oil.unities
                if self.constraints[1] - self.oil >= oil_atual:
                    self.oil += oil_atual
                    oil.unities -= oil_atual
                else:
                    self.uranium = self.constraints[1]
                    oil.unities -= self.constraints[1] - self.oil

    def refuel_uranium(self):

        mina = globals.mines['uranium_earth']

        # Verificamos se é preciso repor o uranio
        if self.uranium < 35:
            # Mutex para o acesso a mina de uranio
            with globals.lock_uranio:
                mina_atual = mina.unities
                if self.constraints[0] - self.uranium >= mina_atual:
                    self.uranium += mina_atual
                    mina.unities -= mina_atual
                else:
                    self.uranium = self.constraints[0]
                    mina.unities -= self.constraints[0] - self.uranium

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            # Lógica dos ataques aos planetas e reposição de recursos da lua quando necessário
            self.refuel_oil()
            self.refuel_uranium()
            pass
