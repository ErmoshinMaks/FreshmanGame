from Engine import *
from UI import *
from menu import *



class Controller:
    Engine=Engine()
    UI=UI()
    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    W = screen.get_width()
    H = screen.get_height()

    def start(self):
        #___________________________________
        self.show_menu(self.Engine,self.UI)

    def add(self,object):
        self.Engine.add(object)

    def show_menu(self,Engine,UI):
        menu=Menu()
        menu.show_menu(Engine,UI)