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
        
        uranium_ok = False
        oil_ok = False
      
        while(True):

            # Teste para terminar a execução do while
            # caso todos os planetas sejam terraformados durante
            # a execução do while e o programa todo poder terminar
            if globals.get_planets_terraform() == []:
                break
            
            # Verificação se tem recursos suficientes para o foguete
            # Caso aquele recurso já seja suficiente, a variável
            # é setada como True
            if (self.uranium >= uranio) and uranium_ok == False:
                uranium_ok = True
                
            if (self.fuel >= fuel) and oil_ok == False:
                oil_ok = True

            # não tem recurso suficiente pra abastecer o foguete
            if (not(uranium_ok) or not(oil_ok)):
                
                # tenta reabastecer a base
                self.tenta_reabastecer_base(uranio, fuel)
            
            # tem recurso, então descontamos os recursos que vão ser
            # utilizados pelo foguete e saimos do while retornando True
            else:
                self.uranium -= uranio
                self.fuel -= fuel
                return True
    
    def tenta_reabastecer_base(self, q_uranium, q_fuel):
        
        # verifica se o recurso faltante 
        # é uranium e faz o reabastecimento
        if self.uranium < q_uranium:
            self.refuel_uranium()

        # verifica se o recurso faltante 
        # é oil e faz o reabastecimento
        if self.fuel < q_fuel:
            self.refuel_oil()


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

        else:
            # Mutex para o acesso a mina de combustivel
            with globals.lock_oil:
                oil_atual = oil.unities
                # Se a quantidade que falta para a capacidade máxima da base
                # for maior ou igual do que a quantidade disponivel na mina,
                # a base pega toda a quantidade disponivel na mina
                if self.constraints[1] - self.fuel >= oil_atual:
                    self.fuel += oil_atual
                    oil.unities -= oil_atual
                
                # Caso contrário, a mina tem quantidade suficiente para 
                # completar a base, então definimos a quantidade com a 
                # capacidade máxima e tiramos da mina o que foi adicionado
                # para completar
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

        else:
            # Mutex para o acesso a mina de uranio
            with globals.lock_uranio:
                mina_atual = mina.unities
                # Se a quantidade que falta para a capacidade máxima da base
                # for maior ou igual do que a quantidade disponivel na mina,
                # a base pega toda a quantidade disponivel na mina
                if self.constraints[0] - self.uranium >= mina_atual:
                    self.uranium += mina_atual
                    mina.unities -= mina_atual
                
                # Caso contrário, a mina tem quantidade suficiente para 
                # completar a base, então definimos a quantidade com a 
                # capacidade máxima e tiramos da mina o que foi adicionado
                # para completar
                else:
                    self.uranium = self.constraints[0]
                    mina.unities -= self.constraints[0] - self.uranium

    
    def verifica_abastecimento_lua(self):
        '''Verifica se a lua precisa ser reabastecida'''

        # Utiliza um lock para garantir que só uma base verifique 
        # se a lua precisa de recursos por vez
        globals.acquire_verifica_abastecer_lua()

        # Se a lua precisar ser reabastecida, a variável
        # abastecer lua é setado como False, para que 
        # nenhuma outra base tente reabastecer a lua ao 
        # mesmo tempo, e então começa o processo de 
        # lançamento do foguete para a lua
        if (globals.get_abastecer_lua() == True):
            globals.set_abastecer_lua(False)
            globals.release_verifica_abastecer_lua()
        
            self.lanca_foguete_lua()

        else:
            globals.release_verifica_abastecer_lua()

    def lanca_foguete_lua(self):
            
        # Teste para verificar e gastar/repor
        # os recursos utilizados pelo foguete
        if (self.base_rocket_resources('LION')):
            
            nome = self.name
            # condicional necessário por conta da diferença
            # entre o nome dado na instancia do objeto e 
            # da chave do dicionario de bases
            if nome == 'CANAVERAL CAPE':
                nome = 'canaveral_cape'
            
            # Pegamos a instancia da base que fará o lançamento e
            # criamos o foguete como LION com as quantidades
            # de recursos que a lua precisa
            base = (globals.get_bases_ref())[nome.lower()]
            resources = globals.get_moon_needs()
            foguete = Rocket('LION')
            foguete.fuel_cargo, foguete.uranium_cargo = resources

            # Criação da thread que fará o lançamento e todas as ações do foguete
            thread_foguete = Thread(target = lambda: foguete.voyage_moon(base))
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

            with globals.planet_locks.terraform_locks[planet.name.lower()]:
                if planet.terraform > 0:
                    # Criação da thread que fará o lançamento e todas as ações do foguete
                    thread_foguete = Thread(target = lambda: rocket.launch(base, planet))
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
            # Uso o try e except para o caso da lista de planetas a serem terraformados
            # ficar vazia no meio da execução e isso causar um erro
        
            try: 
                self.lanca_foguete(choice(foguetes), choice(planetas))
            except:
                print("O foguete não deve ser lançado pois todos os planetas já foram terraformados!")
