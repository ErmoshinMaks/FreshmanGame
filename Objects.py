from VirtualClasses import *
from Enums import *

class Cloud(NotMaterial):
    def __init__(self,image,point,Name):
        super().__init__(point,Name)
        self.image=image

class Platform(Block):
    def __init__(self,image,point,Name):
        super().__init__(image,point,Name)


class Player(Human):
    def __init__(self,point,Name="Player",shoot_progress=0,hp=100, maxhp=100, xp=0):
        super().__init__(point,Name,shoot_progress,hp, maxhp, xp)
        self.animation = Animation(self.load_sprites(),Orientation.Non,type(self))  # Sprites = [стоит, движение,смерть,стрельба]
        self.Phys = Physics(x=point.x, y=point.y, vx=0, vy=0, wx=0, wy=Move_Const.g.value,
                            width=self.animation.image.get_rect().width, height=self.animation.image.get_rect().height)
        self.shoot_progress=shoot_progress
        self.maxhp=100
        self.Developer=False

    def move(self,keys,Map):
        if keys[pygame.K_F1] and keys[pygame.K_F2]:
            if self.Developer==False:
                self.Developer=True
            else:
                self.Developer = False
        elif keys[pygame.K_SPACE] and keys[pygame.K_RIGHT]:
                self.animation.moveStatus = Orientation.Bullet_Right_move
                self.animation.last_status = Orientation.Right
                self.shoot_progress += 1
                self.Phys.v.x = Move_Const.vx.value
                self.shoot(Map)

        elif keys[pygame.K_SPACE] and keys[pygame.K_LEFT]:
                self.animation.moveStatus = Orientation.Bullet_Left_move
                self.animation.last_status = Orientation.Left
                self.shoot_progress += 1
                self.Phys.v.x = -Move_Const.vx.value
                self.shoot(Map)

        elif keys[pygame.K_SPACE] and keys[pygame.K_UP]:
                self.animation.moveStatus=Orientation.Bullet_stand
                if not Map.gup:
                    if self.Phys.crd.y == self.Phys.y0:
                        self.Phys.v.y = -Move_Const.vy.value
                else:
                    self.animation.moveStatus = Orientation.Down
                self.shoot_progress += 1
                self.shoot(Map)

        elif keys[pygame.K_SPACE]:
                self.animation.moveStatus=Orientation.Bullet_stand
                self.shoot_progress += 1
                self.shoot(Map)

        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT] and not Map.gup:
            self.Phys.v.x = Move_Const.vx.value
            self.animation.moveStatus=Orientation.UpRight
            if self.Phys.crd.y == self.Phys.y0:
                self.Phys.v.y = -Move_Const.vy.value

        elif keys[pygame.K_UP] and keys[pygame.K_LEFT] and not Map.gup:
            self.animation.moveStatus = Orientation.UpLeft
            self.Phys.v.x = -Move_Const.vx.value
            if self.Phys.crd.y == self.Phys.y0:
                self.Phys.v.y = -Move_Const.vy.value

        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] and Map.gup:
            self.Phys.v.x = Move_Const.vx.value
            self.animation.moveStatus=Orientation.UpRight
            if self.Phys.crd.y == self.Phys.y0:
                self.Phys.v.y = Move_Const.vy.value

        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and Map.gup:
            self.animation.moveStatus = Orientation.UpLeft
            self.Phys.v.x = -Move_Const.vx.value
            if self.Phys.crd.y == self.Phys.y0:
                self.Phys.v.y = Move_Const.vy.value

        elif keys[pygame.K_LEFT]:
            self.animation.moveStatus = Orientation.Left
            self.Phys.v.x = -Move_Const.vx.value


        elif keys[pygame.K_RIGHT]:
            self.animation.moveStatus = Orientation.Right
            self.Phys.v.x = Move_Const.vx.value


        elif keys[pygame.K_UP]:
            if not Map.gup:
                if self.Phys.crd.y == self.Phys.y0:
                    self.Phys.v.y = -Move_Const.vy.value
            else:
                self.animation.moveStatus = Orientation.Down


        elif keys[pygame.K_DOWN]:
            if not Map.gup:
                self.animation.moveStatus = Orientation.Down
            else:
                if self.Phys.crd.y == self.Phys.y0:
                    self.Phys.v.y = -Move_Const.vy.value

        elif keys[pygame.K_h] and self.Developer:
            self.hp=min(self.hp+4, self.maxhp)

        elif keys[pygame.K_d] and self.Developer:
            self.get_damage(1)

        elif keys[pygame.K_o] and self.Developer:
            self.get_damage(self.hp)

        elif keys[pygame.K_f] and self.Developer:
            self.hp=self.maxhp

        else:
            self.animation.moveStatus=Orientation.Non

        self.animation.show(self)
        self.Phys.move()
        self.Phys.interactions(Map.Objects)
        if self.Phys.dam>0 and self.Phys.crd.y==self.Phys.y0:
            self.get_damage(self.Phys.dam)

        screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        W = screen.get_width()
        H = screen.get_height()
        self.Phys.d = Point(W // 2, H // 2) - self.Phys.crd
        self.Point = self.Phys.crd

    def get_damage(self, dmg):
        damage_sound = pygame.mixer.Sound(r"SFX\damage_player.mp3")
        damage_sound.play()
        self.hp = max(self.hp - dmg, 0)

    def death(self):
        self.animation.moveStatus=Orientation.Death

    def shoot(self,Map):
            if(self.shoot_progress%11==0):#11 заменить на enum как?

                if self.animation.moveStatus == Orientation.Bullet_Right_move:
                    point=self.Point+Point(self.animation.image.get_rect().width,self.animation.image.get_rect().height//2+50)

                elif self.animation.moveStatus == Orientation.Bullet_Left_move:
                    point=self.Point+Point(-self.animation.image.get_rect().width+100,self.animation.image.get_rect().height//2+50)

                elif self.animation.moveStatus==Orientation.Bullet_stand:
                    if self.animation.last_status in [Orientation.Right,Orientation.UpRight]:
                        point = self.Point + Point(self.animation.image.get_rect().width,self.animation.image.get_rect().height // 2 + 50)

                    elif self.animation.last_status in [Orientation.Left,Orientation.UpLeft]:
                        point = self.Point + Point(-self.animation.image.get_rect().width + 100,self.animation.image.get_rect().height // 2 + 50)

                Bullet_o=Bullet(point, "Пуля",self.animation.last_status)
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

        shootGroup = [[pygame.image.load(r"Sprites\Freshman_Sprites\13.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\14.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\15.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\16.png").convert_alpha()],
                      [pygame.image.load(r"Sprites\Freshman_Sprites\17.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\18.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\19.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\20.png").convert_alpha()],
                      [pygame.image.load(r"Sprites\Freshman_Sprites\21.png").convert_alpha(),
                      pygame.image.load(r"Sprites\Freshman_Sprites\22.png").convert_alpha()]]

        deathGroup = [pygame.image.load(r"Sprites\Freshman_Sprites\Death.png").convert_alpha()]

        # Group = [стоит, движение,смерть,стрельба]
        Group = [pygame.image.load(r"Sprites\Freshman_Sprites\1.png").convert_alpha(),
                 [leftGroup, rightGroup, downGroup], deathGroup, shootGroup]
        return Group

class Mobs(Human):#создать класс анимации
    def __init__(self,point,Name,hp):
        super().__init__(point, Name, hp)
        self.animation = Animation(self.load_sprites(),Orientation.Right, type(self))
        self.Point0 = point.copy()
        self.Phys = Physics(x=point.x, y=point.y, vx=0, vy=0, wx=0, wy=Move_Const.g.value,
                            width=self.animation.image.get_rect().width, height=self.animation.image.get_rect().height)

    def move(self,Map):
        self.animation.show(self)
        if self.animation.moveStatus == Orientation.Left:
            self.Point.x += 2
            if self.Point.x > self.Point0.x + 250:
                self.animation.moveStatus = Orientation.Right
        elif self.animation.moveStatus == Orientation.Right:
            self.Point.x -= 2
            if self.Point.x < self.Point0.x - 250:
                self.animation.moveStatus = Orientation.Left
        self.damage(Map.Freshman)
        self.Phys.interactions(Map.Objects)

    def damage(self,Freshman):
        if (Freshman.Phys.crd.x <= self.Point.x+self.animation.image.get_width() <= Freshman.Phys.crd.x + Freshman.animation.image.get_width() and Freshman.Phys.crd.y <= self.Point.y++self.animation.image.get_height() <= Freshman.Phys.crd.y + Freshman.animation.image.get_height()):
            Freshman.get_damage(1)


    def death(self):
        self.animation.moveStatus=Orientation.Death

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


class Bullet(Damage_Object):
    def __init__(self,point,Name,moveStatus,damage=1,onmap="Yes"):
        super().__init__(damage)
        self.Point=point
        self.Name=Name
        self.image=pygame.image.load(r"Sprites\Bullet_Sprites\red_bullet.png").convert_alpha()
        self.moveStatus=moveStatus
        self.Point0=point.copy()
        self.onmap=onmap
        self.shoot_progress=0

    def move(self):
        if self.moveStatus in [Orientation.Right,Orientation.UpRight]:
            self.Point.x+=15
        elif self.moveStatus in [Orientation.Left,Orientation.UpLeft]:
            self.Point.x-=15


    def check_collision(self, Object):#переписать это говно
        return (Object.Point.x<=self.Point.x<=Object.Point.x+Object.animation.image.get_width() and \
        Object.Point.y<=self.Point.y<=Object.Point.y+Object.animation.image.get_height())

class Poop(Damage_Object):
    def __init__(self,point,Name,moveStatus,damage=1,onmap="Yes"):
        super().__init__(damage)
        self.Point=point
        self.Name=Name
        self.image=pygame.image.load(r"Sprites\Bullet_Sprites\blue_bullet.png").convert_alpha()
        self.moveStatus=moveStatus
        self.Point0=point.copy()
        self.onmap=onmap
        self.shoot_progress=0

    def move(self):
        if self.moveStatus in [Orientation.Right,Orientation.UpRight]:
            self.Point.x-=7
        elif self.moveStatus in [Orientation.Left,Orientation.UpLeft]:
            self.Point.x+=7


    def check_collision(self, Object):#переписать это говно
        return (Object.Point.x<=self.Point.x<=Object.Point.x+Object.animation.image.get_width() and \
        Object.Point.y<=self.Point.y<=Object.Point.y+Object.animation.image.get_height())

class Boss_Kozlov(Human):
    def __init__(self,point,Name,hp):
        super().__init__(point, Name,hp)
        self.animation = Animation(self.load_sprites(),Orientation.Right, type(self))
        self.Point0 = point.copy()
        self.Phys = Physics(x=point.x, y=point.y, vx=0, vy=0, wx=0, wy=Move_Const.g.value,
                            width=self.animation.image.get_rect().width, height=self.animation.image.get_rect().height)

    def move(self,Map):
        self.animation.show(self)
        if self.animation.moveStatus == Orientation.Left:
            self.Point.x += 2
            self.shoot_progress+=1
            if Map.Freshman.Point.x+1000 >= self.Point.x:
                self.shoot(Map)
            if self.Point.x > self.Point0.x + 400:
                self.animation.moveStatus = Orientation.Right
        elif self.animation.moveStatus == Orientation.Right:
            self.Point.x -= 2
            self.shoot_progress += 1
            if Map.Freshman.Point.x+1000 >= self.Point.x:
                self.shoot(Map)
            if self.Point.x < self.Point0.x:
                self.animation.moveStatus = Orientation.Left
        self.damage(Map.Freshman)
        self.Phys.interactions(Map.Objects)

    def damage(self,Freshman):
        if (Freshman.Phys.crd.x <= self.Point.x+self.animation.image.get_width() <= Freshman.Phys.crd.x + Freshman.animation.image.get_width() and Freshman.Phys.crd.y <= self.Point.y++self.animation.image.get_height() <= Freshman.Phys.crd.y + Freshman.animation.image.get_height()):
            Freshman.hp=max(Freshman.hp-20, 0)

    def shoot(self,Map):
            if(self.shoot_progress%83==0):#11 заменить на enum как?

                if self.animation.moveStatus == Orientation.Left:
                    point=self.Point+Point(self.animation.image.get_rect().width+350,self.animation.image.get_rect().height//2+20)

                elif self.animation.moveStatus == Orientation.Right:
                    point=self.Point+Point(-self.animation.image.get_rect().width,self.animation.image.get_rect().height//2+20)

                Poop_o=Poop(point, "Какашка",self.animation.last_status)
                bullet_sound=pygame.mixer.Sound(r"SFX\bullet.mp3")
                bullet_sound.play()
                Map.add(Poop_o)

    def death(self):
        self.animation.moveStatus=Orientation.Death

    def load_sprites(self):
        rightGroup = [pygame.image.load(r"Sprites\Kozlov_Sprites\01.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Kozlov_Sprites\02.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Kozlov_Sprites\03.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Kozlov_Sprites\04.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\05.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\06.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\07.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\08.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\09.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\10.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\11.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\12.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\13.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\14.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\15.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\16.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\17.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\18.png").convert_alpha()]

        leftGroup = [pygame.image.load(r"Sprites\Kozlov_Sprites\19.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Kozlov_Sprites\20.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Kozlov_Sprites\21.png").convert_alpha(),
                        pygame.image.load(r"Sprites\Kozlov_Sprites\22.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\23.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\24.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\25.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\26.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\27.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\28.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\29.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\30.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\31.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\32.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\33.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\34.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\35.png").convert_alpha(),
                         pygame.image.load(r"Sprites\Kozlov_Sprites\36.png").convert_alpha()]

        deathGroup = [pygame.image.load(r"Sprites\Kozlov_Sprites\Death.png").convert_alpha()]
        shootGroup=[]

        Group = [pygame.image.load(r"Sprites\Kozlov_Sprites\01.png").convert_alpha(), [leftGroup, rightGroup], deathGroup,
                 shootGroup]
        return Group

class DamagePlatform(Damage_Object,Platform):
    def __init__(self,image,point,Name,damage):
        Block.__init__(self,image,point,Name)
        Damage_Object.__init__(self,damage)

class KillingPlatform(DamagePlatform):
    def __init__(self,image,point,Name,damage,tchd=False):
        DamagePlatform.__init__(self,image,point,Name,damage)
        self.tchd=tchd

class Animation:
    animation_move=None
    animation_death=None
    animation_shoot=None

    def __init__(self,sprites=[],moveStatus=None,type_obj=type(Creature)):
        self.type_obj = type_obj
        self.animation_progress=0
        self.moveStatus=moveStatus
        self.image=sprites[0]#текущий спрайт
        self.animotion_stand=sprites[0]
        self.animation_move=Animation_move(sprites[1],type_obj)
        self.animation_death = Animation_death(sprites[2], type_obj)
        self.animation_shoot = Animation_shoot(sprites[3], type_obj)
        self.last_status = Orientation.Non


    def show(self,Object):
        self.animation_progress+=1
        if Object.hp>0:
            self.animation_shoot.show(Object, self)
            self.animation_move.show(Object,self)
            if self.moveStatus == Orientation.Non:
                self.image = self.animotion_stand

        else:
            self.animation_death.show(Object,self)


class Animation_move:
    def __init__(self,sprites,type_obj):#sprites=[левая,правая,...]
        self.sprites = sprites
        self.type_obj = type_obj

    def show(self,Object,main_anim):
        if main_anim.moveStatus == Orientation.UpRight:
            main_anim.last_status=main_anim.moveStatus
            main_anim.image = self.sprites[1][0]

        elif main_anim.moveStatus == Orientation.Right:
            main_anim.last_status = main_anim.moveStatus
            main_anim.image = self.sprites[1][int(main_anim.animation_progress // 8) % len(self.sprites[1])]

        elif main_anim.moveStatus == Orientation.UpLeft:
            main_anim.last_status = main_anim.moveStatus
            main_anim.image = self.sprites[0][0]

        elif main_anim.moveStatus == Orientation.Left:
            main_anim.last_status = main_anim.moveStatus
            main_anim.image = self.sprites[0][int(main_anim.animation_progress // 8) % len(self.sprites[0])]

        elif main_anim.moveStatus == Orientation.Down and type(self.type_obj)==type(Player):
            main_anim.image = self.sprites[2][int(main_anim.animation_progress // 8) % len(self.sprites[2])]

class Animation_death:
    def __init__(self,sprites,type_obj):#sprites=смерть
        self.sprites = sprites
        self.type_obj = type_obj

    def show(self, Object, main_anim):
        main_anim.image = self.sprites[0]
        if main_anim.animation_progress % 157 == 0:
            Object.onmap="No"

class Animation_shoot:
    def __init__(self,sprites,type_obj):#sprites=[влево,вправо]
        self.sprites = sprites
        self.type_obj = type_obj

    def show(self, Object, main_anim):
        if main_anim.moveStatus == Orientation.Bullet_stand and main_anim.last_status in [Orientation.Right, Orientation.UpRight]:
            main_anim.image = self.sprites[2][1]

        elif main_anim.moveStatus == Orientation.Bullet_stand and main_anim.last_status in [Orientation.Left, Orientation.UpLeft]:
            main_anim.image = self.sprites[2][0]

        elif main_anim.moveStatus == Orientation.Bullet_Right_move:
            main_anim.image = self.sprites[1][int(main_anim.animation_progress // 8) % len(self.sprites[1])]

        elif main_anim.moveStatus == Orientation.Bullet_Left_move:
            main_anim.image = self.sprites[0][int(main_anim.animation_progress // 8) % len(self.sprites[0])]



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

class Physics:
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
        if self.crd.y >= self.y0:
            self.crd.y = self.y0
            gdam = int(self.v.y/15) * 50
            self.v.y = 0
        else:
            gdam=0
        p0=self.crd.copy()
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
                    p0.y = Object.down()

                elif self.checkside(Object):
                    if self.checkleft(Object):
                        self.v.x = 0
                        p0.x = Object.left() - self.size.x
                    if self.checkright(Object):
                        self.v.x = 0
                        p0.x = Object.right()
                if self.checkfall(Object):
                    self.y0 = 100000
                    self.x1 = -100000
                    self.x2 = 100000
        if gdam>0:
            self.dam+=gdam
            gdam=-1
        elif gdam==-1:
            self.dam-=gdam
            gdam=0
        self.crd=p0.copy()

class Message:
    def __init__(self,point,text="",onmap="Yes"):
        self.text=text
        self.point=point
        self.onmap=onmap

    def draw_text(self,screen,Map):
        pygame.draw.rect(pygame.display.set_mode([0, 0], pygame.FULLSCREEN), (255, 255, 255),(self.point.x, self.point.y, 600, 100))
        font_name = pygame.font.match_font('koysan')
        font = pygame.font.Font(font_name, 50)
        text_surface = font.render(self.text, True, (70, 130, 180))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.point.x, self.point.y)
        screen.blit(text_surface, text_rect)

