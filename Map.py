from Abstract_object import *
import pygame
import sys



class Map:
    Objects = []
    Freshman=0
    gup=False

    # def __init__(self,player):
    #     self.Freshman=player

    def add(self, Object):
        self.Objects.append(Object)


    def move(self,keys):
        self.Freshman.Phys.v.x = Move_Const.zero.value

        self.check_hp()
        self.all_move(keys)
        self.delete()

    def paint(self,screen):
        for obj in self.Objects:
            screen.blit(obj.image, (obj.Point + self.Freshman.Phys.d).tuple())
        screen.blit(self.Freshman.image, (self.Freshman.Point + self.Freshman.Phys.d).tuple())
        pygame.draw.rect(pygame.display.set_mode([0, 0], pygame.FULLSCREEN), (0, 0, 0),
                         (100, 100, self.Freshman.maxhp, 20))
        pygame.draw.rect(pygame.display.set_mode([0, 0], pygame.FULLSCREEN), (0, 192, 0),
                         (100, 100, self.Freshman.hp, 20))
        f1 = pygame.font.Font(None, 36)
        text = f1.render(f"{self.Freshman.hp} / {self.Freshman.maxhp}", True,
                          (0, 0, 0))
        screen.blit(text, (100+self.Freshman.maxhp+20, 98))

    def all_move(self,keys):
        if keys[pygame.K_g]:
            self.invert()

        self.Freshman.move(keys,self)
        self.move_mobs()
        self.move_bullet()

    def bullet_damage(self,bullet):
            for enemy in self.Objects:
                if type(enemy)==Mobs and bullet.check_collision(enemy):
                    enemy.hp-=1

    def check_hp(self):
        for obj in self.Objects:
            if type(obj)==Mobs:
                if obj.hp<=0:
                    if (obj.Animation.moveStatus!=Orientation.Death):
                        self.Freshman.xp += 20
                        self.Freshman.maxhp += int(self.Freshman.xp ** 0.7 - (self.Freshman.xp - 20) ** 0.7) + 1
                        self.Freshman.hp += int(self.Freshman.xp ** 0.7 - (self.Freshman.xp - 20) ** 0.7) + 1
                    obj.death()

        if self.Freshman.hp<=0:
            self.Freshman.death()

        if self.Freshman.hp>self.Freshman.maxhp:
            self.Freshman.hp=self.Freshman.maxhp


    def delete(self):
        for obj in self.Objects:
            if obj.onmap=="No":
                self.Objects.remove(obj)
        # if self.Freshman.onmap=="No":
        #     sys.exit()

    def move_mobs(self):
        for obj in self.Objects:
            if type(obj)==Mobs:
                 obj.move(self)

    def move_bullet(self):
        for obj in self.Objects:
            if type(obj)==Bullet:
                if obj.Point.x>obj.Point0.x+400 or obj.Point.x<obj.Point0.x-400:
                    obj.onmap="No"
                else:
                    self.bullet_damage(obj)
                    obj.move()

    def create_map(self,level):
        lines=[]
        platform_l = pygame.image.load(r"Sprites\Platform_Sprites\Normal_floor.png").convert_alpha()
        Mobs_sprite1 = pygame.image.load(r"Sprites\Mobs_Sprites\1.png").convert_alpha()
        platform_s=pygame.image.load(r"Sprites\Platform_Sprites\Normal_platform.png").convert_alpha()
        platform_d = pygame.image.load(r"Sprites\Platform_Sprites\Damaging_platform.png").convert_alpha()
        platform_k = pygame.image.load(r"Sprites\Platform_Sprites\Killing_platform.png").convert_alpha()
        platform_a = pygame.image.load(r"Sprites\Platform_Sprites\Lava_floor.png").convert_alpha()
        cloud=pygame.image.load(r"Sprites\Cloud_Sprites\1.png").convert_alpha()
        player = pygame.image.load(r"Sprites\Freshman_Sprites\1.png").convert_alpha()
        #одна ячейка
        long=500
        hight=225
        path_level='Maps/'+level.value+'.txt'
        file=open(path_level,'r')
        for line in file:
            lines.append(line)

        for i in range(len(lines)-1,0-1,-1):
            for j in range(len(lines[i])):
                if lines[i][j]=="1":#длинная платформа
                    self.add(Platform(platform_l, Point(long*j,hight*i), "Floor"))
                if lines[i][j]=="2":#моб как узнать размеры спрайта?
                    self.add(Mobs(Mobs_sprite1, Point(long*j+225,hight*(i+1)-259), "Самый дикий препод", Orientation.Right,100))
                if lines[i][j]=="3":#маленькие платформы
                    self.add(Platform(platform_s,Point(long*j+225,hight*i),"Platform"))
                if lines[i][j]=="4":#облака
                    self.add(Cloud(cloud,Point(long*j+225,hight*i),"Cloud"))
                if lines[i][j]=="5":#игрок
                    self.Freshman=Player(player, Point(long*j+225,hight*i), "Первокур Серега", "None")
                if lines[i][j]=="7":#платформа, которая делает кусь
                    self.add(DamagePlatform(platform_d,Point(long*j+225,hight*i),"Damaging Platform", 1))
                if lines[i][j]=="8":#прыгай, но не стой
                    self.add(KillingPlatform(platform_k,Point(long*j+225,hight*i),"Killing Platform", 999))
                if lines[i][j]=="9":#пол — это лава
                    self.add(DamagePlatform(platform_a,Point(long*j+225,hight*i),"Lava", 99))

    def invert(self):
        self.Freshman.Phys.w.y=-self.Freshman.Phys.w.y
        self.gup = not self.gup