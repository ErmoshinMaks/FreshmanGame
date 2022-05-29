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
        running = True
        #игровой цикл
        while running:

            if self.Map.running==False:
                back_sound.stop()
                running = False
                damage_sound = pygame.mixer.Sound(r"SFX\win.mp3")
                damage_sound.play()
                self.win_animation(W,H,screen,clock,FPS)
                self.Map.running=True
                break

            if self.check_death():
                back_sound.stop()
                death_sound.play(0)
                self.losing_animation(W,H,screen,clock,FPS)
                running= False
                break


            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
                if i.type==pygame.KEYDOWN:
                    if i.key == pygame.K_ESCAPE:
                        back_sound.stop()
                        self.Map.Objects.clear()
                        self.Map.All_Objects.clear()
                        self.Map.Freshman=0
                        running=False
                        break


            if running==False:
                self.Map.All_Objects.clear()
                self.Map.Objects.clear()
                break

            keys = pygame.key.get_pressed()

            screen.fill(color)

            #отрисовка объектов
            self.Map.spawn_objects()
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

    def draw_text(self,screen, text, size, x, y,color):
        font_name = pygame.font.match_font('Helvetica')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    def win_animation(self,W,H,screen,clock,FPS):
        k = 0

        color = (135, 206, 235)

        self.Map.Objects.clear()
        self.Map.All_Objects.clear()
        self.Map.Freshman = 0

        self.Map.Freshman = Player(Point(W / 2 - 100, H / 2), "Первокур Серега")
        self.Map.Freshman.animation.moveStatus = Orientation.Right

        while (k != 200):
            k += 1
            self.Map.Freshman.animation.show(self.Map.Freshman)
            self.Map.Freshman.point.x += 1

            screen.fill(color)
            screen.blit(self.Map.Freshman.animation.image, (self.Map.Freshman.point).tuple())
            self.draw_text(screen, "WINNER", 100, W / 2, H / 4, (255, 255, 255))
            pygame.display.update()
            pygame.display.flip()
            clock.tick(FPS)

        self.Map.Objects.clear()
        self.Map.Freshman = 0

    def losing_animation(self,W,H,screen,clock,FPS):

        color = (0, 0, 0)

        self.Map.Objects.clear()
        self.Map.All_Objects.clear()
        self.Map.Freshman = 0

        Mob=Mobs(Point(W / 2 - 100, H / 2), "Самый дикий препод",100)
        Mob.animation.moveStatus = Orientation.Left

        start_ticks = pygame.time.get_ticks()
        while (True):
            Mob.animation.show(Mob)
            Mob.point.x += 1

            screen.fill(color)
            screen.blit(Mob.animation.image, (Mob.point).tuple())
            self.draw_text(screen, "ВЫ ДЕД ИНСАЙД", 100, W / 2, H / 4, (255, 255, 255))
            pygame.display.update()
            pygame.display.flip()
            clock.tick(FPS)
            if (pygame.time.get_ticks()-start_ticks)>=6000:
                break

        self.Map.Objects.clear()
        self.Map.Freshman = 0