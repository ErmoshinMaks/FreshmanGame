import pygame
pygame.init()

class Abstract_object(pygame.sprite.Sprite):
    def __init__(self,point,name="unknown",onmap="Yes"):
        pygame.sprite.Sprite.__init__(self)
        self.Point = point
        #self.rect = self.image.get_rect(centerx=self.Point.x,centery=self.Point.y)
        self.name=name
        self.onmap=onmap

class Material(Abstract_object):
    def __init__(self,point,Name):
        super().__init__(point,Name)


class NotMaterial(Abstract_object):
    def __init__(self,point,Name):
        super().__init__(point,Name)

class Block(Material):
    def __init__(self,image,point,Name):
        super().__init__(point,Name)
        self.image=image

    def left(self):
        return self.Point.x

    def right(self):
        return self.Point.x+self.image.get_rect().width

    def up(self):
        return self.Point.y

    def down(self):
        return self.Point.y+self.image.get_rect().height


class Creature(Material):
    def __init__(self,point,Name,hp=100,maxhp=100,xp=0):
        super().__init__(point,Name)
        self.hp=hp
        self.maxhp=maxhp
        self.xp=xp

class Human(Creature):
    def __init__(self,point,Name,shoot_progress=0,hp=100, maxhp=100, xp=0):
        super().__init__(point,Name,hp,maxhp,xp)
        self.shoot_progress=shoot_progress

class Damage_Object:
    def __init__(self, damage):
        self.damage=damage