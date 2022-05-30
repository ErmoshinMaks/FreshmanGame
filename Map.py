from Objects import *

class Map:
    Objects = []
    All_Objects=[]
    Freshman=0
    gup=False
    running=True

    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    W = screen.get_width()
    H = screen.get_height()

    def add(self, Object):
        self.All_Objects.append(Object)


    def all_move(self,keys):
        if keys[pygame.K_g] and self.Freshman.Developer:
            self.invert()
        self.Freshman.move(keys,self)
        self.move_mobs()
        self.move_bullet()

    def move(self,keys):
        self.Freshman.Phys.v.x = Move_Const.zero.value

        self.check_hp()
        self.all_move(keys)
        #self.delete()

    def move_mobs(self):
        for obj in self.Objects:
            if type(obj) in [Mobs,Boss_Kozlov]:
                 obj.move(self)

    def move_bullet(self):
        for obj in self.Objects:
            if type(obj) in [Bullet,Poop]:
                if obj.point.x>obj.Point0.x+obj.maxlen or obj.point.x<obj.Point0.x-obj.maxlen:
                    obj.onmap="No"
                else:
                    self.bullet_damage(obj)
                    obj.move()

    def bullet_damage(self,bullet):
            for enemy in self.Objects:
                if type(enemy) in [Mobs,Boss_Kozlov] and bullet.check_collision(enemy):
                    enemy.get_damage(1)
            if type(bullet)==Poop and bullet.check_collision(self.Freshman):
                self.Freshman.get_damage(5)


    def check_hp(self):
        for obj in self.Objects:
            if type(obj) in [Mobs,Boss_Kozlov]:
                if obj.hp<=0:
                    if (obj.animation.moveStatus!=Orientation.Death):
                        self.Freshman.xp += 20
                        self.Freshman.maxhp += int(self.Freshman.xp ** 0.7 - (self.Freshman.xp - 20) ** 0.7) + 1
                        self.Freshman.hp += int(self.Freshman.xp ** 0.7 - (self.Freshman.xp - 20) ** 0.7) + 1
                    obj.death()

        if self.Freshman.hp<=0:
            self.Freshman.death()

        if self.Freshman.hp>self.Freshman.maxhp:
            self.Freshman.hp=self.Freshman.maxhp


    def spawn_objects(self):
        for object in self.All_Objects:
            if self.Freshman.point.x-self.W<object.point.x<=self.Freshman.point.x or self.Freshman.point.x<=object.point.x<self.Freshman.point.x+self.W:
                if not(object in self.Objects):
                    self.Objects.append(object)
            else:
                if object in self.Objects:
                    self.Objects.remove(object)

            if object.onmap=="No":
                if object in self.Objects:
                    self.Objects.remove(object)
                self.All_Objects.remove(object)
                if type(object) in [Boss_Kozlov]:
                    self.running = False


    def create_map(self,level):
        lines=[]
        platform_l = pygame.image.load(r"Sprites\Platform_Sprites\Normal_floor.png").convert_alpha()
        platform_s=pygame.image.load(r"Sprites\Platform_Sprites\Normal_platform.png").convert_alpha()
        platform_d = pygame.image.load(r"Sprites\Platform_Sprites\Damaging_platform.png").convert_alpha()
        platform_k = pygame.image.load(r"Sprites\Platform_Sprites\Killing_platform.png").convert_alpha()
        platform_a = pygame.image.load(r"Sprites\Platform_Sprites\Lava_floor.png").convert_alpha()
        cloud=pygame.image.load(r"Sprites\Cloud_Sprites\1.png").convert_alpha()
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
                    self.add(Mobs(Point(long*j+225,hight*(i+1)-259), "Самый дикий препод",100))
                if lines[i][j]=="3":#маленькие платформы
                    self.add(Platform(platform_s,Point(long*j+225,hight*i),"Platform"))
                if lines[i][j]=="4":#облака
                    self.add(Cloud(cloud,Point(long*j+225,hight*i),"Cloud"))
                if lines[i][j]=="5":#игрок
                    self.Freshman=Player(Point(long*j+225,hight*i), "Первокур Серега")
                if lines[i][j]=="7":#платформа, которая делает кусь
                    self.add(DamagePlatform(platform_d,Point(long*j+225,hight*i),"Damaging Platform", 1))
                if lines[i][j]=="8":#прыгай, но не стой
                    self.add(KillingPlatform(platform_k,Point(long*j+225,hight*i),"Killing Platform", 999))
                if lines[i][j]=="9":#пол — это лава
                    self.add(DamagePlatform(platform_a,Point(long*j,hight*i),"Lava", 99))
                if lines[i][j]=="k":#моб как узнать размеры спрайта?
                    self.add(Boss_Kozlov(Point(long*j+115,hight*(i+1)-166), "Типа Козлов",1000))


    def invert(self):
        self.Freshman.Phys.w.y=-self.Freshman.Phys.w.y
        self.gup = not self.gup


def cmp_Point(a,b):
    return a.point.x>b.point.x