import pygame
import enum
pygame.init()

class Abstract_object(pygame.sprite.Sprite):
    def __init__(self,image,point,name="unknown",onmap="Yes"):
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.Point = point
        self.rect = self.image.get_rect(centerx=self.Point.x,centery=self.Point.y)
        self.name=name
        self.onmap=onmap


class Material(Abstract_object):
    def __init__(self,image,point,Name):
        super().__init__(image,point,Name)

    def check_collision(self, Object):#переписать это говно, используется в основном для пули
        return (Object.Point.x<=self.Point.x<=Object.Point.x+Object.image.get_width() and \
        Object.Point.y<=self.Point.y<=Object.Point.y+Object.image.get_height())


class NotMaterial(Abstract_object):
    def __init__(self,image,point,Name):
        super().__init__(image,point,Name)


class Cloud(NotMaterial):
    def __init__(self,image,point,Name):
        super().__init__(image,point,Name)



class Creature(Material):
    def __init__(self,image,point,Name,moveStatus,hp=100,maxhp=100,xp=0):
        super().__init__(image,point,Name)
        self.hp=hp
        self.maxhp=maxhp
        self.xp=xp
        self.Phys = Physics(x=point.x, y=point.y, vx=0, vy=0, wx=0, wy=Move_Const.g.value, width=image.get_rect().width, height=image.get_rect().height)
        #self.GroupSprites = GroupSprites
        self.moveStatus = moveStatus
        self.animation_progress = 0


class Block(Material):
    def __init__(self,image,point,Name):
        super().__init__(image,point,Name)

    def left(self):
        return self.Point.x

    def right(self):
        return self.Point.x+self.image.get_rect().width

    def up(self):
        return self.Point.y

    def down(self):
        return self.Point.y+self.image.get_rect().height

class Platform(Block):
    def __init__(self,image,point,Name):
        super().__init__(image,point,Name)


class Human(Creature):
    def __init__(self,image,point,Name,moveStatus,shoot_progress=0,hp=100, maxhp=100, xp=0):
        super().__init__(image,point,Name,moveStatus,hp,maxhp,xp)
        self.shoot_progress=shoot_progress

    def move(self):
        self.animation()
        self.Phys.move()
        self.Phys.size.x = self.image.get_rect().width
        self.Phys.size.y = self.image.get_rect().height


class Player(Human):
    def __init__(self,image,point,Name,moveStatus,shoot_progress=0,hp=100, maxhp=100, xp=0):
        super().__init__(image,point,Name,moveStatus,hp,maxhp,xp)
        self.Animation = Animation(self.load_sprites(), self.moveStatus,type(self))  # Sprites = [стоит, движение,смерть,стрельба]
        self.shoot_progress=shoot_progress
        self.maxhp=100

    def move(self,keys,Map):
        #показания хп
        # screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        # f1 = pygame.font.Font(None, 36)
        # text1 = f1.render(str(self.hp), True,(180, 0, 0))
        # screen.blit(text1,(self.Point.x+self.image.get_width()//2,self.Point.y-self.image.get_height()//2))

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT] and not Map.gup:
            self.Phys.v.x = Move_Const.vx.value
            self.Animation.moveStatus=Orientation.UpRight
            if self.Phys.crd.y == self.Phys.y0:
                self.Phys.v.y = -Move_Const.vy.value

        elif keys[pygame.K_UP] and keys[pygame.K_LEFT] and not Map.gup:
            self.Animation.moveStatus = Orientation.UpLeft
            self.Phys.v.x = -Move_Const.vx.value
            if self.Phys.crd.y == self.Phys.y0:
                self.Phys.v.y = -Move_Const.vy.value

        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] and Map.gup:
            self.Phys.v.x = Move_Const.vx.value
            self.Animation.moveStatus=Orientation.UpRight
            if self.Phys.crd.y == self.Phys.y0:
                self.Phys.v.y = Move_Const.vy.value

        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and Map.gup:
            self.Animation.moveStatus = Orientation.UpLeft
            self.Phys.v.x = -Move_Const.vx.value
            if self.Phys.crd.y == self.Phys.y0:
                self.Phys.v.y = Move_Const.vy.value

        elif keys[pygame.K_LEFT]:
            self.Animation.moveStatus = Orientation.Left
            self.Phys.v.x = -Move_Const.vx.value


        elif keys[pygame.K_RIGHT]:
            self.Animation.moveStatus = Orientation.Right
            self.Phys.v.x = Move_Const.vx.value


        elif keys[pygame.K_UP]:
            if not Map.gup:
                if self.Phys.crd.y == self.Phys.y0:
                    self.Phys.v.y = -Move_Const.vy.value
            else:
                self.Animation.moveStatus = Orientation.Down


        elif keys[pygame.K_DOWN]:
            if not Map.gup:
                self.Animation.moveStatus = Orientation.Down
            else:
                if self.Phys.crd.y == self.Phys.y0:
                    self.Phys.v.y = -Move_Const.vy.value

        else:
            self.Animation.moveStatus=Orientation.Non

        if keys[pygame.K_h]:
            self.hp=min(self.hp+4, self.maxhp)

        if keys[pygame.K_d]:
            self.hp=max(self.hp-1, 0)

        if keys[pygame.K_o]:
            self.hp = 0

        if keys[pygame.K_f]:
            self.hp=self.maxhp

        if keys[pygame.K_q]:
            self.Animation.moveStatus = Orientation.Bullet_Left
            self.shoot_progress += 1
            self.shoot(Map)

        elif keys[pygame.K_e]:
            self.Animation.moveStatus = Orientation.Bullet_Right
            self.shoot_progress += 1
            self.shoot(Map)

        self.Animation.show(self)
        self.Phys.move()
        self.Phys.interactions(Map.Objects)
        if self.Phys.dam>0 and self.Phys.crd.y==self.Phys.y0:
            self.hp=max(self.hp-self.Phys.dam,0)

        screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        W = screen.get_width()
        H = screen.get_height()
        self.Phys.d = Point(W // 2, H // 2) - self.Phys.crd
        self.Point = self.Phys.crd

    def death(self):
        self.Animation.moveStatus=Orientation.Death


    def shoot(self,Map):
            if(self.shoot_progress%11==0):#11 заменить на enum как?
                bullet = pygame.image.load(r"Sprites\Bullet_Sprites\bullet.png").convert_alpha()

                if(self.Animation.moveStatus==Orientation.Bullet_Right):
                    point=self.Point+Point(self.image.get_rect().width,self.image.get_rect().height//2+40)

                elif(self.Animation.moveStatus==Orientation.Bullet_Left):
                    point=self.Point+Point(-self.image.get_rect().width+100,self.image.get_rect().height//2+40)

                Bullet_o=Bullet(bullet,point, "Пуля",self.Animation.moveStatus)
                bullet_sound=pygame.mixer.Sound(r"SFX\bullet.mp3")
                bullet_sound.play()
                Map.add(Bullet_o)

    def load_sprites(self):
        leftGroup = [pygame.image.load(r"Sprites\Freshman_Sprites\2.png").convert_alpha(),
                     pygame.image.load(r"Sprites\Freshman_Sprites\3.png").convert_alpha(),
                     pygame.image.load(r"Sprites\Freshman_Sprites\4.png").convert_alpha(),
                     pygame.image.load(r"Sprites\Freshman_Sprites\5.png").convert_alpha()]

        rightGroup = [pygame.image.load(r"Sprites\Freshman_Sprites\6.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\7.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\8.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\9.png").convert_alpha()]

        downGroup = [pygame.image.load(r"Sprites\Freshman_Sprites\10.png").convert_alpha(),
                     pygame.image.load(r"Sprites\Freshman_Sprites\11.png").convert_alpha(),
                     pygame.image.load(r"Sprites\Freshman_Sprites\12.png").convert_alpha()]

        shootGroup = [pygame.image.load(r"Sprites\Freshman_Sprites\pistol_left.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\pistol_right.png").convert_alpha()]

        deathGroup = [pygame.image.load(r"Sprites\Freshman_Sprites\Death.png").convert_alpha()]

        # Group = [стоит, движение,смерть,стрельба]
        Group = [pygame.image.load(r"Sprites\Freshman_Sprites\1.png").convert_alpha(),
                 [leftGroup, rightGroup, downGroup], deathGroup, shootGroup]
        return Group

class Mobs(Human):#создать класс анимации
    def __init__(self,image,point,Name,moveStatus,hp):
        super().__init__(image,point, Name, moveStatus, hp)
        self.GroupSprites = self.load_sprites()
        self.image = pygame.image.load(r"Sprites\Mobs_Sprites\1.png").convert_alpha()
        self.Animation = Animation(self.load_sprites(), moveStatus, type(self))
        self.Point0 = point.copy()

    def move(self,Map):
        self.Animation.show(self)
        if self.Animation.moveStatus == Orientation.Left:
            self.Point.x += 2
            if self.Point.x > self.Point0.x + 250:
                self.Animation.moveStatus = Orientation.Right
        elif self.Animation.moveStatus == Orientation.Right:
            self.Point.x -= 2
            if self.Point.x < self.Point0.x - 250:
                self.Animation.moveStatus = Orientation.Left
        self.damage(Map.Freshman)
        self.Phys.interactions(Map.Objects)

    def damage(self,Freshman):
        if (Freshman.Phys.crd.x <= self.Point.x+self.image.get_width() <= Freshman.Phys.crd.x + Freshman.image.get_width() and Freshman.Phys.crd.y <= self.Point.y++self.image.get_height() <= Freshman.Phys.crd.y + Freshman.image.get_height()):
            Freshman.hp=max(Freshman.hp-1, 0)


    def death(self):
        self.Animation.moveStatus=Orientation.Death

    def load_sprites(self):
        leftGroup = [pygame.image.load(r"Sprites\Mobs_Sprites\2.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Mobs_Sprites\3.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Mobs_Sprites\4.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Mobs_Sprites\5.png").convert_alpha()]

        rightGroup = [pygame.image.load(r"Sprites\Mobs_Sprites\6.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Mobs_Sprites\7.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Mobs_Sprites\8.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Mobs_Sprites\9.png").convert_alpha()]
        deathGroup = [pygame.image.load(r"Sprites\Mobs_Sprites\10.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Mobs_Sprites\11.png").convert_alpha()]
        shootGroup=[]

        Group = [pygame.image.load(r"Sprites\Mobs_Sprites\1.png").convert_alpha(), [leftGroup, rightGroup], deathGroup,
                 shootGroup]
        return Group




class Damage_Object:
    def __init__(self, damage):
        self.damage=damage

class Bullet(Material):#тут должно быть множественное наследование
    def __init__(self,image,point,Name,moveStatus):
        super().__init__(image,point,Name)
        self.moveStatus=moveStatus
        self.Point0=point.copy()

    def move(self):
        if self.moveStatus == Orientation.Bullet_Right:
            self.Point.x+=10
        elif self.moveStatus == Orientation.Bullet_Left:
            self.Point.x-=10
        elif self.moveStatus==Orientation.Non:
            self.Point.x += 10



class DamagePlatform(Damage_Object,Block):
    def __init__(self,image,point,Name,damage):
        Block.__init__(self,image,point,Name)
        Damage_Object.__init__(self,damage)

class KillingPlatform(Damage_Object,Block):
    def __init__(self,image,point,Name,damage,tchd=False):
        Block.__init__(self,image,point,Name)
        Damage_Object.__init__(self,damage)
        self.tchd=tchd

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, p2):
        return Point(self.x + p2.x, self.y + p2.y)

    def __sub__(self, p2):
        return Point(self.x - p2.x, self.y - p2.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)

    def __truediv__(self, n):
        return Point(self.x / n, self.y / n)

    def tuple(self):
        return (self.x, self.y)

    def copy(self):
        return Point(self.x,self.y)

class Physics:#добавить методы для столкновений
    def __init__(self, x=0, y=0, vx=0, vy=0, wx=0, wy=0, y0=90000, x1=0, x2=1000, width=0, height=0, dx=0, dy=0, dam=0):
        self.crd = Point(x, y)
        self.v = Point(vx, vy)
        self.w = Point(wx, wy)
        self.y0 = y0#изменить название
        self.x1 = x1#изменить название
        self.x2 = x2#изменить название
        self.size = Point(width, height)
        self.d = Point(dx, dy)#изменить название
        self.dam = 0

    def left(self):
        return self.crd.x

    def right(self):
        return self.crd.x+self.size.x

    def up(self):
        return self.crd.y

    def down(self):
        return self.crd.y+self.size.y

    def move(self):
        self.crd += self.v
        self.v += self.w
        if self.crd.y >= self.y0:
            self.crd.y = self.y0
            self.v.y = 0

    def checkside(self, Object):
        return self.right() >= Object.left() and self.left() <= Object.right() and \
               self.up() < Object.down() and self.down() > Object.up()

    def checkleft(self, Object):
        return self.left() < Object.left() and self.v.x > 0

    def checkright(self, Object):
        return self.left() > Object.left() and self.v.x < 0

    def checkup(self, Object):
        return self.right() > Object.left() and \
        self.left() < Object.right() and \
        self.down() <= Object.up() and \
        Object.up() - self.size.y <= self.y0

    def checkdown(self, Object):
        return self.right() > Object.left() and \
                self.left() < Object.right() and \
                self.up() < Object.down() and \
                self.up() > Object.up() and \
                self.v.y < 0

    def checkfall(self, Object):
        return self.right() <= self.x1 or self.left() >= self.x2

    def interactions(self, Objects):
        for Object in Objects:
            if type(Object)==Platform or type(Object)==DamagePlatform or type(Object)==KillingPlatform:
                if self.checkup(Object):
                    self.y0 = Object.up() - self.size.y
                    self.x1 = Object.left()
                    self.x2 = Object.right()
                    if type(Object)==DamagePlatform:
                        self.dam = Object.damage
                    elif type(Object)==Platform:
                        self.dam = 0

                    if type(Object) == KillingPlatform:
                        if self.crd.y==self.y0:
                            if Object.tchd:
                                self.dam = Object.damage
                                Object.tchd = False
                            else:
                                self.dam = 0
                                Object.tchd = True
                        else:
                            Object.tchd = False
                    elif type(Object)==Platform:
                        self.dam = 0

                if self.checkdown(Object):
                    self.v.y = 0
                    self.crd.y = Object.down()

                elif self.checkside(Object):
                    if self.checkleft(Object):
                        self.v.x = 0
                        self.crd.x = Object.left() - self.size.x
                    if self.checkright(Object):
                        self.v.x = 0
                        self.crd.x = Object.right()
                if self.checkfall(Object):
                    self.y0 = 100000
                    self.x1 = -100000
                    self.x2 = 100000


class Animation:
    animation_move=None
    animation_death=None
    animation_shoot=None

    def __init__(self,sprites,moveStatus,type_obj):
        self.type_obj = type_obj
        self.animation_progress=0
        self.moveStatus=moveStatus
        self.animotion_stand=sprites[0]
        self.animation_move=Animation_move(sprites[1],type_obj)
        self.animation_death = Animation_death(sprites[2], type_obj)
        self.animation_shoot = Animation_shoot(sprites[3], type_obj)


    def show(self,Object):
        self.animation_progress+=1
        if Object.hp>0:
            self.animation_move.show(Object,self)
            self.animation_shoot.show(Object,self)
            if self.moveStatus == Orientation.Non:
                Object.image = self.animotion_stand

        else:
            self.animation_death.show(Object,self)


class Animation_move:
    def __init__(self,sprites,type_obj):#sprites=[левая,правая,...]
        self.sprites = sprites
        self.type_obj = type_obj

    def show(self,Object,main_anim):
        if main_anim.moveStatus == Orientation.UpRight:
            Object.image = self.sprites[1][0]

        elif main_anim.moveStatus == Orientation.Right:
            Object.image = self.sprites[1][int(main_anim.animation_progress // 8) % len(self.sprites[1])]

        elif main_anim.moveStatus == Orientation.UpLeft:
            Object.image = self.sprites[0][0]

        elif main_anim.moveStatus == Orientation.Left:
            Object.image = self.sprites[0][int(main_anim.animation_progress // 8) % len(self.sprites[0])]

        elif main_anim.moveStatus == Orientation.Down and type(self.type_obj)==type(Player):
            Object.image = self.sprites[2][int(main_anim.animation_progress // 8) % len(self.sprites[2])]

class Animation_death:
    def __init__(self,sprites,type_obj):#sprites=смерть
        self.sprites = sprites
        self.type_obj = type_obj

    def show(self, Object, main_anim):
        Object.image = self.sprites[0]
        if main_anim.animation_progress % 157 == 0:
            Object.onmap="No"

class Animation_shoot:
    def __init__(self,sprites,type_obj):#sprites=[влево,вправо]
        self.sprites = sprites
        self.type_obj = type_obj

    def show(self, Object, main_anim):
        if main_anim.moveStatus == Orientation.Bullet_Right:  # "Space"
            Object.image = self.sprites[1]

        elif main_anim.moveStatus == Orientation.Bullet_Left:  # "Space"
            Object.image = self.sprites[0]


class Orientation(enum.Enum):#разделить на разные енамы
    Left="Left"
    Right="Right"
    UpRight="UpRight"
    UpLeft="UpLeft"
    Down="Down"
    Non="None"
    Space="Space"
    Bullet_Right="Bullet_Right"
    Bullet_Left="Bullet_Left"
    Death="Death"

class Move_Const(enum.Enum):
    vx=7
    vy=9
    zero=0
    g=0.15

