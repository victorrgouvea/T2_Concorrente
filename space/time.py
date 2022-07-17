
from threading import Thread
from time import sleep

import globals

######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class SimulationTime(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.current_time = 0
    
    def simulation_time(self):
        return self.current_time
    
    def run(self):
        while(globals.get_release_system() == False):
            pass
        
        # Mudanças feitas para terminar o programa e
        # fazer o print final do total de anos
        # O release no semaforo é para o caso de a
        # lua estar esperando por recursos, o que 
        # fazia o programa ficar travado
        while(globals.get_planets_terraform() != []):
            print(f"{self.current_time} year(s) have passed...")
            self.current_time+=1
            sleep(1)
        
        globals.release_sem_refuel()
        print(f"======== ALL PLANETS ARE TERRAFORMED! TOTAL YEARS: {self.current_time} ========")
        print(globals.fog_choice)
