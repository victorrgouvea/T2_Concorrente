from platform import release
from secrets import choice
import globals
from threading import Thread
from space.rocket import Rocket
from random import Choice


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
                quant = {'ALCANTARA': 70, 'MOON': 50, 'MOSCOU': 100, 'CABO CANAVERAL': 100, 'URANIUM': 35}

            case 'FALCON':
                quant = {'ALCANTARA': 100, 'MOON': 90, 'MOSCOU': 120, 'CABO CANAVERAL': 120, 'URANIUM': 35}
               
            case 'LION':
                # como vai com recursos dentro, verificar valor correto
                quant= {'ALCANTARA': 100, 'MOON': 'OUT', 'MOSCOU': 115, 'CABO CANAVERAL': 115, 'URANIUM': 75}
        
            case _:
                print("Invalid rocket name")
                return False
        
        if (quant[self.name] == 'OUT'):
            print("IMPOSSÍVEL LANÇAR O FOGUETE LION DA LUA!")
            return False
        
        abastecido = False
        uranium_ok =  False
        oil_ok = False
      
        while(not(abastecido)):

            # verifica se tem recurso suficiente
            
            if self.uranium >= quant['URANIUM']:
                uranium_ok = True
                self.uranium = self.uranium - quant['URANIUM']
            
            if (self.fuel >= quant[self.name]):
                oil_ok = True
                self.fuel -= quant[self.name]

            # não tem recurso suficiente pra abastecer o foguete
            if (not(uranium_ok) or not(oil_ok)):
                # tenta reabastecer a base
                # se conseguir o loop é refeito
                
                abastecido = self.tenta_reabastecer_base(quant['URANIUM'], quant[self.name])

                # caso não tenha conseguido abastecer um dos combustíveis
                # ele devolve a quantidade já retirada
                if (abastecido):
                    if (uranium_ok):
                        self.uranium += quant['URANIUM']
                    
                    if (oil_ok):
                        self.fuel += quant[self.name]

                    return False
            
            # tem recurso, então o foguete já foi abastecido
            # e o loop não deve continuar
            else:
                return True
    
    def tenta_reabastecer_base(self, q_uranium, q_fuel):
        # CRIAR DUAS THREADS PARA FAZER A VERIFICAÇÃO
        # PARELELAMENTE
        
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
            globals.set_abastecer_lua(True)
            
            # mutex que controla a chegada do foguete lion na lua
            globals.acquire_reabastecer_refuel_oil()
            self.fuel += 120

            if (self.constraints[0] -  self.fuel <= 75):
                self.uranium = self.constraints[0]
            
            else:
                self.uranium += 75

            print('Lua abastecida de uranium com sucesso!')

        else:
            # Mutex para o acesso a mina de combustivel
            with globals.lock_oil:
                oil_atual = oil.unities
                if self.constraints[1] - self.oil >= oil_atual:
                    self.fuel += oil_atual
                    oil.unities -= oil_atual
                else:
                    self.fuel = self.constraints[1]
                    oil.unities -= self.constraints[1] - self.oil

    def refuel_uranium(self):

        mina = globals.mines['uranium_earth']

        # verifica se é a lua que quer ser reabastecida
        if self.name == 'MOON':
            globals.set_abastecer_lua(True)

            # mutex que controla a chegada do foguete lion na lua
            globals.acquire_reabastecer_refuel_uranium()
            self.uranium += 75

            if (self.constraints[1] -  self.fuel <= 120):
                self.fuel = self.constraints[1]
            
            else:
                self.fuel += 120

            #verificar se a quantidade de oil e abastecer
            print('Lua abastecida de combustível com sucesso!')
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

    
    def verifica_abastecimento_lua(self):
        # Lógica dos ataques aos planetas e reposição de recursos da lua quando necessário
        # condicional para saber se a lua precisa ser reabastecida

        # SÓ OIL
        globals.acquire_verifica_abastecer_lua()
        if (globals.get_abastecer_lua() == True):
            globals.set_abastecer_lua(False)
            globals.release_verifica_abastecer_lua()
        
            self.lanca_foguete(None, 'LION')

        else:
            globals.release_verifica_abastecer_lua()

    def lanca_foguete(self, foguete, planeta):

        if (self.base_rocket_resources(foguete)):
           
            thread_foguete = Thread(target = Rocket.launch(self.name, planeta, foguete))
            thread_foguete.start()
        
        else:
            print('A base ' + self.name + ' tentou lançar o foguete ' + foguete + ', mas não conseguiu por falta de recursos!')

    def run(self):
        # adquiri o mutex que controla o abastecimento da lua
        globals.acquire_reabastecer_refuel_oil()
        globals.acquire_reabastecer_refuel_uranium()

        foguetes = ['DRAGON', 'FALCON']
        planetas = ['MARS', 'IO', 'GANIMEDES', 'EUROPA']
       
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            choice()
            self.verifica_abastecimento_lua()
            self.lanca_foguete(choice(foguetes), choice(planetas))
