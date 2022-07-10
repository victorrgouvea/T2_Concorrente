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
                quant_oil = {'ALCANTARA': 70, 'MOON': 50, 'MOSCOU': 100, 'CABO CANAVERAL': 100}

            case 'FALCON':
                quant_oil = {'ALCANTARA': 100, 'MOON': 90, 'MOSCOU': 120, 'CABO CANAVERAL': 120}
               
            case 'LION':
                quant_oil = {'ALCANTARA': 100, 'MOON': 'OUT', 'MOSCOU': 115, 'CABO CANAVERAL': 115}
        
            case _:
                print("Invalid rocket name")
                return False
        
        if (quant_oil[self.name] == 'OUT'):
            print("IMPOSSÍVEL LANÇAR O FOGUETE LION DA LUA!")
            return False
        
        abastecido = False
        uranium_ok =  False
        oil_ok = False
      
        while(not(abastecido)):

            # verifica se tem recurso suficiente
            if self.uranium >= 35:
                uranium_ok = True
                self.uranium = self.uranium - 35
            
            if (self.fuel >= quant_oil[self.name]):
                oil_ok = True
                self.fuel -= quant_oil[self.name]

            # não tem recurso suficiente pra abastecer o foguete
            if (not(uranium_ok) or not(oil_ok)):
                # tenta reabastecer a base
                # se conseguir o loop é refeito
                abastecido = self.tenta_reabastecer_base(35, quant_oil[self.name])
            
            # tem recurso, então o foguete já foi abastecido
            # e o loop não deve continuar
            else:
                abastecido = True
    
    def tenta_reabastecer_base(self, q_uranium, q_fuel):
        # não tem recurso suficiente pra lançar o foguete
        uranium_ok = False
        fuel_ok = False
        # verifica se o recurso faltante é uranium
        # e tenta abastecer
        if self.uranium < q_uranium:
            self.refuel_uranium()
            if self.uranium < q_uranium:
                uranium_ok = False
            
            else:
                uranium_ok = True
        else:
            uranium_ok = True

        # verifica se o recurso faltante é oil
        # e tenta abastecer
        if self.fuel < q_fuel:
            self.refuel_oil()
            if self.fuel < q_fuel:
                fuel_ok = False

            else:
                fuel_ok = True
        else:
            fuel_ok = True

        # retorna a condição de abastecimento ou não
        # a not aqui, ocorre pelo fato de o loop no método
        # que chama, aconetecer no caso da variável que recebe
        # ser falsa
        return (not(uranium_ok and fuel_ok))    

    def refuel_oil(self):

        oil = globals.mines['oil_earth']

        # verifica se é a lua que quer ser reabastecida
        if self.name == 'MOON':
            pass
        else:
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

        # verifica se é a lua que quer ser reabastecida
        if self.name == 'MOON':
            pass
        else:
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
