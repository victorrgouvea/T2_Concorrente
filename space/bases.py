import globals
from threading import Thread
from space.rocket import Rocket
from random import choice



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
        
        # Aqui é definido, baseado no nome do foguete que será lançado,
        # a quantidade de recursos necessárias para o lançamento
        match rocket_name:
            case 'DRAGON':
                quant = {'ALCANTARA': 70, 'MOON': 50, 'MOSCOW': 100, 'CANAVERAL CAPE': 100, 'URANIUM': 35}

            case 'FALCON':
                quant = {'ALCANTARA': 100, 'MOON': 90, 'MOSCOW': 120, 'CANAVERAL CAPE': 120, 'URANIUM': 35}
               
            case 'LION':
                quant= {'ALCANTARA': 100, 'MOON': 'OUT', 'MOSCOW': 115, 'CANAVERAL CAPE': 115}
        
            case _:
                print("Invalid rocket name")
                return False
        
        if (self.name == 'MOON' and rocket_name == 'LION'):
            print("IMPOSSÍVEL LANÇAR O FOGUETE LION DA LUA!")
            return False
        
        abastecido = False
        uranium_ok =  False
        oil_ok = False
      
        while(not(abastecido)):

            # Caso seja o foguete lion, precisamos saber se temos
            # recursos suficientes para o seu lançamento e para
            # a sua carga com os recursos da lua
            if rocket_name == 'LION':
                resources = globals.get_moon_needs()
                uranio, fuel = resources
                fuel += quant[self.name]

            # Se for um dos foguetes de ataque, só precisamos
            # dos recursos para o lançamento
            else:
                uranio = quant['URANIUM']
                fuel = quant[self.name]
            
            # Verificação se tem recursos suficientes para o foguete
            # Também verifico o caso de ser o segundo loop após a
            # tentativa de reabastecer a base e o recurso ja ser suficiente
            # no primeiro loop. Se ele já foi suficiente no primeiro loop e
            # o desconto da sua quantidade já foi feita, não posso repetir isso
            # no segundo loop
            if (self.uranium >= uranio) and uranium_ok == False:
                uranium_ok = True
                self.uranium -= uranio
                
            if (self.fuel >= fuel) and oil_ok == False:
                oil_ok = True
                self.fuel -= fuel

            # não tem recurso suficiente pra abastecer o foguete
            if (not(uranium_ok) or not(oil_ok)):
                # tenta reabastecer a base
                # se conseguir o loop é refeito
                
                abastecido = self.tenta_reabastecer_base(uranio, fuel)

                # caso não tenha conseguido abastecer um dos combustíveis
                # ele devolve a quantidade já retirada e, no caso do Lion,
                # ele seta a variável de abastecer a lua como True indicando
                # que não conseguiu lançar o foguete e a lua ainda não foi reabastecida
                if (abastecido):
                    if (uranium_ok):
                        self.uranium += uranio
                    
                    if (oil_ok):
                        self.fuel += fuel

                    if rocket_name == 'LION':
                        globals.set_abastecer_lua(True)

                    return False
            
            # tem recurso, então o foguete já foi abastecido
            # e o loop não deve continuar
            else:
                return True
    
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
            
            # leva o maximo de combustivel que cabe no foguete
            fuel = 120

            # caso o que falte para o maximo da capacidade da lua
            # seja menor ou igual que a capacidade maxima do foguete,
            # ele leva somente o que precisa para completar
            if (self.constraints[0] - self.fuel <= 75):
                uranium = self.constraints[0] - self.fuel
            
            # caso contrario ele leva o maximo que o foguete pode carregar
            else:
                uranium = 75

            # Indica as outras bases que precisa de recursos e 
            # as quantidades necessárias
            globals.set_moon_needs((uranium, fuel))
            globals.set_abastecer_lua(True)

            # semaforo que controla a chegada do foguete lion na lua
            globals.acquire_sem_refuel()

            # apos a chegada do foguete, podemos atribuir os valores
            # dos recursos que chegaram
            self.uranium += uranium
            self.fuel += fuel
            
            print('Lua abastecida com sucesso!')

        else:
            # Mutex para o acesso a mina de combustivel
            with globals.lock_oil:
                oil_atual = oil.unities
                if self.constraints[1] - self.fuel >= oil_atual:
                    self.fuel += oil_atual
                    oil.unities -= oil_atual
                else:
                    self.fuel = self.constraints[1]
                    oil.unities -= self.constraints[1] - self.fuel

    def refuel_uranium(self):

        mina = globals.mines['uranium_earth']

        # verifica se é a lua que quer ser reabastecida
        if self.name == 'MOON':

            # leva o maximo de uranio que cabe no foguete
            uranium = 75

            # caso o que falte para o maximo da capacidade da lua
            # seja menor ou igual que a capacidade maxima do foguete,
            # ele leva somente o que precisa para completar
            if (self.constraints[1] - self.fuel <= 120):
                fuel = self.constraints[1] - self.fuel
            
            # caso contrario ele leva o maximo que o foguete pode carregar
            else:
                fuel = 120

            # Indica as outras bases que precisa de recursos e 
            # as quantidades necessárias
            globals.set_moon_needs((uranium, fuel))
            globals.set_abastecer_lua(True)

            # semaforo que controla a chegada do foguete lion na lua
            globals.acquire_sem_refuel()

            # apos a chegada do foguete, podemos atribuir os valores
            # dos recursos que chegaram
            self.uranium += uranium
            self.fuel += fuel
            
            print('Lua abastecida com sucesso!')

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
        '''Verifica se a lua precisa ser reabastecida'''

        # Utiliza um lock para garantir que só uma base verifique 
        # se a lua precisa de recursos por vez
        globals.acquire_verifica_abastecer_lua()
        if (globals.get_abastecer_lua() == True):
            globals.set_abastecer_lua(False)
            globals.release_verifica_abastecer_lua()
        
            self.lanca_foguete_lua()

        else:
            globals.release_verifica_abastecer_lua()

    def lanca_foguete_lua(self):
            
        if (self.base_rocket_resources('LION')):
            
            base = (globals.get_bases_ref())[self.name.lower()]
            resources = globals.get_moon_needs()
            foguete = Rocket('LION')
            foguete.fuel_cargo, foguete.uranium_cargo = resources

            thread_foguete = Thread(target = foguete.voyage_moon(base))
            thread_foguete.start()

    def lanca_foguete(self, foguete, planeta):

        # Teste para verificar e gastar/repor
        # os recursos utilizados pelo foguete
        if (self.base_rocket_resources(foguete)):
           
            nome = self.name
            # condicional necessário por conta da diferença
            # entre o nome dado na instancia do objeto e 
            # da chave do dicionario de bases
            if nome == 'CANAVERAL CAPE':
                nome = 'canaveral_cape'
            
            # Pegamos as instancias da base e planeta escolhidos
            # e instanciamos o foguete
            base = (globals.get_bases_ref())[nome.lower()]
            planet = (globals.get_planets_ref())[planeta.lower()]
            rocket = Rocket(foguete)

            # Criação da thread que fará o lançamento e todas as ações do foguete
            thread_foguete = Thread(target = rocket.launch(base, planet))
            thread_foguete.start()


    def run(self):

        # set da lista de planetas a serem terraformados
        globals.set_planets_terraform(['MARS', 'IO', 'GANIMEDES', 'EUROPA'])
        # lista de foguetes para atacar os planetas
        foguetes = ['DRAGON', 'FALCON']
       
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
        
        while(True):

            planetas = globals.get_planets_terraform()
            
            # Caso não tenha mais planetas a serem terraformados,
            # a execução do for é parada 
            if planetas == []:
                break

            # Caso não seja a base lunar, verifica e
            # repoe os recursos da lua se necessário
            if self.name != 'MOON':
                self.verifica_abastecimento_lua()
            
            # Lançamento de um foguete aleatório em um planeta aleatório
            self.lanca_foguete(choice(foguetes), choice(planetas))
