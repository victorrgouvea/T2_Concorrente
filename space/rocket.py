from random import randrange, random
import globals
from time import sleep


class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0
            

    def nuke(self, planet):
        '''Explosão do foguete ao chegar no planeta'''
        
        dano = self.damage()
        nome = planet.name.lower()
        polo = self.nuke_pole(planet)

        # Utilizo um lock para atualizar a variável de 
        # terraform com o dano causado pelo foguete
        with globals.planet_locks.terraform_locks[nome]:
            planet.terraform -= dano

        # Dependendo do polo atingido pelo foguete, fazemos o 
        # print e o release do lock do respectivo polo
        if polo == 'norte':
            print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
            (globals.planet_locks.polo_norte_locks[nome]).release()
        else:
            print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
            (globals.planet_locks.polo_sul_locks[nome]).release()

        # Aqui é feito o release do semaforo para indicar 
        # que uma nuke foi detectada naquele planeta
        (globals.planet_locks.nuke_event[nome]).release()


    def nuke_pole(self, planet):
        '''Decide qual polo o foguete vai explodir'''
        
        nome = planet.name.lower()

        # Caso ja tenha algum foguete indo para o norte:
        if (globals.planet_locks.polo_norte_locks[nome]).locked():
            
            # E caso tenha outro foguete também indo ao sul,
            # ele espera até que o foguete com direção ao polo norte 
            # o atinga, para então se encaminhar ao mesmo polo
            if (globals.planet_locks.polo_sul_locks[nome]).locked():
                (globals.planet_locks.polo_norte_locks[nome]).acquire()
                return 'norte'
            
            # Caso o polo sul não seja destino de nenhum foguete, ele se direciona para lá
            else:
                (globals.planet_locks.polo_sul_locks[nome]).acquire()
                return 'sul'
        
        # Caso nenhum foguete esteja direcionado ao polo norte, ele vai para lá
        else:
            (globals.planet_locks.polo_norte_locks[nome]).acquire()
            return 'norte'
    
    def reabastecer_lua_uranium(self):
        print('Abastecimento da lua de uranium iniciado!')
        globals.release_reabastecer_refuel_uranium()
        globals.acquire_reabastecer_refuel_uranium()

        
    
    def reabastecer_lua_oil(self):
        print('Abastecimento da lua de combustível iniciado!')
        globals.release_reabastecer_refuel_oil()
        globals.acquire_reabastecer_refuel_oil()



    def voyage(self, planet, resource):
        '''Eventos do foguete após o lançamento'''
        
        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.
        self.simulation_time_voyage(planet)
        failure = self.do_we_have_a_problem()

        if (self.name == 'LION'):
            if (failure == False):
                if (resource == 'URANIUM E OIL'):
                    self.reabastecer_lua_uranium()
                    self.reabastecer_lua_oil()

                elif (resource ==  'URANIUM'):
                    self.reabastecer_lua_uranium()
        
                
                elif (resource == 'OIL'):
                    self.reabastecer_lua_oil()

            else:
                print('Planeta destino inválido ou falha no lançamento!')
    
        else:
            # Caso o foguete não falhe ou seja destruído e o planeta
            # ainda não esteja terraformado, ele atinge o planeta
            # (utlizo os locks dessa maneira para o mutex do terraform
            # não ficar travado durante toda a execução do nuke)
            (globals.planet_locks.terraform_locks[planet.name]).acquire()
            if failure == False and planet.terraform > 0:
                (globals.planet_locks.terraform_locks[planet.name]).release()
                self.nuke(planet)
            else:
                (globals.planet_locks.terraform_locks[planet.name]).release()




    ####################################################
    #                   ATENÇÃO                        # 
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################
    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            sleep(2) # Marte tem uma distância aproximada de dois anos do planeta Terra.
        else:
            sleep(5) # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False
            
    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")
    
    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True
    
    def damage(self):
        return random()

    def launch(self, base, planet, resource):
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet, resource)        
