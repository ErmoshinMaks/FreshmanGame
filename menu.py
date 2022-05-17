import pygame
import sys
import enum

class Button_status(enum.Enum):
    Start="Старт"
    Finish="Выход"
    level1='1'
    level2='2'
    level3='3'
    level4='4'
    Non="Ничего"

class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text = text
        f1 = pygame.font.Font(None, 36)
        self.text_surf = f1.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self,screen):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

    def change_text(self, newtext):
        f1 = pygame.font.Font(None, 36)
        self.text_surf = f1.render(newtext, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
                return True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    #print('click')
                    self.pressed = False
                    self.change_text(self.text)
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'



class Menu(pygame.sprite.Sprite):
    #background=pygame.image.load(r"Sprites\menu.png").convert_alpha()
    running = True
    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    W = screen.get_width()
    H = screen.get_height()
    FPS = 60
    color = (255, 250, 250)
    clock = pygame.time.Clock()

    button1 = Button('Старт', 200, 40, (W//2-90, H//2-200), 5)
    #button2 = Button('Уровни', 200, 40, (W//2-90, H//2+100), 5)
    button3 = Button('Выход', 200, 40, (W//2-90, H//2+350), 5)
    buttons = [button1,button3]
    button_pressed=Button_status.Non

    def show_levels(self):
        button_lvl1=Button('Уровень 1', 200, 40, (self.W//2-300, self.H//2-100), 5)
        button_lvl2=Button('Уровень 2', 200, 40, (self.W//2-90, self.H//2-100), 5)
        button_lvl3=Button('Уровень 3', 200, 40, (self.W//2+120, self.H//2-100), 5)
        button_lvl4=Button('Уровень 4', 200, 40, (self.W//2+330, self.H//2-100), 5)
        self.buttons.append(button_lvl1)
        self.buttons.append(button_lvl2)
        self.buttons.append(button_lvl3)
        self.buttons.append(button_lvl4)


    def buttons_draw(self):
        for b in self.buttons:
            b.draw(self.screen)

    def check_click(self):
        for b in self.buttons:
            if b.check_click():
                if b.text=='Старт':
                    self.button_pressed=Button_status.Start
                if b.text=='Выход':
                    self.button_pressed=Button_status.Finish
                if b.text=='Уровень 1':
                    self.button_pressed=Button_status.level1
                if b.text=='Уровень 2':
                    self.button_pressed=Button_status.level2
                if b.text=='Уровень 3':
                    self.button_pressed=Button_status.level3
                if b.text=='Уровень 4':
                    self.button_pressed=Button_status.level4
                break

    def show_menu(self,Engine,UI):
        while self.running:

            for i in pygame.event.get():
                if self.button_pressed==Button_status.Finish:
                    sys.exit()

                if self.button_pressed==Button_status.Start:
                    self.show_levels()
                #уровни
                if self.button_pressed==Button_status.level1:
                    self.button_pressed=Button_status.Non
                    Engine.game_cycle(UI,Button_status.level1)

                if self.button_pressed==Button_status.level2:
                    self.button_pressed = Button_status.Non
                    Engine.game_cycle(UI,Button_status.level2)

                if self.button_pressed==Button_status.level3:
                    self.button_pressed = Button_status.Non
                    Engine.game_cycle(UI,Button_status.level3)

            self.screen.fill(self.color)
            self.buttons_draw()
            self.check_click()
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(self.FPS)


