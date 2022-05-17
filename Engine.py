import pygame
import sys
from Map import *
from menu import *




class Engine:
    Map = Map()

    def add(self,object):
        self.Map.add(object)


    def game_cycle(self,UI,level):
        #параметры
        screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        pygame.mixer.init()
        # фоновый звук
        # self.music()
        back_sound = pygame.mixer.Sound(r"SFX\background.mp3")
        death_sound = pygame.mixer.Sound(r"SFX\death.mp3")
        back_sound.play(100)

        W = screen.get_width()
        H = screen.get_height()

        FPS = 60
        color = (135, 206, 235)
        #время
        clock = pygame.time.Clock()
        self.Map.create_map(level)
        #игровой цикл
        running=True
        while running:

            if self.check_death():
                back_sound.stop()
                death_sound.play(0)
                color=(0,0,0)
                screen.fill(color)
                self.draw_text(screen, "GAME OVER", 64, W / 2, H/ 4)
                self.Map.Objects.clear()
                self.Map.Freshman = 0
                running = False
                pygame.display.update()
                pygame.display.flip()
                clock.tick(FPS)
                pygame.time.wait(6000)
                break


            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
                if i.type==pygame.KEYDOWN:
                    if i.key == pygame.K_ESCAPE:
                        back_sound.stop()
                        self.Map.Objects.clear()
                        self.Map.Freshman=0
                        running=False
                        break




            keys = pygame.key.get_pressed()

            screen.fill(color)

            #отрисовка объектов
            UI.paint_Map(screen,self.Map)
            pygame.display.update()
            self.move(keys)
            pygame.display.flip()
            clock.tick(FPS)



    def move(self,keys):
        self.Map.move(keys)

    def music(self):
        back_sound=pygame.mixer.Sound(r"Music\background.mp3")
        back_sound.play(100)

    def check_death(self):
        if self.Map.Freshman.onmap == "No":
            return True

    def draw_text(self,screen, text, size, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)