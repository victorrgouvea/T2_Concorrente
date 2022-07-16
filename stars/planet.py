from threading import Thread
import globals

class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform, name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self):
        print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def planet_is_safe(self):
        print(f"🪐 - {self.name} IS COMPLETELY HABITABLE!")
        planetas = globals.get_planets_terraform()
        planetas.remove(self.name)
        globals.set_planets_terraform(planetas)

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        # Enquanto o planeta não for habitável, o satelite
        # detecta a chegada de foguetes
        while(self.terraform > 0):
            
            # Utilizo um semaforo que só é liberado 
            # quando uma nuke atinge o planeta
            (globals.planet_locks.nuke_event[self.name.lower()]).acquire()
            self.nuke_detected()

        # Após o planeta ser terraformado, ele é retirado da
        # lista de planetas para não ser bombardeado novamente
        self.planet_is_safe()